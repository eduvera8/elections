# Age and cohort heterogeneity

> This is the project's core analytical contribution. The claim being tested is narrow and
> falsifiable: **if conflict legacies work through personal memory, the effect must be
> concentrated in cohorts who experienced the violence firsthand, and must decay as those
> cohorts leave the electorate.**

> De la Calle (2024) — the leading paper in this literature — finds the conflict gradient
> weakening across 2011, 2016 and 2021 and attributes it, in his conclusion, to "the
> decreasing political clout of the age cohorts with direct experience of the conflict."
> He does not test it: no age data, no cohort measure, no panel. See
> `06-delacalle-2024-notes.md`. **Our job is to run that test.**

## 1. The exposure arithmetic

The conflict ran 1980–2000, with peaks around 1983–84 and 1989–92. Guzmán was captured in
September 1992. Voting age in Peru is 18. (Note: illiterate citizens were enfranchised by
the 1979 constitution, which matters because conflict zones were disproportionately
illiterate and Quechua-speaking — the conflict coincides with the first elections in which
those populations could vote at all.)

Birth cohorts, and what they experienced:

| Born | Age in 1983 (peak) | Age in 1992 (capture) | Age in 2026 | Exposure |
|------|--------------------|-----------------------|-------------|----------|
| ≤1962 | 21+ | 30+ | 64+ | Adult for the entire conflict |
| 1963–1974 | 9–20 | 18–29 | 52–63 | Child at the peak, adult by the end |
| 1975–1982 | — | 10–17 | 44–51 | Childhood/adolescence under the conflict |
| 1983–2000 | — | — | 26–43 | Born into it or after the peak; little/no memory |
| 2001–2008 | — | — | 18–25 | **Zero personal exposure** |

Two consequences that drive the whole design:

- **In 1995, there is almost no young/old contrast on "lived through it at all."** Every
  voter in 1995 (born ≤1977) was alive and in Peru during the worst years. The only
  available contrast is *adult* vs. *child* exposure.
- **By 2026, a substantial block of the electorate (roughly the 18–25 band) has no
  personal exposure whatsoever.** The share of the electorate with firsthand adult memory
  falls monotonically across 1995 → 2026.

That monotonic decline is the source of identification. It is not a nuisance; it is the
treatment.

**A third consequence, found while implementing `src/exposure.py`:** the *fully* unexposed
cohort — born after the conflict formally ended in 2000 — only reaches voting age in 2019.
So the clean "no personal memory at all" comparison group exists **only in 2021 and 2026**.
Before that, every voter in every election had lived through at least part of the conflict.
This sharpens the case for including 2026: it is the second of only two elections in which
the zero-exposure contrast is available at all, and the first in which that cohort is large
enough to matter.

## 2. The problem: official results have no age

ONPE and JNE publish results by *distrito* and by *mesa de sufragio*. Neither carries voter
age. So age heterogeneity has to be recovered indirectly. Three routes, in ascending order
of credibility and descending order of feasibility.

### Route A — Ecological interaction (district level). Feasible now.

Interact conflict intensity with the district's share of the electorate old enough to have
experienced the conflict:

```
vote_share[d,t] = β1·conflict[d] + β2·(conflict[d] × exposed_share[d,t])
                + β3·exposed_share[d,t] + X[d,t]·γ + δ[region,t] + ε[d,t]
```

where `exposed_share[d,t]` is the fraction of district *d*'s registered electorate in year
*t* who were ≥18 (or ≥12, as an alternative) during the conflict peak.

Source for `exposed_share`: the **padrón electoral**, published by ONPE/RENIEC for each
election with counts by district × sex × age group. This is the critical dataset for this
project and the first thing to acquire. Where padrón age breakdowns are unavailable for
older elections, fall back to INEI census age structure (1981, 1993, 2007, 2017) and
interpolate — but document the substitution, since census residence and electoral
registration diverge in exactly the migration-heavy districts we care about.

Weakness: this is an ecological interaction. A positive β2 is consistent with the memory
mechanism but also with anything else that correlates with having an older electorate
(out-migration of the young, rurality, lower education). Treat Route A as descriptive.

### Route B — Cohort-exposure at the individual level. The credible design.

Use survey microdata with respondent age, district/province, and vote choice, and define
exposure as *age during the district's own peak-violence years*:

