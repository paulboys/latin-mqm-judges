# LITERA — attribution (CC BY 4.0)

Files in this directory are redistributed from the **LITERA** project under the
**Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

- **Source:** Paul Rosu, "LITERA: An LLM Based Approach to Latin-to-English Translation,"
  Findings of the Association for Computational Linguistics: NAACL 2025.
- **Repository:** https://github.com/paulrosu11/LITERA
- **License:** CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
- **Retrieved:** 2026-10-02, from branch `main`.

Files (verbatim copies, unmodified):
- `TestData.jsonl` — Classical Latin test set (68 pairs; complete sentences, e.g. Virgil,
  Cicero). Used here as a **clean-gold** substrate for the planted-error recall test
  (Classical register — a contrast anchor, not an Ussher proxy).
- `ModernLatinTest.jsonl` — Early-Modern / Neo-Latin test set (307 pairs; University of
  Warwick Neo-Latin anthology). On inspection these are **verse line-fragments**, loosely
  aligned; **set aside** for defect injection. Retained for provenance.

Changes: none to the data. We use it as input substrate only. `FineTuningData.jsonl`
(the project's training set) was downloaded locally but is not redistributed here.

Per CC BY 4.0 we credit the author and indicate that no changes were made to the data.


> In the public `latin-mqm-judges` repository only `TestData.jsonl` is included (the file the
> experiment uses); the other LITERA files are available from the LITERA repository above.
