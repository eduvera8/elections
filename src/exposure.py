"""Cohort-exposure arithmetic for the Peru conflict-legacies project.

Turns a banded age distribution of a district's electorate into the share that was
old enough to have experienced the internal armed conflict firsthand.

The quantity of interest, `exposed_share[d, t]`, is defined as:

    the fraction of district d's registered electorate in election year t who were
    at least `min_age_at_reference` years old in `reference_year`

A voter aged `a` in election year `t` was aged `a - (t - reference_year)` in the
reference year. So the condition "was at least `m` years old in year `r`" becomes a
simple threshold on current age:

    a >= m + (t - r)

Example: to capture voters who were adults (18+) at the height of the violence in
1992, in the 2026 election, the threshold age is 18 + (2026 - 1992) = 52.

Reference years worth reporting side by side:
    1983  first peak
    1992  Guzman's capture; the violence's political turning point
    2000  formal end of the CVR's mandate period

See docs/03-age-heterogeneity.md for the design this feeds.
"""

from __future__ import annotations

from dataclasses import dataclass

CONFLICT_START = 1980
CONFLICT_END = 2000


@dataclass(frozen=True)
class AgeBand:
    """A half-open age band [lo, hi) and the number of registered voters in it.

    The open-ended top band (e.g. "70+") is represented by hi=None and is treated as
    closed at `OPEN_TOP_ASSUMED_HI` when interpolation is needed.
    """

    lo: int
    hi: int | None
    count: float

    OPEN_TOP_ASSUMED_HI = 100

    @property
    def upper(self) -> int:
        return self.OPEN_TOP_ASSUMED_HI if self.hi is None else self.hi

    def __post_init__(self) -> None:
        if self.lo < 0:
            raise ValueError(f"age band lower bound must be non-negative, got {self.lo}")
        if self.hi is not None and self.hi <= self.lo:
            raise ValueError(f"age band must have hi > lo, got [{self.lo}, {self.hi})")
        if self.count < 0:
            raise ValueError(f"voter count must be non-negative, got {self.count}")


def threshold_age(election_year: int, reference_year: int, min_age_at_reference: int) -> int:
    """Current age above which a voter met the exposure condition.

    Raises if the reference year is after the election year, which would mean asking
    about an age the electorate had not yet reached.
    """
    if reference_year > election_year:
        raise ValueError(
            f"reference_year {reference_year} is after election_year {election_year}"
        )
    return min_age_at_reference + (election_year - reference_year)


def exposed_share(
    bands: list[AgeBand],
    election_year: int,
    reference_year: int = 1992,
    min_age_at_reference: int = 18,
) -> float:
    """Share of the electorate at or above the exposure threshold age.

    Bands that straddle the threshold are split by linear interpolation, which assumes
    voters are uniformly distributed within a band. That assumption is mild for the
    5-year bands the padron electoral typically uses and gets worse for wide bands; if
    your source only publishes wide bands, say so in the paper rather than hiding it.

    Returns a share in [0, 1]. Raises ValueError on an empty electorate.
    """
    if not bands:
        raise ValueError("no age bands supplied")

    total = sum(b.count for b in bands)
    if total <= 0:
        raise ValueError("total electorate is zero; cannot compute a share")

    cut = threshold_age(election_year, reference_year, min_age_at_reference)
    exposed = 0.0

    for b in bands:
        if b.lo >= cut:
            exposed += b.count
        elif b.upper > cut:
            width = b.upper - b.lo
            exposed += b.count * (b.upper - cut) / width

    return exposed / total


def exposure_profile(
    bands_by_year: dict[int, list[AgeBand]],
    reference_year: int = 1992,
    min_age_at_reference: int = 18,
) -> dict[int, float]:
    """exposed_share for each election year, for the cohort-replacement test.

    The decline in this series across 1995 -> 2026 is the project's motivating figure:
    if the conflict effect is carried by personal memory, the estimated conflict
    coefficient should decay in step with it.
    """
    return {
        year: exposed_share(bands, year, reference_year, min_age_at_reference)
        for year, bands in sorted(bands_by_year.items())
    }


def unexposed_share(bands: list[AgeBand], election_year: int) -> float:
    """Share of the electorate born after the conflict ended — zero personal exposure.

    These are the voters for whom any conflict effect must be transmitted rather than
    remembered (family socialisation, party machines, terruqueo).
    """
    cut = election_year - CONFLICT_END
    if cut <= 0:
        return 0.0
    total = sum(b.count for b in bands)
    if total <= 0:
        raise ValueError("total electorate is zero; cannot compute a share")

    unexposed = 0.0
    for b in bands:
        if b.upper <= cut:
            unexposed += b.count
        elif b.lo < cut:
            width = b.upper - b.lo
            unexposed += b.count * (cut - b.lo) / width
    return unexposed / total
