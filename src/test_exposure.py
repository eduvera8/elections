"""Self-contained checks for src/exposure.py. Run: python3 -m pytest src/ -q
or, with no pytest installed: python3 src/test_exposure.py
"""
from exposure import AgeBand, exposed_share, exposure_profile, threshold_age, unexposed_share

# A flat synthetic electorate: 1000 voters in every 5-year band from 18 to 80.
FLAT = [AgeBand(lo, lo + 5, 1000) for lo in range(18, 80, 5)] + [AgeBand(80, None, 1000)]


def test_threshold_age():
    # Adults (18+) in 1992, observed in the 2026 election, are 52 or older.
    assert threshold_age(2026, 1992, 18) == 52
    # In 1995, the same cohort is 21 or older.
    assert threshold_age(1995, 1992, 18) == 21


def test_reference_after_election_rejected():
    try:
        threshold_age(1995, 2000, 18)
    except ValueError:
        return
    raise AssertionError("expected ValueError when reference_year > election_year")


def test_everyone_exposed_in_1995():
    # Threshold is 21; only the 18-20 part of the first band is unexposed.
    s = exposed_share(FLAT, 1995, reference_year=1992, min_age_at_reference=18)
    assert 0.94 < s < 0.99, s


def test_exposure_falls_over_time():
    years = [1995, 2000, 2001, 2006, 2011, 2016, 2021, 2026]
    profile = exposure_profile({y: FLAT for y in years})
    shares = [profile[y] for y in years]
    assert shares == sorted(shares, reverse=True), shares
    assert shares[0] > shares[-1]


def test_interpolation_at_band_edge():
    # Threshold exactly on a band boundary: no interpolation, clean split.
    bands = [AgeBand(18, 50, 100), AgeBand(50, None, 100)]
    s = exposed_share(bands, 1992 + 32, reference_year=1992, min_age_at_reference=18)
    assert abs(s - 0.5) < 1e-9, s


def test_unexposed_is_zero_before_conflict_end():
    assert unexposed_share(FLAT, 1995) == 0.0
    assert unexposed_share(FLAT, 2000) == 0.0


def test_unexposed_cohort_enters_only_in_2021():
    # Someone born in 2001 turns 18 in 2019, so the first election with any
    # fully unexposed voters is 2021. Before that the share is exactly zero even
    # though the conflict ended in 2000.
    assert unexposed_share(FLAT, 2011) == 0.0
    s21 = unexposed_share(FLAT, 2021)
    s26 = unexposed_share(FLAT, 2026)
    assert s26 > s21 > 0, (s21, s26)


def test_empty_electorate_rejected():
    try:
        exposed_share([AgeBand(18, 25, 0)], 2026)
    except ValueError:
        return
    raise AssertionError("expected ValueError on zero electorate")


def test_bad_band_rejected():
    for bad in [lambda: AgeBand(25, 18, 10), lambda: AgeBand(-1, 20, 10), lambda: AgeBand(18, 25, -5)]:
        try:
            bad()
        except ValueError:
            continue
        raise AssertionError("expected ValueError on malformed AgeBand")


if __name__ == "__main__":
    import sys
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} checks passed")
    sys.exit(0)
