"""jev_judge.py — run JEV as a discriminative MQM judge over a units JSONL.

Reads units (segment_id / latin_text / final_english), asks JEV one question set per unit, and
writes one record per unit. The third judge alongside mqm_judge.py (Opus, Gemini).

Question sets (defined in jev_questions.py):
  legacy  has_error (noul) / severity (choice) / faithfulness (score), as in jev_probe.py
  mqm     legacy + severity_v2 (both option orders) + 6 MQM-category nouls + 13 mechanism nouls;
          adds derived p_error_core / p_error_fine / typed_core / typed_fine / severity_v2

Writes incrementally and resumes: units already judged without error in --output are skipped.

Usage:
    python jev_judge.py --input .../fluent_set_input.jsonl --output .../jev_on_fluent.jsonl
        (official api.typesafe.ai + TYPE_SET_API_KEY by default; --endpoint overrides,
         and a non-official endpoint uses the legacy JEV_API_KEY)
    python jev_judge.py --question-set mqm --input ... --output .../jev_mqm_on_x.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jev_probe import load_key, call_jev, find_answers, _strip_carets, OFFICIAL_ENDPOINT
from jev_questions import QUESTION_SETS, derive

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def _english(u: dict) -> str:
    if u.get("final_english"):
        return u["final_english"]
    h = u.get("translation_history") or []
    return (h[-1] or {}).get("english", "") if h else ""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--question-set", choices=sorted(QUESTION_SETS), default="legacy")
    ap.add_argument("--endpoint", default=OFFICIAL_ENDPOINT)
    ap.add_argument("--model", default="jev-latest")
    ap.add_argument("--timeout", type=float, default=60.0)
    ap.add_argument("--limit", type=int, default=None, help="Judge only the first N units (smoke test).")
    args = ap.parse_args(argv)
    questions = QUESTION_SETS[args.question_set]

    key = load_key(args.endpoint)
    units = [json.loads(l) for l in args.input.read_text(encoding="utf-8").splitlines() if l.strip()]
    if args.limit:
        units = units[:args.limit]

    # resume: keep records judged without error, re-try the rest
    done = []
    if args.output.exists():
        done = [r for r in (json.loads(l) for l in args.output.read_text(encoding="utf-8").splitlines() if l.strip())
                if r.get("error") is None and r.get("has_error") is not None]
    done_ids = {r["segment_id"] for r in done}
    if done_ids:
        print(f"resuming: {len(done_ids)} units already judged in {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in done), encoding="utf-8")
    out_fh = args.output.open("a", encoding="utf-8")

    for i, u in enumerate(units, 1):
        if u.get("segment_id", "") in done_ids:
            continue
        latin = _strip_carets(u.get("latin_text") or "").strip()
        eng = _strip_carets(_english(u)).strip()
        body = {"state": f"LATIN:\n{latin}\n\nENGLISH:\n{eng}", "model": args.model, "questions": questions}
        rec = {"segment_id": u.get("segment_id", ""), "question_set": args.question_set, "endpoint": args.endpoint,
               "has_error": None, "severity": None, "severity_probs": None, "faithfulness": None,
               "raw": None, "error": None, "latency_s": None, "usage": None}
        t0 = time.perf_counter()
        try:
            resp = call_jev(args.endpoint, key, body, args.timeout)
            rec["latency_s"] = round(time.perf_counter() - t0, 3)  # wall-clock for the API call
            rec["usage"] = (resp or {}).get("usage")
            rec["raw"] = resp
            a = find_answers(resp, questions)
            if isinstance(a, dict):
                he = a.get("has_error") or {}
                sv = a.get("severity") or {}
                fa = a.get("faithfulness") or {}
                rec["has_error"] = he.get("noul")
                rec["severity"] = sv.get("choice")
                rec["severity_probs"] = sv.get("probabilities")
                rec["faithfulness"] = fa.get("score")
                if args.question_set == "mqm":
                    missing = [q for q in questions if q not in a]
                    if missing:
                        rec["error"] = f"missing answers: {missing}"
                    rec.update(derive(a))
        except Exception as e:
            rec["error"] = f"{type(e).__name__}: {str(e)[:150]}"
        out_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        out_fh.flush()
        extra = (f" core={rec.get('p_error_core')} fine={rec.get('p_error_fine')} sev2={rec.get('severity_v2')}"
                 if args.question_set == "mqm" else "")
        print(f"[{i}/{len(units)}] {rec['segment_id']}: has_error={rec['has_error']} "
              f"sev={rec['severity']} faith={rec['faithfulness']}{extra}{' ERR ' + rec['error'] if rec['error'] else ''}")
    out_fh.close()
    print(f"\nwrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
