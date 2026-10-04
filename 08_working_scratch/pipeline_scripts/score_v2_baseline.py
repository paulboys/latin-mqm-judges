"""score_v2_baseline.py — provisional baseline scoring of judges on the fluent-misgloss v2 pool.

PROVISIONAL: scored against the PRE-ADJUDICATION key (candidate_pool.jsonl as written by Claude),
not the classicist's frozen key. Treat every number as a baseline to be re-scored, not a result.

Per judge: detection recall on error items, FP rate on negatives (Wilson 95% CIs), broken down by
group, by who wrote the error (Claude-planted vs Baker-real), by expected severity; pair accuracy
(flags the error AND passes its negative); FP on negatives whose reference carries an
inherited-issue flag vs not; and pairwise McNemar exact tests on recall between judges.

Detection = "flagged anything" (mqm: n_issues >= 1; jev: has_error >= thr or severity != none),
the same rule as score_recall.py.
"""
from __future__ import annotations

import argparse
import json
import sys
from math import comb, sqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_recall import flagged, judge_kind  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0, c - h), min(1, c + h))


def fmt(k, n):
    lo, hi = wilson(k, n)
    return f"{k}/{n} ({100 * k / n:.0f}%, {100 * lo:.0f}-{100 * hi:.0f})" if n else "-"


def mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pool", type=Path, required=True)
    ap.add_argument("--judge", action="append", required=True, help="label:path ; 'jev*' legacy JEV, 'jevcore*'/'jevfine*' decomposed JEV")
    ap.add_argument("--jev-threshold", type=float, default=0.5)
    ap.add_argument("--out", type=Path, default=None, help="write per-item flags JSONL here")
    args = ap.parse_args(argv)

    pool = {r["item_id"]: r for r in (json.loads(l) for l in args.pool.read_text(encoding="utf-8").splitlines() if l.strip())}
    errs = [i for i, r in pool.items() if r["is_error_stimulus"]]
    negs = [i for i, r in pool.items() if not r["is_error_stimulus"]]

    flags = {}
    for spec in args.judge:
        label, path = spec.split(":", 1)
        kind = judge_kind(label)
        out = {json.loads(l)["segment_id"]: json.loads(l) for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()}
        flags[label] = {i: flagged(kind, out.get(i), args.jev_threshold) for i in pool}

    def rate(label, ids):
        v = [flags[label][i] for i in ids if flags[label][i] is not None]
        return sum(v), len(v)

    def author(r):
        return "baker-real" if r["group"] == "U-R" else "claude-planted"

    def worst(r):
        s = {e["severity"] for e in r["expected"]}
        return "major" if "major" in s else "minor"

    print("PROVISIONAL BASELINE: pre-adjudication key; single run per judge.\n")
    print(f"pool: {len(errs)} error items, {len(negs)} negatives\n")
    for label in flags:
        na = sum(flags[label][i] is None for i in pool)
        print(f"=== {label}   (missing/errored: {na})")
        print(f"  recall (all errors)   {fmt(*rate(label, errs))}")
        print(f"  FP rate (all negs)    {fmt(*rate(label, negs))}")
        for g in ("U-P", "U-R", "L-P"):
            print(f"    recall {g:<5}         {fmt(*rate(label, [i for i in errs if pool[i]['group'] == g]))}")
        for a in ("claude-planted", "baker-real"):
            print(f"    recall {a:<15} {fmt(*rate(label, [i for i in errs if author(pool[i]) == a]))}")
        for s in ("major", "minor"):
            print(f"    recall {s:<15} {fmt(*rate(label, [i for i in errs if worst(pool[i]) == s]))}")
        for g in ("U-P", "U-R", "L-P", "U-V", "L-V"):
            print(f"    FP {g:<5}             {fmt(*rate(label, [i for i in negs if pool[i]['group'] == g]))}")
        inh = [i for i in negs if pool[i].get("inherited_issues")]
        clean = [i for i in negs if not pool[i].get("inherited_issues") and pool[i]["group"] in ("U-P", "L-P")]
        print(f"    FP refs w/ inherited flag   {fmt(*rate(label, inh))}")
        print(f"    FP refs w/o flag (U-P/L-P)  {fmt(*rate(label, clean))}")
        pairs = [i for i in errs if i + "__ref" in pool]
        ok = [i for i in pairs if flags[label][i] is not None and flags[label][i + "__ref"] is not None]
        both = sum(flags[label][i] and not flags[label][i + "__ref"] for i in ok)
        print(f"  pair accuracy (flags error, passes its negative)  {fmt(both, len(ok))}\n")

    labels = list(flags)
    print("=== pairwise recall difference (McNemar exact, error items both judged)")
    for x in range(len(labels)):
        for y in range(x + 1, len(labels)):
            A, B = labels[x], labels[y]
            ids = [i for i in errs if flags[A][i] is not None and flags[B][i] is not None]
            b = sum(flags[A][i] and not flags[B][i] for i in ids)
            c = sum(flags[B][i] and not flags[A][i] for i in ids)
            print(f"  {A} vs {B}: {A}-only {b}, {B}-only {c}, p={mcnemar(b, c):.3f}  (n={len(ids)})")
    print("\n=== pairwise FP difference (McNemar exact, negatives both judged)")
    for x in range(len(labels)):
        for y in range(x + 1, len(labels)):
            A, B = labels[x], labels[y]
            ids = [i for i in negs if flags[A][i] is not None and flags[B][i] is not None]
            b = sum(flags[A][i] and not flags[B][i] for i in ids)
            c = sum(flags[B][i] and not flags[A][i] for i in ids)
            print(f"  {A} vs {B}: {A}-only {b}, {B}-only {c}, p={mcnemar(b, c):.3f}  (n={len(ids)})")

    missed_all = [i for i in errs if all(flags[l][i] is False for l in labels)]
    print(f"\n=== error items missed by every judge ({len(missed_all)}): {', '.join(missed_all)}")
    fp_all = [i for i in negs if all(flags[l][i] is True for l in labels)]
    print(f"=== negatives flagged by every judge ({len(fp_all)}): {', '.join(fp_all)}")

    if args.out:
        args.out.write_text("".join(json.dumps({"item_id": i, "is_error": pool[i]["is_error_stimulus"], "group": pool[i]["group"],
                                                **{l: flags[l][i] for l in labels}}) + "\n" for i in pool), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
