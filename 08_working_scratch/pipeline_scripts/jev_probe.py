"""G3 — tiny JEV Latin-capability probe.

Gate G3 of the Stage-0 plan. Poses structured Choice/Score/Noul questions to the JEV
model (TypeSafe AI) on a handful of Ussher Latin cases whose correct answer we ALREADY
know, and checks whether JEV's typed answers + confidence track the known truth. This
decides whether JEV can comprehend early-modern scholarly Latin AT ALL before we build
anything on it (the LiT capability lesson: do not assume source comprehension).

NOT a validation of JEV as an MQM instrument — just a go/no-go capability check.

Security: the key is read from env or the gitignored repo-root .env, bound to the endpoint:
TYPE_SET_API_KEY for the official host, JEV_API_KEY (legacy reseller) for any other.
It is never printed. The key is sent ONLY to --endpoint (default the OFFICIAL host).
Use --dry-run to print request bodies without sending anything.

Usage:
    python jev_probe.py --dry-run                     # print requests, send nothing
    python jev_probe.py                               # hit official api.typesafe.ai
    python jev_probe.py --endpoint https://.../v1/systemone   # override host (confirm first!)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUT = ("04_translation_work/ab/antiquitates_ch2/mqm/jev_probe_raw.jsonl")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OFFICIAL_ENDPOINT = "https://api.typesafe.ai/v1/systemone"


# Keys are bound to endpoints so a key is only ever sent to the host it was issued for:
# the official TypeSafe key (TYPE_SET_API_KEY) goes only to OFFICIAL_ENDPOINT; the legacy
# reseller key (JEV_API_KEY, jevmodel.org) only to non-official endpoints.
OFFICIAL_KEY_VAR = "TYPE_SET_API_KEY"
LEGACY_KEY_VAR = "JEV_API_KEY"


def load_key(endpoint: str = OFFICIAL_ENDPOINT) -> str:
    import os
    var = OFFICIAL_KEY_VAR if endpoint == OFFICIAL_ENDPOINT else LEGACY_KEY_VAR
    key = os.environ.get(var, "").strip()
    if key:
        return key
    # fall back to repo-root .env (two parents up from pipeline_scripts)
    env = Path(__file__).resolve().parents[2] / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.split("=", 1)[0].strip() == var and "=" in s:
                v = s.split("=", 1)[1].strip().strip("'\"`")
                if v:
                    return v
    raise SystemExit(f"{var} not found in env or repo-root .env (needed for {endpoint})")


def _strip_carets(t: str) -> str:
    return re.sub(r"\^[A-Za-z0-9]{1,2}", "", t or "")


# --- Known-answer cases drawn from the ch1 tutoring units -----------------------
# Each: a Latin source + an English rendering whose correctness we already established,
# plus the expected verdict. C and D are a MINIMAL PAIR (same Latin; negation dropped vs intact).
CASES = [
    # --- clean controls ---
    {
        "id": "D_clean_short",
        "latin": "Quo naves possunt accedere, verba Dei non possunt?",
        "english": "Where ships can reach, can the words of God not reach?",
        "expected": "CLEAN (and contains a correctly-rendered negation; must NOT flag).",
    },
    {
        "id": "G_clean_long",
        "latin": ("Verba Tertulliani haec sunt; \"Tiberius, cujus tempore nomen Christianum in "
                  "saeculum introivit, annunciatum sibi ex Syria Palaestina, quod illic veritatem "
                  "illius divinitatis revelaverat, detulit ad senatum cum praerogativa suffragii sui. "
                  "Senatus, quia non in se probaverat, respuit."),
        "english": ("Tertullian's words are these: \"Tiberius, in whose time the Christian name "
                    "entered the world, when it had been reported to him from Syria Palaestina that "
                    "there the truth of that divinity had been revealed, brought the matter before the "
                    "senate with the endorsement of his own vote. The senate, because it had not itself "
                    "approved it, rejected it."),
        "expected": "CLEAN (faithful; contains a preserved negation 'non in se'; must NOT over-flag).",
    },
    # --- blatant errors (JEV's floor: if it misses these, no-go) ---
    {
        "id": "E_wrong_number",
        "latin": "Simonem Petrum viginti autem et tres annos transegisse Romae.",
        "english": "That Simon Peter passed thirty-three years at Rome.",
        "expected": "ERROR (major/Number): Latin 'viginti et tres' = twenty-three, not thirty-three.",
    },
    {
        "id": "F_blatant_mistranslation",
        "latin": "Quo naves possunt accedere, verba Dei non possunt?",
        "english": "The holy monks founded a monastery beside the river in the desert.",
        "expected": "ERROR (critical): English is unrelated to the Latin (wholesale mistranslation).",
    },
    {
        "id": "C2_negation_declarative",
        "latin": "Non enim separat mare eum, qui fecerat mare.",
        "english": "For the sea does separate him who had made the sea.",
        "expected": "ERROR (critical): Latin 'non separat' = does NOT separate; dropping it reverses the assertion.",
    },
    # --- subtle / real cases from the tutoring units ---
    {
        "id": "A_subject_object_swap",
        "latin": "Non enim separat mare eum, qui fecerat mare.",
        "english": "For the sea does not separate them from him who had made the sea.",
        "expected": "ERROR but SUBTLE (we split minor/major): invented 'them' + 'from', subject/object shift.",
    },
    {
        "id": "B_entity_wrong_referent",
        "latin": ("cum is [Plutarchus] Claudiae illius priscae, Vestalis utique illius "
                  "nominatissimae, mentionem faciat: non hujus, quae eodem cum illo vixit seculo."),
        "english": ("although Plutarch makes mention of that ancient Claudia, that most renowned "
                    "Vestal, and not of this Claudia, who lived in the same age as Pudens."),
        "expected": "ERROR (major/Entity): 'cum illo' = Plutarch (the subject 'is'), not Pudens.",
    },
]

# --- One consistent question set applied to every case -------------------------
# Defined in jev_questions.py (LEGACY_V1); the decomposed MQM set lives there too.
from jev_questions import LEGACY_V1 as QUESTIONS  # noqa: E402


def build_request(case: dict, model: str) -> dict:
    state = f"LATIN:\n{_strip_carets(case['latin'])}\n\nENGLISH:\n{_strip_carets(case['english'])}"
    return {"state": state, "model": model, "questions": QUESTIONS}


def call_jev(endpoint: str, key: str, body: dict, timeout: float) -> dict:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        endpoint, data=data, method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def find_answers(resp: dict, questions: dict = QUESTIONS) -> dict:
    """Locate the per-question answer map, which may sit at root or under a wrapper key."""
    if not isinstance(resp, dict):
        return {}
    for k in ("answers", "results", "questions", "output", "data"):
        v = resp.get(k)
        if isinstance(v, dict) and any(q in v for q in questions):
            return v
    return resp  # assume keyed at root


def fmt_answer(qid: str, ans: dict) -> str:
    if not isinstance(ans, dict):
        return f"{qid}={ans!r}"
    if "noul" in ans:
        return f"{qid}: yes_prob={ans['noul']}"
    if "choice" in ans:
        return f"{qid}: {ans['choice']} (conf={ans.get('confidence')})"
    if "score" in ans:
        return f"{qid}: score={ans['score']} (conf={ans.get('confidence')})"
    return f"{qid}={json.dumps(ans, ensure_ascii=False)}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--endpoint", default=OFFICIAL_ENDPOINT,
                    help=f"JEV endpoint (default official: {OFFICIAL_ENDPOINT})")
    ap.add_argument("--model", default="jev-latest")
    ap.add_argument("--timeout", type=float, default=60.0)
    ap.add_argument("--dry-run", action="store_true", help="Print request bodies; send nothing.")
    ap.add_argument("--raw", action="store_true", help="Print full raw JSON responses.")
    ap.add_argument("--out", default=DEFAULT_OUT,
                    help=f"Write per-case raw responses to this JSONL (default: {DEFAULT_OUT}). '' to skip.")
    args = ap.parse_args(argv)

    if args.dry_run:
        print("DRY RUN — no network, no key sent.\n")
        for c in CASES:
            print(f"### {c['id']}  (expected: {c['expected']})")
            print(json.dumps(build_request(c, args.model), ensure_ascii=False, indent=2))
            print()
        return 0

    if args.endpoint != OFFICIAL_ENDPOINT:
        print(f"WARNING: sending key to NON-OFFICIAL endpoint {args.endpoint}", file=sys.stderr)
    key = load_key(args.endpoint)
    run_ts = datetime.now(timezone.utc).isoformat()
    print(f"Endpoint: {args.endpoint}  model={args.model}  ts={run_ts}\n")
    records = []
    for c in CASES:
        print(f"### {c['id']}")
        print(f"  expected: {c['expected']}")
        rec = {
            "case_id": c["id"], "expected": c["expected"],
            "latin": _strip_carets(c["latin"]), "english": _strip_carets(c["english"]),
            "endpoint": args.endpoint, "request_model": args.model, "ts": run_ts,
            "raw_response": None, "parsed": {}, "error": None,
        }
        try:
            resp = call_jev(args.endpoint, key, build_request(c, args.model), args.timeout)
            rec["raw_response"] = resp
        except urllib.error.HTTPError as e:
            rec["error"] = f"HTTP {e.code}: {e.read()[:200]!r}"
            print(f"  {rec['error']}")
            records.append(rec)
            continue
        except Exception as e:
            rec["error"] = f"{type(e).__name__}: {str(e)[:160]}"
            print(f"  ERROR: {rec['error']}")
            records.append(rec)
            continue
        if args.raw:
            print("  RAW:", json.dumps(resp, ensure_ascii=False)[:800])
        ans = find_answers(resp)
        rec["parsed"] = {qid: (ans.get(qid) if isinstance(ans, dict) else None) for qid in QUESTIONS}
        for qid in QUESTIONS:
            print("  " + fmt_answer(qid, ans.get(qid, "<missing>") if isinstance(ans, dict) else ans))
        print()
        records.append(rec)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as fh:
            for r in records:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"Wrote {len(records)} raw records to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
