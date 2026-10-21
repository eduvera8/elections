# src/

Scripts that turn `data/raw/` into `data/processed/`. Nothing here should require a manual
step; anyone cloning this repo should be able to rebuild every analysis panel from scratch.

## What exists

| File | Status | What it does |
|---|---|---|
| `exposure.py` | **working, tested** | Cohort-exposure arithmetic: converts a banded age distribution of a district's electorate into the share with firsthand conflict exposure. Implements the design in `docs/03-age-heterogeneity.md` |
| `test_exposure.py` | **working** | 9 checks on the above. Run `python3 src/test_exposure.py` (no pytest needed) |

## What does not exist yet, in build order

1. `build_district_crosswalk.py` — map every district-year to a stable 1993-vintage unit.
   **Must come first**; see `docs/05-threats-to-inference.md` §4.
2. `fetch_election_results.py` — district results for the eight elections from JNE Infogob
   and ONPE. Cross-check the two against each other.
3. `fetch_padron_age.py` — padrón electoral by district × sex × age group. Feeds `exposure.py`.
   Highest-value acquisition after the crosswalk.
4. `build_conflict_panel.py` — CVR/RUV victim records aggregated to district × perpetrator ×
   period. Must support both the CVR and the Rendón attributions (see §2 of the threats doc).
5. `build_analysis_panel.py` — join the above into one district × election panel.

No fetch script has been written, because the environment this repo was set up in had no
outbound network access, and shipping untested download code that claims to work would be
worse than shipping none. The endpoints are recorded in `docs/02-data-sources.md`; verify
them before writing against them.

## Conventions

- Scripts read from `data/raw/`, write to `data/interim/` or `data/processed/`, and never
  modify `data/raw/`.
- Every script prints what it read and what it wrote.
- Record the URL and retrieval date of anything downloaded in `docs/02-data-sources.md`.
