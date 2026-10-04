"""harvest_divergences.py — surface Opus vs Gemini ch1 translation divergences.

Part of "harvest real ones" for the fluent-misgloss recall set: where two frontier models
render the SAME Latin differently, a fluent misgloss (in one of them) often hides. This
aligns the two ch1 translations by segment_id, scores divergence, and emits the most-
divergent units as an ADJUDICATION WORKLIST (Latin + both renderings + the differing spans
+ blank verdict fields) for a human to mark which rendering — if either — carries a real
error. The adjudicated output becomes part of the real-error test set (with a human key).

This is a candidate-generator, NOT a judge: it says "these differ", not "this is wrong."

Usage:
    python harvest_divergences.py --top 30
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OPUS = Path("03_segmented_text/part1/segments_sentences_xpage.jsonl")
GEMINI = Path("03_segmented_text/part1/segments_sentences_xpage_gemini31_ch1.jsonl")
OUT_MD = Path("04_translation_work/ab/antiquitates_ch2/mqm/harvest_divergences.md")
OUT_JSONL = Path("04_translation_work/ab/antiquitates_ch2/mqm/harvest_divergences.jsonl")


def _strip_carets(t: str) -> str:
    return re.sub(r"\^[A-Za-z0-9]{1,2}", "", t or "")


def _english(r: dict) -> str:
    h = r.get("translation_history") or []
    if h and (h[-1] or {}).get("english"):
        return h[-1]["english"]
    return r.get("final_english") or ""


def _load(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        sid = r.get("segment_id", "")
        if sid:
            out[sid] = r
    return out


def _tokens(s: str):
    return re.findall(r"\w+|[^\w\s]", s.lower())


def _diff_spans(a: str, b: str):
    """Return the differing chunks as (opus_chunk, gemini_chunk) pairs (word-level)."""
    at, bt = _tokens(a), _tokens(b)
    sm = SequenceMatcher(a=at, b=bt, autojunk=False)
    spans = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        spans.append({"op": tag,
                      "opus": " ".join(at[i1:i2]),
                      "gemini": " ".join(bt[j1:j2])})
    return sm.ratio(), spans


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--top", type=int, default=30, help="emit the N most-divergent units")
    ap.add_argument("--min-latin-words", type=int, default=6, help="skip trivially short units")
    args = ap.parse_args(argv)

    opus, gem = _load(OPUS), _load(GEMINI)
    shared = [s for s in opus if s in gem]
    rows = []
    for sid in shared:
        latin = _strip_carets(opus[sid].get("latin_text") or "").strip()
        if len(latin.split()) < args.min_latin_words:
            continue
        oe = _strip_carets(_english(opus[sid])).strip()
        ge = _strip_carets(_english(gem[sid])).strip()
        if not oe or not ge:
            continue
        ratio, spans = _diff_spans(oe, ge)
        # keep only substantive differences (ignore pure punctuation/quote-style churn)
        sub = [s for s in spans if re.search(r"\w", s["opus"] + s["gemini"])
               and (s["opus"].strip() or s["gemini"].strip())]
        if not sub:
            continue
        rows.append({"segment_id": sid, "latin": latin, "opus_english": oe, "gemini_english": ge,
                     "divergence": round(1 - ratio, 3), "n_diff_spans": len(sub), "diff_spans": sub})

    rows.sort(key=lambda r: r["divergence"], reverse=True)
    top = rows[:args.top]

    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("w", encoding="utf-8") as fh:
        for r in rows:  # full ranked list to jsonl
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    lines = ["# Opus vs Gemini ch1 — divergence adjudication worklist", "",
             f"{len(shared)} shared units; {len(rows)} with substantive divergence; "
             f"top {len(top)} shown (full ranked list in harvest_divergences.jsonl).", "",
             "For each: does EITHER rendering carry a real error? Mark which model, dimension "
             "(Accuracy/Fluency/Terminology/Style), error type, severity (minor/major/critical), "
             "and why — or 'both fine / defensible divergence'. This is the human answer key.", "",
             "---", ""]
    for i, r in enumerate(top, 1):
        lines.append(f"## {i}. {r['segment_id']}  (divergence {r['divergence']}, {r['n_diff_spans']} spans)")
        lines.append(f"**LATIN:** {r['latin']}")
        lines.append("")
        lines.append(f"**OPUS:** {r['opus_english']}")
        lines.append("")
        lines.append(f"**GEMINI:** {r['gemini_english']}")
        lines.append("")
        lines.append("**Differing spans (opus | gemini):**")
        for s in r["diff_spans"][:8]:
            lines.append(f"- [{s['op']}] `{s['opus']}` | `{s['gemini']}`")
        lines.append("")
        lines.append("**Adjudication:** which model (if either) errs | dimension | type | severity | why:")
        lines.append("> ")
        lines.append("")
        lines.append("---")
        lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"shared units: {len(shared)} | substantive divergences: {len(rows)} | top emitted: {len(top)}")
    print(f"wrote:\n  {OUT_MD}\n  {OUT_JSONL}")
    if top:
        print("\nMost-divergent few:")
        for r in top[:5]:
            print(f"  {r['segment_id']}  div={r['divergence']}  spans={r['n_diff_spans']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
