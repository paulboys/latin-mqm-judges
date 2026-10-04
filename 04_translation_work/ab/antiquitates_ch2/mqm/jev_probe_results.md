# G3 — JEV Latin-capability probe: results

Gate G3 of the Stage-0 plan. Go/no-go capability check (NOT a validation): can JEV
comprehend Ussher's early-modern scholarly Latin well enough to be worth testing as a
discriminative judge? Run 2026-10-02 via `jev_probe.py` against `https://jevmodel.org/v1/
systemone` (Paul's key is issued by that reseller host), model returned `jev-1.13.0`.

## Evidence / reproducibility
Raw per-case JEV responses (full `probabilities`/`confidence`/`legend`/`usage`) are saved to
`jev_probe_raw.jsonl` in this directory — the auditable source behind every number below.
Regenerate with:
`python 08_working_scratch/pipeline_scripts/jev_probe.py --endpoint https://jevmodel.org/v1/systemone`
(cases live in that script's `CASES` list). The run below reproduced on a second execution
(values within run-to-run noise), e.g. C2 `has_error` 0.95 both times.

## Method
7 hand-built cases with known verdicts: 2 clean controls, 4 unambiguous errors, 1 subtle
boundary case. Each asked three JEV questions on the Latin+English state: `has_error`
(noul, yes-probability), `severity` (choice: none/minor/major/critical), `faithfulness`
(score 0–4). Tiny n; a smoke test, not a benchmark.

## Results
| Case | Known truth | has_error | severity | faithfulness | Verdict |
|---|---|---|---|---|---|
| D clean (short) | clean | 0.09 | none (0.86) | 3.84 | correct |
| G clean (long, preserved negation) | clean | 0.25 | none (0.55) | 3.53 | correct, no over-flag |
| E wrong number (23→33) | error (Number) | 0.98 | critical (0.92) | 1.66 | caught |
| F wholesale mistranslation | error (critical) | 0.98 | critical (0.99) | 0.18 | caught |
| C2 dropped negation (declarative) | error (critical) | 0.95 | critical (0.87) | 2.15 | caught |
| B entity (Pudens≠Plutarch) | error (Entity) | 0.86 | critical (0.48) | 2.41 | caught |
| A subject/object "them" (subtle) | error (subtle) | 0.20 | none (0.66) | 3.48 | missed — boundary case |

## Verdict: PASS (promising, with caveats)
- JEV flagged **all 4 unambiguous errors** and passed **both clean controls** without
  false-flagging their correctly-rendered negations.
- The entity case (B) requires actually resolving the Latin referent (`cum illo` = the
  subject Plutarch, not Pudens) — real comprehension, not surface matching.
- Its one miss (A) is the subtle subject/object error we ourselves split minor/major on.

## Honest caveats (binding on any downstream use)
1. **n = 7 constructed cases.** Capability smoke test, NOT a validation of JEV as an MQM
   instrument. Validity on Ussher's Latin is established only by the human anchor (The classicist).
2. **Severity skews harsh.** JEV stamped `critical` on the number error (E) and the entity
   error (B) where we would say `major`. Strong on **detection**, over-severe on
   **severity calibration** — a datum to report, not to hide.
3. **v1 lesson (verify your own test).** The first probe's "dropped negation" case put the
   negation inside a *rhetorical question*, where polarity does not reverse the assertion;
   JEV correctly passed it, and scoring it as a miss would have manufactured a false failure.
   Fixed to a declarative in v2 (C2), which JEV then caught at 0.95.
4. **Host:** key is a jevmodel.org reseller key (not TypeSafe's official api.typesafe.ai),
   exposed in-session → rotate after use. Public-domain Latin only was sent.

## Gate status — Stage 0 COMPLETE
- **G1 (JEV access):** ✓ key works against jevmodel.org; `jev-1.13.0`; ~700 tokens/case of a
  100k free budget.
- **G2 (corpora):** ✓ (see `corpus_verification.md`) — LITERA CC BY 4.0 reference-only;
  IPC classical-register, availability unconfirmed; both reference-only (no MQM labels).
- **G3 (JEV Latin capability):** ✓ PASS as above.

→ Decision point reached: choose **Ussher-focused slice** vs **full benchmark program**.
