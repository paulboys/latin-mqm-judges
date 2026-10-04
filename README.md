# latin-mqm-judges

**Can automatic judges catch fluent mistranslations of Latin?** This repository holds the test sets,
code, raw judge outputs and analysis for an experiment comparing three automatic translation-quality
judges on Latin→English translation:

- **Claude Opus 4.8** and **Gemini 3.1 Pro**, prompted as MQM annotators (they return an issue list
  with error type and severity, plus a 0–100 score);
- **TypeSafe JEV** (`jev-1.13.0`), a "System One" model that returns typed, probability-valued
  answers to structured questions, tested with its original 3-question set and with a 24-question
  set decomposed along the MQM error taxonomy.

The target is the hardest class of translation error: a **fluent misgloss**, English that reads
smoothly but misreads the Latin (wrong referent, wrong case role, wrong clause relation, wrong mood).
The source text is James Ussher's *Britannicarum Ecclesiarum Antiquitates* (1639), chapters 1–2,
with a Classical contrast set from LITERA.

> **Status: provisional.** The answer keys were written by Claude (Opus 5.5) and have **not yet been
> adjudicated** by the project's classicist; several items are explicitly contested. Judges were run
> once or twice. Read every number below as a baseline, not a result. See [Limitations](#limitations).

## Test sets

| Set | Items | What it is | Folder |
|---|---|---|---|
| **v1** | 22 (12 errors, 10 negatives) | Real fluent misglosses from Ussher drafts + Claude-written misglosses on LITERA Classical, each with its correct counterpart | `…/mqm/fluent/` |
| **v2** | 144 (66 errors, 78 negatives) | One error **planted** into a published reference (Baker 1930 for Ussher ch. 2; LITERA gold for Classical) + 9 real errors found in Baker + meaning-preserving rewrites | `…/mqm/fluent_v2/` |
| **v3** | 107 (51 errors, 56 negatives) | **Hard set**: 17 real grammar-dependent errors made by MT models (Opus 4.8, Gemini 3.1 Pro, Fable 5) on Ussher ch. 1–2, each paired with another model's correct rendering; 34 simulated errors reproducing the same mechanisms on real model renderings; 6 real-but-defensible divergences | `…/mqm/fluent_v3/` |

Each set has a `candidate_pool.jsonl` (items + proposed MQM labels + rationale), a `worksheet.md`
(the adjudication sheet), and `runs/` (judge inputs, provisional keys, raw outputs, analyses).
`…` = `04_translation_work/ab/antiquitates_ch2`.

## Provisional findings

**Discrimination on the hard set (v3, two runs; provisional key).**

| | Errors caught | Correct flagged | Ranking AUC |
|---|---|---|---|
| Gemini 3.1 Pro | 42/51 · 41/51 | 7/56 · 6/56 | 0.89 · 0.90 |
| JEV, original 3 questions | 24/51 · 26/51 | 3/56 · 5/56 | 0.82 · 0.82 |
| JEV, MQM 24 questions (as an MQM issue list) | 26/51 · 24/51 | 7/56 · 7/56 | 0.71 · 0.69 (penalty) |

Gemini caught significantly more errors than either JEV setup (McNemar p<0.001); false positives did
not differ significantly. Run-to-run flag agreement was 94–96 %.

**Efficiency (v3 run 2, measured, 107 items).**

| per item | latency mean / median | tokens in + out + thinking |
|---|---|---|
| Gemini 3.1 Pro | 5.27 / 5.14 s | 895 + 74 + 420 = 1,389 |
| JEV, 3 questions | 0.25 / 0.23 s | 619 + 79 = 698 |
| JEV, 24 questions | 0.24 / 0.23 s | 2,848 + 542 = 3,390 |

JEV was about 21× faster, and its latency did not grow with the number of questions. Token use was
about half of Gemini's with 3 questions and about 2.4× with 24; relative *cost* depends on per-token
prices, which are not applied here.

**Other findings** (details in each set's `runs/*.md`):
- On v2 (mostly blunt planted errors) all judges rank errors well (Opus score AUC 1.000, Gemini 0.98,
  JEV 0.945). Opus flags many correct sentences, but almost all of those flags are *minor*: an
  any-flag scoring rule penalises it, a major-only rule does not.
- On the small subtle set (v1, n=22) no judge is distinguishable from the others or confidently
  above chance.
- Decomposing JEV's question along MQM categories (TypeSafe's own guidance) did **not** improve
  discrimination, but it lets JEV return typed errors; Entity errors were typed reliably.
- JEV's probabilities are miscalibrated in a set-dependent way (too high on clean text in v2, too
  low in v3), so no single cut-off transfers between sets.
- Real model errors were missed far more often than simulated ones, but several of the missed real
  items are themselves contested renderings, so this gap partly reflects label certainty.

## Reproduce

Requires Python ≥ 3.10 (standard library only). Run everything from the repository root.

**Rebuild the test sets** (deterministic; byte-identical to the shipped files):
```
python 08_working_scratch/pipeline_scripts/build_fluent_v2_pool.py
python 08_working_scratch/pipeline_scripts/build_fluent_v3_pool.py
```
Both scripts assert that every Latin passage and reference/base translation is copied verbatim
from its source file.

