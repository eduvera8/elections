"""Build data/raw/results.csv from the ONPE mirrors cloned from GitHub.

    python3 -I src/build_results.py --onpe2021 DIR --onpe2026 DIR --out data/raw/results.csv

Sources (both are community mirrors of ONPE output, not ONPE itself):

  2021 first round  jmcastagnetto/2021-elecciones-generales-peru-datos-de-onpe
                    District-level, scraped from resultados.eleccionesgenerales2021.pe
  2026 second round oscarzamora/onpe-scraper-2026-2
                    Mesa-level, aggregated to district here

Both are read as untrusted input: paths are passed as arguments and nothing in them
is imported or executed.

A note on UBIGEO: ONPE uses the RENIEC code, not the INEI code. The 2021 mirror carries
both, so this script reports which convention the 2026 mirror follows rather than
assuming. Whichever it is, the output uses ONPE/RENIEC codes consistently and keeps the
INEI code alongside where available.
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

FUJIMORISTA_2021 = "FUERZA POPULAR"
LEFT_2021 = "PARTIDO POLITICO NACIONAL PERU LIBRE"  # Castillo, per De la Calle's coding
PID_FUJIMORISTA_2026 = "8"   # Fuerza Popular, Keiko Fujimori
PID_LEFT_2026 = "10"         # Juntos por el Peru, Roberto Sanchez
PID_BLANK, PID_NULL, PID_CONTESTED = "80", "81", "82"


def _rows(path: Path, delim: str = ","):
    with path.open(newline="", encoding="utf-8") as f:
        yield from csv.DictReader(f, delimiter=delim)


def _int(x: str) -> int:
    return int(float(str(x).replace(",", "").strip() or 0))


def load_2021(d: Path) -> tuple[dict, dict]:
    """District-level 2021 first round. Returns (records, ubigeo->ubigeo_inei)."""
    rec: dict[str, dict] = defaultdict(lambda: defaultdict(int))
    inei: dict[str, str] = {}

    for r in _rows(d / "presidencial-resultados-partidos.csv"):
        u = r["ubigeo"]
        inei[u] = r.get("ubigeo_inei", "")
        if r["partido"] == FUJIMORISTA_2021:
            rec[u]["fujimorista_votes"] += _int(r["total_votos"])
        elif r["partido"] == LEFT_2021:
            rec[u]["left_votes"] += _int(r["total_votos"])

    for r in _rows(d / "presidencial-datos-votos.csv"):
        u, m, n = r["ubigeo"], r["metrica"], _int(r["cantidad"])
        if m == "TOTAL DE VOTOS VÁLIDOS":
            rec[u]["valid_votes"] = n
        elif m in ("VOTOS EN BLANCO", "VOTOS NULOS"):
            rec[u]["blank_null_votes"] += n

    for r in _rows(d / "presidencial-datos-generales.csv"):
        rec[r["ubigeo"]]["registered"] = _int(r["ELECTORES_HABIL"])

    return rec, inei


def load_2026(d: Path) -> dict:
    """Mesa-level 2026 second round, aggregated to district."""
    mesa_ubigeo: dict[str, str] = {}
    rec: dict[str, dict] = defaultdict(lambda: defaultdict(int))

    for r in _rows(d / "mesas_data.txt", "\t"):
        if r["codigo_estado_acta"] != "C":  # only counted actas
            continue
        key = r["codigo_mesa"]
        mesa_ubigeo[key] = r["id_ubigeo"]
        rec[r["id_ubigeo"]]["registered"] += _int(r["electores_habiles"])

    unmatched = 0
    for r in _rows(d / "votos.txt", "\t"):
        u = mesa_ubigeo.get(r["codigo_mesa"])
        if u is None:
            unmatched += 1
            continue
        v, pid = _int(r["votos"]), r["partido_id"]
        if pid == PID_FUJIMORISTA_2026:
            rec[u]["fujimorista_votes"] += v
            rec[u]["valid_votes"] += v
        elif pid == PID_LEFT_2026:
            rec[u]["left_votes"] += v
            rec[u]["valid_votes"] += v
        elif pid in (PID_BLANK, PID_NULL):
            rec[u]["blank_null_votes"] += v
        elif pid == PID_CONTESTED:
            rec[u]["contested_votes"] += v
    if unmatched:
        print(f"  ! {unmatched:,} vote rows had no matching counted acta (dropped)")
    return rec


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--onpe2021", required=True, type=Path)
    ap.add_argument("--onpe2026", required=True, type=Path)
    ap.add_argument("--out", default=Path("data/raw/results.csv"), type=Path)
    a = ap.parse_args(argv)

    print("2021 first round:")
    r21, inei = load_2021(a.onpe2021)
    print(f"  {len(r21):,} districts")

    print("2026 second round:")
    r26 = load_2026(a.onpe2026 / "output")
    print(f"  {len(r26):,} districts (incl. overseas constituencies)")

    # Which UBIGEO convention does the 2026 mirror use? Report, do not assume.
    onpe_keys, inei_keys = set(r21), {v for v in inei.values() if v}
    print(f"  ubigeo overlap with 2021 ONPE/RENIEC codes: "
          f"{len(set(r26) & onpe_keys):,} / {len(r26):,}")
    print(f"  ubigeo overlap with 2021 INEI codes:        "
          f"{len(set(r26) & inei_keys):,} / {len(r26):,}")

    a.out.parent.mkdir(parents=True, exist_ok=True)
    cols = ["ubigeo", "ubigeo_inei", "year", "round", "fujimorista_votes",
            "left_votes", "valid_votes", "blank_null_votes", "registered"]
    n = 0
    with a.out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for year, rnd, rec in [(2021, 1, r21), (2026, 2, r26)]:
            for u, d in sorted(rec.items()):
                if not d.get("valid_votes"):
                    continue
                w.writerow({
                    "ubigeo": u,
                    "ubigeo_inei": inei.get(u, ""),
                    "year": year, "round": rnd,
                    "fujimorista_votes": d.get("fujimorista_votes", 0),
                    "left_votes": d.get("left_votes", 0),
                    "valid_votes": d["valid_votes"],
                    "blank_null_votes": d.get("blank_null_votes", 0),
                    "registered": d.get("registered", 0),
                })
                n += 1
    print(f"\nwrote {a.out} ({n:,} district-election rows)")

    # National totals, as a check against the published result.
    for year, rnd, rec in [(2021, 1, r21), (2026, 2, r26)]:
        fuji = sum(d.get("fujimorista_votes", 0) for d in rec.values())
        left = sum(d.get("left_votes", 0) for d in rec.values())
        valid = sum(d.get("valid_votes", 0) for d in rec.values())
        bn = sum(d.get("blank_null_votes", 0) for d in rec.values())
        print(f"\n{year} round {rnd} national totals from this aggregation:")
        print(f"  fujimorista {fuji:>12,}  ({100*fuji/valid:6.2f}% of valid)")
        print(f"  left        {left:>12,}  ({100*left/valid:6.2f}% of valid)")
        print(f"  valid       {valid:>12,}")
        print(f"  blank+null  {bn:>12,}  ({100*bn/(valid+bn):6.2f}% of cast)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
