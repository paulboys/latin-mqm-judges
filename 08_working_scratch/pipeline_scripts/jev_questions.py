"""jev_questions.py — JEV question sets and how their answers are combined.

LEGACY_V1   the original 3 questions (has_error / severity / faithfulness) used for the G3 probe and
            the v1/v2 runs. Unchanged, so those runs stay reproducible.
MQM         decomposed set (2026-10-04), following TypeSafe's question-design guidance
            (docs.typesafe.ai: "A judgment that depends on several things is best split into one
            question per thing"; noul: "Avoid multi-condition questions"; jev-1.13 jaggedness:
            "jev-1.13 leans toward the option that comes first" in a Choice):
              - CORE: one noul per MQM category (6)
              - FINE: one noul per grammar-level error mechanism (13)
              - severity_v2 asked in BOTH option orders, averaged in code (option-order bias)
            The MQM request also carries LEGACY_V1 unchanged. TypeSafe documents every question as
            "evaluated in parallel and in isolation against the same state", so the sets do not
            contaminate each other and the legacy answers give a paired comparison.

Combination rule (PRE-REGISTERED before any MQM run; not tuned on results):
  p_error_<set> = max over that set's Accuracy + Terminology nouls (Fluency excluded)
  typed_<set>   = every noul >= TYPED_THRESHOLD, mapped to its MQM (dimension, error_type)
"""
from __future__ import annotations

TYPED_THRESHOLD = 0.5

LEGACY_V1 = {
    "has_error": {
        "type": "noul",
        "instructions": ("The STATE gives a LATIN source and an ENGLISH translation. Return the "
                         "probability that the English misrepresents the Latin's meaning in any way "
                         "(mistranslation, omission, addition, wrong proper name, altered number, or "
                         "dropped negation). Preserved Greek or a defensible paraphrase is NOT an error."),
    },
    "severity": {
        "type": "choice",
        "instructions": "Classify the single most severe translation error in the English relative to the Latin.",
        "criteria": {
            "none": "Faithful; no meaning error.",
            "minor": "Noticeable but meaning preserved; reader not misled.",
            "major": "Meaning changed or lost on a point; reader misled.",
            "critical": "Meaning reversed/destroyed, hallucination, or corrupted name/number.",
        },
    },
    "faithfulness": {
        "type": "score",
        "instructions": "Rate how faithfully the English renders the meaning of the Latin.",
        "criteria": [
            "no meaning preserved", "severe distortion", "significant errors",
            "minor errors only", "fully faithful",
        ],
    },
}

_CTX = "The state gives a LATIN passage and an ENGLISH translation of it. "
_SAME = ("The English means the same as the Latin; any differences are only of wording, word order, "
         "idiom or sentence structure, or untranslated Greek.")


def _noul(question, true, false=_SAME):
    return {"type": "noul", "instructions": _CTX + question, "criteria": {"true": true, "false": false}}


