# Reading notes: De la Calle (2024)

**Luis De la Calle (University of Sheffield), "When rebels lose: The impact of civil war
legacies on contemporary electoral outcomes in Peru, 2011–2021," *Electoral Studies* 90
(2024) 102827.** Open access, CC BY. Received 19 Jun 2023, accepted 1 Jul 2024.
PDF is committed at the repository root.

**Read in full.** These notes are the basis for the gap analysis in `01-research-design.md`.

## Argument

A 2×2 typology: who won the war × who did more of the killing. Peru occupies the
under-studied cell — **incumbent won, rebels did more of the killing** — and the prediction
is that the winner's successor party gets a victimisation premium while parties ideologically
aligned with the defeated rebels are penalised. Two hypotheses:

- **H1** More rebel violence/presence → more support for Keiko Fujimori
- **H2** More rebel violence/presence → less support for left-wing candidates

Mechanism: Sendero governed by coercion with almost no public-goods provision, so it generated
pure grievance; and because it never transitioned into a legal party (unlike the FMLN or the
Nepali Maoists), its violence stayed politically unredeemed while the state's role was
minimised in the victors' national narrative.

## Design — and the four limits that define this project's opening

- **Unit**: district. **Elections**: first rounds of 2011, 2016, 2021 only.
- **Outcomes**: vote share for Keiko Fujimori, and for Humala (2011), Mendoza (2016),
  Castillo (2021).
- **Estimator**: OLS, robust SEs, dummies for five macro-regions (Lima/Callao, Coast,
  Amazonas, northern Andes, southern Andes).
- **N**: 809 in the Andean-only models of Table 4.

Four things it does **not** do, each of which this project can:

1. **No panel, no district fixed effects, no instrument.** Zero occurrences of "panel",
   "fixed effect" or "instrument" in the paper. Six separate cross-sections, one per
   candidate-year. So the across-election change in coefficients is never formally tested.
2. **Only three elections, all first rounds.** 1995, 2000, 2001, 2006 and 2026 are absent.
   (2006 appears in a descriptive table only, noting Keiko did not run and Martha Chávez was
   the party's frontrunner.)
3. **No engagement with the attribution dispute.** Rendón is not cited; neither is the RUV.
   The paper uses the CVR's documented records and states plainly that "around 53 percent of
   the 11,000 fully documented deaths were caused by Sendero," acknowledging the database is
   "only a sub-sample of all killings."
4. **No age or cohort analysis** — see below, which is the important part.

## Key regressors

- **"Difference in killings" = SP deaths minus state-repression deaths.** Positive = more
  rebel violence, negative = more state repression. He adopts the difference because the two
  counts correlate at 0.76. **He concedes the cost explicitly: the measure assigns 0 both to
  peaceful districts and to districts with heavy two-sided violence.** That throws away
  precisely the hardest-hit districts of Ayacucho, Huancavelica and Apurímac. Separated
  measures are in the Online Appendix (Tables 4A–5A), reportedly unchanged.
- **Rebel presence**, from Sendero's capacity to disrupt the municipal elections of 1980,
  1983, 1986 and 1989, coded in three levels: safe state control (no disruption);
  *contested* (election held but >50% spoiled ballots); *full rebel control* (election not
  held, or turnout <50%). Entered as the proportion of those election years spent in each
  state. Note he uses turnout and spoiled ballots as a **wartime** measure of rebel control —
  not as a contemporary outcome, so the blank/null-vote outcome idea in
  `01-research-design.md` is not pre-empted.
- Robustness: replicates León (2012)'s dichotomised violence indicator (Tables 6A–7A) and
  province-level aggregation (Tables 9A–10A).

## Controls

Spanish-speaker share from the 1981 census (proxy for historical marginalisation and state
weakness); land redistributed under the revolutionary government (Guardado 2018); recognised
peasant community (Instituto del Bien Común); Izquierda Unida mayoral wins in any of
1980/83/86/89 as prewar left strength; **Alberto Fujimori's 1990 first-round vote** (to test
whether the legacy is endogenous to pre-existing Fujimori support — he flags serious missing
data, since the 1990 election could not run properly in many districts under rebel threat);
INEI monetary poverty 2013 and 2018; 2016 homicide rate; COVID-19 deaths per capita as of
11 April 2021 (datosabiertos.gob.pe); population 2015; district size; distance to provincial
capital; provincial-capital dummy.