**Re-score the stored judge outputs** (no API keys needed), e.g.:
```
S=08_working_scratch/pipeline_scripts; R=04_translation_work/ab/antiquitates_ch2/mqm/fluent_v3
python $S/score_v3_breakdown.py --pool $R/candidate_pool.jsonl \
    --judge gemini:$R/runs/gemini_on_v3_run2.jsonl --judge jev:$R/runs/jev_on_v3_run2.jsonl
python $S/judge_auc.py --key $R/runs/v3_key_provisional.jsonl --pool $R/candidate_pool.jsonl \
    --judge gemini:$R/runs/gemini_on_v3_run2.jsonl --judge jev:$R/runs/jev_on_v3_run2.jsonl
python $S/jev_calibration.py --key $R/runs/v3_key_provisional.jsonl --jev $R/runs/jev_on_v3_run2.jsonl
python $S/judge_efficiency.py --judge gemini:$R/runs/gemini_on_v3_run2.jsonl --judge jev:$R/runs/jev_on_v3_run2.jsonl
```
Judge-label prefixes select the output shape: `jev*` = JEV original questions, `jevcore*`/`jevfine*`
= JEV decomposed (max rule), anything else = an MQM issue list (Opus, Gemini, or JEV converted with
`jev_to_mqm.py`).

**Re-run the judges** (needs API access). Copy `.env.example` to `.env` and fill in the keys.
```
# Gemini as MQM judge
python $S/mqm_judge.py --segments $R/runs/v3_input.jsonl --judge-provider gemini \
    --judge-model gemini-3.1-pro-preview --label gemini-on-v3 --output $R/runs/gemini_on_v3.jsonl
# Opus as MQM judge (shells out to the `claude` CLI, which must be installed and logged in)
python $S/mqm_judge.py --segments $R/runs/v3_input.jsonl --judge-provider anthropic \
    --judge-model claude-opus-4-8 --label opus-on-v3 --output $R/runs/opus_on_v3.jsonl
# JEV, original or decomposed MQM question set (official TypeSafe endpoint)
python $S/jev_judge.py --input $R/runs/v3_input.jsonl --output $R/runs/jev_on_v3.jsonl
python $S/jev_judge.py --question-set mqm --input $R/runs/v3_input.jsonl --output $R/runs/jev_mqm_on_v3.jsonl
python $S/jev_to_mqm.py --set core --input $R/runs/jev_mqm_on_v3.jsonl --output $R/runs/jevmqm_core_on_v3.jsonl
```
All judge runners write incrementally and resume after interruption. They record latency and token
usage per item. Model outputs are not fully deterministic; expect small run-to-run differences.

## Repository layout

Paths mirror the source project so the scripts run unchanged.

```
08_working_scratch/pipeline_scripts/   all code (judges, set builders, scorers)
04_translation_work/ab/antiquitates_ch2/mqm/
    fluent/  fluent_v2/  fluent_v3/    the three test sets, keys, judge outputs, analyses
    real_error_seed.*, litera_fluent_misglosses.*   v1 provenance
    baker_segments.jsonl               v2 source: Ussher ch. 2 Latin + Baker 1930 English
    harvest_divergences.jsonl          v3 source: Opus vs Gemini ch. 1 drafts (built by harvest_divergences.py from the full drafts, not shipped)
    jev_probe_*                        initial JEV Latin-capability probe
04_translation_work/ab/antiquitates_ch2/baker_benchmark/baker_scores_*.jsonl
                                       v3 source: Opus 4.8 / Gemini 3.1 Pro / Fable 5 ch. 2 translations
09_analysis/external_corpora/litera/   LITERA Classical test data (CC BY 4.0)
```

## Limitations

- **Unadjudicated keys.** Every error label and severity was proposed by Claude and awaits the
  classicist adjudicator. An external review already disputed three v1 labels. Re-score when the
  adjudicated keys are released.
- **Authorship bias.** Claude wrote the planted and simulated errors and found the real ones, so the
  sets lean towards errors a Claude-family reader can see. This may favour the Opus judge, which is
  why v3 was run with Gemini and JEV only.
- **Small samples.** v1 has 22 items, and v3 has 17 real errors, so many intervals are wide.
- **Few runs.** v1/v2: one run per judge. v3: two runs.
- **Scoring choices matter.** Any-flag vs major-only detection changes Opus's false-positive rate
  dramatically. The JEV combination rules were fixed before scoring and not tuned.
- **Efficiency** is wall-clock from one machine (network included) and token counts, not money.

## Licences and attribution

- **Code:** MIT, see `LICENSE`.
- **Data, annotations and analyses created in this project:** CC BY 4.0, see `DATA_LICENSE.md`.
- **Ussher's Latin text (1639):** public domain.
- **LITERA** Classical test data: CC BY 4.0, Paul Rosu, *LITERA: An LLM Based Approach to
  Latin-to-English Translation*, Findings of NAACL 2025; see `09_analysis/external_corpora/litera/ATTRIBUTION.md`.
- **Baker (1930)** English translation of *Antiquitates* ch. 2: excerpts used as references.
- **Model outputs** from Claude Opus 4.8, Gemini 3.1 Pro, Fable 5 and JEV are included as
  experimental data.

## Credits

Paul Boys (design, direction), with an anonymous classicist adjudicator. Built with Claude Code.

```
@misc{latin-mqm-judges,
  title  = {latin-mqm-judges: LLM and System-One judges on fluent Latin mistranslations},
  author = {Boys, Paul},
  year   = {2026},
  url    = {https://github.com/paulboys/latin-mqm-judges}
}
```
