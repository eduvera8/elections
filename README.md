# Conflict Legacies and the Fujimorista Vote in Peru, 1995–2026

Research project: do districts that suffered more political violence during Peru's
internal armed conflict (1980–2000) vote differently today — and does the answer
depend on **who did the killing** (Sendero Luminoso, the armed forces, the rondas
campesinas) and on **how old the voters are**?

## The question

Eight presidential elections, two Fujimoris, and one fujimorista victory at each end
of the panel:

| Year | Contest | Outcome |
|------|---------|---------|
| 1995 | Alberto Fujimori vs. Pérez de Cuéllar | Fujimori landslide (~64%), 3 years after Guzmán's capture |
| 2000 | Alberto Fujimori vs. Toledo | Fujimori "wins"; election widely held fraudulent, Toledo boycotted the runoff |
| 2001 | Toledo vs. Alan García | Post-collapse realignment, no Fujimori on the ballot |
| 2006 | García vs. Humala | Humala's first run |
| 2011 | Humala vs. Keiko Fujimori | Keiko loses runoff (~48.5 / 51.5) |
| 2016 | Keiko vs. Kuczynski | Keiko loses runoff (~49.88 / 50.12) |
| 2021 | Keiko vs. Castillo | Keiko loses runoff (~49.87 / 50.13) |
| 2026 | Keiko vs. Roberto Sánchez | **Keiko wins** runoff (~50.1 / 49.9), ~50k votes |

All runoff percentages above are from memory/secondary sources and **must be verified
against ONPE before use**. See `docs/02-data-sources.md`.

## Why this is publishable

The closest existing paper — De la Calle (2024), *Electoral Studies* 90:102827, PDF at the
repository root — covers **2011, 2016 and 2021 only**, as six separate OLS cross-sections, and
finds that districts hit harder by *Sendero* violence (relative to state violence) give Keiko a
premium and the left a penalty.

Crucially, it observes that gradient **weakening** across the three elections and attributes
this, in its conclusion, to "the decreasing political clout of the age cohorts with direct
experience of the conflict" — then does not test it, having no age data, no cohort measure and
no panel. This project extends it in three directions it cannot reach:

1. **The long panel.** 1995, 2000, 2001 and 2006 are uncovered. The 1990s are where the
   mechanism was formed, with Alberto personally on the ballot and the war still fresh.
2. **2026.** Brand new, and the first fujimorista presidential win since 1995.
3. **Age / cohort heterogeneity — running the test De la Calle proposes.** The memory
   mechanism implies the effect should live in cohorts who experienced the violence firsthand
   and should decay as those cohorts leave the electorate, at a rate that cohort-replacement
   data predicts. An eight-election panel can test that; three cross-sections cannot.
   See `docs/03-age-heterogeneity.md` — this is the core analytical contribution.

A useful accident of the data: the 2011, 2016, 2021 and 2026 runoffs were all near-ties
nationally (~50/50). With the national swing roughly held constant, movement in the
district-level geography is unusually clean to interpret.

## Documentation

| File | Contents |
|------|----------|
| `docs/01-research-design.md` | Question, contribution, estimating equations |
| `docs/02-data-sources.md` | Every data source, unit, access route, known gotchas |
| `docs/03-age-heterogeneity.md` | The cohort design — three routes, exposure arithmetic |
| `docs/04-literature.md` | Annotated reading list |
| `docs/05-threats-to-inference.md` | FONCODES, displacement, attribution dispute, district splits |
| `docs/06-delacalle-2024-notes.md` | Full reading notes on the paper this project builds from |
| `docs/GIT-BASICS.md` | How this repo works, if you're new to git/GitHub |

## Layout

```
data/raw/        downloaded, never edited, NOT committed (see .gitignore)
data/interim/    cleaned intermediates, NOT committed
data/processed/  final analysis panels, NOT committed
src/             scripts that turn raw into processed
refs/            papers and PDFs, NOT committed
docs/            design and data documentation — this IS committed
notebooks/       exploratory analysis
```

Rule of thumb: **code and documentation are committed, data and PDFs are not.** Anyone
should be able to clone this repo, run `src/`, and rebuild `data/processed` from scratch.

## Status

Scaffolding only. No data has been downloaded and no analysis has been run. The scripts in
`src/` are documented stubs — the endpoints in them are recorded from documentation and
**have not been tested**, because the environment this was set up in had no outbound
network access.
