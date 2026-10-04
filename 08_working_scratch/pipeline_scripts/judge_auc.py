"""judge_auc.py — like-for-like discrimination (ROC AUC) of every judge's CONTINUOUS signal.

Compares, on the same items and key:
  mqm-shape judges (Opus, Gemini): -score (0-100, lower = worse) and mqm_penalty (higher = worse)
  jev-shape judge: has_error probability and -faithfulness
AUC = P(signal on an error item > signal on a negative), ties 0.5. Pairwise differences use a
paired bootstrap over items (items resampled jointly, so judge correlation is respected).
Also reports pair-ranking: within each error/negative pair, does the error get the worse signal?

Usage:
    python judge_auc.py --key <key.jsonl> --judge opus:<f> --judge gemini:<f> --judge jev:<f> [--pool pool.jsonl]
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jev_questions import TYPE_MAP  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _load(p):
    return [json.loads(l) for l in Path(p).read_text(encoding="utf-8").splitlines() if l.strip()]


def auc(pos, neg):
    if not pos or not neg:
        return float("nan")
    return sum((p > n) + 0.5 * (p == n) for p in pos for n in neg) / (len(pos) * len(neg))


def signals(kind, rec):
    if rec is None:
        return {}
    if kind == "jev":
        out = {}
        if rec.get("has_error") is not None:
            out["p(has_error)"] = float(rec["has_error"])
        if rec.get("faithfulness") is not None:
            out["-faithfulness"] = -float(rec["faithfulness"])
        # decomposed MQM question set (jev_questions.py): pre-registered max, plus noisy-OR
        ans = ((rec.get("raw") or {}).get("answers") or {})
        for name in ("core", "fine"):
            if rec.get(f"p_error_{name}") is not None:
                out[f"p_error_{name}(max)"] = float(rec[f"p_error_{name}"])
                ps = [v.get("noul") for q, v in ans.items()
                      if q.startswith(name + "_") and isinstance(v, dict) and v.get("noul") is not None
                      and TYPE_MAP.get(q, ("",))[0] != "Fluency"]
                if ps:
                    prod = 1.0
                    for p in ps:
                        prod *= 1 - p
                    out[f"p_error_{name}(noisy_or)"] = 1 - prod
        return out
    if rec.get("n_issues") is None:
        return {}
    out = {"mqm_penalty": float(rec.get("mqm_penalty") or 0)}
    if isinstance(rec.get("score"), (int, float)):
        out["-score"] = -float(rec["score"])
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", type=Path, required=True)
    ap.add_argument("--judge", action="append", required=True)
    ap.add_argument("--pool", type=Path, default=None)
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--title", default="")
    args = ap.parse_args(argv)

    key = {r["segment_id"]: bool(r["is_error_stimulus"]) for r in _load(args.key)}
    pair = {}
    if args.pool:
        pair = {r["item_id"]: r["pair_id"] for r in _load(args.pool)}
    else:  # v1 naming: X and X__gold
        pair = {s: s.removesuffix("__gold") for s in key}

    sig = {}  # (judge, signal) -> {item: value}
    for spec in args.judge:
        label, path = spec.split(":", 1)
        kind = "jev" if label.lower().startswith("jev") else "mqm"
        recs = {r["segment_id"]: r for r in _load(path)}
        for s in key:
            for name, v in signals(kind, recs.get(s)).items():
                sig.setdefault(f"{label} {name}", {})[s] = v

    common = [s for s in key if all(s in d for d in sig.values())]
    pos = [s for s in common if key[s]]
    neg = [s for s in common if not key[s]]
    print(f"{args.title}\nitems with every signal: {len(common)} ({len(pos)} errors, {len(neg)} negatives)\n")

    rng = random.Random(11)
    boots = {k: [] for k in sig}
    for _ in range(args.boot):
        bp = [rng.choice(pos) for _ in pos]
        bn = [rng.choice(neg) for _ in neg]
        for k, d in sig.items():
            boots[k].append(auc([d[s] for s in bp], [d[s] for s in bn]))

    print(f"{'signal':<28}{'AUC':>7}{'95% CI':>15}   pair-ranking (error worse than its own negative)")
    pairs = {}
    for s in common:
        pairs.setdefault(pair.get(s), {})[key[s]] = s
    full = [v for p, v in pairs.items() if p and True in v and False in v]
    for k, d in sig.items():
        a = auc([d[s] for s in pos], [d[s] for s in neg])
        b = sorted(boots[k])
        w = sum(d[v[True]] > d[v[False]] for v in full)
        t = sum(d[v[True]] == d[v[False]] for v in full)
        print(f"{k:<28}{a:7.3f}   {b[int(.025 * len(b))]:.3f}-{b[int(.975 * len(b)) - 1]:.3f}   {w}/{len(full)} (+{t} ties)")

    print("\npaired bootstrap AUC differences (row minus column; 95% CI; * = CI excludes 0)")
    ks = list(sig)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            diffs = sorted(x - y for x, y in zip(boots[ks[i]], boots[ks[j]]))
            lo, hi = diffs[int(.025 * len(diffs))], diffs[int(.975 * len(diffs)) - 1]
            pt = auc([sig[ks[i]][s] for s in pos], [sig[ks[i]][s] for s in neg]) - auc([sig[ks[j]][s] for s in pos], [sig[ks[j]][s] for s in neg])
            star = "*" if lo > 0 or hi < 0 else " "
            print(f"  {ks[i]:<26} - {ks[j]:<26} {pt:+.3f}  [{lo:+.3f}, {hi:+.3f}] {star}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
