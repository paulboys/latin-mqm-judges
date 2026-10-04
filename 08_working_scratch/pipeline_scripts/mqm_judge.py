"""LLM-MQM judge: structured error annotation of a translation vs its Latin source.

An LLM annotates the ENGLISH translation for errors against the LATIN source, using
an MQM Core taxonomy (Accuracy / Fluency / Terminology / Style) and emitting three
things per unit: a holistic 0-100 score, a 10-point quality classification, and a
localized issue list (severity + dimension + error type + span). Used for the
cross-provider MQM design (whitepaper pivot 2026-08-30): Gemini judges Opus's ch2
translation, Opus judges Gemini's, with Baker as a shared anchor.

--------------------------------------------------------------------------------
WARRANT / HONEST FRAMING (do not overstate this instrument)
--------------------------------------------------------------------------------
The prompt STRUCTURE (three-part output, MQM Core, severities -1/-5/-25, LLM judge)
is adapted from Skorobogat, Prabhu & Bethge, "Round-Trip Translation Reveals What
Frontier Multilingual Benchmarks Miss" (arXiv 2604.12911, 2026) — the LiT benchmark.
LiT is credited as a STRUCTURAL precedent ONLY. It is NOT a validation of this
instrument for our task, for three reasons established by reading the paper:
  1. LiT's reported ρ=0.94 is a Spearman rank correlation of an aggregate score with
     LMArena CROWD preference across n=6 models ("directional contrast, not a
     standalone hypothesis test" — their words). No expert-MQM, no segment-level
     validation anywhere in the paper.
  2. LiT covers modern languages only (no Latin; "Latin" there = the script).
  3. Decisively: LiT's round-trip design makes its judge compare TWO ENGLISH texts,
     so the judge never needs to comprehend the source language. Our task is the
     opposite — direct Latin->English — so the judge MUST comprehend early-modern
     scholarly Latin. We remove the exact property that makes LiT's judge reliable
     and land it on the capability in question.
Therefore this instrument's validity for our purposes is established SOLELY by the
expert human anchor (a co-author with doctoral-level Classics training), not by LiT.
Prior 2026-08-30 runs used a different, under-specified taxonomy and are void.

Scoring: primary metric is the mean LLM 0-100 score (LiT's alternative scoring).
Secondary: MQM penalty per 100 source tokens, weights Minor 1 / Major 5 / Critical 25.

Usage
-----
    python mqm_judge.py --segments <translation.jsonl> --start-page 46 --end-page 67 \\
        --judge-provider gemini --judge-model gemini-3.1-pro-preview \\
        --label gemini-judges-opus --output mqm_gemini_on_opus.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from provider_config import default_config, load_config  # noqa: E402
from translation_adapters import (  # noqa: E402
    AnthropicTranslationAdapter,
    GeminiTranslationAdapter,
    _extract_json_object,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# MQM severity weights (Lommel et al. / LiT convention).
_SEVERITY_WEIGHT = {"minor": 1, "major": 5, "critical": 25}

_CLASSIFICATIONS = [
    "1-nonsense", "2-severe distortion", "3-failed gist", "4-unreliable",
    "5-machine-like", "6-understandable but flawed", "7-good", "8-very good",
    "9-excellent", "10-perfect",
]

_MQM_PROMPT = """You are evaluating a translation of early-modern scholarly Latin (James Ussher's \
'Britannicarum Ecclesiarum Antiquitates', 1639 — ecclesiastical history, dense with proper \
names, patristic and classical citations, and embedded Greek) into English.

You are given the LATIN SOURCE and an ENGLISH TRANSLATION. Judge how faithfully and fluently \
the English renders the Latin. This is a DIRECT evaluation against the Latin source: there is \
no reference translation, and you must NOT reward or penalise similarity to any particular \
English version. The required target register is modern scholarly English.

TASK-SPECIFIC RULES (this domain, not generic MT):
- Embedded Greek quoted verbatim in the English is CORRECT — Ussher quotes Greek and preserving \
it is required. NEVER flag preserved Greek as untranslated.
- A remembered English Bible verse substituted for the Latin scripture Ussher actually prints is \
a MISTRANSLATION (Accuracy), even though it reads fluently — he argues from the Latin wording.
- Numerals, dates, and proper names must match the Latin exactly (Accuracy: Number / Date / Entity).
- Defensible synonyms, faithful paraphrase, and legitimate stylistic choices are NOT errors.

Produce three things:
1. score: an integer 0-100 for overall faithfulness + fluency (100 = perfect, 0 = no meaning preserved).
2. classification: exactly one of these ten labels, judged against the Latin source:
   1-nonsense (gibberish / wrong language / unrelated to the Latin);
   2-severe distortion (unrecognizable fragments; core meaning lost or misleading);
   3-failed gist (topic broadly right but mostly misleading or incomprehensible);
   4-unreliable (meaning often preserved but significant mistranslations present);
   5-machine-like (meaning roughly preserved, no critical errors, but overly literal/awkward);
   6-understandable but flawed (meaning preserved; grammar functional but distracting errors);
   7-good (accurate meaning; grammatical with only minor errors);
   8-very good (fluent and accurate; no grammatical errors; may miss minor nuance of the Latin);
   9-excellent (captures exact meaning and tone; reads as professional scholarly translation);
   10-perfect (flawless; captures nuance, idiom, and subtext of the Latin exactly).
3. issues: a list of the errors you found. Each issue names an MQM dimension and error type from:
   - Accuracy: Mistranslation, Omission, Addition, Untranslated, Number, Date, Entity
   - Fluency: Grammar, Spelling, Punctuation, Unintelligible
   - Terminology: Wrong-term, Inconsistent
   - Style: Register, Awkward
   and a severity:
   - minor: limited impact (slight awkwardness or non-critical fluency; meaning preserved);
   - major: significant loss or change of meaning, or a mistranslation that alters meaning;
   - critical: complete loss of meaning, hallucination, or a corrupted citation/number/name.

CRITICAL INSTRUCTION: flag ONLY genuine errors you can justify against the Latin. Do NOT invent \
errors, and do NOT flag defensible synonyms, faithful paraphrase, legitimate register choices, or \
preserved Greek. A wrong flag is worse than a missed one. If the translation is faithful and \
correct, return an empty issues list.

Output a SINGLE valid JSON object, no markdown, no prose, EXACTLY this schema:
{"score": <0-100 int>, "classification": "<one label>", "issues": [{"severity": "minor|major|critical", "dimension": "Accuracy|Fluency|Terminology|Style", "error_type": "<one type>", "span": "<english span>", "description": "<why, referencing the Latin>"}]}

LATIN:
__LATIN__

ENGLISH:
__ENGLISH__
"""


def english_for(record: dict) -> str:
    history = record.get("translation_history") or []
    if history:
        text = (history[-1] or {}).get("english") or ""
        if text.strip():
            return text
    return record.get("final_english") or ""


def _page_num(record: dict) -> int | None:
    pid = str(record.get("page_id") or "")
    m = re.search(r"(\d+)", pid) or re.search(r"_p(\d+)_", str(record.get("segment_id") or ""))
    return int(m.group(1)) if m else None


def _strip_carets(text: str) -> str:
    return re.sub(r"\^[A-Za-z0-9]{1,2}", "", text or "")


def _build_judge(provider_name: str, model: str | None):
    if provider_name == "gemini":
        provider = load_config().get("gemini")
        if model:
            provider = replace(provider, model=model)
        return GeminiTranslationAdapter(provider, temperature=0.0)
    provider = default_config().get("anthropic")
    if model:
        provider = replace(provider, model=model)
    return AnthropicTranslationAdapter(provider)


def _normalize_class(c: str) -> str:
    """Map a returned classification to a canonical label (judges sometimes drop
    the numeric prefix, e.g. 'excellent' -> '9-excellent')."""
    c = (c or "").strip().lower()
    if not c:
        return ""
    m = re.match(r"\s*(\d{1,2})", c)
    if m:
        for canon in _CLASSIFICATIONS:
            if canon.startswith(m.group(1) + "-"):
                return canon
    for canon in _CLASSIFICATIONS:
        if canon.split("-", 1)[1] in c:
            return canon
    return c


def _parse_output(raw: str) -> tuple[float | None, str, list[dict]]:
    """Parse {score, classification, issues:[...]} from the judge's raw output."""
    obj = _extract_json_object(raw)
    score = obj.get("score")
    try:
        score = float(score)
    except (TypeError, ValueError):
        score = None
    classification = _normalize_class(str(obj.get("classification", "")))
    issues_raw = obj.get("issues")
    issues: list[dict] = []
    if isinstance(issues_raw, list):
        for e in issues_raw:
            if not isinstance(e, dict):
                continue
            sev = str(e.get("severity", "")).lower().strip()
            if sev not in _SEVERITY_WEIGHT:
                # A malformed severity is recorded as-is with weight 0, never
                # silently promoted to a scored severity (the earlier bug).
                sev = f"?{sev}"
            issues.append({
                "severity": sev,
                "dimension": str(e.get("dimension", "")),
                "error_type": str(e.get("error_type", "")),
                "span": str(e.get("span", "")),
                "description": str(e.get("description", "")),
            })
    return score, classification, issues


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--segments", type=Path, required=True)
    ap.add_argument("--start-page", type=int, default=None)
    ap.add_argument("--end-page", type=int, default=None)
    ap.add_argument("--judge-provider", choices=["anthropic", "gemini"], required=True)
    ap.add_argument("--judge-model", default=None)
    ap.add_argument("--label", required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--limit", type=int, default=None, help="Judge only the first N units (smoke test).")
    args = ap.parse_args(argv)

    judge = _build_judge(args.judge_provider, args.judge_model)

    units = []
    for line in args.segments.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        pn = _page_num(r)
        if args.start_page is not None and (pn is None or pn < args.start_page):
            continue
        if args.end_page is not None and (pn is None or pn > args.end_page):
            continue
        latin = _strip_carets(str(r.get("latin_text") or "")).strip()
        english = _strip_carets(english_for(r)).strip()
        if not latin or not english:
            continue
        units.append({"segment_id": r.get("segment_id", ""), "latin": latin, "english": english})

    if args.limit:
        units = units[:args.limit]

    # Incremental + resumable: each record is appended as it completes, and units already
    # judged successfully in --output are skipped, so a killed long run (nested-CLI Opus
    # judge, >600s) loses nothing.
    results = []
    if args.output.exists():
        for line in args.output.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if r.get("n_issues") is not None:
                    results.append(r)
    done = {r["segment_id"] for r in results}
    if done:
        print(f"resuming: {len(done)} units already judged in {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in results), encoding="utf-8")
    out_fh = args.output.open("a", encoding="utf-8")
    for i, u in enumerate(units, 1):
        if u["segment_id"] in done:
            continue
        prompt = _MQM_PROMPT.replace("__LATIN__", u["latin"]).replace("__ENGLISH__", u["english"])
        t0 = time.perf_counter()
        try:
            raw = judge.complete_text(prompt)
            score, classification, issues = _parse_output(raw)
        except Exception as exc:
            score, classification, issues = None, "", None
            print(f"  {u['segment_id']}: judge error: {type(exc).__name__}: {str(exc)[:120]}",
                  file=sys.stderr)
        penalty = (sum(_SEVERITY_WEIGHT.get(e["severity"], 0) for e in issues) if issues else 0)
        rec = {
            "segment_id": u["segment_id"],
            "score": score,
            "classification": classification,
            "n_issues": (len(issues) if issues is not None else None),
            "mqm_penalty": penalty,
            "src_tokens": len(u["latin"].split()),
            "issues": issues,
            # efficiency telemetry: wall-clock seconds for this item (including any retries),
            # attempts, and provider token usage where the adapter exposes it (Gemini usageMetadata)
            "latency_s": round(time.perf_counter() - t0, 3),
            "attempts": getattr(judge, "last_attempts", None),
            "usage": getattr(judge, "last_usage", None),
        }
        results.append(rec)
        out_fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        out_fh.flush()
        print(f"[{i}/{len(units)}] {u['segment_id']}: score={score} "
              f"class={classification[:14]} issues={'ERR' if issues is None else len(issues)}")
    out_fh.close()

    scored = [r for r in results if r["n_issues"] is not None]
    valid_scores = [r["score"] for r in scored if isinstance(r["score"], (int, float))]
    tot_pen = sum(r["mqm_penalty"] for r in scored)
    tot_tok = sum(r["src_tokens"] for r in scored) or 1
    by_sev = Counter(e["severity"] for r in scored for e in (r["issues"] or []))
    by_dim = Counter(e["dimension"] for r in scored for e in (r["issues"] or []))
    by_class = Counter(r["classification"] for r in scored if r["classification"])
    summary = {
        "label": args.label,
        "judge_provider": args.judge_provider,
        "judge_model": args.judge_model,
        "segments_file": str(args.segments),
        "units_scored": len(scored),
        "mean_score_0_100": (round(sum(valid_scores) / len(valid_scores), 2) if valid_scores else None),
        "total_issues": sum((r["n_issues"] or 0) for r in scored),
        "mqm_penalty_per_100_src_tokens": round(100 * tot_pen / tot_tok, 3),
        "by_severity": dict(by_sev),
        "by_dimension": dict(by_dim),
        "classification_distribution": dict(by_class),
    }
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n" + json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
