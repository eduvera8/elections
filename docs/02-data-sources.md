# Data sources

**None of the URLs below have been tested.** They are recorded from documentation and
memory; the environment this was written in had no outbound network access. Verify each one
and correct this file as you go — that is part of the work, not a chore.

## Electoral results

| Source | What | Unit | Notes |
|---|---|---|---|
| JNE **Infogob** (`infogob.jne.gob.pe`) | Historical results, candidates, parties | District | Best coverage back to the 1960s; the only realistic route to 1995–2006 |
| **ONPE** (`onpe.gob.pe`, `resultados.onpe.gob.pe`) | Official results | Mesa de sufragio and district | Mesa-level for recent elections; the official tally of record |
| ONPE/RENIEC **padrón electoral** | Registered electorate by district × sex × age group | District | **Critical for this project.** Acquire first. See `03-age-heterogeneity.md` |

Cross-check ONPE against Infogob for at least two elections before trusting either. Verify
all runoff percentages quoted in `README.md` against ONPE.

## Conflict victimisation

| Source | What | Unit | Access |
|---|---|---|---|
| **CVR** victim database (`cverdad.org.pe`) | ~24,000 directly documented victims: date, district, presumed perpetrator | Individual | Public in some form; confirm current availability |
| **RUV** — Registro Único de Víctimas, Consejo de Reparaciones (`ruv.gob.pe`), Ley 28592 | Much larger individual + collective registries, district-coded | Individual and collective | **Restricted.** The 2018 Reglamento reserves access to the documentary collection and individualised information to the purposes set out in the regulation. Plan a formal institutional request with a named affiliation; budget months, not days |
| **Defensoría del Pueblo** | Enforced-disappearance lists | Individual | Pre-CVR lists, also used as a CVR input |
| **EPAF** (Equipo Peruano de Antropología Forense) | Exhumations, burial sites | Site | Useful cross-check on under-reported state violence |
| Burial-sites registry (*Lugares de Entierro*) | Clandestine grave sites | Site | Independent signal on killings never reported as deaths |

On the number and the perpetrator split, read **both** sides before coding anything:
Rendón (2019) in *Research & Politics*, Manrique-Vallier & Ball's refutation, Rendón's
rejoinder, and Manrique-Vallier & Ball's multi-list capture-recapture re-estimation (arXiv
1906.04763). See `04-literature.md` and `05-threats-to-inference.md`.

## Covariates

| Source | What |
|---|---|
| **INEI** censuses 1981, 1993, 2007, 2017 | Population, age structure, language, literacy, poverty. The 1993 census sits in the middle of the conflict — valuable |
| INEI district poverty maps | Mapas de pobreza |
| **ENAHO** | Household survey; excellent geography, no vote question |
| **MEF** / Schady replication data | FONCODES allocations — see `05-threats-to-inference.md` |
| MINEDU, MINSA | Schools, health posts; public-goods channel |
| DEVIDA / UNODC | Coca cultivation |

## Survey microdata (for the cohort design)

| Source | What |
|---|---|
| **LAPOP / Barómetro de las Américas, Peru** | Age, province (sometimes district), presidential vote and recall, conflict-victimisation items in some waves. Roughly 2006–2023. Free registration |
| ENAHO | Age and geography, no voting |

## Geography

District boundaries and **UBIGEO** codes change over time; Peru created many districts
between 1980 and 2026. A consistent crosswalk is a precondition for everything else — see
`05-threats-to-inference.md`.

## Conventions

- Everything downloaded goes in `data/raw/` untouched, with a note in this file recording
  the URL and the date retrieved.
- `data/raw/` is gitignored. If a source disappears, the only recovery is the note you wrote
  here. Write the note.
- Scripts in `src/` must rebuild `data/processed/` from `data/raw/` with no manual steps.

---

## Provenance of what is actually in the repo (2026-10-21)

`data/raw/results.csv` is committed (an explicit exception in `.gitignore`): it is small,
it is public official results, and the 2026 round is not available from ONPE's open-data
portal at all. Built by `src/build_results.py` from two community mirrors cloned from
GitHub — the only host this environment can reach.

| Election | Source repo | Original source | Unit as published |
|---|---|---|---|
| 2021 first round | `jmcastagnetto/2021-elecciones-generales-peru-datos-de-onpe` | scraped from `resultados.eleccionesgenerales2021.pe` | district |
| 2026 second round | `oscarzamora/onpe-scraper-2026-2` | scraped from the ONPE 2026 runoff results API | mesa de sufragio, aggregated to district here |

Also cloned, for the UBIGEO problem: `jmcastagnetto/ubigeo-peru-aumentado`
(RENIEC↔INEI district code crosswalk). ONPE uses the **RENIEC** ubigeo, not INEI.

### Validation

2026 second round, aggregated from 92,766 counted actas:

| | this aggregation | published | diff |
|---|---|---|---|
| Fujimori (Fuerza Popular) | 9,223,397 | 9,223,396 | +1 |
| Sánchez (Juntos por el Perú) | 9,173,739 | 9,173,755 | −16 |
| share | 50.13% / 49.87% | ~50.1% / ~49.9% | — |

Essentially exact. The 2026 data is sound.

### Known limitation on 2021

The 2021 mirror is a near-final snapshot (`date_upd` 2021-05-11), not the certified final
count. It gives Fujimori 13.40% of valid votes against an official 13.41%, and Castillo
19.06% against an official 18.92%; total valid votes are about 1% below the official figure.
Fine for exploratory work, but **refresh from ONPE's open data before publishing** — the
mirror's own README notes ONPE later released the first round at
`datosabiertos.gob.pe/dataset/resultados-por-mesa-de-las-elecciones-presidenciales-2021-primera-vuelta-oficina-nacional-de`.

### Still missing, and why

`cvr_deaths.csv`, `padron_age.csv` and `controls.csv` could not be obtained. This
environment's network policy gives **no DNS resolution at all** for onpe.gob.pe,
infogob.jne.gob.pe, inei.gob.pe, datosabiertos.gob.pe, cverdad.org.pe, ruv.gob.pe,
arxiv.org, dataverse.harvard.edu, zenodo.org, data.humdata.org and ourworldindata.org.
Only GitHub, PyPI and npm are reachable. A search of GitHub-hosted mirrors found no
district-level CVR death counts; none appears to exist publicly.
