"""Build the district x election panel and run the headline models.

    python3 src/pipeline.py                 # uses data/raw/
    python3 src/pipeline.py --data DIR      # uses another directory

Degrades gracefully: it reports which input files it found, which models it could
therefore run, and what is missing to unlock the rest. See src/schema.py for the
expected files and columns.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import schema
from exposure import AgeBand, exposed_share

OUTCOMES = {
    "fujimorista_share": "fujimorista vote share",
    "left_share": "leading-left vote share",
    "blank_null_share": "blank + null share",
    "turnout": "turnout",
}


# ---------------------------------------------------------------- loading


def _read(path: Path, spec: schema.FileSpec) -> pd.DataFrame | None:
    if not path.exists():
        return None
    df = pd.read_csv(path, dtype={"ubigeo": str})
    problems = schema.validate(df, spec)
    if problems:
        print(f"  ! {path.name}: {len(problems)} schema problem(s)")
        for p in problems:
            print(f"      {p}")
    return df


def load_inputs(data_dir: Path) -> dict[str, pd.DataFrame | None]:
    print(f"Reading from {data_dir}/")
    found = {}
    for key, spec in [
        ("results", schema.RESULTS),
        ("deaths", schema.DEATHS),
        ("padron", schema.PADRON),
        ("controls", schema.CONTROLS),
    ]:
        df = _read(data_dir / spec.filename, spec)
        found[key] = df
        mark = "found" if df is not None else "MISSING"
        extra = f" ({len(df):,} rows)" if df is not None else f" -> no {spec.unlocks}"
        print(f"  {spec.filename:18} {mark}{extra}")
    return found


# ---------------------------------------------------------------- panel


def conflict_measures(deaths: pd.DataFrame, pop: pd.DataFrame | None) -> pd.DataFrame:
    """District-level conflict regressors from the perpetrator-coded death counts.

    Builds both De la Calle's difference measure and the separated counts, because the
    difference assigns zero to peaceful districts and to two-sided-violence districts
    alike (see docs/06-delacalle-2024-notes.md).
    """
    wide = (
        deaths.pivot_table(index="ubigeo", columns="perpetrator", values="deaths",
                           aggfunc="sum", fill_value=0)
        .reindex(columns=schema.PERPETRATORS, fill_value=0)
        .reset_index()
    )
    wide["insurgent"] = wide["sendero"] + wide["mrta"]
    wide["total_deaths"] = wide[schema.PERPETRATORS].sum(axis=1)

    if pop is not None:
        wide = wide.merge(pop[["ubigeo", "population"]], on="ubigeo", how="left")
        scale = wide["population"].replace(0, np.nan) / 1000.0
    else:
        print("  ! no population data: conflict measures are raw counts, not per capita")
        scale = 1.0

    for col in ["sendero", "state", "rondas", "insurgent", "total_deaths"]:
        wide[f"{col}_pc"] = wide[col] / scale

    # The headline regressor, and the variation it throws away.
    wide["diff_pc"] = wide["sendero_pc"] - wide["state_pc"]
    wide["two_sided"] = (
        (wide["sendero"] > 0) & (wide["state"] > 0)
    ).astype(int)
    wide["any_violence"] = (wide["total_deaths"] > 0).astype(int)
    return wide


def exposure_by_district(padron: pd.DataFrame, reference_year: int = 1992,
                         min_age: int = 18) -> pd.DataFrame:
    """exposed_share for every district-year in the padron file."""
    rows = []
    for (ubigeo, year), grp in padron.groupby(["ubigeo", "year"]):
        bands = [
            AgeBand(
                lo=int(r.age_lo),
                hi=None if pd.isna(r.age_hi) else int(r.age_hi),
                count=float(r.voters),
            )
            for r in grp.itertuples()
        ]
        try:
            share = exposed_share(bands, int(year), reference_year, min_age)
        except ValueError as e:
            print(f"  ! exposure failed for {ubigeo} {year}: {e}")
            continue
        rows.append({"ubigeo": ubigeo, "year": int(year), "exposed_share": share})
    return pd.DataFrame(rows)


def build_panel(inp: dict[str, pd.DataFrame | None]) -> pd.DataFrame:
    res = inp["results"].copy()

    # Shares. Districts with no valid votes recorded are dropped, not zero-filled.
    res["valid_votes"] = res["valid_votes"].replace(0, np.nan)
    res["fujimorista_share"] = 100 * res["fujimorista_votes"] / res["valid_votes"]
    res["left_share"] = 100 * res["left_votes"] / res["valid_votes"]
    if "blank_null_votes" in res:
        cast = res["valid_votes"] + res["blank_null_votes"]
        res["blank_null_share"] = 100 * res["blank_null_votes"] / cast
    if "registered" in res:
        cast = res["valid_votes"] + res.get("blank_null_votes", 0)
        res["turnout"] = 100 * cast / res["registered"].replace(0, np.nan)

    panel = res.merge(
        conflict_measures(inp["deaths"], inp["controls"]), on="ubigeo", how="left"
    )
    if inp["controls"] is not None:
        extra = [c for c in inp["controls"].columns
                 if c not in ("ubigeo", "population")]
        panel = panel.merge(inp["controls"][["ubigeo", *extra]], on="ubigeo", how="left")
    if inp["padron"] is not None:
        panel = panel.merge(exposure_by_district(inp["padron"]),
                            on=["ubigeo", "year"], how="left")
    return panel


# ---------------------------------------------------------------- models


def _ols(df: pd.DataFrame, y: str, rhs: list[str], cluster: str | None = "ubigeo"):
    import statsmodels.api as sm

    cols = [y, *rhs] + ([cluster] if cluster else [])
    d = df[[c for c in dict.fromkeys(cols) if c in df.columns]].dropna()
    if len(d) < len(rhs) + 10:
        return None, len(d)
    X = sm.add_constant(d[rhs].astype(float))
    if cluster and d[cluster].nunique() > 1:
        fit = sm.OLS(d[y].astype(float), X).fit(
            cov_type="cluster", cov_kwds={"groups": d[cluster]}
        )
    else:
        fit = sm.OLS(d[y].astype(float), X).fit(cov_type="HC1")
    return fit, len(d)


def _stars(p: float) -> str:
    return "**" if p < 0.01 else "*" if p < 0.05 else "+" if p < 0.10 else " "


def cross_sections(panel: pd.DataFrame, rnd: int = 1) -> pd.DataFrame:
    """Model A — one OLS per election year. Reproduces De la Calle's design."""
    controls = [c for c in ["poverty_rate", "spanish_share_1981", "log_pop", "rural"]
                if c in panel.columns]
    rows = []
    for year, grp in panel[panel["round"] == rnd].groupby("year"):
        for y in OUTCOMES:
            if y not in grp.columns:
                continue
            fit, n = _ols(grp, y, ["diff_pc", *controls], cluster=None)
            if fit is None:
                continue
            rows.append({
                "year": int(year), "outcome": y, "n": n,
                "beta_diff": fit.params["diff_pc"],
                "se": fit.bse["diff_pc"],
                "p": fit.pvalues["diff_pc"],
                "r2": fit.rsquared,
            })
    return pd.DataFrame(rows)


