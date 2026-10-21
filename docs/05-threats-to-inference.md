# Threats to inference

Ordered by how likely each one is to sink the paper.

## 1. FONCODES — the confound that will decide whether this publishes

Schady (*APSR* 94(2), 2000) shows that Alberto Fujimori's social fund, FONCODES, spiked its
spending before elections and was steered toward provinces where it would have the largest
political effect. Separately, the claim that Fujimori "strategically invested during the
1990s in towns heavily affected by the war" circulates in the literature on the conflict's
legacies.

If both are true, then "conflict intensity → fujimorista vote" is partly, or wholly,
"conflict intensity → targeted spending → fujimorista vote." For the 2011–2021 elections
this is distant enough to be second-order. **For 1995 and 2000 it is binding**, and those are
precisely the elections this project adds.

**What De la Calle (2024) does and does not do here.** He runs a mediation analysis on the
clientelism channel and finds negligible average causal mediation effects — but his proxy for
Fujimori-era public-goods provision is **growth in district electricity access from 1993 to
2007** (data from Kreiman 2021). That window spans two post-Fujimori administrations and
conflates national electrification policy with targeted political spending. FONCODES is never
mentioned in the paper, and Schady (2000) is not cited.

So the channel is not unexamined, but it has not been tested with actual spending data, and
certainly not on the elections where it matters most. Get district- or province-level FONCODES
allocations (MEF, or Schady's replication data) and redo the mediation on 1995 and 2000.
Handled well this becomes the paper's mechanism section rather than its fatal flaw: did
fujimorismo buy these districts, or did they come to it on their own?

## 2. Perpetrator attribution is academically disputed

The CVR's headline figure is 69,280 deaths (95% CI roughly 61,000–77,500), of which ~46% are
attributed to Sendero Luminoso, ~30% to state agents, and the remainder to rondas/CADs, MRTA
(~1.5%), paramilitary groups and unidentified actors. But the 69,280 is a multiple-systems-
estimation extrapolation from roughly 24,000 directly documented victims, and the perpetrator
split is contested:

- **Rendón (2019)** argues the CVR obtained Sendero's share essentially by subtraction from a
  combined total; re-estimating directly on the strata with sufficient data gives ~48,000 total
  and makes the **state** responsible for the larger share. That is a sign reversal on this
  project's key regressor.
- **Manrique-Vallier & Ball (2019)** reply that Rendón's Sendero estimate falls *below* already-
  observed Sendero deaths — logically impossible — and that his direct estimator carries its own
  selection bias. Their multi-list capture-recapture re-estimation reproduces N ≈ 69,280 with
  perpetrator proportions matching 2003.
- Rendón's rejoinder holds the line. The dispute is unresolved.

**Implication for this project.** The disagreement has so far been fought purely on statistical
grounds, with no downstream application — De la Calle (2024) does not cite Rendón at all, and
works from the CVR's roughly 11,000 fully documented deaths (53% attributed to Sendero) while
acknowledging the database is only a sub-sample. Run the entire analysis under both attributions. If
the results are stable, the paper is robust to the most serious objection available. If the sign
flips, that *is* the paper — the first substantive demonstration that the dispute changes a
real conclusion.

**Direction of the measurement bias is known and works against you.** State violence was
disproportionately enforced disappearance: clandestine, no surviving witnesses, in emergency
zones under military command, against overwhelmingly Quechua-speaking victims with strong
reasons not to testify. Insurgent violence was more often public and witnessed. Testimony
collection was voluntary, and RUV registration depended on non-random NGO and outreach
presence. Net effect: state-attributed deaths are plausibly more under-counted, which biases
against finding state-violence effects. Use the burial-sites registry and EPAF exhumation data
as an independent check on where state killings went unrecorded.

## 3. Displacement breaks the link between places and people

The conflict displaced roughly 600,000 people, overwhelmingly out of the Andean conflict zones
and into Lima's conos. By 2026, "districts where violence happened" and "people who experienced
violence" are badly divergent, and any district-level estimate is partly a composition artifact.

- Attenuates district-level estimates toward zero (treated people left treated districts).
- Contaminates the control group (receiving districts contain treated people).
- Interacts with age: those displaced were disproportionately young adults at the time.

Mitigations: use census questions on place of birth vs. residence to measure net conflict-era
out-migration per district and control for it; and flip the problem into a second paper — did
displaced populations carry conflict-driven voting into Lima?

## 4. District boundary changes

Peru created a substantial number of new districts between 1980 and 2026. UBIGEO codes are
reassigned and split. Nothing in this project works without a consistent crosswalk mapping every
district in every year to a stable 1993-vintage (or 1981-vintage) unit.

This is a few weeks of unglamorous work and it must come first. Build it from INEI UBIGEO
histories and district-creation laws, test it by checking that population and electorate totals
reconcile across boundary changes, and commit the crosswalk as a documented artifact — it is
reusable and other researchers will want it.

Where splits cannot be resolved cleanly, aggregate to **province** (196 units) rather than guess.
Losing resolution is better than a silently wrong merge.

## 5. Reverse causality and selection into violence

Violence was not randomly assigned. Sendero chose where to operate — poorer, more remote,
more indigenous districts with weaker state presence — and the army responded where Sendero was.
So conflict intensity is correlated with everything that also predicts voting.

District fixed effects handle the time-invariant part. For the rest, the honest options are: (a)
lean on the cohort design in `03-age-heterogeneity.md`, which compares cohorts within districts
and so does not need conflict intensity to be exogenous across districts; (b) find an
instrument, knowing the obvious ones (distance to Ayacucho, altitude, pre-1980 peasant
organisation, Guzmán's university networks) are weak and contestable. Route B is the better bet.

## 6. The 2000 election is not a clean observation

Fraudulent, and Toledo boycotted the runoff. Do not pool it silently. See `01-research-design.md`.

## 7. Terruqueo as a competing mechanism

From 2011 onward the right campaigned by accusing opponents of terrorist sympathies. This acts on
voters with no personal conflict memory and is mediated politics, not experience. If the
fujimorista premium in conflict districts survives among unexposed cohorts, terruqueo is the
leading explanation. The existing literature on it is entirely qualitative — there is room to be
the first to measure it, but it needs a measurement strategy (campaign-event data, media content,
or candidate-level rhetoric coded by district-level exposure).