# (id, question, true-description, MQM dimension, MQM error_type)
_CORE = [
    ("core_mistranslation", "Does the English give any part of the Latin a different meaning from the one it has in the Latin?",
     "Some word, phrase or clause means something different in the English than in the Latin.", "Accuracy", "Mistranslation"),
    ("core_entity", "Does the English name or refer to a different person, place or written work than the Latin does?",
     "A person, place or work in the English is not the one the Latin means.", "Accuracy", "Entity"),
    ("core_omission", "Does the English leave out something that the Latin says?",
     "Some content of the Latin is missing from the English.", "Accuracy", "Omission"),
    ("core_addition", "Does the English say something that the Latin does not say?",
     "The English contains content with no basis in the Latin.", "Accuracy", "Addition"),
    ("core_terminology", "Does the English use the wrong term for a technical term in the Latin, such as a liturgical, legal or calendar term or the title of a work?",
     "A technical term or title is rendered with the wrong term.", "Terminology", "Wrong-term"),
    ("core_fluency", "Is the English ungrammatical or hard to read?",
     "The English has grammatical errors or is hard to follow.", "Fluency", "Grammar"),
]
_FINE = [
    ("fine_word_sense", "Does the English give any Latin word a meaning it does not have in this context?",
     "A Latin word is translated with a sense it cannot have here.", "Accuracy", "Mistranslation"),
    ("fine_roles", "Does the English change who does what to whom, compared with the Latin?",
     "The doer, the receiver or the person addressed differs from the Latin.", "Accuracy", "Mistranslation"),
    ("fine_reference", "Does any name or pronoun in the English refer to a different person, place or thing than in the Latin?",
     "A name or pronoun points to the wrong person, place or thing.", "Accuracy", "Entity"),
    ("fine_clause_relation", "Does the English change how two clauses relate to each other (cause, concession, purpose, result, time or condition), compared with the Latin?",
     "The logical link between clauses differs from the Latin.", "Accuracy", "Mistranslation"),
    ("fine_modality", "Does the English change how certain a statement is, compared with the Latin (for example stating as fact something the Latin presents as hypothetical, reported or uncertain)?",
     "The English is more or less certain, or more or less real, than the Latin.", "Accuracy", "Mistranslation"),
    ("fine_number", "Does the English change a number or a date, compared with the Latin?",
     "A number or date differs from the Latin.", "Accuracy", "Mistranslation"),
    ("fine_quantifier", "Does the English change a quantity word such as all, some, none, each or any, compared with the Latin?",
     "A quantity word differs from the Latin.", "Accuracy", "Mistranslation"),
    ("fine_negation", "Does the English drop, add or reverse a negation, compared with the Latin?",
     "A negation is missing, added or reversed.", "Accuracy", "Mistranslation"),
    ("fine_omission", "Does the English leave out a word, phrase or clause that the Latin contains?",
     "Some word, phrase or clause of the Latin has no counterpart in the English.", "Accuracy", "Omission"),
    ("fine_addition", "Does the English contain a word, phrase or clause with no counterpart in the Latin?",
     "The English adds content that is not in the Latin.", "Accuracy", "Addition"),
    ("fine_terminology", "Does the English mistranslate the title of a work or a liturgical, legal or calendar term?",
     "A title or technical term is rendered wrongly.", "Terminology", "Wrong-term"),
    ("fine_grammar", "Is the English ungrammatical?",
     "The English contains a grammatical error.", "Fluency", "Grammar"),
    ("fine_ambiguity", "Is the English ambiguous where the Latin is not, for example a pronoun or relative clause that could attach to the wrong word?",
     "A reader could reasonably attach a word or clause to the wrong thing.", "Fluency", "Ambiguity"),
]

TYPE_MAP = {qid: (dim, et) for qid, _, _, dim, et in _CORE + _FINE}
SETS = {"core": [q[0] for q in _CORE], "fine": [q[0] for q in _FINE]}

_SEV_LEVELS = [
    ("none", "The English conveys what the Latin says; a reader is not misled."),
    ("slightly", "A reader is misled on a small detail that does not change the main point."),
    ("substantially", "A reader is misled on a point that matters to what the passage claims."),
    ("completely", "A reader gets the main point of the Latin wrong or reversed."),
]
_SEV_Q = "How far would a reader relying only on this English be misled about what the Latin says?"
SEVERITY_V2 = {
    "severity_v2_fwd": {"type": "choice", "instructions": _CTX + _SEV_Q, "criteria": dict(_SEV_LEVELS)},
    "severity_v2_rev": {"type": "choice", "instructions": _CTX + _SEV_Q, "criteria": dict(reversed(_SEV_LEVELS))},
}

MQM = {**LEGACY_V1, **SEVERITY_V2, **{q: _noul(text, true) for q, text, true, _, _ in _CORE + _FINE}}

QUESTION_SETS = {"legacy": LEGACY_V1, "mqm": MQM}


def derive(answers: dict) -> dict:
    """Pre-registered combination of MQM-set answers into per-set error probabilities and typed issues."""
    out = {}
    for name, ids in SETS.items():
        ps = {q: (answers.get(q) or {}).get("noul") for q in ids}
        acc = [p for q, p in ps.items() if p is not None and TYPE_MAP[q][0] != "Fluency"]
        out[f"p_error_{name}"] = max(acc) if acc else None
        out[f"typed_{name}"] = [{"question": q, "dimension": TYPE_MAP[q][0], "error_type": TYPE_MAP[q][1], "p": p}
                                for q, p in ps.items() if p is not None and p >= TYPED_THRESHOLD]
    f, r = (answers.get("severity_v2_fwd") or {}).get("probabilities"), (answers.get("severity_v2_rev") or {}).get("probabilities")
    if f and r:
        avg = {k: (f.get(k, 0) + r.get(k, 0)) / 2 for k, _ in _SEV_LEVELS}
        out["severity_v2_probs"] = avg
        out["severity_v2"] = max(avg, key=avg.get)
    return out