```
exposure[i] = f( violence[district(i), years when i was aged a..a+k] )
```

This is the design in **León (2012, Journal of Human Resources)** on the conflict's
human-capital effects, which uses district × birth-cohort exposure to CVR violence. Borrow
it wholesale; the precedent is well established and referees know it.

It gives a **within-district, across-cohort** comparison, which differences out everything
fixed about the district — poverty, rurality, altitude, FONCODES money, distance to Lima.
That is a far stronger claim than Route A can support.

Candidate data: LAPOP / Barómetro de las Américas Peru waves (roughly 2006–2023) — age,
province (sometimes district), presidential vote and vote recall, and conflict-victimization
items in some waves. ENAHO has excellent geography and age but does not ask about voting.

Weakness: survey samples are thin in exactly the small, high-violence Andean districts
where the treatment is strongest. Expect to pool waves and work at province level.

### Route C — Mesa-level, *if* the padrón is age-ordered. Verify before investing.

ONPE publishes results at *mesa de sufragio* level. In some countries, voters are allocated
to polling tables in an order correlated with birth year (e.g. by registration or document
number). **If Peru's padrón does this, mesa-level results approximate cohort-level results
and this project gets a near-experimental design for free.**

I do not know whether Peru's padrón is ordered this way, and it should not be assumed.
Verify against ONPE's padrón-formation documentation and, if possible, by checking whether
the age composition of individual mesas is published or inferable. This is the single
highest-value thing to check early: if Route C works, it supersedes A and B.

## 3. The overidentifying test — cohort replacement

This is what the eight-election panel buys and what a three-election panel cannot do.

If the effect is carried by firsthand memory, then the district-level coefficient on
conflict intensity should **decay across elections at a rate predicted by cohort
replacement**. Concretely: construct `exposed_share[d,t]` for each of the eight elections,
and test whether the estimated β1[t] tracks the national decline in exposed share.

- Coefficient decays in step with cohort replacement → consistent with personal memory.
- Coefficient stable while exposed share falls → the effect is being transmitted to
  unexposed cohorts (family socialisation, local political organisation, party machines),
  **not** carried by memory. That is a different and arguably more interesting finding.
- Coefficient grows → look for a confound; something other than the conflict is loading on
  these districts (most likely candidate: the post-2000 reorganisation of the party system
  and the rise of regional movements).

Write the prediction down before estimating. A pre-registered cohort-decay profile is what
separates this from a fishing expedition.

## 4. Four things that will complicate the age story

1. **Mortality selection.** The violence killed people, and the dead do not vote. High-violence
   districts lost adults, so the surviving old cohort there is selected on survival. The
   direction of bias depends on who was targeted, which differs by perpetrator — Sendero's
   victims included local authorities and leaders, state violence fell on suspected
   sympathisers.
2. **Displacement is age-structured.** Roughly 600,000 people were displaced, disproportionately
   young adults at the time. Those who stayed or returned are today's old cohort. So "old
   voters in high-violence districts" is a doubly selected population — survived, and did not
   leave. Conversely, the displaced carried their experience to Lima's conos, where it is now
   attributed to low-violence receiving districts. This biases district-level estimates toward
   zero and is worth studying in its own right.
3. **Intergenerational transmission.** Young voters in conflict districts did not experience the
   violence but were raised by people who did. An age-null result is therefore **not** evidence
   against a memory mechanism — it may be evidence of transmission. This is why the cohort
   *gradient* matters more than a binary old/young split.
4. **Terruqueo as a competing channel.** From 2011 onward, and especially in 2021, the right
   campaigned by accusing opponents of terrorist sympathies. That mechanism works on voters
   with *no* personal conflict memory — it is mediated politics, not experience. If the
   fujimorista premium in conflict districts holds up among unexposed cohorts in 2021 and
   2026, terruqueo is a plausible explanation and should be modelled, not residualised.
   The existing terruqueo literature is entirely qualitative, so there is room here.

## 5. Immediate next steps

1. Verify whether the padrón electoral is age-ordered at mesa level (Route C). Highest value.
2. Acquire padrón electoral by district × age group for all eight elections.
3. Build the district crosswalk (see `docs/05-threats-to-inference.md`) — nothing works without it.
4. Construct `exposed_share[d,t]` and plot its national decline 1995 → 2026. That single figure
   is the paper's motivating graphic.
