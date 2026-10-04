"""score_v3_breakdown.py — score judges on the v3 hard set, split by ORIGIN (real model errors vs
simulated edits) and by keyed severity, with pair accuracy and Wilson CIs.

PROVISIONAL unless --pool is the classicist's adjudicated key. Detection uses score_recall.flagged /
judge_kind, so 'jev*' = legacy JEV, 'jevcore*'/'jevfine*' = decomposed JEV (max rule), and any
other label = an issue-list judge (Opus/Gemini, or JEV converted by jev_to_mqm.py).

Usage:
    python score_v3_breakdown.py --pool .../fluent_v3/candidate_pool.jsonl --judge gemini:... --judge jev:...
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_recall import flagged, judge_kind, dim_match  # noqa: E402
from score_v2_baseline import fmt, mcnemar  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _load(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pool", type=Path, required=True)
    ap.add_argument("--judge", action="append", required=True)
    ap.add_argument("--jev-threshold", type=float, default=0.5)
    args = ap.parse_args(argv)

    pool = {r["item_id"]: r for r in _load(args.pool)}
    origin = lambda r: "simulated" if r["origin"].startswith("simulated") else "real"  # noqa: E731
    errs = [i for i, r in pool.items() if r["is_error_stimulus"]]
    negs = [i for i, r in pool.items() if not r["is_error_stimulus"]]
    print(f"PROVISIONAL: {len(errs)} errors ({sum(origin(pool[i]) == 'real' for i in errs)} real, "
          f"{sum(origin(pool[i]) == 'simulated' for i in errs)} simulated), {len(negs)} negatives\n")

    flags, typed = {}, {}
    for spec in args.judge:
        label, path = spec.split(":", 1)
        kind = judge_kind(label)
        out = {r["segment_id"]: r for r in _load(path)}
        flags[label] = {i: flagged(kind, out.get(i), args.jev_threshold) for i in pool}
        typed[label] = ({i: (flags[label][i] and dim_match(out[i], pool[i]["expected"], kind)) for i in errs}
                        if kind != "jev" else None)

    def rate(label, ids):
        v = [flags[label][i] for i in ids if flags[label][i] is not None]
        return sum(v), len(v)

    worst = lambda r: "major" if any(e["severity"] == "major" for e in r["expected"]) else "minor"  # noqa: E731
    boundary = [i for i in negs if i.startswith("B-")]
    for label in flags:
        print(f"=== {label}   (missing: {sum(flags[label][i] is None for i in pool)})")
        print(f"  recall, all errors        {fmt(*rate(label, errs))}")
        for o in ("real", "simulated"):
            print(f"    {o:<23} {fmt(*rate(label, [i for i in errs if origin(pool[i]) == o]))}")
        for s in ("major", "minor"):
            print(f"    keyed {s:<17} {fmt(*rate(label, [i for i in errs if worst(pool[i]) == s]))}")
        if typed[label] is not None:
            t = [typed[label][i] for i in errs if flags[label][i] is not None]
            print(f"  typed recall (dimension)  {fmt(sum(bool(x) for x in t), len(t))}")
        print(f"  FP, all negatives         {fmt(*rate(label, negs))}")
        print(f"    paired correct renders  {fmt(*rate(label, [i for i in negs if not i.startswith('B-') and pool[i]['pair_id'] in pool]))}")
        print(f"    defensible (B-) items   {fmt(*rate(label, boundary))}")
        pairs = [i for i in errs if any(n for n in negs if pool[n]['pair_id'] == pool[i]['pair_id'])]
        ok = both = 0
        for i in pairs:
            n = next(n for n in negs if pool[n]["pair_id"] == pool[i]["pair_id"])
            if flags[label][i] is None or flags[label][n] is None:
                continue
            ok += 1
            both += bool(flags[label][i] and not flags[label][n])
        print(f"  pair accuracy             {fmt(both, ok)}\n")

    labels = list(flags)
    print("=== pairwise McNemar (recall on errors / FP on negatives)")
    for x in range(len(labels)):
        for y in range(x + 1, len(labels)):
            A, B = labels[x], labels[y]
            for name, ids in (("recall", errs), ("FP", negs)):
                ids = [i for i in ids if flags[A][i] is not None and flags[B][i] is not None]
                b = sum(flags[A][i] and not flags[B][i] for i in ids)
                c = sum(flags[B][i] and not flags[A][i] for i in ids)
                print(f"  {name:<6} {A} vs {B}: {A}-only {b}, {B}-only {c}, p={mcnemar(b, c):.3f}")
    missed = [i for i in errs if all(flags[l][i] is False for l in labels)]
    print(f"\nerrors missed by every judge ({len(missed)}): {', '.join(missed)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
