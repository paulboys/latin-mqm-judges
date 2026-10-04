"""score_recall.py — score judges on the fluent-misgloss set (detection recall + false positives).

For each judge, against the human key:
  error stimuli    -> DETECTION recall (judge flagged any error) and, for issue-list judges
                      (mqm), TYPED recall (flagged an issue of the expected MQM dimension).
  hard negatives   -> FALSE-POSITIVE rate (judge flagged where the rendering is correct).

Handles two judge output shapes:
  mqm_judge.py  -> {segment_id, n_issues, issues:[{dimension,error_type,severity}], score}
  jev_judge.py  -> {segment_id, has_error(0-1), severity(choice), faithfulness}

Usage:
    python score_recall.py --key .../fluent_set_key.jsonl \
        --judge opus:.../opus_on_fluent.jsonl --judge gemini:.../gemini_on_fluent.jsonl \
        --judge jev:.../jev_on_fluent.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _load(path):
    return {json.loads(l)["segment_id"]: json.loads(l)
            for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip()}


def judge_kind(label):
    """Judge output shape from its label: 'jevcore'/'jevfine' = decomposed JEV (MQM question set,
    jev_questions.py), 'jev' = legacy JEV, anything else = issue-list MQM judge (Opus/Gemini)."""
    lab = label.lower()
    for k in ("jevcore", "jevfine", "jev"):
        if lab.startswith(k):
            return k
    return "mqm"


def flagged(kind, rec, jev_thr):
    """Did this judge flag an error on the unit?"""
    if rec is None:
        return None  # missing / judge errored
    if kind in ("jevcore", "jevfine"):
        p = rec.get("p_error_" + kind[3:])  # pre-registered: max over Accuracy+Terminology nouls
        return None if p is None else p >= jev_thr
    if kind == "jev":
        he, sv = rec.get("has_error"), rec.get("severity")
        if he is None and sv is None:
            return None
        return (he is not None and he >= jev_thr) or (sv not in (None, "none"))
    # mqm-style
    n = rec.get("n_issues")
    if n is None:
        return None
    return n >= 1


def dim_match(rec, expected, kind="mqm"):
    issues = rec.get("typed_" + kind[3:]) if kind in ("jevcore", "jevfine") else rec.get("issues")
    dims = {(i.get("dimension") or "").lower() for i in (issues or [])}
    want = {(e.get("dimension") or "").lower() for e in expected}
    return bool(dims & want)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--key", required=True)
    ap.add_argument("--judge", action="append", required=True, help="label:path ; label 'jev*' = legacy JEV, 'jevcore*'/'jevfine*' = decomposed JEV")
    ap.add_argument("--jev-threshold", type=float, default=0.5)
    args = ap.parse_args(argv)

    key = _load(args.key)
    err_ids = [s for s, k in key.items() if k["is_error_stimulus"]]
    neg_ids = [s for s, k in key.items() if not k["is_error_stimulus"]]

    print(f"KEY: {len(key)} stimuli = {len(err_ids)} errors + {len(neg_ids)} hard negatives\n")
    print(f"{'judge':<10} {'det.recall':>12} {'typed.recall':>13} {'FP rate':>9} {'n/a':>5}")
    print("-" * 54)

    per_judge_cat = {}
    for spec in args.judge:
        label, path = spec.split(":", 1)
        kind = judge_kind(label)
        out = _load(path)

        det = typed = det_na = 0
        cat = defaultdict(lambda: [0, 0])  # error_type -> [detected, total]
        for s in err_ids:
            rec = out.get(s)
            fl = flagged(kind, rec, args.jev_threshold)
            et = (key[s]["expected"][0].get("error_type") or "?") if key[s]["expected"] else "?"
            if fl is None:
                det_na += 1
                continue
            cat[et][1] += 1
            if fl:
                det += 1
                cat[et][0] += 1
                if kind != "jev" and dim_match(rec, key[s]["expected"], kind):
                    typed += 1
        fp = fp_tot = 0
        for s in neg_ids:
            fl = flagged(kind, out.get(s), args.jev_threshold)
            if fl is None:
                continue
            fp_tot += 1
            if fl:
                fp += 1
        n_err = len(err_ids) - det_na
        dr = f"{det}/{n_err}" if n_err else "-"
        tr = (f"{typed}/{n_err}" if n_err else "-") if kind != "jev" else "n/a"
        fpr = f"{fp}/{fp_tot}" if fp_tot else "-"
        print(f"{label:<10} {dr:>12} {tr:>13} {fpr:>9} {det_na:>5}")
        per_judge_cat[label] = (kind, cat)

    print("\nDetection recall by error type (detected/total):")
    types = sorted({t for _, c in per_judge_cat.values() for t in c})
    hdr = "  " + f"{'type':<16}" + "".join(f"{lab:>14}" for lab in per_judge_cat)
    print(hdr)
    for t in types:
        row = "  " + f"{t:<16}"
        for lab, (kind, c) in per_judge_cat.items():
            d, tot = c.get(t, [0, 0])
            row += f"{(str(d)+'/'+str(tot)) if tot else '-':>14}"
        print(row)

    # JEV calibration: mean has_error on errors vs negatives
    for spec in args.judge:
        label, path = spec.split(":", 1)
        if judge_kind(label) != "jev":
            continue
        out = _load(path)
        he_err = [out[s]["has_error"] for s in err_ids if out.get(s) and out[s].get("has_error") is not None]
        he_neg = [out[s]["has_error"] for s in neg_ids if out.get(s) and out[s].get("has_error") is not None]
        if he_err and he_neg:
            print(f"\n{label} has_error separation: mean(errors)={sum(he_err)/len(he_err):.2f} "
                  f"vs mean(negatives)={sum(he_neg)/len(he_neg):.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
