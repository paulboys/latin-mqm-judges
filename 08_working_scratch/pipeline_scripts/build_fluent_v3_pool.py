"""build_fluent_v3_pool.py — HARD set of REAL (naturally occurring) model errors, for the classicist.

Every error item is a verbatim (trimmed) rendering produced by an MT model on Ussher ch1/ch2:
nothing is planted. Its paired negative is ANOTHER model's verbatim rendering of the same Latin
that gets the point right. Plus real-but-defensible divergences as hard negatives (over-flag test).
Errors were found by Claude (Opus 5.5) reading the Latin against the drafts (2026-10-03), so the
set is biased toward errors a Claude-family reader can see; report results with that caveat.

Sources (provenance-checked letters-only, so trimming/quote marks are allowed but not rewording):
  ch2: 04_.../baker_benchmark/baker_scores_{opus-4-8,gemini-3-1-pro,fable-5}.jsonl (mt_english)
  ch1: 04_.../mqm/harvest_divergences.jsonl (opus_english / gemini_english)
  v1 carry-over: 04_.../mqm/fluent/fluent_set_input.jsonl (keys as in v1; still pending the classicist)

Writes 04_.../mqm/fluent_v3/candidate_pool.jsonl + worksheet.md + runs/v3_input.jsonl, v3_key_provisional.jsonl
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MQM = ROOT / "04_translation_work/ab/antiquitates_ch2/mqm"
BB = ROOT / "04_translation_work/ab/antiquitates_ch2/baker_benchmark"
OUT = MQM / "fluent_v3"
MODEL = {"opus": "opus-4-8", "gemini": "gemini-3-1-pro", "fable": "fable-5"}


def _letters(s):
    return re.sub(r"[^a-z]", "", s.lower().replace("æ", "ae").replace("œ", "oe"))


SRC = {}  # (unit, model) -> (latin, english)
for short, m in MODEL.items():
    for l in (BB / f"baker_scores_{m}.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(l)
        SRC[(r["unit_id"], short)] = (r["latin"], r["mt_english"])
for l in (MQM / "harvest_divergences.jsonl").read_text(encoding="utf-8").splitlines():
    r = json.loads(l)
    SRC[(r["segment_id"], "opus")] = (r["latin"], r["opus_english"])
    SRC[(r["segment_id"], "gemini")] = (r["latin"], r["gemini_english"])


def chk(unit, model, latin, english):
    la, en = SRC[(unit, model)]
    assert _letters(latin) in _letters(la), f"{unit}/{model}: Latin not in source"
    assert _letters(english) in _letters(en), f"{unit}/{model}: English not in {model} output"


def E(span, sev, etype="Mistranslation", dim="Accuracy"):
    return {"span": span, "dimension": dim, "error_type": etype, "severity": sev}


rows = []


def pair(hid, unit, latin, err_model, err_en, neg_model, neg_en, exp, why, contestable=""):
    chk(unit, err_model, latin, err_en)
    chk(unit, neg_model, latin, neg_en)
    for e in exp:
        if not e["span"].startswith("(missing)"):
            assert e["span"] in err_en, f"{hid}: span not in error rendering"
    base = dict(pair_id=hid, unit=unit, latin=latin, origin="real-model-output")
    rows.append({**base, "item_id": hid, "is_error_stimulus": True, "stimulus_english": err_en,
                 "rendered_by": MODEL[err_model], "expected": exp, "rationale": why,
                 "contestable": contestable, "counterpart_english": neg_en, "counterpart_by": MODEL[neg_model]})
    rows.append({**base, "item_id": hid + "__neg", "is_error_stimulus": False, "stimulus_english": neg_en,
                 "rendered_by": MODEL[neg_model], "expected": [],
                 "rationale": f"Another model's real rendering that gets the {hid} point right; needs a full check that it is clean.",
                 "contestable": "", "counterpart_english": err_en, "counterpart_by": MODEL[err_model]})


def boundary(hid, unit, latin, model, en, why):
    chk(unit, model, latin, en)
    rows.append(dict(pair_id=hid, unit=unit, latin=latin, origin="real-model-output", item_id=hid,
                     is_error_stimulus=False, stimulus_english=en, rendered_by=MODEL[model], expected=[],
                     rationale=why, contestable="boundary: keyed no-error, the classicist may disagree",
                     counterpart_english="", counterpart_by=""))


# ------------------------------------------------------------------ real errors, ch2
pair("H-01", "seg_p0047_s0001",
     "Postea etiam alii duo reges pagani successive comperta vitæ eorum sanctimonia, unicuique eorum unam portionem terræ concesserunt; ac ad petitionem ipsorum, secundum morem gentis, brevi dictas duodecim hidas confirmaverunt.",
     "opus", "Afterwards two other pagan kings also, one after the other, having learned of the holiness of their life, each granted them one portion of land; and at their request, according to the custom of the people, they confirmed the said twelve hides by charter.",
     "fable", "Afterwards two other pagan kings also, in succession, having learned of the sanctity of their life, granted to each of them one portion of land; and at their petition, according to the custom of the nation, they confirmed the said twelve hides by charter.",
     [E("each granted them one portion of land", "major")],
     "unicuique eorum (dative) = to EACH of them (the twelve), one portion apiece = the twelve hides of the next clause. Opus makes each KING the giver of one portion (two in all), breaking the link to the twelve hides.")
pair("H-02", "seg_p0050_s0006",
     "Glastoniæ bis sex hidas dedit Arviragus rex: Joseph cum sociis jura reliquit eis.",
     "fable", "King Arviragus gave twice six hides of Glastonbury to Joseph and his companions, and left the rights to them.",
     "gemini", "King Arviragus gave twice six hides of Glastonbury: Joseph with his companions left the rights to them.",
     [E("to Joseph and his companions, and left the rights to them", "major")],
     "Each verse is its own clause: Joseph (with companions) is the subject of reliquit, and leaves the rights to 'them' (eis). Fable folds Joseph into line 1 as recipient and makes Arviragus the one who 'left the rights'.",
     "Joseph is indeclinable, so case alone does not force it; the verse structure and the redundant eis do.")
pair("H-03", "seg_p0062_s0001",
     "Neque enim aliquem hodie, si Thomam Dempsterum exceperis, tam stulte credulum esse existimamus, cui absurdissimum illud commentum, de Josepho muro incluso, probabile videri possit",
     "opus", "For I do not suppose that anyone today—unless you make an exception of Thomas Dempster—is so foolishly credulous that that most absurd fabrication about Joseph walled up in a tomb could seem probable to him",
     "fable", "for I do not think that anyone today — unless you except Thomas Dempster — is so foolishly credulous that that most absurd fiction of Joseph shut up within a wall could seem probable to him",
     [E("walled up in a tomb", "minor")],
     "muro incluso = shut up in a wall: the Titus legend (p0060: a very thick wall broken open). 'tomb' substitutes a different confinement and blurs which tale Ussher means.",
     "severity: minor vs major")
pair("H-04", "seg_p0055_s0001",
     "Josephum ab Arimathea, cum a Judæis nequiter in carcerem ductus fuisset, et a Deo Optimo Maximo miraculose liberatum taliter ut nusquam postea in Judæa visum fuisse.",
     "opus", "that Joseph of Arimathea, after he had been wickedly cast into prison by the Jews and miraculously delivered by God Most Good and Most Great, was thereafter nowhere seen in Judaea.",
     "fable", "that Joseph of Arimathea, after he had been wickedly thrown into prison by the Jews, was so miraculously delivered by Almighty God that he was never afterward seen in Judaea",
     [E("and miraculously delivered by God Most Good and Most Great, was thereafter nowhere seen", "minor")],
     "liberatum taliter ut ... visum fuisse = delivered IN SUCH A WAY THAT he was never seen again (result clause). Opus folds the deliverance into the temporal clause and drops the causal link.")
pair("H-05", "seg_p0053_s0002",
     "quibus duodecim hidæ ab Arvirago paganicis erroribus decepto concessæ erant.",
     "fable", "and to these, twelve hides were granted by Arviragus, who was still deceived by pagan errors.",
     "opus", "To these men twelve hides were granted by Arviragus, who was deceived by pagan errors.",
     [E("still", "minor", "Addition")],
     "No adhuc in this sentence (contrast p0053_s0001 'adhuc ... involuto'). 'still' imports a later conversion, the very point Harding asserts and Ussher's sources deny.",
     "may be judged a harmless carry-over")
pair("H-06", "seg_p0052_s0001",
     "Auxit prodigiosos ritus Josephus Arimathæus, advena Britanniæ plauſsbilis; qui de Solomonis fonte artem hauserat.",
     "fable", "Joseph of Arimathea, a plausible newcomer to Britain, augmented their prodigious rites; he had drawn his art from the fountain of Solomon.",
     "opus", "Joseph of Arimathea, a newcomer whom Britain welcomed, increased its prodigious rites; he had drawn his art from Solomon's fountain.",
     [E("a plausible newcomer", "minor")],
     "plausibilis = applauded / welcome (Baker: 'a welcome stranger'). Modern 'plausible' = seemingly credible: a false friend.",
     "archaic English 'plausible' = deserving applause")
pair("H-07", "seg_p0050_s0008",
     "Postea vero a beato Johanne apostolo ipsi prædicationi Ephesiorum insudante, beatæ perpetuæque virginis Mariæ paranymphus delegatus est",
     "fable", "Afterwards, while the blessed apostle John was laboring at the preaching to the Ephesians, he was appointed paranymph of the blessed and perpetual virgin Mary",
     "gemini", "But afterwards, by the blessed apostle John, who was himself laboring in the preaching to the Ephesians, he was delegated as the paranymph of the blessed and perpetual virgin Mary",
     [E("while the blessed apostle John was laboring", "minor")],
     "a + ablative with passive delegatus est = agent: John appointed him. Fable reads it as an ablative absolute (time) and drops who made the appointment. (Opus makes the same misreading.)")
pair("H-08", "seg_p0056_s0001",
     "Tres vero istos reges paganos, Arviragum, Marium et Coillum fuisse, ad marginem libri Malmesburiensis, qui MS. habetur in bibliotheca collegii S. Trinitatis Cantabrigiæ, annotatum invenio: quod ipsum etiam innuit Johannes Capgravius; quanquam parum hic sibi constans.",
     "opus", "That those three kings — Arviragus, Marius, and Coilus — were pagans I find noted in the margin of the Malmesbury manuscript held in the library of Trinity College, Cambridge; and John Capgrave hints at the same, though he is hardly consistent with himself here.",
     "gemini", "I find it annotated in the margin of a book of William of Malmesbury, which is kept as a manuscript in the library of Trinity College, Cambridge, that these three pagan kings were Arviragus, Marius, and Coillus: which John Capgrave also intimates, although he is little consistent with himself here.",
     [E("That those three kings — Arviragus, Marius, and Coilus — were pagans", "major")],
     "istos reges paganos picks up Malmesbury's 'tres reges licet pagani' (p0055); the marginal note IDENTIFIES the kings. Capgrave's inconsistency (next sentence) is about WHICH kings granted the hides. (Fable makes the same misreading.)",
     "word order permits the predicate reading; 'Quos tamen reges ... paganos extitisse vix admittit' fits either")
pair("H-09", "seg_p0057_s0002",
     "Patricii discipulus Gildas Albanius, de victoria Aurelii Ambrosii librum scripsisse dicitur: quem de rebus a Josepho et sociis apud Glastonienses gestis authorem citat Foxus noster.",
     "gemini", "Gildas Albanius, a disciple of Patrick, is said to have written a book, \"On the Victory of Aurelius Ambrosius\", whom our Foxe cites as an authority concerning the deeds performed by Joseph and his companions at Glastonbury.",
     "fable", "Gildas Albanius, the disciple of Patrick, is said to have written a book on the victory of Aurelius Ambrosius, and our Foxe cites him as an authority for the deeds done by Joseph and his companions at Glastonbury.",
     [E("whom our Foxe cites", "minor")],
     "quem = Gildas (cited as authority). Placed after the title, English 'whom' attaches to Aurelius Ambrosius, so Foxe's authority becomes Ambrosius.",
     "could be classed Fluency (ambiguity) rather than Accuracy")
# ------------------------------------------------------------------ real errors, ch1
pair("H-10", "seg_p0043_s0008",
     "Diligat ipsa senem quondam: sed et illa marito Tunc quoque cum fuerit, non videatur anus.",
     "opus", "May she love him one day when he is old; but may she too, even when she shall have grown old to her husband, then likewise not seem an old woman.",
     "gemini", "May she herself love him when he is an old man: but may she also, even when she is old, not seem an old woman to her husband.",
     [E("grown old to her husband", "minor")],
     "marito (dative) goes with non videatur: may she not SEEM old TO HER HUSBAND. Opus attaches it to growing old and loses the point of the wish.")
pair("H-11", "seg_p0044_s0001",
     "Postquam bis senis ingentem fascibus annum Rexerat, asserto qui sacer orbe fuit",
     "opus", "After he had governed the mighty year with its twice-six fasces — he who was hallowed when the world had been set free",
     "gemini", "After he had ruled the great year with twelve fasces, which was sacred because the world was freed",
     [E("he who was hallowed", "minor")],
     "qui refers to annum: the great year (68/69) made sacred by the world's liberation from Nero (asserto orbe). Opus refers it to Silius.",
     "qui is masculine, so Silius is grammatically possible; the standard reading is the year")
pair("H-12", "seg_p0040_s0002",
     "Et Sophronius patriarcha Hierosolymitanus, in sermone de natali apostolorum, Paulum Hispanis et Britannis evangelium prædicasse significat",
     "gemini", "And Sophronius, patriarch of Jerusalem, in his sermon on the nativity of the apostles, indicates that Paul preached the gospel to the Spaniards and the Britons",
     "opus", "And Sophronius, patriarch of Jerusalem, in his sermon on the feast of the apostles, indicates that Paul preached the gospel to the Spaniards and the Britons",
     [E("nativity of the apostles", "minor", "Wrong-term", "Terminology")],
     "natalis of saints = their feast (heavenly birthday, i.e. martyrdom day), a liturgical term; 'nativity' = physical birth.")
pair("H-13", "seg_p0052_s0002",
     "De duodecim discipulis a B. Philippo in Britanniam missis, Malmesburiensis quidam monachus in eulogii sui libro secundo hunc in modum meminit",
     "gemini", "Concerning the twelve disciples sent into Britain by the blessed Philip, a certain monk of Malmesbury records in the second book of his eulogy in this manner",
     "fable", "Concerning the twelve disciples sent into Britain by the blessed Philip, a certain monk of Malmesbury makes mention in the second book of his \"Eulogium\" in this manner",
     [E("his eulogy", "minor", "Wrong-term", "Terminology")],
     "Eulogium is the title of a chronicle (Eulogium historiarum), cited again in p0063 and p0067. 'his eulogy' turns it into a speech of praise.")


# ------------------------------------------------------------------ SIMULATED errors modeled on the real ones
# Base = a real model rendering judged clean (verbatim); stimulus = base + ONE minimal edit reproducing a
# real error MECHANISM. Negative = the unedited base. Every diff must fall inside the keyed span.
def mark_diff(ref, stim):
    import difflib
    a, b = ref.split(), stim.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal":
            out += b[j1:j2]
        else:
            if i2 > i1:
                out.append("~~" + " ".join(a[i1:i2]) + "~~")
            if j2 > j1:
                out.append("**" + " ".join(b[j1:j2]) + "**")
    return " ".join(out)


def _diff_in_span(base, stim, spans):
    import difflib
    a, b = base.split(), stim.split()
    cover = set()
    for s in spans:
        if s.startswith("(missing)"):
            continue
        i0 = len(stim[:stim.index(s)].split())
        cover |= set(range(max(0, i0 - 1), i0 + len(s.split()) + 1))
    miss = any(s.startswith("(missing)") for s in spans)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        if op == "delete" and miss:
            continue
        if not set(range(j1, max(j2, j1 + 1))) <= cover:
            return False
    return True


def sim(sid, unit, latin, base_model, base, stim, exp, mechanism, modeled_on, why):
    chk(unit, base_model, latin, base)
    assert stim != base
    for e in exp:
        if not e["span"].startswith("(missing)"):
            assert e["span"] in stim, f"{sid}: span not in stimulus"
    assert _diff_in_span(base, stim, [e["span"] for e in exp]), f"{sid}: edit outside keyed span"
    common = dict(pair_id=sid, unit=unit, latin=latin, origin="simulated (claude-opus-5.5) on real base",
                  mechanism=mechanism, modeled_on=modeled_on)
    rows.append({**common, "item_id": sid, "is_error_stimulus": True, "stimulus_english": stim,
                 "rendered_by": f"{MODEL[base_model]} + planted edit", "expected": exp, "rationale": why,
                 "contestable": "", "counterpart_english": base, "counterpart_by": MODEL[base_model],
                 "diff": mark_diff(base, stim)})
    rows.append({**common, "item_id": sid + "__neg", "is_error_stimulus": False, "stimulus_english": base,
                 "rendered_by": MODEL[base_model], "expected": [],
                 "rationale": "Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.",
                 "contestable": "", "counterpart_english": stim, "counterpart_by": "planted"})


SIM = [
    ("S-01", "seg_p0055_s0002", "et quod tres reges pagani ipsis duodecim, ad eorum sustenementum, duodecim portiones terræ dederunt.",
     "opus", "and that three pagan kings gave those twelve men twelve portions of land for their sustenance",
     "and that three pagan kings each gave those twelve men twelve portions of land for their sustenance",
     [E("each gave", "major")], "distributive scope", "H-01",
     "No distributive in the Latin: the three kings together gave twelve portions (the Twelve Hides). 'each' makes thirty-six."),
    ("S-02", "seg_p0060_s0002", "quum adversus Hispanos, Scotos et Gallos coram Martino V. ab Anglis renovata esset hæc controversia.",
     "opus", "when this controversy had been revived by the English against the Spaniards, the Scots, and the French before Martin V.",
     "when this controversy had been revived by the Spaniards, the Scots, and the French against the English before Martin V.",
     [E("by the Spaniards, the Scots, and the French against the English", "major")], "who did what to whom", "H-02",
     "ab Anglis = by the English (agent); adversus Hispanos ... = against the Spaniards. The swap reverses who renewed the dispute."),
    ("S-03", "seg_p0060_s0004", "Ille ergo qui dicit, probat",
     "opus", "He therefore who makes the assertion must prove it",
     "He therefore who denies the assertion must prove it",
     [E("denies the assertion", "major")], "who did what to whom", "H-02",
     "qui dicit = he who asserts (the legal maxim). The next sentence ('the burden of proof does not rest upon the one who denies') shows the reversal is wrong."),
    ("S-04", "seg_p0064_s0001", "non quidem in muro, sed in Caiphæ carcere detentum",
     "opus", "was held not indeed within a wall but in the prison of Caiaphas",
     "was held not indeed within a wall but in the prison of Pilate",
     [E("the prison of Pilate", "major", "Entity")], "substitution inside the legend", "H-03",
     "in Caiphæ carcere = Caiaphas' prison (Harding's version). Pilate is the natural Passion-story substitute."),
    ("S-05", "seg_p0066_s0007", "et quod attulerit secum duo vasa argentea non grandia, in quibus erat de sanguine et aqua sacratissima, quæ profluxerat de latere Christi mortui.",
     "opus", "and that he brought with him two small silver vessels, in which was some of the most sacred blood and water that had flowed from the side of the dead Christ.",
     "and that he brought with him two small silver vessels, in which was some of the most sacred blood and water that had flowed from the hands of the dead Christ.",
     [E("from the hands of the dead Christ", "major")], "substitution inside the legend", "H-03",
     "de latere = from the side (the spear wound, Jn 19:34, the source of 'blood and water')."),
    ("S-06", "seg_p0054_s0001", "Isti viri certe divino spiritu aﬄati, cum a rege parum terræ ad inhabitandum (proxime Welliam oppidum, circiter millia passuum quatuor) dono accepissent, ibi novæ religionis prima jecerunt fundamenta",
     "gemini", "These men, certainly inspired by the divine spirit, having received as a gift from the king a small piece of land to inhabit (near the town of Wells, about four miles away), laid the first foundations of the new religion there",
     "These men, certainly inspired by the divine spirit, in order to receive as a gift from the king a small piece of land to inhabit (near the town of Wells, about four miles away), laid the first foundations of the new religion there",
     [E("in order to receive", "major")], "clause relation (circumstance vs purpose)", "H-04",
     "cum + pluperfect subjunctive (accepissent) = having received: the gift came first. A purpose clause reverses the sequence."),
    ("S-07", "seg_p0035_s0004", "Quod profecto divina providentia ita tunc Cæsaris sensibus ingessit, ut absque ullo obstaculo, in ipsis duntaxat initiis Evangelii sermo usquequaque percurreret.",
     "gemini", "Divine providence surely instilled this into Caesar's mind at that time, so that without any obstacle, at the very beginnings of the Gospel, its word might run everywhere.",
     "Divine providence surely instilled this into Caesar's mind at that time, because without any obstacle, at the very beginnings of the Gospel, its word ran everywhere.",
     [E("because without any obstacle, at the very beginnings of the Gospel, its word ran everywhere", "major")], "clause relation (result vs cause)", "H-04",
     "ita ... ut + subjunctive = so that (result): providence acted in order that the word could spread. 'because' makes the spread the cause."),
    ("S-08", "seg_p0060_s0005", "Potest autem dici quod eductus cum a prædicatione non cessaret, iterum sit ab ipsis Judæis inclusus.",
     "gemini", "But it can be said that, having been brought out, since he did not cease from preaching, he was again enclosed by the Jews themselves.",
     "But it can be said that, having been brought out, although he did not cease from preaching, he was again enclosed by the Jews themselves.",
     [E("although", "major")], "cum-clause type (causal vs concessive)", "v1 cum->when",
     "cum + subjunctive is causal here: he was re-imprisoned BECAUSE he kept preaching. 'although' breaks the explanation."),
    ("S-10", "seg_p0066_s0003", "Quem habuerit eventum ista inquisitio, non invenio: ab his tamen qui Glastoniense monasterium viderunt est proditum, et sacellum ibi Josephi nomini dicatum, et tumulum etiam positum fuisse, hoc inscriptum epitaphio.",
     "opus", "What outcome that inquiry had I do not find; yet it has been reported by those who saw the monastery of Glastonbury that a chapel there was dedicated to the name of Joseph, and that a tomb was also set up, inscribed with this epitaph.",
     "What outcome that inquiry had I do not find; yet it has been reliably reported by those who saw the monastery of Glastonbury that a chapel there was dedicated to the name of Joseph, and that a tomb was also set up, inscribed with this epitaph.",
     [E("reliably", "minor", "Addition")], "imported stance", "H-05",
     "Nothing in the Latin vouches for the report (est proditum = it has been handed down). 'reliably' adds an endorsement Ussher does not give."),
    ("S-12", "seg_p0049_s0001", "Nam præterquam quod Isidorus in hoc ipso opere, capite secundo et octogesimo et in officio Toletano, quod Gothicum et Mozarabum vulgo appellatur",
     "fable", "For besides the fact that Isidore, in this very work, at chapter 82, and in the Toledan office, which is commonly called the Gothic and Mozarabic",
     "For besides the fact that Isidore, in this very work, at chapter 82, and in the Toledan council, which is commonly called the Gothic and Mozarabic",
     [E("the Toledan council", "minor", "Wrong-term", "Terminology")], "technical/liturgical term", "H-12",
     "officium = the liturgical office (the Mozarabic rite). The Councils of Toledo are famous, which makes 'council' a plausible substitute."),
    ("S-17", "seg_p0053_s0001", "Monachi tamen ibidem aliam prætendunt fundationem a rege Arvirago (filio Kimbelini regis Britonum, in cujus tempore Christus Jesus de Maria virgine natus fuit)",
     "opus", "The monks there, however, allege another foundation, by king Arviragus (son of Kimbelinus king of the Britons, in whose time Christ Jesus was born of the Virgin Mary)",
     "The monks there, however, allege another foundation, by king Arviragus (in whose time Christ Jesus was born of the Virgin Mary, son of Kimbelinus king of the Britons)",
     [E("in whose time Christ Jesus was born of the Virgin Mary, son of Kimbelinus king of the Britons", "major")], "relative-pronoun antecedent", "H-11",
     "cujus refers to Kimbelinus (Christ was born in Cymbeline's reign). Moving the clause attaches it to Arviragus and shifts the chronology a generation."),
    ("S-21", "seg_p0066_s0005", "observatio festi S. Josephi ad VI. Calendas Augusti",
     "opus", "the observance of the feast of St. Joseph on the sixth day before the Kalends of August",
     "the observance of the feast of St. Joseph on the sixth day after the Kalends of August",
     [E("after the Kalends of August", "major")], "technical/calendar term", "H-12",
     "ad VI. Calendas = the 6th day BEFORE the Kalends (27 July); Roman dates count backwards. 'after' gives 6 August."),
    ("S-23", "seg_p0061_s0001", "adhuc tamen Hispani primo susceperunt fidem, quod probatur, quia Jacobus martyrium subiit vivente Petro.",
     "opus", "the Spaniards still received the faith first; and this is proved because James suffered martyrdom while Peter was still alive.",
     "the Spaniards still received the faith first; and this is proved because Peter suffered martyrdom while James was still alive.",
     [E("Peter suffered martyrdom while James was still alive", "major")], "who did what (ablative absolute)", "v1 them/him",
     "Jacobus ... subiit vivente Petro = James was martyred while Peter lived (ablative absolute). The swap reverses the order the argument depends on."),
    ("S-26", "seg_p0042_s0004", "Patrem vero Lini Herculanum quendam fuisse liber pontificalis asserit.",
     "opus", "The Book of the Pontiffs, however, asserts that the father of Linus was a certain Herculanus.",
     "The Book of the Pontiffs, however, asserts that Linus was the father of a certain Herculanus.",
     [E("Linus was the father of a certain Herculanus", "major")], "identification vs predication (double accusative)", "H-08",
     "Patrem Lini = the father OF LINUS (genitive); Herculanum is the predicate. The edit reverses the relationship."),
    ("S-28", "seg_p0063_s0002", "Quod et cum ipsius Josephi ætate, qui Domino passionem adeunte inter Judæos senator honoratus fuerat",
     "fable", "which agrees well both with the age of Joseph himself, who, when the Lord went to his passion, had been an honored senator among the Jews",
     "which agrees well both with the age of Joseph himself, who, after the Lord went to his passion, became an honored senator among the Jews",
     [E("after the Lord went to his passion, became", "minor")], "temporal relation (ablative absolute + pluperfect)", "H-04",
     "Domino passionem adeunte = when the Lord was going to his Passion; fuerat = had (already) been a senator. The point is that Joseph was already senior then."),
    ("S-30", "seg_p0062_s0002", "nec integra regna ab ullo apostolorum Christiana facta esse constat",
     "opus", "nor is it established that entire kingdoms were made Christian by any of the apostles",
     "nor is it established that entire kingdoms were made Christian by all of the apostles",
     [E("by all of the apostles", "major")], "quantifier scope", "H-01",
     "ab ullo = by ANY (none did). 'by all' only denies that every apostle did, which undercuts Ussher's reply."),
    ("S-33", "seg_p0059_s0001", "Verum et otio meo et lectoris patientia abutar, si nugacissima commenta, quæ ex stramentitiis ejusmodi scriptis tum ab Hardingo et Capgravio, tum in magna Glastoniensium tabula de Josepho referuntur, commemorem.",
     "opus", "But I would abuse both my own leisure and the reader's patience were I to rehearse the utterly trifling fictions concerning Joseph which are reported out of such strawy writings, whether by Harding and Capgrave or in the great Table of the Glastonbury monks.",
     "But I have abused both my own leisure and the reader's patience in rehearsing the utterly trifling fictions concerning Joseph which are reported out of such strawy writings, whether by Harding and Capgrave or in the great Table of the Glastonbury monks.",
     [E("I have abused both my own leisure and the reader's patience in rehearsing", "major")], "mood (hypothetical vs factual)", "v1 impleverat",
     "abutar ... si commemorem = I WOULD abuse ... IF I were to recount: Ussher declines to recount them. The edit says he has done so."),
    ("S-34", "seg_p0061_s0002", "Jam certum est quod si Joseph fuisset in Anglia, hoo fuisset postquam de carcere fuisset liberatus per Titum, et sic post octogesimum annum a nativitate Domini",
     "gemini", "Now it is certain that if Joseph had been in England, this would have been after he had been freed from prison by Titus, and thus after the eightieth year from the birth of the Lord",
     "Now it is certain that since Joseph had been in England, this was after he had been freed from prison by Titus, and thus after the eightieth year from the birth of the Lord",
     [E("since Joseph had been in England, this was", "major")], "mood (counterfactual vs factual)", "v1 impleverat",
     "si ... fuisset ... fuisset = contrary-to-fact: Alphonsus DENIES Joseph was in England. 'since' asserts he was."),
]
# Revision 2026-10-04: one Latin sentence per item (no simulated item may share a unit with any
# other item), and edits must read as PLAUSIBLE (no semantic nonsense). These replace the earlier
# versions of the same ids, which collided with other items' sentences or produced nonsense
# (S-16 "the Gauls understood Isidore", S-20 "our dying Redeemer ... taking his body down",
# S-25 "Vives" judging himself).
REVISED = {s[0]: s for s in [
    ("S-09", "seg_p0057_s0001", "Ex Juvenale vero constat Arviragum Domitiano imperante regem Britannorum extitisse: quum sub Vespasiano anno LXXVI. Josephus noster obiisse dicatur.",
     "gemini", "But from Juvenal it is clear that Arviragus was king of the Britons during the reign of Domitian, whereas our Joseph is said to have died under Vespasian in the year 76.",
     "But from Juvenal it is clear that Arviragus was king of the Britons during the reign of Domitian, whereas our Joseph is known to have died under Vespasian in the year 76.",
     [E("is known to have died", "minor")], "imported stance", "H-05",
     "dicatur = is SAID (reported tradition, which Ussher is testing). 'is known' turns the tradition into established fact."),
    ("S-11", "seg_p0058_s0002", "Ejus hæc producuntur verba, quæ ex variis exemplaribus descripta hic exhibemus, licet quæ legantur prorsus indigna.",
     "opus", "These words of his are put forward, which I set out here as copied from various exemplars, although they are utterly unworthy of being read.",
     "These words of his are put forward, which I set out here as copied from various examples, although they are utterly unworthy of being read.",
     [E("various examples", "minor")], "false friend", "H-06",
     "exemplaria = manuscript copies (exemplars) of a text, not 'examples'. Ussher is collating copies of Melkin's text."),
    ("S-13", "seg_p0046_s0003", "Sic igitur ille, præmissa præfatione ad Henricum Blesensem, Henrici I. regis ex Adela sorore nepotem, Wintoniensem tum episcopum et Glastoniensem abbatem, archæologiam suam ab apostolicis exorditur temporibus.",
     "gemini", "Thus, having prefixed a preface to Henry of Blois, nephew of King Henry I by his sister Adela, and at that time bishop of Winchester and abbot of Glastonbury, he begins his ancient history from apostolic times.",
     "Thus, having prefixed a preface by Henry of Blois, nephew of King Henry I by his sister Adela, and at that time bishop of Winchester and abbot of Glastonbury, he begins his ancient history from apostolic times.",
     [E("a preface by Henry of Blois", "major")], "addressee (ad) vs author", "H-07",
     "praefatione ad Henricum = a preface addressed TO Henry (Malmesbury's dedicatee). 'by' makes Henry the author."),
    ("S-14", "seg_p0040_s0001", "et post primam apologiam, cujus ipse in posteriore ad Timotheum epistola meminit, a Nerone dimissum, evangelium Christi in occidentis quoque partibus prædicavisse.",
     "opus", "and that, after his first defense — which he himself mentions in the later epistle to Timothy — having been released by Nero, he preached the gospel of Christ in the regions of the West as well.",
     "and that, after his first defense — which he himself mentions in the later epistle to Timothy — having been released under Nero, he preached the gospel of Christ in the regions of the West as well.",
     [E("released under Nero", "minor")], "agent vs circumstance", "H-07",
     "a Nerone dimissum = released BY Nero (agent: Nero himself acquitted him). 'under Nero' reduces it to a date."),
    ("S-15", "seg_p0038_s0002", "Romæ hos a sanctis apostolis episcopos ordinatos, et ad prædicandum verbum Dei in Hispanias directos esse",
     "opus", "these men were ordained bishops at Rome by the holy apostles, and were sent into Spain to preach the word of God",
     "these men were ordained bishops at Rome for the holy apostles, and were sent into Spain to preach the word of God",
     [E("for the holy apostles", "major")], "agent vs beneficiary", "H-07",
     "a sanctis apostolis ordinatos = ordained BY the apostles (the claim to apostolic consecration). 'for' leaves the ordainer unnamed."),
    ("S-16", "seg_p0048_s0002", "Quod autem de Philippi in Galliis apostolatu habet Freculphus a Malmesburiensi citatus; ex Isidori libro de patribus utriusque Testamenti ad verbum expressit.",
     "fable", "But what Freculphus, cited by Malmesbury, has concerning Philip's apostolate in the Gauls, he copied word for word from Isidore's book “On the Fathers of Both Testaments”",
     "But what Freculphus, citing Malmesbury, has concerning Philip's apostolate in the Gauls, he copied word for word from Isidore's book “On the Fathers of Both Testaments”",
     [E("citing Malmesbury", "major")], "agent vs subject (passive participle)", "H-07",
     "a Malmesburiensi citatus = cited BY Malmesbury: the 12th-c. writer quotes the 9th-c. Freculph. 'citing' reverses the dependence (and the chronology)."),
    ("S-18", "seg_p0042_s0002", "In fine posterioris ad Timotheum epistolæ, commemorantur simul ab apostolo Pudens, et Linus, et Claudia.",
     "opus", "At the end of the latter epistle to Timothy, Pudens, and Linus, and Claudia are mentioned together by the apostle.",
     "At the end of the latter epistle of Timothy, Pudens, and Linus, and Claudia are mentioned together by the apostle.",
     [E("epistle of Timothy", "major")], "addressee (ad) vs author", "H-02",
     "ad Timotheum = TO Timothy (Paul's letter). 'of Timothy' reads as a letter by Timothy, which clashes with 'by the apostle'."),
    ("S-19", "seg_p0067_s0003", "Joseph vero ab Arimathia ibidem sepultus est juxta dictam Ecclesiam [B. Mariæ] cum duabus phialis plenis de sudore Christi sanguineo, quas secum de terra sancta detulerat.",
     "opus", "Joseph of Arimathea indeed was buried there beside the said church [of the Blessed Mary], with two vials filled with the bloody sweat of Christ, which he had brought with him from the Holy Land.",
     "Joseph of Arimathea indeed was buried there beside the said church [of the Blessed Mary], with two vials filled with the bloody sweat of Christ, which had been brought to him from the Holy Land.",
     [E("which had been brought to him", "minor")], "reflexive/agent attachment", "H-10",
     "quas secum ... detulerat = which HE had brought WITH HIMSELF (secum, active). The edit has others bring them to him."),
    ("S-20", "seg_p0065_s0003", "dum tamen absque damno dilectorum nobis in Christo, abbatis et conventus dicti monasterii, et ruina ecclesiæ et domorum suarum ibidem id fieri valeat",
     "gemini", "provided, however, that this can be done without damage to our beloved in Christ, the abbot and convent of the said monastery, and without the ruin of their church and houses there",
     "provided, however, that this can be done without damage from our beloved in Christ, the abbot and convent of the said monastery, and without the ruin of their church and houses there",
     [E("without damage from our beloved in Christ", "major")], "person affected vs source", "H-10",
     "absque damno dilectorum = without loss TO the abbot and convent (objective genitive: they are protected). 'from' makes them the threat."),
    ("S-22", "seg_p0039_s0002", "In martyrologio tamen et breviario Romano, ut et in Bedæ, Usuardi, atque Adonis martyrologiis, ad Octobris diem octavum et vigesimum in Perside martyrium subiisse legitur.",
     "opus", "Yet in the Roman Martyrology and Breviary, as also in the martyrologies of Bede, Usuard, and Ado, he is recorded under the twenty-eighth day of October to have undergone martyrdom in Persia.",
     "Yet in the Roman Martyrology and Missal, as also in the martyrologies of Bede, Usuard, and Ado, he is recorded under the twenty-eighth day of October to have undergone martyrdom in Persia.",
     [E("Missal", "minor", "Wrong-term", "Terminology")], "technical/liturgical term", "H-12",
     "breviarium = the Breviary (Divine Office), where saints' lessons are read. The Missal is a different liturgical book."),
    ("S-24", "seg_p0061_s0003", "quod Joseph ab Arimathia cum duodecim sociis, aut ex persecutione Herodiana, vel præsidum Romanorum in Judæa, ad Angliam vectus est. Ibidem, quæ de Christo viderat et audierat prædicavit, et prædicando plures convertit",
     "fable", "that Joseph of Arimathea, with twelve companions, driven either by the Herodian persecution or by that of the Roman governors in Judaea, was carried over to England; there he preached what he had seen and heard concerning Christ, and by preaching converted many",
     "that Joseph of Arimathea, with twelve companions, driven either by the Herodian persecution or by that of the Roman governors in Judaea, was carried over to England; there Peter preached what he had seen and heard concerning Christ, and by preaching converted many",
     [E("there Peter preached", "major", "Entity")], "wrong referent", "v1 illo->Pudens",
     "The subject of praedicavit is still Joseph. Peter is named in the same sentence a little later (preaching at Antioch), which makes the slip plausible."),
    ("S-25", "seg_p0045_s0001", "Nerone vero summam rerum obtinente (et quidem, ut pluribus placet, sub finem imperii illius) a Paulo illa scripta est epistola, in qua Timotheum salutant Pudens et Linus et Claudia.",
     "opus", "While Nero held the supreme power (and indeed, as most hold, toward the end of his reign), Paul wrote that epistle in which Pudens, Linus, and Claudia greet Timothy.",
     "While Nero held the supreme power (and indeed, as most hold, toward the end of his reign), Paul wrote that epistle in which Pudens, Linus, and Claudia greet Paul.",
     [E("greet Paul", "major", "Entity")], "wrong referent", "v1 illo->Pudens",
     "Timotheum salutant = they greet TIMOTHY (the addressee). Paul is the writer."),
    ("S-27", "seg_p0060_s0003", "Et post non longo tempore a passione Christi, Eleutherius papa regnum Angliæ totaliter convertit ad fidem.",
     "fable", "And not long after the passion of Christ, Pope Eleutherius converted the kingdom of England wholly to the faith.",
     "And not long before the passion of Christ, Pope Eleutherius converted the kingdom of England wholly to the faith.",
     [E("not long before the passion", "major")], "temporal relation", "H-04",
     "post ... a passione = AFTER the Passion. 'before' puts a pope's conversion of England before Christ's death."),
    ("S-29", "seg_p0039_s0003", "Simonem Petrum, “ duodecim quidem annos esse versatum in oriente, viginti autem et tres annos transegisse Romæ, et in Britannia, et in civitatibus quæ sunt in occidente,” retulit alicubi Eusebius Pamphili",
     "opus", "Eusebius Pamphili reports somewhere that Simon Peter “spent twelve years in the East, but passed twenty-three years at Rome, and in Britain, and in the cities which lie in the West”",
     "Eusebius Pamphili reports somewhere that Simon Peter “spent twenty-three years in the East, but passed twelve years at Rome, and in Britain, and in the cities which lie in the West”",
     [E("spent twenty-three years in the East, but passed twelve years at Rome", "major")], "number-to-place mapping", "LITERA deity swap (v1)",
     "duodecim ... in oriente, viginti et tres ... Romae = twelve years in the East, twenty-three in Rome and the West. The swap reverses where Peter spent most of his ministry."),
    ("S-31", "seg_p0066_s0006", "Nemo tamen monachorum unquam scivit certum locum sepulchri hujus sancti, vel designavit.",
     "opus", "Yet none of the monks ever knew the exact place of this saint's burial, or pointed it out.",
     "Yet not all of the monks knew the exact place of this saint's burial, or pointed it out.",
     [E("not all of the monks knew", "major")], "negation/quantifier scope", "H-01",
     "nemo = NO ONE (none knew). 'not all' implies some did, the opposite of Good's point."),
    ("S-32", "seg_p0036_s0001", "Hinc Arnobius “ Tam velociter currit sermo ejus ut, cum per tot millia annorum in sola Judæa notus fuerit Deus, nunc intra paucos annos, nec ipsos Iɴᴅᴏs lateat a parte orientis, nec ipsos Bʀɪᴛᴏɴᴇs a parte occidentis.",
     "opus", "So swiftly does his word run that, although for so many thousands of years God was known in Judaea alone, now, within a few years, it is hidden neither from the Indians themselves in the east nor from the Britons themselves in the west.",
     "So swiftly does his word run that, because for so many thousands of years God was known in Judaea alone, now, within a few years, it is hidden neither from the Indians themselves in the east nor from the Britons themselves in the west.",
     [E("because", "minor")], "concessive vs causal", "v1 cum->when",
     "cum ... fuerit is concessive here: ALTHOUGH God was known only in Judaea for millennia, now the word reaches the ends of the earth. 'because' makes the long obscurity the cause of the spread."),
]}
for s in sorted(SIM + list(REVISED.values())):
    sim(*s)

# one Latin sentence per item: no item may share a unit or a 6-word Latin run with another,
# except the two v1 carry-overs, which are two models' real errors on the same Ussher sentence.
_ALLOWED = {frozenset({"seed_p0043_s0009_opus__illo_pudens", "seed_p0043_s0009_gemini__cum_when"})}
_per_pair = {}
for r in rows:
    _per_pair.setdefault(r["pair_id"], r)


def _sixgrams(s):
    w = re.sub(r"[^a-z ]", "", s.lower().replace("æ", "ae").replace("œ", "oe")).split()
    return {" ".join(w[k:k + 6]) for k in range(len(w) - 5)}


_ids = list(_per_pair)
for i in range(len(_ids)):
    for j in range(i + 1, len(_ids)):
        a, b = _per_pair[_ids[i]], _per_pair[_ids[j]]
        if frozenset({_ids[i], _ids[j]}) in _ALLOWED:
            continue
        assert a["unit"] != b["unit"] and not (_sixgrams(a["latin"]) & _sixgrams(b["latin"])), \
            f"Latin reused: {_ids[i]} and {_ids[j]}"

# ------------------------------------------------------------------ real but defensible divergences (hard negatives)
boundary("B-01", "seg_p0065_s0001",
         "Extat vetustus catalogus sanctorum in Anglia sepultorum Saxonice scriptus, ac Latine, a Gotcelino Bertiniano monacho Cantuariensi, Anselmi archiepiscopi diebus editus",
         "gemini", "There is an ancient catalogue of saints buried in England, written in Saxon, and published in Latin by Goscelin of Saint-Bertin, a monk of Canterbury, in the days of Archbishop Anselm",
         "Attaches Latine to editus (Goscelin published it in Latin) rather than to scriptus (written in Saxon and Latin). The punctuation permits both.")
boundary("B-02", "seg_p0063_s0001",
         "Sed temporis illam circumstantiam in nullis Anglorum annalibus expressam reperit.",
         "fable", "but one finds that circumstance of time expressed in none of the annals of the English",
         "Impersonal 'one finds' for reperit (he finds). The claim (no English annal states it) is preserved.")
boundary("B-03", "seg_p0050_s0005",
         "Regi consuluit Joseph tunc credere Christum: Arviragus renuit rex hoc, nec credit in ipsum.",
         "gemini", "Joseph then advised the king to believe in Christ: King Arviragus refused this, and does not believe in him.",
         "Historic present 'credit' kept as English present after a past verb. Literal; truth conditions preserved.")
boundary("B-04", "seg_p0047_s0003",
         "Hæc autem ita se habere, tum ex charta beati Patricii, tum ex scriptis seniorum cognoscimus.",
         "gemini", "Moreover, I know that these things are so, both from the charter of the blessed Patrick and from the writings of the elders.",
         "Authorial plural cognoscimus rendered 'I'. Standard.")
boundary("B-05", "seg_p0062_s0003",
         "Quomodo ergo ibi prædicavit, quo nondum ingressus est?",
         "opus", "How then did he preach in a place he had never entered?",
         "nondum = not yet; 'never' in a rhetorical question. Arguably a slight strengthening.")
boundary("B-06", "seg_p0058_s0003",
         "Hunc Mevinum Britannum chronographum appellat Johannes Hardingus in chronico suo poemate",
         "gemini", "John Harding calls this British chronographer Mevinus in his chronicle poem",
         "Reads Mevinum as the name Harding gives (rather than 'calls this Mevinus a British chronographer'). Both readings fit the context.")

# ------------------------------------------------------------------ v1 real seeds carried over (keys as in v1; pending the classicist)
v1in = {json.loads(l)["segment_id"]: json.loads(l) for l in (MQM / "fluent/fluent_set_input.jsonl").read_text(encoding="utf-8").splitlines()}
v1key = {json.loads(l)["segment_id"]: json.loads(l) for l in (MQM / "fluent/fluent_set_key.jsonl").read_text(encoding="utf-8").splitlines()}
for sid in ["seed_p0033_s0002_opus__them_him", "seed_p0043_s0009_opus__illo_pudens", "seed_p0043_s0009_gemini__cum_when",
            "seed_p0039_l0002_v2__in_to", "seed_p0033_s0001_opus__sonant", "seed_p0039_l0002_v0__to_western"]:
    k = v1key[sid]
    rows.append(dict(pair_id=sid, unit=sid, latin=v1in[sid]["latin_text"], origin="real-model-output (v1 seed)",
                     item_id="V1-" + sid.removeprefix("seed_"), is_error_stimulus=k["is_error_stimulus"],
                     stimulus_english=v1in[sid]["final_english"], rendered_by="v1 seed", expected=k["expected"],
                     rationale="Carried over from v1 with its v1 label (see fluent/fluent_set_combined.md). #5 in->to is CONTESTED (external review).",
                     contestable="v1 label pending the classicist", counterpart_english="", counterpart_by=""))
# natural negative for them/him: Gemini's real rendering of the same clause
chk("seg_p0033_s0002", "gemini", "Non enim separat mare eum, qui fecerat mare.", "For the sea does not separate him who made the sea.")
rows.append(dict(pair_id="seed_p0033_s0002_opus__them_him", unit="seg_p0033_s0002", latin="Non enim separat mare eum, qui fecerat mare.",
                 origin="real-model-output", item_id="V1-p0033_s0002__neg_gemini", is_error_stimulus=False,
                 stimulus_english="For the sea does not separate him who made the sea.", rendered_by=MODEL["gemini"], expected=[],
                 rationale="Gemini's real rendering of the them/him clause; gets eum right.", contestable="", counterpart_english="", counterpart_by=""))

# ------------------------------------------------------------------ write
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "runs").mkdir(exist_ok=True)
(OUT / "candidate_pool.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
(OUT / "runs/v3_input.jsonl").write_text("".join(json.dumps({"segment_id": r["item_id"], "latin_text": r["latin"], "final_english": r["stimulus_english"]}, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
(OUT / "runs/v3_key_provisional.jsonl").write_text("".join(json.dumps({"segment_id": r["item_id"], "is_error_stimulus": r["is_error_stimulus"], "source": r["origin"], "expected": r["expected"]}, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

errs = [r for r in rows if r["is_error_stimulus"]]
n_real = len([r for r in errs if r["origin"] == "real-model-output"])
n_v1 = len([r for r in errs if "v1" in r["origin"]])
n_sim = len([r for r in errs if r["origin"].startswith("simulated")])
W = ["# Fluent-misgloss set v3: HARD set (for the classicist)", "",
     "**Status: PRE-ADJUDICATION.** Two kinds of grammar-dependent error, all on Ussher ch1/ch2:",
     f"- **Real (H-, V1-):** {n_real + n_v1} errors a model actually made, trimmed verbatim from the drafts. Each is paired with another model's real rendering of the same Latin that gets it right.",
     f"- **Simulated (S-):** {n_sim} errors. Each takes a real model rendering judged clean and makes ONE minimal edit reproducing the *mechanism* of a real error (`modeled_on`). The unedited rendering is the paired negative, and the change is marked ~~removed~~ **added**.",
     "Claude (Opus 5.5) found the real errors and wrote the simulated edits, so the set leans towards errors a Claude-family reader can see. Report results split by origin.", "",
     f"- Error items: **{len(errs)}** ({n_real} real new + {n_v1} real from v1 + {n_sim} simulated)",
     f"- Negatives: **{len(rows) - len(errs)}**: paired correct/base renderings, 6 real-but-defensible divergences (B-), and the v1 hard negatives", "",
     "At Paul's request (2026-10-04), Gemini and JEV were run on this set as a PROVISIONAL baseline against Claude's unadjudicated key.",
     "The results are **withheld from you** until you've frozen the key. Please don't look in `fluent_v3/runs/`. No item will be edited in response to judge output.", "",
     "For each error: `[ ] accept` `[ ] accept, change:` `[ ] reject: not an error (the Latin permits it)`. For each negative: `[ ] clean` `[ ] has an error:`.",
     "Items marked **contestable** are the reason this set exists; please rule on them explicitly.", ""]
for r in rows:
    W += ["---", "", f"### {r['item_id']}  ·  `{r['unit']}`  ·  rendered by {r['rendered_by']}", "", f"**Latin:** {r['latin']}", "",
          f"**English (stimulus):** {r['stimulus_english']}", ""]
    if r["is_error_stimulus"]:
        if r.get("diff"):
            W += [f"**Change vs real base ({r['counterpart_by']}):** {r['diff']}", "",
                  f"*Mechanism:* {r['mechanism']} (modeled on {r['modeled_on']})", ""]
        W += ["**Proposed MQM:**"] + [f"- `{e['span']}` · {e['dimension']} / {e['error_type']} / **{e['severity']}**" for e in r["expected"]]
        W += ["", f"**Why the Latin forces it:** {r['rationale']}"]
        if r["contestable"]:
            W += ["", f"**Contestable:** {r['contestable']}"]
        if r["counterpart_english"] and not r.get("diff"):
            W += ["", f"*Correct counterpart ({r['counterpart_by']}):* {r['counterpart_english']}"]
        W += ["", "`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`", ""]
    else:
        W += [f"**Expected:** no error. {r['rationale']}"]
        if r["contestable"]:
            W += ["", f"**Contestable:** {r['contestable']}"]
        W += ["", "`[ ] clean` `[ ] has an error:` ______", ""]
(OUT / "worksheet.md").write_text("\n".join(W), encoding="utf-8")
print(f"{len(rows)} items: {len(errs)} errors, {len(rows) - len(errs)} negatives")
