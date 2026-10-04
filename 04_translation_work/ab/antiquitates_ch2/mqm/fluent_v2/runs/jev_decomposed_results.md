# JEV: legacy vs decomposed (MQM) questions, v1 + v2 (2026-10-04)

**Why.** TypeSafe's docs recommend one factor per question ("Avoid multi-condition questions";
"decompose it"), and our legacy `has_error` bundles about eight. Several questions per request is
documented as fine ("evaluated in parallel and in isolation"). Question sets: `jev_questions.py`.
Runner: `jev_judge.py --question-set mqm`. Raw numbers: `jev_decomposed_comparison.txt`.

**Design.** One request per item carried the legacy 3 questions, `severity_v2` in both option
orders, 6 MQM-category nouls (`core_*`) and 13 mechanism nouls (`fine_*`): 24 answers per call,
about 3.3k tokens versus about 750 for the legacy set. The combination rule was fixed before the run:
p_error = max over a set's Accuracy + Terminology nouls; typed = nouls ≥ 0.5. Keys: v1 = v1 key
(n=22, subtle errors); v2 = the PROVISIONAL, unadjudicated key (n=144, mostly blunt errors).

**Controls.**
- Model drift: the legacy-only rerun on 5 v2 items reproduced the stored `has_error` to ±0.03.
- Isolation: the legacy `has_error` asked inside the 24-question request ranks the same as the
  stored legacy run (v2 AUC 0.941 vs 0.945, paired difference CI includes 0), consistent with the
  docs' isolation claim.

## Results (AUC = P(error item scored above a correct one); 95% CI)

| Signal | v1 (subtle, n=22) | v2 (provisional, n=144) |
|---|---|---|
| legacy `has_error` | 0.72 (0.48–0.92) | 0.945 (0.91–0.97) |
| core max (pre-registered) | 0.70 (0.46–0.90) | 0.924 (0.88–0.96) |
| fine max (pre-registered) | 0.68 (0.43–0.89) | 0.903 (0.85–0.95) |
| Opus 0–100 score / Gemini penalty | 0.75 / 0.83 | 1.000 / 0.987 |

1. **Decomposition did not improve discrimination.** On v1, legacy, core and fine can't be
   separated (all CIs include chance; n=22). On v2 the fine max is **worse** than legacy
   (−0.042, CI −0.081 to −0.009). Core is not distinguishable from legacy.
2. **Why the max hurts (inference, not tested directly):** the max over 10+ nouls lifts the
   scores of correct items (mean on v2 negatives: legacy 0.31, core 0.36, fine 0.45), so
   calibration gets worse (Brier skill +0.55 → +0.48 → +0.36). The noisy-OR combination is no
   better (computed after the run, so exploratory).
3. **What decomposition adds: JEV can now name the error type.** Exact error-type match: Entity
   is reliable (v1 3/3; v2 9/10 core, 10/10 fine). Mistranslation is weaker (v2 42/53 core;
   v1 2/6 core, **0/6 fine**). Wrong-term was 0/2 on v1. On the subtle v1 mistranslations, the
   mechanism-level questions (roles, clause relation, modality...) did not fire.
4. **Option-order bias exists but is small here.** Putting `none` first versus last moved
   P(none) by 0.01–0.02 on average; the forward and reversed severity disagreed on 3/22 (v1)
   and 15/144 (v2) items.

## Limits
- Single run; the v2 key is provisional (The classicist has not ruled); v1 n=22.
- The v2 errors are mostly blunt, so v2 can't show gains on subtle errors; v3 (hard set) is the
  real test, held until the classicist freezes its key.
- The noul wording was written once and not iterated (deliberately, to avoid tuning on results).
  Better wording might do better; that would need a held-out set.

## Implication
Keep the **legacy `has_error`** as JEV's detection signal. If error types are wanted, add the
**core** nouls (they type Entity and Omission well). Don't use the fine max for detection. On
subtle errors, no JEV question set tested here beats chance with confidence.

## Addendum: JEV scored as an MQM issue-list judge (apples-to-apples with Opus/Gemini)
`jev_to_mqm.py` (no fitting; rules fixed before scoring): each noul ≥0.5 becomes a typed issue; a
single per-item severity comes from severity_v2 (most probable non-"none" level; slightly/
substantially/completely → minor/major/critical); penalty = 1/5/25, as `mqm_judge.py`. Primary =
core set. Same scorers as Opus/Gemini. Raw: `jev_as_mqm_comparison.txt`.

| | v2 recall | v2 FP | v2 pair acc. | v2 penalty AUC | v1 recall | v1 FP | v1 penalty AUC |
|---|---|---|---|---|---|---|---|
| Opus | 66/66 | 51/78 | 18/66 | 0.998 | 8/12 | 4/10 | 0.74 |
| Gemini | 66/66 | 24/78 | 42/66 | 0.987 | 8/12 | 0/10 | 0.83 |
| JEV (core) | 58/66 | 22/78 | 41/66 | 0.889 | 7/12 | 3/10 | 0.68 |

- **Recall:** JEV misses 8 v2 errors that both LLMs catch (McNemar p=0.008 vs each).
- **False positives:** JEV ≈ Gemini (22 vs 24/78, p=0.85), far below Opus (51/78). Pair accuracy ≈ Gemini.
- **Penalty ranking:** JEV is clearly behind (v2 −0.10 vs both; v1 Gemini − JEV = +0.16, CI excludes 0).
  JEV's own legacy `has_error` ranks better (0.945) than its converted penalty: the penalty is
  coarse (one severity per item, ties) and overlapping questions stack issues (≈2.8 per flagged item).
- **Severity skews harsh:** 55/224 JEV issues are critical vs 11/116 for Gemini, matching the G3 probe note.
- Limits as above: provisional v2 key, one run, v1 n=22.
