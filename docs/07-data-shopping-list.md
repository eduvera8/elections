# What data is needed, in priority order

Run `python3 src/schema.py` for the exact columns. Put files in `data/raw/`. The pipeline
degrades gracefully, so partial data still produces output — it reports what it could run
and what each missing file would unlock.

## Tier 0 — two files, and the project has an answer

| File | Where | What to pull |
|---|---|---|
| `results.csv` | ONPE (`resultados.onpe.gob.pe`) or JNE Infogob (`infogob.jne.gob.pe`) | District-level presidential results. **2021 and 2026 first rounds are enough to start.** Columns: ubigeo, year, round, fujimorista_votes, left_votes, valid_votes, blank_null_votes, registered |
| `cvr_deaths.csv` | CVR victim database (`cverdad.org.pe`) | Deaths by district and presumed perpetrator, collapsed to: ubigeo, perpetrator (sendero/state/rondas/mrta/other), deaths |

With just these two, the pipeline runs Model A and answers the question that decides whether
the project is worth continuing:

**Is the conflict gradient still there in 2026, and is it weaker than in 2021?**

- Gradient has kept shrinking → De la Calle's cohort-decay conjecture gains support, and the
  cohort test becomes the paper.
- Gradient jumped back up in 2026, the year fujimorismo finally won → his decay story is
  wrong or incomplete, and *that* is the paper.
- Gradient is gone → the legacy has expired; a shorter paper documenting the end of it, with
  the cohort data as the explanation.

All three outcomes are publishable. There is no version of this result that wastes the day.

## Tier 1 — the file that makes the project novel

| File | Where | What to pull |
|---|---|---|
| `padron_age.csv` | ONPE / RENIEC padrón electoral | Registered electors by **district x age band** for each election year. Columns: ubigeo, year, age_lo, age_hi, voters |

Without this there is no cohort test and the project is a replication with extra years. With
it, Model C estimates whether the conflict gradient lives in cohorts who remember the
conflict firsthand — the mechanism De la Calle proposes and does not test.

If ONPE only publishes the padrón by age for recent elections, substitute INEI census age
structure (1981, 1993, 2007, 2017) for the earlier years and interpolate. Document the
substitution; census residence and electoral registration diverge in exactly the
migration-heavy districts that matter here.

## Tier 2 — credible specifications

| File | Where | What to pull |
|---|---|---|
| `controls.csv` | INEI | ubigeo, population, region, poverty_rate, spanish_share_1981, rural |

## Faster than downloading anything: ask the author

The paper's data availability statement reads **"Data will be available on my website."** There
is no repository deposit. Luis De la Calle is at the University of Sheffield and his email is
printed on the paper's first page (`l.delacalle@sheffield.ac.uk`).

His dataset already contains the CVR deaths coded by perpetrator at district level, his
three-level wartime rebel-control measure built from the 1980–89 municipal elections, and all
his controls. Asking for it would save weeks of assembly and costs one email. Academics
normally share, and the request is flattering: you are extending the paper, not attacking it.

It does not cover 1995–2006 results, 2026, or the padrón age data — those still need
collecting — but it removes the hardest part.

## On Maldonado, Merolla & Zechmeister (2019)

Not available, and **not blocking.** It is the citation behind De la Calle's cohort remark and
would have offered individual-level corroboration, not the test itself. The district-level
cohort design in `03-age-heterogeneity.md` stands without it.

If individual-level evidence is wanted later, LAPOP / Barómetro de las Américas Peru is free
after registration and has age, province, and vote choice across roughly 2006–2023 — the
Route B substitute.

## District boundary changes

Peru created districts throughout this period, so `ubigeo` codes are not stable across 1995–2026.
The pipeline joins on `ubigeo` as given and will silently mismatch split districts. For the
Tier 0 check across 2021 and 2026 this barely bites — two adjacent elections, few changes. For
the full 1995–2026 panel it has to be fixed first; see `05-threats-to-inference.md` §4.
