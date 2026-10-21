# src/

Scripts that turn `data/raw/` into results. Nothing here needs a manual step.

## Run it

```bash
python3 src/schema.py                            # what files and columns are expected
python3 src/make_synthetic.py                    # write synthetic test data
PYTHONPATH=src python3 src/pipeline.py --data data/synthetic   # prove the pipeline works
PYTHONPATH=src python3 src/pipeline.py           # the real thing, once data/raw/ is filled
python3 src/test_exposure.py                     # unit checks on the cohort arithmetic
```

## What exists

| File | Status | What it does |
|---|---|---|
| `schema.py` | working | Expected input files, columns, and validation. The contract with whoever collects the data |
| `exposure.py` | working, tested | Cohort-exposure arithmetic: banded age distribution → share of the electorate with firsthand conflict exposure |
| `test_exposure.py` | working | 9 checks on the above |
| `pipeline.py` | working, validated | Builds the district × election panel and runs Models A, B and C |
| `make_synthetic.py` | working | Synthetic data matching the schema, for testing. Writes to `data/synthetic/`, never `data/raw/` |

## The models

- **Model A** — one OLS per election year. Reproduces De la Calle's design, extended to all
  eight elections.
- **Model B** — pooled, district fixed effects, conflict × year interactions. The formal decay
  test his six separate cross-sections cannot perform.
- **Model C** — conflict × `exposed_share`, district fixed effects. **The novel test**: does the
  conflict gradient live in cohorts with firsthand memory? Needs `padron_age.csv`.

## Pipeline validation

`make_synthetic.py` plants a data-generating process in which the conflict gradient acts
*only* through exposed cohorts, with a true interaction coefficient of 0.40. Running the
pipeline on it recovers:

- **Model C**: `diff_x_exposed` = 0.4449 (SE 0.0449) — the planted value, within about one SE.
- **Model A**: betas falling 0.36 → 0.15 across 1995–2026, the decay that cohort replacement
  produces mechanically.
- **Model B**: joint test rejects constant interactions, F = 21.63, p < 0.0001.

So the pipeline detects the effect we are looking for when it is present. **Those numbers are
from invented data and are not findings about Peru.**

## Still to write

1. `build_district_crosswalk.py` — stable district units across 1995–2026. Needed before the
   full panel; see `docs/05-threats-to-inference.md` §4.
2. Fetch scripts. Deliberately absent: this environment's network policy blocks every data
   host, so download code could not be tested, and untested fetch code that claims to work is
   worse than none. Endpoints are in `docs/02-data-sources.md`, requirements in
   `docs/07-data-shopping-list.md`.
