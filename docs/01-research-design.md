# Research design

## Question

Do Peruvian districts that suffered more political violence in 1980–2000 vote differently in
1995–2026, and does the answer depend on (a) which actor did the killing and (b) the age
composition of the electorate?

## Contribution relative to De la Calle (2024)

De la Calle, *Electoral Studies* 90 (2024) 102827, is the direct precedent. District-level,
first rounds of 2011/2016/2021, outcome = vote shares for Keiko Fujimori and three main
left candidates, key regressor = deaths attributed to Sendero *relative to* deaths by
security forces, plus Sendero territorial presence. Finding: conflict-affected districts
give Fujimori a premium and the left a penalty, robust to crime, poverty, COVID-19 deaths
and long-run marginalisation; Castillo partly offset it in 2021 in poor and COVID-hit
districts.

**That paper has not been read yet** — the environment had no network access and the upload
did not arrive. Read it first and revise this document. Everything here assumes the summary
above is accurate; confirm the specification, the controls, and whether it uses runoffs or
only first rounds before claiming any gap.

Four extensions, in order of how defensible they are:

1. **Panel extension backwards (1995, 2000, 2001, 2006).** Covers the period when the
   mechanism formed and Alberto was personally on the ballot.
2. **Panel extension forwards (2026).** New data; first fujimorista win since 1995.
3. **Age/cohort heterogeneity and the cohort-replacement test.** See `03-age-heterogeneity.md`.
4. **Three-way perpetrator split** — Sendero / armed forces / rondas campesinas-CADs —
   instead of a single ratio. The rondas were state-allied but locally recruited and locally
   commanded; blame attribution should behave differently for them than for the army, and
   nobody appears to have separated them.

## Outcomes

For each election *t* and district *d*:

- Fujimorista vote share (first round and, where applicable, runoff)
- Left vote share (define the bloc explicitly per election; this is a coding decision that
  needs a documented rule, not ad-hoc judgement)
- Turnout
- **Blank + null share** (`voto blanco` / `viciado`). Peru has compulsory voting with fines,
  so spoiling is a genuine exit option rather than apathy. Two reasons this matters here:
  conflict districts are where Sendero burned ballots and enforced boycotts (Chuschi, 1980),
  and the 2000 runoff — which Toledo boycotted — produced a very large deliberate spoiled
  vote that is itself a protest measure.

## Key regressors

From the CVR victim database and/or the RUV, aggregated to district:

- Deaths per 1,000 inhabitants, by presumed perpetrator: Sendero Luminoso, state agents,
  rondas campesinas/CADs, MRTA, other/unknown
- Enforced disappearances specifically (a state-violence signature)
- Sendero territorial presence (binary or intensity)
- Timing: deaths in 1980–85 vs 1986–92 vs 1993–2000, to allow the exposure arithmetic in
  `03-age-heterogeneity.md`

**Do not use MRTA as a separate treatment.** At roughly 1.5% of deaths, concentrated in San
Martín, Junín and urban Lima, and largely selective and urban, there is not enough
district-level variation. Fold it into "insurgent" and say so.

## Specification

Baseline, district fixed effects where the panel allows:

```
y[d,t] = α[d] + τ[t] + Σ_p β[p,t]·deaths[d,p] + X[d,t]·γ + ε[d,t]
```

With district fixed effects, the time-invariant conflict measures are absorbed, so the
object of interest is the **interaction with election year** — i.e. how the conflict gradient
evolves across 1995 → 2026. That is the right target anyway given the cohort-replacement test.

Report everything twice: once with CVR perpetrator attribution, once with Rendón's. If the
sign on the perpetrator split flips, that is a finding in its own right and a direct
empirical intervention in an unresolved statistical dispute (see `05-threats-to-inference.md`).

## Controls

Poverty, rurality, altitude, Quechua/indigenous-language share, education, distance to Lima,
contemporary crime, coca cultivation, mining canon transfers, regional × year fixed effects.
And — non-negotiable for the 1990s elections — FONCODES allocations (see
`05-threats-to-inference.md`).

## Handle 2000 separately

The 2000 election was fraudulent and Toledo withdrew from the runoff. Do not pool it with
clean elections without comment. It is still useful: the first round is informative about
geography, and the runoff's spoiled-ballot share is a clean protest measure. Report it as a
separate case, not as one more panel period.

## Candidate journals

*Electoral Studies*, *Comparative Political Studies*, *Journal of Peace Research*, *Journal of
Conflict Resolution*, *Latin American Politics and Society*, *Political Behavior*.
