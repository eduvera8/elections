"""Generate SYNTHETIC data matching the schema, to test the pipeline end to end.

    python3 src/make_synthetic.py            # writes data/synthetic/
    python3 src/pipeline.py --data data/synthetic

The numbers it produces are INVENTED. They exist only to prove the pipeline runs and
recovers a planted effect; they are not findings about Peru and must never be reported
as such. It writes to data/synthetic/, never data/raw/, so real and fake cannot mix.

The planted data-generating process is the hypothesis under test:

    fujimorista_share = a + b * diff_pc * exposed_share + ...

i.e. the conflict gradient operates ONLY through cohorts with firsthand memory. Because
exposed_share falls across 1995-2026, a correctly specified pipeline should show (i) a
declining per-election beta in Model A and (ii) a positive, significant interaction in
Model C. If it does, the pipeline can detect the real thing.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import schema

RNG = np.random.default_rng(20261021)
N_DISTRICTS = 1800
TRUE_INTERACTION = 0.40  # the coefficient the pipeline should recover in Model C


def main(out: Path = Path("data/synthetic")) -> None:
    out.mkdir(parents=True, exist_ok=True)
    ubigeo = [f"{i:06d}" for i in range(10101, 10101 + N_DISTRICTS)]

    population = RNG.lognormal(8.5, 1.2, N_DISTRICTS).round()
    regions = RNG.choice(
        ["Lima", "Coast", "Amazonas", "North Andes", "South Andes"], N_DISTRICTS
    )

    # Violence: heavy-tailed and two-sided, with the ~0.76 correlation the paper reports.
    latent = RNG.gamma(0.4, 6.0, N_DISTRICTS)
    sendero = RNG.poisson(latent * 1.3)
    state = RNG.poisson(latent * 0.9)
    controls = pd.DataFrame({
        "ubigeo": ubigeo,
        "population": population,
        "region": regions,
        "poverty_rate": np.clip(RNG.beta(2, 3, N_DISTRICTS), 0, 1),
        "spanish_share_1981": np.clip(RNG.beta(5, 2, N_DISTRICTS), 0, 1),
        "rural": RNG.binomial(1, 0.6, N_DISTRICTS),
    })
    controls.to_csv(out / "controls.csv", index=False)

    deaths = pd.concat([
        pd.DataFrame({"ubigeo": ubigeo, "perpetrator": "sendero", "deaths": sendero}),
        pd.DataFrame({"ubigeo": ubigeo, "perpetrator": "state", "deaths": state}),
        pd.DataFrame({"ubigeo": ubigeo, "perpetrator": "rondas",
                      "deaths": RNG.poisson(latent * 0.2)}),
        pd.DataFrame({"ubigeo": ubigeo, "perpetrator": "mrta",
                      "deaths": RNG.poisson(0.05, N_DISTRICTS)}),
    ])
    deaths.to_csv(out / "cvr_deaths.csv", index=False)

    diff_pc = (sendero - state) / (population / 1000.0)

    # Padron: five-year bands, with the electorate ageing across the panel.
    padron_rows, exposed = [], {}
    bands = [(lo, lo + 5) for lo in range(18, 80, 5)] + [(80, None)]
    for year in schema.ELECTIONS:
        # Older electorates earlier in the panel; districts differ in age structure.
        tilt = RNG.normal(0, 0.35, N_DISTRICTS)
        for i, u in enumerate(ubigeo):
            weights = []
            for lo, _ in bands:
                # A smooth age profile, shifted per district.
                w = np.exp(-((lo - 35 - 8 * tilt[i]) ** 2) / (2 * 22.0 ** 2))
                weights.append(w)
            weights = np.array(weights) / sum(weights)
            total = max(population[i] * 0.62, 50)
            for (lo, hi), w in zip(bands, weights):
                padron_rows.append({
                    "ubigeo": u, "year": year, "age_lo": lo,
                    "age_hi": "" if hi is None else hi,
                    "voters": round(total * w),
                })
    padron = pd.DataFrame(padron_rows)
    padron.to_csv(out / "padron_age.csv", index=False)

    # Recompute exposed_share the same way the pipeline will, to build the outcome.
    from pipeline import exposure_by_district
    exp_df = exposure_by_district(padron.assign(
        age_hi=pd.to_numeric(padron["age_hi"], errors="coerce")
    ))
    exposed = {(r.ubigeo, r.year): r.exposed_share for r in exp_df.itertuples()}

    # Results. The planted DGP: the gradient acts only via exposed cohorts.
    rows = []
    district_effect = RNG.normal(0, 4.0, N_DISTRICTS)
    for year in schema.ELECTIONS:
        year_level = {1995: 48, 2000: 45, 2001: 20, 2006: 22,
                      2011: 38, 2016: 36, 2021: 35, 2026: 40}[year]
        for i, u in enumerate(ubigeo):
            es = exposed.get((u, year), 0.0)
            registered = max(int(population[i] * 0.62), 50)
            fuji_pct = (
                year_level
                + TRUE_INTERACTION * diff_pc[i] * es
                + district_effect[i]
                + RNG.normal(0, 3.0)
            )
            left_pct = 100 - fuji_pct - 35 + RNG.normal(0, 3.0)
            fuji_pct = float(np.clip(fuji_pct, 1, 90))
            left_pct = float(np.clip(left_pct, 1, 90))
            valid = int(registered * RNG.uniform(0.78, 0.92))
            rows.append({
                "ubigeo": u, "year": year, "round": 1,
                "fujimorista_votes": int(valid * fuji_pct / 100),
                "left_votes": int(valid * left_pct / 100),
                "valid_votes": valid,
                "blank_null_votes": int(valid * RNG.uniform(0.03, 0.18)),
                "registered": registered,
            })
    pd.DataFrame(rows).to_csv(out / "results.csv", index=False)

    print(f"SYNTHETIC data written to {out}/ — invented numbers, not findings.")
    print(f"  planted interaction coefficient (Model C target): {TRUE_INTERACTION}")
    print(f"  {N_DISTRICTS:,} districts x {len(schema.ELECTIONS)} elections")


if __name__ == "__main__":
    main()