def decay_test(panel: pd.DataFrame, outcome: str, rnd: int = 1):
    """Model B — pooled, district fixed effects, conflict x year interactions.

    This is the test De la Calle's six separate cross-sections cannot perform: whether
    the conflict gradient genuinely changes across elections. District FE absorb the
    time-invariant conflict measure, so the interactions carry all the information.
    """
    d = panel[(panel["round"] == rnd)].dropna(subset=[outcome, "diff_pc"]).copy()
    years = sorted(d["year"].unique())
    if len(years) < 3:
        return None, "needs at least 3 elections in the panel"
    base = years[0]

    rhs = []
    for yr in years[1:]:
        d[f"y{yr}"] = (d["year"] == yr).astype(float)
        rhs.append(f"y{yr}")
    for yr in years[1:]:
        d[f"diff_x_{yr}"] = d["diff_pc"] * (d["year"] == yr).astype(float)
        rhs.append(f"diff_x_{yr}")

    # Within-district transformation = district fixed effects.
    dm = d.copy()
    for c in [outcome, *rhs]:
        dm[c] = dm[c] - dm.groupby("ubigeo")[c].transform("mean")

    fit, n = _ols(dm, outcome, rhs)
    return fit, f"base year {base}, N={n}, {d['ubigeo'].nunique():,} districts"


def cohort_test(panel: pd.DataFrame, outcome: str, rnd: int = 1):
    """Model C — the novel test: does the conflict gradient live in exposed cohorts?

    conflict x exposed_share, with district fixed effects. A positive interaction means
    the gradient is stronger where more of the electorate remembers the conflict
    firsthand, which is the mechanism De la Calle proposes and does not test.
    """
    if "exposed_share" not in panel.columns:
        return None, "needs data/raw/padron_age.csv"
    d = panel[panel["round"] == rnd].dropna(
        subset=[outcome, "diff_pc", "exposed_share"]
    ).copy()
    if d["year"].nunique() < 2:
        return None, "needs at least 2 elections with padron age data"

    d["diff_x_exposed"] = d["diff_pc"] * d["exposed_share"]
    rhs = ["exposed_share", "diff_x_exposed"]
    for yr in sorted(d["year"].unique())[1:]:
        d[f"y{yr}"] = (d["year"] == yr).astype(float)
        rhs.append(f"y{yr}")

    dm = d.copy()
    for c in [outcome, *rhs]:
        dm[c] = dm[c] - dm.groupby("ubigeo")[c].transform("mean")
    fit, n = _ols(dm, outcome, rhs)
    return fit, f"N={n}, {d['ubigeo'].nunique():,} districts"


