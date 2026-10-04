"""jev_calibration.py — how reliable are JEV's has_error probabilities against a ground-truth key?

Treats JEV's `has_error` (the `noul` yes-probability) as a probabilistic error detector and
reports, against the key's is_error_stimulus labels:
  - separation: mean p on errors vs negatives
  - discrimination: ROC AUC (Mann-Whitney), bootstrap 95% CI
  - calibration: Brier score vs the base-rate forecaster (Brier skill score), reliability bins, ECE
  - thresholded accuracy at 0.5 and the best threshold (best is optimistic: chosen on the same data)
  - paired ranking: within each error/negative pair, is p(error) > p(negative)?
  - the same for `faithfulness` (lower = worse), as a second signal
Optional --exclude-pairs drops pairs by id (for a pre-registered sensitivity check only; never
select exclusions from judge output).

Usage:
    python jev_calibration.py --key <key.jsonl> --jev <jev_on_x.jsonl> [--pool candidate_pool.jsonl]
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _load(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def auc(pos, neg):
    """P(score_pos > score_neg) with ties = 0.5 (Mann-Whitney)."""
    if not pos or not neg:
        return float("nan")
    s = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return s / (len(pos) * len(neg))


def boot_auc(pos, neg, n=2000, seed=7):
    rng = random.Random(seed)
    vals = sorted(auc([rng.choice(pos) for _ in pos], [rng.choice(neg) for _ in neg]) for _ in range(n))
    return vals[int(0.025 * n)], vals[int(0.975 * n) - 1]


def report(name, items):
    """items: list of (y in {0,1}, p in [0,1], faith or None, pair_id or None, item_id)."""
    ys = [y for y, *_ in items]
    ps = [p for _, p, *_ in items]
    n, k = len(items), sum(ys)
    base = k / n
    pos = [p for y, p, *_ in items if y]
    neg = [p for y, p, *_ in items if not y]
    brier = sum((p - y) ** 2 for y, p in zip(ys, ps)) / n
    brier_base = sum((base - y) ** 2 for y in ys) / n
    print(f"\n=== {name}: n={n} ({k} errors, {n - k} negatives; base rate {base:.2f})")
    print(f"  mean p(has_error): errors {sum(pos) / len(pos):.3f}  vs  negatives {sum(neg) / len(neg):.3f}")
    lo, hi = boot_auc(pos, neg)
    print(f"  ROC AUC {auc(pos, neg):.3f}  (bootstrap 95% {lo:.3f}-{hi:.3f}; 0.5 = chance)")
    print(f"  Brier {brier:.3f}  vs base-rate forecaster {brier_base:.3f}  -> skill {1 - brier / brier_base:+.3f} (0 = no better than base rate)")
    print("  reliability (p bin: n, mean p, observed error rate):")
    ece = 0.0
    for lo_b in [i / 10 for i in range(10)]:
        b = [(y, p) for y, p in zip(ys, ps) if lo_b <= p < lo_b + 0.1 or (lo_b == 0.9 and p == 1.0)]
        if b:
            mp = sum(p for _, p in b) / len(b)
            ob = sum(y for y, _ in b) / len(b)
            ece += len(b) / n * abs(mp - ob)
            print(f"    [{lo_b:.1f}-{lo_b + 0.1:.1f}) n={len(b):3d}  mean p={mp:.2f}  observed={ob:.2f}  {'#' * len(b)}")
    print(f"  ECE (expected calibration error) {ece:.3f}")
    acc5 = sum((p >= 0.5) == bool(y) for y, p in zip(ys, ps)) / n
    tp5 = sum(p >= 0.5 for p in pos)
    fp5 = sum(p >= 0.5 for p in neg)
    print(f"  at p>=0.5: recall {tp5}/{len(pos)}, FP {fp5}/{len(neg)}, accuracy {acc5:.2f}")
    best = max(sorted(set(ps)), key=lambda t: sum((p >= t) == bool(y) for y, p in zip(ys, ps)))
    accb = sum((p >= best) == bool(y) for y, p in zip(ys, ps)) / n
    print(f"  best threshold on this data {best:.2f} -> accuracy {accb:.2f} (optimistic: tuned in-sample; majority-class accuracy {max(base, 1 - base):.2f})")
    pairs = {}
    for y, p, f, pid, iid in items:
        if pid:
            pairs.setdefault(pid, {})[y] = p
    full = [v for v in pairs.values() if 0 in v and 1 in v]
    if full:
        w = sum(v[1] > v[0] for v in full)
        t = sum(v[1] == v[0] for v in full)
        print(f"  paired: p(error) > p(its negative) in {w}/{len(full)} pairs ({t} ties); mean gap {sum(v[1] - v[0] for v in full) / len(full):+.3f}")
    fpos = [-f for y, p, f, *_ in items if y and f is not None]
    fneg = [-f for y, p, f, *_ in items if not y and f is not None]
    if fpos and fneg:
        print(f"  faithfulness: mean on errors {-sum(fpos) / len(fpos):.2f} vs negatives {-sum(fneg) / len(fneg):.2f}; "
              f"AUC (lower faith = error) {auc(fpos, fneg):.3f}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", type=Path, required=True, help="JSONL with segment_id/item_id + is_error_stimulus")
    ap.add_argument("--jev", type=Path, required=True)
    ap.add_argument("--pool", type=Path, default=None, help="v2 candidate_pool.jsonl (enables pair ids + group splits)")
    ap.add_argument("--label", default="JEV")
    ap.add_argument("--signal", default="has_error", choices=["has_error", "p_error_core", "p_error_fine"],
                    help="which probability to evaluate: legacy has_error, or the decomposed set's pre-registered max")
    ap.add_argument("--exclude-pairs", default="", help="comma-separated pair ids to drop (pre-registered only)")
    args = ap.parse_args(argv)

    key = {r.get("segment_id") or r.get("item_id"): r for r in _load(args.key)}
    pool = {r["item_id"]: r for r in _load(args.pool)} if args.pool else {}
    jev = {r["segment_id"]: r for r in _load(args.jev)}
    excl = {s for s in args.exclude_pairs.split(",") if s}

    items, missing = [], 0
    for sid, k in key.items():
        r = jev.get(sid)
        if not r or r.get(args.signal) is None:
            missing += 1
            continue
        pid = pool[sid]["pair_id"] if sid in pool else (sid.removesuffix("__gold") if "litera" in sid else None)
        if pid in excl:
            continue
        items.append((int(bool(k["is_error_stimulus"])), float(r[args.signal]), r.get("faithfulness"), pid, sid))
    print(f"{args.label}: {len(items)} items scored, {missing} missing/errored" + (f", {len(excl)} pairs excluded" if excl else ""))
    report(f"{args.label} — all", items)
    if pool:
        for name, groups in (("Ussher (U-P, U-R, U-V)", {"U-P", "U-R", "U-V"}), ("LITERA (L-P, L-V)", {"L-P", "L-V"})):
            sub = [it for it in items if pool[it[4]]["group"] in groups]
            report(f"{args.label} — {name}", sub)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
