# G2 — Corpus verification (primary-source)

Gate G2 of the Stage-0 plan. Verifies the second-hand research-summary claims against
primary sources before any build relies on them. Checked 2026-10-02.

## LITERA (Rosu, NAACL 2025 Findings)
Primary: paper `arxiv.org/abs/2504.10660` / `aclanthology.org/2025.findings-naacl.434`;
repo `github.com/paulrosu11/LITERA`.

| Claim (from summary) | Verified? | Primary finding |
|---|---|---|
| License CC BY 4.0 | **YES** | Repo README: "licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0)." Usable + redistributable with attribution. |
| Has an Early-Modern/Neo-Latin test set | **YES** | Repo ships `ModernLatinTest.jsonl`, "sourced from the University of Warwick's Neo-Latin anthology." |
| Reference-only (no error/MQM labels) | **YES** | Repo provides `FineTuningData.jsonl`, `TestData.jsonl` (classical), `ModernLatinTest.jsonl` — Latin↔English pairs only; **no** error annotations / MQM / IAA labels. |
| Sizes ~200 train / ~70 classical / ~350 early-modern | **NOT verified** | Not stated in abstract or README. Fine-tune set described only as "small … ~200 pairs" (Cicero/Virgil/Ovid) in secondary summaries. **Action: confirm by counting the JSONL files at build time** (authoritative), not by trusting prose. |

**Usable claim:** LITERA is a CC BY 4.0 **reference** corpus (no error labels). Its
`ModernLatinTest.jsonl` (Warwick Neo-Latin) is the closest public clean substrate to
Ussher's early-modern Latin → **primary external substrate for defect injection.**

## IPC — Interpres Parallel Corpus (arXiv 2607.03836, 2026-07)
Primary: `arxiv.org/html/2607.03836`.

| Claim | Verified? | Primary finding |
|---|---|---|
| 1,383 aligned triplets, per-work counts | **YES** | Table 1: Ovid Metamorphoses 492, Catullus 166, Cicero Tusculan 260, Quintilian 465 = **1,383**. Triplets = manuscript image / Latin / English. |
| "Medieval Latin" | **CORRECTED** | These are **classical-author** texts (Ovid, Catullus, Cicero, Quintilian) surviving in **medieval manuscripts**. "Medieval" = the manuscript/script (HTR context), **NOT** the language register. IPC is **Classical-register** Latin. |
| English = Perseus / Project Gutenberg | **YES** | More, Smithers, Butler (Perseus) + Yonge (Gutenberg) — older public-domain published translations. |
| Reference-only (no error/MQM labels) | **YES (not stated to have any)** | "expert translations"; no error/MQM annotation reported. |
| License + availability | **NOT stated** | Paper says the *model* releases on HuggingFace "upon acceptance"; **no dataset DOI, license, or download URL given.** ⚠️ We may not be able to obtain IPC, or its license may not permit derivatives. |

**Usable claim:** IPC = a **Classical-register** reference corpus (no error labels), counts
confirmed, but **availability + license unconfirmed** → treat as *contingent*. If obtainable
and license permits, it is the **Classical** end of the diachronic axis; if not, drop it.

## WMT / Unbabel MQM (Phase-1 only; full-program scope)
Not fetched (Phase 1 is gated and optional). Known: WMT MQM (Freitag et al.) carries genuine
human major/minor/critical annotations but on pairs like En–De, En–Ru, Zh–En — **no Latin**.
**Action: confirm exact pairs, schema, and access at Phase-1 time if we go there.**

---

## Consequences for the build
1. **Neither LITERA nor IPC is ready-made MQM gold** — both are reference-only. They serve as
   **clean substrate for defect injection** (our planted-error method), not as pre-labelled
   error sets. (Consistent with the plan.)
2. **Diachronic axis, correctly labelled:** Classical = IPC (if obtainable); Early-Modern =
   LITERA `ModernLatinTest` **and** Ussher. IPC gives *Classical*, not a medieval/EM middle.
3. **Primary external substrate = LITERA `ModernLatinTest.jsonl`** (CC BY 4.0, Warwick
   Neo-Latin, closest register to Ussher). IPC is a *contingent* Classical add-on pending
   license/availability.
4. **Sizes to confirm by counting the actual JSONL files** at build — do not cite the
   ~200/~70/~350 figures as fact; they are unverified secondary numbers.

## Post-download reassessment (2026-10-02, data in `09_analysis/external_corpora/litera/`)
Downloaded and inspected the actual LITERA files — correcting earlier over-optimism:
- **Sizes primary-verified:** FineTuningData 192, TestData (Classical) 68, ModernLatinTest 307.
- **`ModernLatinTest` (early-modern) is Neo-Latin VERSE, line-fragmented and loosely aligned**
  (each line a 5–7-word verse fragment; English enjambed across lines). Early-modern *era*,
  but a weak proxy for Ussher's scholarly *prose* and awkward for clause/sentence defect
  injection. **Set aside** for injection.
- **`TestData` (Classical) IS clean complete sentences** (Virgil, Cicero…), median ~10 Latin
  words. Usable **clean-gold**, but **Classical register**, not Ussher's early-modern prose.
- **Correction to the earlier claim** that LITERA "fixes the substrate hole": it does NOT
  supply clean Ussher-register prose. There is still **no clean early-modern scholarly-prose
  external substrate.**

### Adjusted substrate plan for the planted-error test
- **Primary = Ussher draft + baseline-subtraction** (in-domain; the task we actually care about).
- **Clean-gold anchor = LITERA Classical `TestData`** (complete sentences, no baseline-
  subtraction needed) — gives a Classical-vs-Ussher **register contrast**, honestly labelled.
- **LITERA EM verse + IPC**: not used (EM = verse fragments; IPC = classical register, access
  unconfirmed).

## Gate status
- **G2: COMPLETE** — sizes now verified; substrate reassessed as above.
- **G1 (JEV access): COMPLETE** — key works via jevmodel.org (`jev-1.13.0`).
- **G3 (JEV Latin probe): COMPLETE** — PASS (see `jev_probe_results.md`).
- **Stage 0 done; scope = Ussher-focused slice.**