# ---------------------------------------------------------------- report


def report(panel: pd.DataFrame, inp: dict) -> None:
    print("\n" + "=" * 78)
    print("PANEL")
    print("=" * 78)
    print(f"  {len(panel):,} district-election-round rows")
    print(f"  {panel['ubigeo'].nunique():,} districts")
    print(f"  elections: {sorted(panel['year'].unique())}")
    if "exposed_share" in panel.columns:
        prof = panel.groupby("year")["exposed_share"].mean().dropna()
        if len(prof):
            print("\n  Mean exposed_share by election (firsthand adult conflict memory):")
            for yr, v in prof.items():
                bar = "#" * int(round(v * 40))
                print(f"    {int(yr)}  {v:5.3f}  {bar}")

    print("\n" + "=" * 78)
    print("MODEL A — per-election cross-sections (De la Calle replication)")
    print("=" * 78)
    xs = cross_sections(panel)
    if xs.empty:
        print("  could not run")
    else:
        for outcome, grp in xs.groupby("outcome"):
            print(f"\n  {OUTCOMES.get(outcome, outcome)}:")
            print(f"    {'year':>6} {'beta(diff)':>11} {'se':>8} {'':2} {'N':>7} {'R2':>6}")
            for r in grp.sort_values("year").itertuples():
                print(f"    {r.year:>6} {r.beta_diff:>11.4f} {r.se:>8.4f} "
                      f"{_stars(r.p):>2} {r.n:>7,} {r.r2:>6.3f}")

    print("\n" + "=" * 78)
    print("MODEL B — pooled, district FE, conflict x year (formal decay test)")
    print("=" * 78)
    for outcome in ["fujimorista_share", "left_share"]:
        if outcome not in panel.columns:
            continue
        fit, note = decay_test(panel, outcome)
        print(f"\n  {OUTCOMES[outcome]} — {note}")
        if fit is None:
            continue
        for name in [p for p in fit.params.index if p.startswith("diff_x_")]:
            print(f"    {name:<16} {fit.params[name]:>10.4f} "
                  f"({fit.bse[name]:.4f}) {_stars(fit.pvalues[name])}")
        inter = [p for p in fit.params.index if p.startswith("diff_x_")]
        if len(inter) > 1:
            try:
                w = fit.f_test(" = ".join(inter) + " = 0")
                print(f"    joint test all interactions equal & zero: "
                      f"F={float(np.ravel(w.fvalue)[0]):.2f}, p={float(w.pvalue):.4f}")
            except Exception as e:
                print(f"    joint test unavailable: {e}")

    print("\n" + "=" * 78)
    print("MODEL C — conflict x exposed_share (THE COHORT TEST)")
    print("=" * 78)
    for outcome in ["fujimorista_share", "left_share"]:
        if outcome not in panel.columns:
            continue
        fit, note = cohort_test(panel, outcome)
        print(f"\n  {OUTCOMES[outcome]} — {note}")
        if fit is None:
            continue
        for name in ["diff_x_exposed", "exposed_share"]:
            if name in fit.params:
                print(f"    {name:<16} {fit.params[name]:>10.4f} "
                      f"({fit.bse[name]:.4f}) {_stars(fit.pvalues[name])}")

    missing = [s.filename for s, df in
               [(schema.PADRON, inp["padron"]), (schema.CONTROLS, inp["controls"])]
               if df is None]
    if missing:
        print("\n" + "=" * 78)
        print("STILL MISSING")
        print("=" * 78)
        for s in schema.ALL_SPECS:
            if s.filename in missing:
                print(f"  {s.filename}: unlocks {s.unlocks}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="data/raw", help="directory holding the input CSVs")
    args = ap.parse_args(argv)

    data_dir = Path(args.data)
    inp = load_inputs(data_dir)
    for key, spec in [("results", schema.RESULTS), ("deaths", schema.DEATHS)]:
        if inp[key] is None:
            print(f"\nCannot proceed: {spec.filename} is required.")
            print("Run `python3 src/schema.py` to see every expected file and column.")
            return 1
    report(build_panel(inp), inp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
