# v3 hard set: Gemini vs JEV (legacy and MQM), PROVISIONAL (2026-10-04)

Scored against Claude's **unadjudicated** key; the classicist has not ruled, and five real items are
marked contestable. One run per judge. Raw: `v3_provisional_results.txt`. Withheld from the classicist.
Set: 51 errors (17 real model errors, 34 simulated edits) + 56 negatives.

| | Recall (all) | Real | Simulated | FP | Pair acc. | AUC |
|---|---|---|---|---|---|---|
| Gemini | 42/51 (82%) | 9/17 | 33/34 | 7/56 (12%) | 35/48 | 0.89 (score) / 0.89 (penalty) |
| JEV legacy (`has_error` ≥0.5) | 24/51 (47%) | 5/17 | 19/34 | 3/56 (5%) | 21/48 | 0.82 |
| JEV-MQM core | 26/51 (51%) | 8/17 | 18/34 | 7/56 (12%) | 19/48 | 0.71 (penalty) |
| JEV-MQM fine (secondary) | 36/51 (71%) | 9/17 | 27/34 | 19/56 (34%) | 22/48 | — |

- Gemini catches far more than either JEV setup at their default cut-offs (vs legacy: 19 vs 1
  discordant, p<0.001), with FP not significantly different (12% vs 5%). In ranking, Gemini's
  score beats JEV legacy by +0.07 (CI 0.007 to 0.146); its penalty margin is borderline (CI touches 0).
- JEV-MQM core ≈ JEV legacy on recall (51% vs 47%, p=0.75), with a much coarser penalty ranking
  (0.71, 26 tied pairs). JEV-MQM fine reaches recall closer to Gemini (71%, p=0.11) only by
  flagging a third of the correct renderings (FP 34%, p=0.008 vs Gemini).
- **Real errors are much harder than simulated ones**, for every judge: Gemini 9/17 real vs 33/34
  simulated; JEV legacy 5/17 vs 19/34. The simulated edits do NOT reproduce real difficulty.
  This is the most important design finding.
- JEV's probabilities are now too LOW (the reverse of v2): items scored 0.3–0.4 are errors 67%
  of the time; 0.5 is too strict a cut-off here (in-sample best ≈0.30, optimistic). Brier skill +0.24.
- Missed by every judge: H-02, H-08 (both contestable), H-12, H-13 (liturgical/title terms),
  S-14 ('released under Nero'), V1 in→to (contested). The classicist's rulings decide whether these are misses.

## Run 2 with measured efficiency (2026-10-04) — `v3_run2_efficiency_and_results.txt`
Telemetry added to `mqm_judge.py` (latency, attempts, Gemini usageMetadata incl. thinking tokens)
and `jev_judge.py` (latency, usage). Summary: `judge_efficiency.py`. Wall-clock from this machine
(includes network); tokens, not money (no prices assumed); Gemini thinking budget capped at 4096.

| per item (n=107) | latency mean / median / p90 | tokens in / out / thinking = total |
|---|---|---|
| Gemini 3.1 Pro (MQM prompt) | 5.27 / 5.14 / 7.80 s | 895 / 74 / 420 = 1,389 |
| JEV legacy (3 questions) | 0.25 / 0.23 / 0.30 s | 619 / 79 / 0 = 698 |
| JEV MQM (24 questions) | 0.24 / 0.23 / 0.27 s | 2,848 / 542 / 0 = 3,390 |

- JEV is ~21x faster per item than Gemini (median 0.23 vs 5.14 s), and its latency does not grow
  with the number of questions (24 questions ≈ 3 questions), as TypeSafe documents.
- Tokens: JEV legacy uses about half Gemini's total; JEV MQM uses ~2.4x MORE than Gemini. Whether
  either is cheaper depends on per-token prices, which are not applied here.
- Run 2 reproduces run 1: Gemini recall 41/51, FP 6/56, AUC 0.90 (score); JEV legacy 26/51, 5/56,
  AUC 0.82; JEV-MQM core 24/51, 7/56, penalty AUC 0.69. Gemini > both JEV setups on recall (p<0.001),
  FP not different.
- Run-to-run flag agreement: Gemini 96%, JEV legacy 94% (mean |Δp| 0.022), JEV-MQM core 96%.