## Results

Table 3, coefficient on the difference-in-killings measure:

| | 2011 | 2016 | 2021 |
|---|---|---|---|
| Keiko Fujimori | **0.06\*** | **0.06\*** | **0.04+** |
| Leading left candidate | −0.05\* (Humala) | −0.05\*\* (Mendoza) | −0.03 n.s. (Castillo) |

Rebel "full control" is large for Fujimori (8.57\*\*, 11.92\*\*, 7.13\*\*) and strongly negative
for Humala (−13.23\*\*).

**Note the decay.** 0.06 → 0.06 → 0.04, with significance falling to the 10% level by 2021;
on the left side, −0.05 → −0.05 → −0.03 and insignificant. The gradient is weakening across
the three elections — but with six separate cross-sections, **the decline is never tested**.

Section 7: in Andean districts, poverty and COVID-19 deaths interact with rebel control such
that Castillo partly neutralised the left's penalty in poor and pandemic-hit districts.

## Mechanism test he does run

A mediation analysis (Imai et al. 2011) on the clientelism channel, using **growth in
district electricity access 1993→2007** (data from Kreiman 2021) as a proxy for Fujimori-era
public-goods provision. ACMEs are negligible in every specification, which he reads as
consistent with — though not proof of — the victimisation path rather than the clientelist one.

He cites Soifer & Vieira (2019) and Kreiman (2021) for the claim that Fujimori invested
strategically in war-affected towns.

**This is where FONCODES belongs and does not appear.** FONCODES is never mentioned in the
paper. Electricity-access growth over 1993–2007 is a coarse proxy: it spans two
post-Fujimori administrations and conflates electrification policy with targeted political
spending. Schady's (2000) province-level FONCODES allocations are the direct measure, and
they cover exactly the 1991–95 window this project adds. Redoing the mediation with actual
spending data, on the 1995 and 2000 elections where it bites hardest, is a well-defined
contribution rather than a quibble.

## The conclusion hands us the project

> "…this legacy seems to be waning, a trend also observed in other conflicts in the region
> (Gillooly 2022) and perhaps **related to the decreasing political clout of the age cohorts
> with direct experience of the conflict** (Maldonado et al. 2019)."

That is the age/cohort hypothesis in `03-age-heterogeneity.md`, stated by the author of the
leading paper in the field, offered as the likely explanation for his own central dynamic
finding — and **not tested**. He has no age data, no cohort measure, and no panel in which
to test a decay rate.

This is as clean a position for a follow-up as one gets. The contribution is not "we
disagree with De la Calle"; it is "De la Calle's own proposed explanation for the waning
legacy is testable, and here is the test." Three things make it possible:

1. A panel from 1995 to 2026 — eight elections instead of three — so the decay is estimable
   rather than eyeballed across separate cross-sections.
2. `exposed_share[d,t]` from the padrón electoral, so cohort replacement is measured rather
   than assumed.
3. 2026, which he anticipates in the conclusion ("Keiko Fujimori may well capitalize on this
   opportunity for a final bid") and which duly happened — she won.

Follow up **Maldonado, Merolla & Zechmeister (2019)**, "Public opinion, the specter of
violence, and democracy in contemporary Peru," in Soifer & Vergara (eds.), *Politics after
Violence*. It is the citation behind the cohort claim and likely holds individual-level survey
evidence on age and conflict memory — the natural Route B complement.
