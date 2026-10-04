"""jev_to_mqm.py — turn JEV's MQM-question-set answers into an MQM issue list, in the SAME record
shape as mqm_judge.py (Opus/Gemini), so all three judges are scored apples-to-apples.

Input: a jev_judge.py --question-set mqm output. No new API calls; nothing is fitted.

Conversion rules (fixed 2026-10-04 BEFORE looking at the converted results):
  issues     every noul in the chosen set with p >= 0.5 becomes one issue, typed by
             jev_questions.TYPE_MAP (dimension + error_type). JEV gives no span, so span = "".
  severity   JEV gives ONE severity per item (severity_v2, averaged over both option orders).
             Because the error questions already assert an error, an issue takes the most
             probable NON-none level, renormalised: slightly -> minor, substantially -> major,
             completely -> critical. Every issue on an item shares that severity.
  penalty    sum of mqm_judge._SEVERITY_WEIGHT (minor 1, major 5, critical 25), as for Opus/Gemini.
  score      faithfulness (0-4) x 25, JEV's holistic analogue of the LLMs' 0-100 score.
Sets: "core" (6 MQM-category questions) is the PRIMARY comparison; "fine" (13 mechanism questions)
is secondary, because its questions overlap (e.g. mistranslation / word sense), so one error can
yield several issues and be counted more than once.

Usage:
    python jev_to_mqm.py --input .../jev_mqm_on_v2.jsonl --set core --output .../jevmqm_core_on_v2.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jev_questions import SETS, TYPE_MAP, TYPED_THRESHOLD  # noqa: E402

SEVERITY_WEIGHT = {"minor": 1, "major": 5, "critical": 25}  # = mqm_judge._SEVERITY_WEIGHT
LEVEL_TO_MQM = {"slightly": "minor", "substantially": "major", "completely": "critical"}


def convert(rec: dict, qset: str) -> dict:
    out = {"segment_id": rec["segment_id"], "score": None, "classification": "", "n_issues": None,
           "mqm_penalty": 0, "src_tokens": None, "issues": None, "source": f"jev mqm-set ({qset})"}
    ans = ((rec.get("raw") or {}).get("answers") or {})
    if rec.get("error") or not ans:
        return out
    probs = rec.get("severity_v2_probs") or {}
    nonnone = {k: probs.get(k, 0) for k in LEVEL_TO_MQM}
    sev = LEVEL_TO_MQM[max(nonnone, key=nonnone.get)] if sum(nonnone.values()) > 0 else "minor"
    issues = []
    for q in SETS[qset]:
        p = (ans.get(q) or {}).get("noul")
        if p is not None and p >= TYPED_THRESHOLD:
            dim, et = TYPE_MAP[q]
            issues.append({"severity": sev, "dimension": dim, "error_type": et, "span": "",
                           "description": f"{q} p={p:.2f}"})
    out["issues"] = issues
    out["n_issues"] = len(issues)
    out["mqm_penalty"] = sum(SEVERITY_WEIGHT[i["severity"]] for i in issues)
    if rec.get("faithfulness") is not None:
        out["score"] = round(float(rec["faithfulness"]) * 25, 2)
    out["severity_v2"] = rec.get("severity_v2")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--set", choices=sorted(SETS), default="core")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args(argv)
    recs = [json.loads(l) for l in args.input.read_text(encoding="utf-8").splitlines() if l.strip()]
    conv = [convert(r, args.set) for r in recs]
    args.output.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in conv), encoding="utf-8")
    flagged = sum((c["n_issues"] or 0) > 0 for c in conv)
    print(f"{args.output.name}: {len(conv)} items, {flagged} with >=1 issue, "
          f"{sum(c['n_issues'] or 0 for c in conv)} issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
