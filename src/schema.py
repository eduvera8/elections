"""Expected input files and their columns.

Every file lives in data/raw/ as CSV with a header row. `ubigeo` is the 6-digit
INEI district code as a STRING (leading zeros matter — "010101", not 10101), and is
the join key everywhere.

The pipeline degrades gracefully: with RESULTS + DEATHS alone it reproduces the
De la Calle-style cross-sections, and each further file unlocks more of the design.
`python3 src/pipeline.py` reports which files it found and which models it could run.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

PERPETRATORS = ["sendero", "state", "rondas", "mrta", "other"]
ELECTIONS = [1995, 2000, 2001, 2006, 2011, 2016, 2021, 2026]


@dataclass(frozen=True)
class FileSpec:
    name: str
    filename: str
    required: bool
    unlocks: str
    columns: dict[str, str]
    notes: str = ""
    key: tuple[str, ...] = field(default_factory=lambda: ("ubigeo",))


RESULTS = FileSpec(
    name="Election results",
    filename="results.csv",
    required=True,
    unlocks="everything",
    key=("ubigeo", "year", "round"),
    columns={
        "ubigeo": "6-digit district code, string with leading zeros",
        "year": f"election year, one of {ELECTIONS}",
        "round": "1 for first round, 2 for runoff",
        "fujimorista_votes": "votes for the fujimorista candidate (A. Fujimori 1995/2000, "
        "Martha Chavez 2006, Keiko 2011/2016/2021/2026); blank for 2001",
        "left_votes": "votes for the leading left candidate; see docs for the coding rule",
        "valid_votes": "total valid votes cast",
        "blank_null_votes": "blank + null ballots (voto blanco + viciado)",
        "registered": "registered electors (padron), for turnout",
    },
    notes="Long format (one row per district-year-round) is also accepted if it has "
    "columns ubigeo, year, round, candidate, votes — see loaders.load_results.",
)

DEATHS = FileSpec(
    name="Conflict deaths",
    filename="cvr_deaths.csv",
    required=True,
    unlocks="the key regressor",
    key=("ubigeo", "perpetrator"),
    columns={
        "ubigeo": "6-digit district code",
        "perpetrator": f"one of {PERPETRATORS}",
        "deaths": "count of deaths/disappearances attributed to that perpetrator",
    },
    notes="One row per district-perpetrator. A 'period' column (1980-85 / 1986-92 / "
    "1993-2000) is optional and enables the exposure-timing refinement.",
)

PADRON = FileSpec(
    name="Padron electoral by age",
    filename="padron_age.csv",
    required=False,
    unlocks="THE AGE/COHORT DESIGN — the novel contribution",
    key=("ubigeo", "year", "age_lo"),
    columns={
        "ubigeo": "6-digit district code",
        "year": "election year",
        "age_lo": "lower bound of the age band, inclusive",
        "age_hi": "upper bound, exclusive; leave EMPTY for the open top band (e.g. 80+)",
        "voters": "registered electors in that band",
    },
    notes="Without this file there is no cohort test and the project is just a "
    "replication. This is the single most important file to obtain.",
)

CONTROLS = FileSpec(
    name="District controls",
    filename="controls.csv",
    required=False,
    unlocks="credible specifications",
    columns={
        "ubigeo": "6-digit district code",
        "population": "district population (any recent census year)",
        "region": "macro-region label, e.g. Lima, Coast, Amazonas, North Andes, South Andes",
        "poverty_rate": "optional: INEI monetary poverty share, 0-1",
        "spanish_share_1981": "optional: share of Spanish speakers, 1981 census, 0-1",
        "rural": "optional: 1 if rural",
    },
)

ALL_SPECS = [RESULTS, DEATHS, PADRON, CONTROLS]


def describe() -> str:
    """Human-readable spec of every input file, for docs and for the shopping list."""
    out = []
    for s in ALL_SPECS:
        flag = "REQUIRED" if s.required else "optional"
        out.append(f"\n### {s.filename}  [{flag}] — unlocks: {s.unlocks}")
        out.append(f"key: {', '.join(s.key)}")
        for col, desc in s.columns.items():
            out.append(f"  {col:22} {desc}")
        if s.notes:
            out.append(f"  note: {s.notes}")
    return "\n".join(out)


def validate(df: pd.DataFrame, spec: FileSpec) -> list[str]:
    """Return a list of problems with `df` against `spec`. Empty list means clean."""
    problems = []
    required_cols = [c for c in spec.columns if "optional" not in spec.columns[c]]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        problems.append(f"{spec.filename}: missing columns {missing}")
    if "ubigeo" in df.columns:
        if df["ubigeo"].isna().any():
            problems.append(f"{spec.filename}: ubigeo has missing values")
        lengths = df["ubigeo"].astype(str).str.len().unique().tolist()
        if any(x != 6 for x in lengths):
            problems.append(
                f"{spec.filename}: ubigeo should be 6 characters, found lengths {lengths} "
                "— read it with dtype={'ubigeo': str} to keep leading zeros"
            )
    if "perpetrator" in df.columns:
        bad = sorted(set(df["perpetrator"].dropna().unique()) - set(PERPETRATORS))
        if bad:
            problems.append(f"{spec.filename}: unknown perpetrator values {bad}")
    if "year" in df.columns:
        bad_years = sorted(set(df["year"].dropna().unique()) - set(ELECTIONS))
        if bad_years:
            problems.append(f"{spec.filename}: unexpected election years {bad_years}")
    present = [c for c in spec.key if c in df.columns]
    if present and df.duplicated(subset=present).any():
        n = int(df.duplicated(subset=present).sum())
        problems.append(f"{spec.filename}: {n} duplicate rows on key {present}")
    return problems


if __name__ == "__main__":
    print("Input files expected in data/raw/:")
    print(describe())
