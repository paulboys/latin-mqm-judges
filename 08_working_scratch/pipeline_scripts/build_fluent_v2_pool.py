"""build_fluent_v2_pool.py — candidate pool for the fluent-misgloss set v2 (The classicist adjudicates).

Writes 04_translation_work/ab/antiquitates_ch2/mqm/fluent_v2/:
  candidate_pool.jsonl   one row per stimulus (errors + negatives), pre-adjudication
  worksheet.md           the classicist's adjudication sheet (errors + written negatives full; golds skim)

Groups
  U-P  Ussher ch2, error PLANTED (by Claude) into Baker 1930's English; negative = Baker sentence.
  U-R  Ussher ch2, REAL error in Baker 1930 (human translator); negative = Claude-corrected Baker.
  L-P  LITERA Classical TestData, error PLANTED (by Claude) into the LITERA gold; negative = gold.
  U-V / L-V  meaning-preserving rewrites (hard negatives that test over-flagging).

Provenance guard: every Latin passage must be a substring of its source segment, and every
Baker/LITERA reference a substring of the source English (compared letters-only, so OCR
spacing/punctuation fixes are allowed but wording changes are not), unless marked rejoined.

Contains excerpts of Baker's 1930 English translation of ch. 2 (used as reference translations).
Items deliberately avoid the 8 LITERA sentences already in fluent/ v1.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MQM = ROOT / "04_translation_work/ab/antiquitates_ch2/mqm"
OUT = MQM / "fluent_v2"
AUTHOR = "claude-opus-5.5"


def _letters(s):
    return re.sub(r"[^a-z]", "", s.lower().replace("æ", "ae").replace("œ", "oe"))


baker = {}
for l in (MQM / "baker_segments.jsonl").read_text(encoding="utf-8").splitlines():
    d = json.loads(l)
    baker[d["segment_id"]] = (d["latin_text"], d["translation_history"][0]["english"])
litera = {}
for i, l in enumerate((ROOT / "09_analysis/external_corpora/litera/TestData.jsonl").read_text(encoding="utf-8").splitlines()):
    d = json.loads(l)["data"][0]
    litera[f"T{i:04d}"] = (d["latin"], d["english"])


def check(src, latin, english, rejoined=False):
    la, en = (baker if src.startswith("seg_") else litera)[src]
    assert _letters(latin) in _letters(la), f"{src}: Latin not in source"
    if english is not None and not rejoined:
        assert _letters(english) in _letters(en), f"{src}: reference English not in source"


def E(span, sev, etype="Mistranslation", dim="Accuracy"):
    return {"span": span, "dimension": dim, "error_type": etype, "severity": sev}


rows = []


def planted(pid, group, src, latin, gold, stim, exp, why, rejoined=False):
    check(src, latin, gold, rejoined)
    assert stim != gold
    for e in exp:
        if not e["span"].startswith("(missing)"):
            assert e["span"] in stim, f"{pid}: span not in stimulus"
    ref_src = "baker-1930" if group == "U-P" else "litera-classical-testdata"
    if rejoined:
        ref_src += " (rejoined across misaligned segments)"
    rows.append(dict(item_id=pid, pair_id=pid, group=group, source_ref=src, is_error_stimulus=True,
                     latin=latin, stimulus_english=stim, reference_english=gold, reference_source=ref_src,
                     expected=exp, rationale=why, error_author=AUTHOR, adjudication="full"))
    rows.append(dict(item_id=pid + "__ref", pair_id=pid, group=group, source_ref=src, is_error_stimulus=False,
                     latin=latin, stimulus_english=gold, reference_english=gold, reference_source=ref_src,
                     expected=[], rationale="Published reference used as-is (hard negative).",
                     error_author=None, adjudication="skim"))


def real(pid, src, latin, baker_en, corrected, exp, why, rejoined=False):
    check(src, latin, baker_en, rejoined)
    for e in exp:
        assert e["span"] in baker_en, f"{pid}: span not in Baker"
    rows.append(dict(item_id=pid, pair_id=pid, group="U-R", source_ref=src, is_error_stimulus=True,
                     latin=latin, stimulus_english=baker_en, reference_english=corrected,
                     reference_source=f"{AUTHOR} correction of Baker (UNREVIEWED)",
                     expected=exp, rationale=why, error_author="baker-1930 (human translator)",
                     adjudication="full"))
    rows.append(dict(item_id=pid + "__ref", pair_id=pid, group="U-R", source_ref=src, is_error_stimulus=False,
                     latin=latin, stimulus_english=corrected, reference_english=corrected,
                     reference_source=f"{AUTHOR} correction of Baker (UNREVIEWED)", expected=[],
                     rationale="Claude-written correction; needs full review before use as a negative.",
                     error_author=None, adjudication="full"))


def variant(pid, group, src, latin, ref, var, why, rejoined=False):
    check(src, latin, ref, rejoined)
    rows.append(dict(item_id=pid, pair_id=pid, group=group, source_ref=src, is_error_stimulus=False,
                     latin=latin, stimulus_english=var, reference_english=ref,
                     reference_source="baker-1930" if group == "U-V" else "litera-classical-testdata",
                     expected=[], rationale=why, error_author=None, variant_author=AUTHOR,
                     adjudication="full"))


# ---------------------------------------------------------------- U-P: planted into Baker
planted("U-P-01", "U-P", "seg_p0046_s0003",
        "Sic igitur ille, præmissa præfatione ad Henricum Blesensem, Henrici I. regis ex Adela sorore nepotem, Wintoniensem tum episcopum et Glastoniensem abbatem, archæologiam suam ab apostolicis exorditur temporibus.",
        "Thus, then, with a preliminary preface to Henry of Blois—nephew to King Henry I by his sister Adela—then Bishop of Winchester and Abbot of Glaston, he commences his archæology from Apostolic times.",
        "Thus, then, with a preliminary preface to Henry of Blois—nephew to King Henry I by his daughter Adela—then Bishop of Winchester and Abbot of Glaston, he commences his archæology from Apostolic times.",
        [E("by his daughter Adela", "major")],
        "ex Adela sorore = by (his) sister Adela. 'daughter' misstates the genealogy and makes 'nepotem' (nephew) incoherent.")
planted("U-P-02", "U-P", "seg_p0047_s0001",
        "Postea etiam alii duo reges pagani successive comperta vitæ eorum sanctimonia, unicuique eorum unam portionem terræ concesserunt",
        "Moreover, afterwards, two other pagan kings observing their pious mode of life successively granted to each of them a portion of land",
        "Moreover, afterwards, three other pagan kings observing their pious mode of life successively granted to each of them a portion of land",
        [E("three other pagan kings", "major")],
        "alii duo = two others. The tradition counts three kings in all (the first + two); 'three other' makes four.")
planted("U-P-03", "U-P", "seg_p0047_s0002",
        "Prædicti itaque sancti in eodem deserto conversantes, post pusillum temporis visione archangeli Gabrielis admoniti sunt ecclesiam in honore sanctæ Dei genitricis et virginis Mariæ, in loco cœlitus eis demonstrato construere.",
        "And thus the said saints, dwelling together in this desert place, were in a very short time inspired by a vision of the Archangel Gabriel to build a church in honour of the Holy Mother of God and Virgin Mary in a place divinely revealed to them",
        "And thus the said saints, dwelling together in this desert place, were in a very short time inspired by a vision of the Archangel Michael to build a church in honour of the Holy Mother of God and Virgin Mary in a place divinely revealed to them",
        [E("Archangel Michael", "major", "Entity")],
        "archangeli Gabrielis. Trap: the Eulogium quoted later in ch2 (p0052) names Michael, so the swap is plausible to a reader who knows the chapter.")
planted("U-P-04", "U-P", "seg_p0047_s0003",
        "Duodecim igitur sancti sæpius memorati, in eodem loco Deo et beatæ virgini devota exhibentes obsequia; vigiliis, jejuniis et orationibus vacantes, ejusdem virginis auxilio ac visione (ut credi pium est) in omnibus necessitatibus refocillabantur.",
        "Thereupon the XII saints so frequently mentioned, paying devout homage in that same spot to God and the Blessed Virgin; devoting themselves to vigils, fasts, and prayers, were constantly sustained (as it is pious to believe) in all their needs by the same Virgin's help and presence.",
        "Thereupon the XII saints so frequently mentioned, paying devout homage in that same spot to God and the Blessed Virgin; devoting themselves to vigils, fasts, and prayers, were constantly sustained (as is well attested) in all their needs by the same Virgin's help and presence.",
        [E("as is well attested", "major")],
        "ut credi pium est = as it is pious to believe: marks the claim as devotional belief. 'as is well attested' asserts evidence the Latin disclaims.")
planted("U-P-05", "U-P", "seg_p0047_s0003",
        "Hæc autem ita se habere, tum ex charta beati Patricii, tum ex scriptis seniorum cognoscimus.",
        "That these things are so we learn both from the Charter of the Blessed Patrick and from the Writings of the Elders.",
        "That these things are so we learn both from the Charter of the Blessed Augustine and from the Writings of the Elders.",
        [E("Blessed Augustine", "major", "Entity")],
        "charta beati Patricii = the (forged) Charter of St Patrick, discussed again at p0055. Augustine is a plausible English-church substitute.")
planted("U-P-06", "U-P", "seg_p0048_s0001",
        "senior quidam ex monachis interrogavit eum: quo genus, unde domo? Respondit, Normannum, e Britanniæ monasterio quod Glastingeia dicitur, monachum.",
        "a certain Elder of the monks enquired of him: of what race he was, and where he dwelt? He replied, a Norman, a monk of a monastery in Britain called Glastingeia.",
        "a certain Elder of the monks enquired of him: of what race he was, and where he dwelt? He replied, a Briton, a monk of a monastery in Britain called Glastingeia.",
        [E("a Briton", "major")],
        "Normannum = a Norman. 'Briton' is the natural guess for a Glastonbury monk, which is what makes the swap fluent.")
planted("U-P-07", "U-P", "seg_p0048_s0001",
        "ista in Gallia, illa in Britannia uno eodem tempore exortæ, a summo et magno pontifice consecratæ. Uno tamen gradu illa supereminet: Roma etenim secunda vocatur.",
        "this in Gaul, that in Britain, founded at one and the same time and consecrated by the Most High and Mighty Pontiff. Nevertheless, in one respect that one is supereminent: since it is called Rome the Second.",
        "this in Gaul, that in Britain, founded at one and the same time and consecrated by the Most High and Mighty Pontiff. Nevertheless, in one respect this one is supereminent: since it is called Rome the Second.",
        [E("this one is supereminent", "major")],
        "ista/illa are fixed in the same sentence as Gaul (St Denis) / Britain (Glastonbury); 'illa supereminet' = the British church excels. 'this one' hands the pre-eminence to St Denis.")
planted("U-P-08", "U-P", "seg_p0050_s0002",
        "Josephes ex Joseph genitus patrem comitatur; His aliisque decem jus Glastoniæ propriatur.",
        "Josephes the son of Joseph accompanies his Father: To them and to the other ten the freedom of Glaston is granted.",
        "Josephes the son of Joseph accompanies his Father: To them and to the other eleven the freedom of Glaston is granted.",
        [E("the other eleven", "major")],
        "decem = ten; two named + ten = the twelve of the tradition. 'eleven' makes thirteen.")
planted("U-P-09", "U-P", "seg_p0050_s0003",
        "Joseph cum sociis jussit transire Philippus Ad terram Britonum divinum promere verbum.",
        "Philip ordered Joseph to cross with his companions to the land of Britain to preach the divine Word.",
        "Joseph ordered Philip to cross with his companions to the land of Britain to preach the divine Word.",
        [E("Joseph ordered Philip", "major")],
        "Philippus is nominative (subject of jussit); Joseph is the accusative subject of transire. Verse word order (Joseph first) makes the inversion look natural.")
planted("U-P-10", "U-P", "seg_p0050_s0005",
        "Regi consuluit Joseph tunc credere Christum: Arviragus renuit rex hoc, nec credit in ipsum.",
        "Joseph then counselled the King to believe in Christ: King Arviragus refused this, nor did he believe in Him.",
        "Joseph then counselled the King to believe in Christ: King Arviragus accepted this, and believed in Him.",
        [E("accepted this, and believed in Him", "major")],
        "renuit = refused; nec credit = nor does he believe. Polarity reversed.")
planted("U-P-11", "U-P", "seg_p0052_s0002",
        "Quibus rex Arviragus, licet paganus, ne ulterius laborarent, duodecim hidas terræ eis contulit in insula Avalloniæ, quæ nunc dicitur Glastonia.",
        "On whom the King Arviragus, although a pagan, in order that they might toil no longer, conferred XII hides of land in the Isle of Avalon which is now called Glastonia.",
        "On whom the King Arviragus, although a pagan, in order that they might toil no longer, conferred XII hides of land in the Isle of Avalon which was formerly called Glastonia.",
        [E("which was formerly called Glastonia", "minor")],
        "quae nunc dicitur = which is now called. Reverses which name is current; the main claim (the grant) is untouched -> minor.")
planted("U-P-12", "U-P", "seg_p0052_s0002",
        "duodecim discipuli venerunt in Britanniam majorem, missi a beato Philippo apostolo ad verbum Dei ibidem prædicandum: quorum primus fuit Joseph ab Arimathia, qui Jesum Christum sepelivit.",
        "twelve disciples came into Greater Britain sent thither by the Blessed Apostle Philip to preach the word of God: of whom the chief was Joseph of Arimathea who buried Jesus Christ.",
        "twelve disciples came into Greater Britain sent thither by the Blessed Apostle Philip to preach the word of God: of whom the chief was Joseph of Arimathea who baptized Jesus Christ.",
        [E("who baptized Jesus Christ", "major")],
        "sepelivit = buried. Joseph's identifying deed (Mt 27:57-60) is the basis of the whole legend.")
planted("U-P-13", "U-P", "seg_p0053_s0001",
        "Monachi tamen ibidem aliam prætendunt fundationem a rege Arvirago (filio Kimbelini regis Britonum, in cujus tempore Christus Jesus de Maria virgine natus fuit)",
        "Nevertheless the monks there allege another foundation by King Arviragus (son of Kimbeline, King of the Britons, in whose time Christ Jesus was born of the Virgin Mary)",
        "Nevertheless the monks there allege another foundation by King Arviragus (father of Kimbeline, King of the Britons, in whose time Christ Jesus was born of the Virgin Mary)",
        [E("father of Kimbeline", "major")],
        "filio Kimbelini = son of Kymbeline. Reversing the kinship also breaks the chronology the parenthesis supplies.")
planted("U-P-14", "U-P", "seg_p0053_s0001",
        "Qui Glasconiam venientes, acceperunt possessionem hidarum duodecim, ab Arvirago nobili rege Britanniæ, adhuc paganicis erroribus involuto.",
        "Who, coming to Glastonia, received possession of xii hides from Arviragus, the noble King of Britain, though still steeped in pagan errors.",
        "Who, coming to Glastonia, received possession of xii hides from Arviragus, the noble King of Britain, though already freed from pagan errors.",
        [E("though already freed from pagan errors", "major")],
        "adhuc ... involuto = still entangled. The reversal makes Arviragus a convert, which is exactly the point in dispute (Harding vs the other sources, p0056).")
planted("U-P-15", "U-P", "seg_p0053_s0002",
        "Cumque fidem Christi constanter prædicarent, rex barbarus cum gente sua tam nova audiens et inconsueta, omnino prædicationi eorum consentire renuebat, nec paternas traditiones commutare volebat",
        "And though they steadfastly preached the faith of Christ, the barbarian King with his people, hearing such new and unaccustomed things altogether refused to accept their preaching nor was he willing to depart from the traditions of his fathers",
        "And though they steadfastly preached the faith of Christ, the barbarian King with his people, hearing such new and unaccustomed things altogether refused to accept their preaching",
        [E("(missing) nor was he willing to depart from the traditions of his fathers", "minor", "Omission")],
        "Dropped clause is a second, partly redundant reason for the refusal; the main claim survives -> minor. Clean-boundary omission.")
planted("U-P-16", "U-P", "seg_p0055_s0001",
        "Nam, ut annalium scriptores prodiderunt, in Britanniam transmigravit; ibique et cultum Christi docuit, et multa sui monumenta in valle Avilonis, quæ adhuc visuntur, reliquit.",
        "For, as the writers of the annals shewed, he migrated into Britain; and there he both taught the worship of Christ and left many memorials of himself in the Vale of Avalon, which can there be seen.",
        "For, as the writers of the annals shewed, he migrated into Britain; and there he both taught the worship of Christ and left many memorials of himself in the Vale of Avalon, which can no longer be seen.",
        [E("which can no longer be seen", "major")],
        "quae adhuc visuntur = which are still seen. Negation removes the claimed surviving evidence.")
planted("U-P-17", "U-P", "seg_p0058_s0001",
        "Johannes Capgravius, in vita Josephi, his alium etiam testem addit Melkinum, quem ante Merlinum fuisse ait.",
        "John Capgrave, also, in his Life of Joseph, to these adds another witness, Melkinus, who he says was before Merlin.",
        "John Capgrave, also, in his Life of Joseph, to these adds another witness, Melkinus, who he says came after Merlin.",
        [E("came after Merlin", "major")],
        "ante Merlinum = before Merlin. Capgrave's claim is priority (an older witness).",
        rejoined=True)
planted("U-P-18", "U-P", "seg_p0060_s0003",
        "Et post non longo tempore a passione Christi, Eleutherius papa regnum Angliæ totaliter convertit ad fidem.",
        "And, afterwards, not a long time after the Passion of Christ, Pope Eleutherius converted the whole of the kingdom of England to the faith.",
        "And, afterwards, not a long time after the Passion of Christ, Pope Gregory converted the whole of the kingdom of England to the faith.",
        [E("Pope Gregory", "major", "Entity")],
        "Eleutherius (2nd c., the Lucius legend). Gregory the Great is the famous pope of the English conversion, so the swap reads naturally.")
planted("U-P-19", "U-P", "seg_p0061_s0001",
        "Scriptum est enin de Herode, quod occidit Jacobum gladio, et apposuit ut apprehenderet Petrum, Actuum capite duodecimo. Sed constat, quod Petrus passus est sub Nerone.",
        "For it is written of Herod, that he slew James with the sword, and had the intention to apprehend Peter, Chapter XII of the Acts. But it is well known that Peter suffered under Nero.",
        "For it is written of Herod, that he slew James with the sword, and had the intention to apprehend Peter, Chapter XII of the Acts. But it is well known that Peter suffered under Domitian.",
        [E("under Domitian", "major", "Entity")],
        "sub Nerone. The next sentence's arithmetic uses Nero's date, so the swap breaks the argument.")
planted("U-P-20", "U-P", "seg_p0061_s0002",
        "Nero autem fuit prope annum Domini LIV. et Titus fuit prope annum Domini LXXX.",
        "Nero, moreover, was about the year of Our Lord 54 and Titus about the year 80.",
        "Nero, moreover, was about the year of Our Lord 64 and Titus about the year 80.",
        [E("64", "major")],
        "LIV = 54. Alphonsus' argument is date arithmetic, so a changed numeral alters the reasoning.")
planted("U-P-21", "U-P", "seg_p0061_s0002",
        "Hæc ad patres Basileensis concilii Alphonsus Garsias: in quibus quædam sunt levia admodum, nonnulla etiam oppido ridicula.",
        "Thus Alphonsus Garcias to the Fathers at the Council of Basle: wherein some things are wholly trivial, not a few exceedingly ridiculous.",
        "Thus Alphonsus Garcias to the Fathers at the Council of Constance: wherein some things are wholly trivial, not a few exceedingly ridiculous.",
        [E("Council of Constance", "major", "Entity")],
        "Basileensis concilii. Constance is the other council in the same passage (p0059), so the swap is plausible.")
planted("U-P-22", "U-P", "seg_p0062_s0002",
        "Nam nec totum regnum Hispaniæ a Jacobo conversum fuisse ipsi Hispani dicent; nec integra regna ab ullo apostolorum Christiana facta esse constat: et de antiquitate, non de universalitate susceptionis fidei instituta est quæstio.",
        "For neither do the Spanish themselves say that the whole kingdom of Spain was converted by James; nor is it established that whole kingdoms were made Christian by any one of the Apostles: and, moreover, the question at issue concerns the antiquity, not the universality, of the reception of the faith.",
        "For neither do the Spanish themselves say that the whole kingdom of Spain was converted by James; nor is it established that whole kingdoms were made Christian by any one of the Apostles: and, moreover, the question at issue concerns the universality, not the antiquity, of the reception of the faith.",
        [E("the universality, not the antiquity", "major")],
        "de antiquitate, non de universalitate. The swap inverts Ussher's rebuttal: the dispute is about who was first, not how complete.")
planted("U-P-23", "U-P", "seg_p0062_s0003",
        "A Tito enim, anno æræ Christianæ (non octogesimo sed) septuagesimo eversam esse Hierosolymam certum est",
        "For it is certain that Jerusalem was destroyed by Titus in the 70th year (not the 80th) of the Christian era",
        "For it is certain that Jerusalem was destroyed by Vespasian in the 70th year (not the 80th) of the Christian era",
        [E("by Vespasian", "major", "Entity")],
        "A Tito. Vespasian was emperor in 70, so the swap is a plausible conflation.")
planted("U-P-24", "U-P", "seg_p0063_s0001",
        "Sed temporis illam circumstantiam in nullis Anglorum annalibus expressam reperit.",
        "But in no English annals does he find that express circumstance as to time.",
        "But in many English annals he finds that express circumstance as to time.",
        [E("in many English annals he finds", "major")],
        "in nullis = in none. Reversal turns Ussher's rebuttal of Eysengrein into support.")
planted("U-P-25", "U-P", "seg_p0050_s0004",
        "Fert hos camisia qui promissum tenuerunt: Navigio ceteri terræ mox applicuerunt.",
        "His garment bears those who held the promise: The others soon afterwards brought their ship to land.",
        "His garment bears those who held the promise: The others long afterwards brought their ship to land.",
        [E("long afterwards", "minor")],
        "mox = soon. Timing detail in doggerel verse; limited impact -> minor.")
planted("U-P-26", "U-P", "seg_p0066_s0006",
        "Reconditum abditissime dixerunt, vel ibi, vel in monte, qui monti acuto vicinus, et cui nomen Hamden-hill",
        "They say that it was most carefully concealed, either there, or on a mount, which is in the vicinity of a pointed mountain, and the name of which is Hamden-hill",
        "They say that it was most carefully concealed on a mount, which is in the vicinity of a pointed mountain, and the name of which is Hamden-hill",
        [E("(missing) either there, or", "minor", "Omission")],
        "vel ibi, vel in monte = either there or on a hill. Dropping one alternative turns an uncertain report into a single location; peripheral -> minor.")
planted("U-P-27", "U-P", "seg_p0064_s0001",
        "Johannes Balæus, Ossoriensis aliquando apud Hibernos episcopus, eodem illo anno ex vita hac migrasse eum scribit.",
        "John Bale, sometime Bishop of Ossory in Ireland, writes that he departed this life in that same year.",
        "John Bale, sometime Bishop of Ossory in Wales, writes that he departed this life in that same year.",
        [E("in Wales", "minor", "Entity")],
        "apud Hibernos = among the Irish. Peripheral identifying detail -> minor.")

# ---------------------------------------------------------------- U-R: real errors in Baker 1930
real("U-R-01", "seg_p0050_s0001",
     "Quod vero Josephi Arimathæensis opera in gentibus Britannicis ad fidem perducendis Philippus usus fuerit, id totum ex Glastoniensium monachorum lacunis haustum est",
     "Now, as for Philip having used the aid of Joseph of Arimathea in bringing the people of Britain to the faith, this is to be drawn from the wells of knowledge (lacunis) of the Monks of Glaston",
     "Now, as for Philip having used the aid of Joseph of Arimathea in bringing the people of Britain to the faith, this has been drawn from the stagnant pools (lacunis) of the Monks of Glaston",
     [E("wells of knowledge", "major"), E("is to be drawn", "minor")],
     "lacunae = pits / pools / puddles; Ussher's image is disparaging, and 'wells of knowledge' reverses the evaluation. haustum est is perfect passive ('has been drawn'), not a gerundive. Severity of the first is contestable.")
real("U-R-02", "seg_p0057_s0001",
     "Ex Juvenale vero constat Arviragum Domitiano imperante regem Britannorum extitisse: quum sub Vespasiano anno LXXVI. Josephus noster obiisse dicatur.",
     "From Juvenal, indeed, it appears that Arviragus became King of the Britons while Domitian was Emperor, since our Joseph is said to have died under Vespasian in the year LXXVI.",
     "From Juvenal, indeed, it appears that Arviragus was King of the Britons while Domitian was Emperor, whereas our Joseph is said to have died under Vespasian in the year LXXVI.",
     [E("since", "major"), E("became", "minor")],
     "quum + subjunctive is adversative here: Ussher sets the two dates against each other to show that the Arviragus-Joseph synchronism fails. 'since' makes Joseph's death the cause. Compare v1 #4 (cum -> 'when', keyed minor); 'since' asserts a false causal link, hence major, but contestable. Second: extitisse = was (existed as) king; 'became' adds an accession claim Juvenal doesn't support -> minor, contestable.")
real("U-R-03", "seg_p0060_s0005",
     "Cum ergo Joseph fuerit incarceratus tanto tempore apud Jerusalem, impossibile est eum fuisse in Anglia, cum sit magna distantia.",
     "When, therefore, Joseph was imprisoned at such a time at Jerusalem it is impossible for him to have been in England, at so great a distance.",
     "When, therefore, Joseph was imprisoned for so long a time at Jerusalem it is impossible for him to have been in England, at so great a distance.",
     [E("at such a time", "major")],
     "tanto tempore = for so long a time. Alphonsus' argument is that the length of the imprisonment rules out the journey; 'at such a time' loses the duration. Severity contestable.")
real("U-R-04", "seg_p0063_s0001",
     "Guilielmus quidem Eysengreineus ex annalibus Anglorum narrat eum “ post urbis Hierosolymæ destructionem apostolis adhæsisse; atque hoc pacto jam senem in Britanniam profectum, in urbe Wellia Christum prædicavisse.”",
     "Certainly William Eysengreineus in his annals of the English relates that he \"after the destruction of Jerusalem attached himself to the Apostles: and that, by agreement, he proceeded to Britain when he was now old, and preached Christ in the city of Wells.\"",
     "Certainly William Eysengreineus from the annals of the English relates that he \"after the destruction of Jerusalem attached himself to the Apostles: and that, in this way, he proceeded to Britain when he was now old, and preached Christ in the city of Wells.\"",
     [E("by agreement", "major"), E("in his annals of the English", "major")],
     "hoc pacto = in this way (not a pact), so 'by agreement' invents an event. ex annalibus Anglorum = citing the English annals: Eysengrein is reporting a source, and Ussher's next sentence ('in no English annals does he find...') depends on that.")
real("U-R-05", "seg_p0065_s0001",
     "et de reliquis in Glastoniensi monasterio repositis libellus alter, Henrici III. Anglorum regis temporibus exaratus. In neutro vero Josephi ulla occurrit mentio.",
     "and another book concerning the relics preserved at the Monastery of Glaston, discovered in the times of Henry III, King of England. In neither, indeed, does any mention occur of Joseph.",
     "and another book concerning the relics preserved at the Monastery of Glaston, written in the times of Henry III, King of England. In neither, indeed, does any mention occur of Joseph.",
     [E("discovered", "minor")],
     "exaratus = written. The date of composition is what makes the book's silence about Joseph count as evidence. Keyed minor; arguably major.")
real("U-R-06", "seg_p0066_s0005",
     "Glasconiæ extabant (inquit) laminæ æneæ sculptæ ad perpetuandam memoriam, sacella, crypta, cruces, arma, observatio festi S. Josephi ad VI. Calendas Augusti, quamdiu monachi regum chartis munitissime gaudebant: nunc omnia cum ruinis confusa perierunt.",
     "There were in existence (he says) at Glasconia inscribed tablets of brass to perpetuate his memory, chapels, crypts, crosses, arms, and the observance of the feast of S. Joseph for vi days at the Calends of August, as long as the monks enjoyed most securely the King's Charters: now all things have perished mingled with the ruins.",
     "There were in existence (he says) at Glasconia inscribed tablets of brass to perpetuate his memory, chapels, crypts, crosses, arms, and the observance of the feast of S. Joseph on the sixth day before the Calends of August, as long as the monks enjoyed most securely the King's Charters: now all things have perished mingled with the ruins.",
     [E("for vi days at the Calends of August", "major")],
     "ad VI. Calendas Augusti = on the 6th day before the Kalends of August (27 July, Roman inclusive count). Baker reads it as a six-day feast at 1 August.")
real("U-R-07", "seg_p0057_s0002",
     "Sed neque ille ejusmodi librum unquam vidit: neque Nicolao Sandero ulla fides adhibenda, Gildæ hic authoritatem tam confidenter in libro primo de schismate ita venditanti",
     "But neither he ever saw a book of that kind: nor was any credibility attached to it by Nicholas Sanders, here so confidently praising the authority of Gildas in his first book concerning schism",
     "But neither did he ever see a book of that kind: nor should any credibility be attached to Nicholas Sanders, here so confidently praising the authority of Gildas in his first book concerning schism",
     [E("nor was any credibility attached to it by Nicholas Sanders", "major"), E("neither he ever saw", "minor", "Grammar", "Fluency")],
     "fides adhibenda (gerundive) + dative Nicolao Sandero = no credence should be given TO Sanders. Baker makes Sanders the one who withheld credence, which contradicts the same clause and reverses Ussher's point. Second: ungrammatical inversion.")
real("U-R-08", "seg_p0067_s0002",
     "Utrinque ad latera stipitis, et sub alis crucis, ponitur ampulla inaurata. Et hæc semper denominabantur insignia Sancti Josephi: qui ibi habitasse pie credebatur, et fortasse sepultus esse.",
     "On each side of the shaft and under the arms of the Cross is placed a gilded chalice. And these were always denominated the insignia of St. Joseph who was piously believed to have lived, and probably to have been buried there.",
     "On each side of the shaft and under the arms of the Cross is placed a gilded phial. And these were always denominated the insignia of St. Joseph who was piously believed to have lived, and perhaps to have been buried there.",
     [E("probably", "minor"), E("chalice", "minor")],
     "fortasse = perhaps (a weaker claim than 'probably'). ampulla = flask / phial, matching the two phials of the legend (p0067_s0003), not a chalice. Both peripheral -> minor.")
real("U-R-09", "seg_p0056_s0001",
     "In vita enim Patricii, Johannem Tinmuthensem secutus et Hardingum in chronico, duodecim istas hidas ab Arvirago concessas fuisse scribit",
     "For in the \"Life of Patrick,\" confirming John Tinmuth and Harding in his \"Chronicle,\" he writes that these twelve hides were granted by Arviragus",
     "For in the \"Life of Patrick,\" following John Tinmuth and Harding in his \"Chronicle,\" he writes that these twelve hides were granted by Arviragus",
     [E("confirming", "minor")],
     "secutus = having followed. Capgrave is derivative of Tinmuth and Harding, not independent corroboration of them; this matters to Ussher's source criticism but is local -> minor.",
     rejoined=True)

# ---------------------------------------------------------------- L-P: planted into LITERA gold
LP = [
    ("T0004", "quam diu etiam furor iste tuus nos eludet?",
     "For how much longer will that rage of yours make a mockery of us?",
     "For how much longer will this rage of ours make a mockery of us?",
     [E("this rage of ours", "major")], "iste tuus = that ... of yours; the madness is Catiline's, not the senate's."),
    ("T0005", "quem ad finem sese effrenata iactabit audacia?",
     "To what point will your unbridled audacity throw itself?",
     "To what point has your unbridled audacity thrown itself?",
     [E("has your unbridled audacity thrown itself", "minor")], "iactabit = future. Tense shift; the rhetorical question survives -> minor."),
    ("T0009", "Cum autem dominatu unius omnia tenerentur neque esset usquam consilio aut auctoritati locus, socios denique tuendae rei publicae summos viros amisissem, nec me angoribus dedidi, quibus essem confectus, nisi iis restitissem, nec rursum indignis homine docto voluptatibus.",
     "But when everything was held under the domination of one, and there was nowhere a place for counsel or authority, and finally, when I had lost my allies for defending the republic, the greatest men, I did give myself neither to sorrows, by which I would have been defeated, unless I had resisted them, nor again to pleasures unworthy of a learned man.",
     "But when everything was held under the domination of one, and there was nowhere a place for counsel or authority, and finally, when I had lost my allies for defending the republic, the greatest men, I did give myself neither to sorrows, by which I would have been defeated, unless I had resisted them, nor again to pleasures worthy of a learned man.",
     [E("pleasures worthy of a learned man", "major")], "indignis homine docto = unworthy of a learned man. Dropped negative prefix reverses the evaluation."),
    ("T0010", "Magno ea fletu et mox precationibus faustis audita;",
     "These things were heard with a great crying and soon after with favorable prayers;",
     "These things were heard with great laughter and soon after with favorable prayers;",
     [E("great laughter", "major")], "fletu = weeping."),
    ("T0013", "Postera nocturnos aurora removerat ignes,",
     "The next Aurora had removed the nocturnal fires,",
     "The previous Aurora had removed the nocturnal fires,",
     [E("The previous Aurora", "minor")], "postera = next/following. Sequencing detail -> minor."),
    ("T0014", "solque pruinosas radiis siccaverat herbas:",
     "and the sun had dried the frosty grass with rays of light;",
     "and the moon had dried the frosty grass with rays of light;",
     [E("the moon", "major")], "sol = sun."),
    ("T0015", "ad solitum coiere locum.",
     "they met at the usual place.",
     "they met at a new place.",
     [E("a new place", "minor")], "solitum = usual. Local detail -> minor."),
    ("T0017", "statuunt, ut nocte silenti fallere custodes foribusque excedere temptent,",
     "they decide that in the silent night they would try to deceive the guards and leave from the gates,",
     "they decide that in the silent night they would try to bribe the guards and leave from the gates,",
     [E("bribe the guards", "major")], "fallere = deceive / elude."),
    ("T0018", "cumque domo exierint, urbis quoque tecta relinquant;",
     "and when they left the house, they also would leave behind the roofs of the city;",
     "and when they left the house, they also would set fire to the roofs of the city;",
     [E("set fire to the roofs of the city", "major")], "relinquant = leave behind."),
    ("T0020", "est, non est quod agas, Attale, semper agis.",
     "Whether there is, or is not something to do, Attalus, you always act.",
     "When there is something to do, Attalus, you always act.",
     [E("(missing) or is not", "major", "Omission")], "est, non est = whether there is or is not. The dropped half is the joke (he acts even with nothing to do)."),
    ("T0021", "si res et causae desunt, agis, Attale, mulas.",
     "If affairs and cases are lacking, you drive mules, Attalus.",
     "If affairs and cases are lacking, you drive horses, Attalus.",
     [E("horses", "minor")], "mulas = mules. Changes the image but not the pun on agere -> minor."),
    ("T0024", "Indigentiam vestram nostram putamus.",
     "We think your need our own.",
     "We think our need your own.",
     [E("our need your own", "major")], "vestram ... nostram: the writer takes on the addressees' need. The swap reverses who bears whose burden."),
    ("T0027", "Eius principium si habetis habeamus, simulque finem Ciceronis Pro rege Deiotaro.",
     "If you have the beginning of it, let us have it, along with the end of Cicero's 'For King Deiotarus'.",
     "If you have the beginning of it, let us have it, along with the end of Cicero's 'For Milo'.",
     [E("'For Milo'", "major", "Entity")], "Pro rege Deiotaro. Wrong work requested."),
    ("T0029", "apporto vobis Plautum, lingua non manu, quaeso ut benignis accipiatis auribus.",
     "I present to you Plautus, in speech not in hand, I ask that you all receive with kind ears.",
     "I present to you Terence, in speech not in hand, I ask that you all receive with kind ears.",
     [E("Terence", "major", "Entity")], "Plautum. Terence is the other Roman comic playwright, so the swap is plausible."),
    ("T0031", "Quid faciant leges, ubi sola pecunia regnat, aut ubi paupertas vincere nulla potest?",
     "What may the laws do, where money alone rules or where no poverty can win?",
     "What may the laws do, where money alone rules or where poverty alone can win?",
     [E("poverty alone can win", "major")], "paupertas ... nulla = no poverty can win. Reversal breaks the complaint."),
    ("T0034", "Vix vestem induerat Glauce cum dolorem gravem per omnia membra sensit, et paulo post crudeli cruciatu adfecta e vita excessit.",
     "Scarcely had Glauce put on the garment when she felt severe pain through all her limbs, and shortly thereafter, having been affected by a cruel torture, she exited life.",
     "Scarcely had Glauce put on the garment when she felt severe pain through all her limbs, and long thereafter, having been affected by a cruel torture, she exited life.",
     [E("long thereafter", "minor")], "paulo post = shortly after. Timing only -> minor."),
    ("T0035", "His rebus gestis Medea furore atque amentia impulsa filios suos necavit;",
     "With these deeds done, Medea, driven by fury and madness, killed her own sons;",
     "With these deeds done, Medea, driven by fury and madness, killed her own brothers;",
     [E("her own brothers", "major")], "filios = sons. Trap: Medea did kill her brother Absyrtus in another episode."),
    ("T0037", "Hoc constituto solem oravit ut in tanto periculo auxilium sibi praeberet.",
     "Having made this decision, she implored the sun to provide her assistance in such great peril.",
     "Having made this decision, she implored Jupiter to provide her assistance in such great peril.",
     [E("Jupiter", "major", "Entity")], "solem = Sol, her grandfather, who sends the dragon-chariot."),
    ("T0045", "Puer interit, natum senex effert pater,",
     "the boy dies, an old man, a father buries his son,",
     "the boy dies, a young man, a father buries his son,",
     [E("a young man", "major")], "senex = old man. The lament turns on an old father burying a young son."),
    ("T0051", "At tu, misella, forte avum si amiseris, Hoc destituta vinculo aresces, velut",
     "But you unfortunate little girl, if you should perhaps lose your grandfather, robbed of this bond, you will wither just like",
     "But you unfortunate little girl, if you should perhaps lose your father, robbed of this bond, you will wither just like",
     [E("lose your father", "major")], "avum = grandfather (the speaker); her father is already dead (T0039-0047)."),
    ("T0052", "Crescens amaracus, liquore si suo Suoque sole non alatur, interit.",
     "marjoram, if it is not nourished by its own water and its own sunlight as it grows, dies.",
     "marjoram, if it is nourished by its own water and its own sunlight as it grows, dies.",
     [E("if it is nourished", "major")], "non alatur. Dropped negation."),
    ("T0054", "Sciendum est vt supra diximus quod duplex est furor. malus et bonus.",
     "it should be known, as we said before, that there are two kinds of frenzy, good and bad.",
     "it should be known, as we shall say below, that there are two kinds of frenzy, good and bad.",
     [E("as we shall say below", "minor")], "supra diximus = we said above. Cross-reference direction -> minor."),
    ("T0057", "is est qui hominem supra hominem erigit: et deo proximum dum illo efflatur reddit.",
     "is that which elevates man above man and brings him closest to God for as long as he is enthused with it.",
     "is that which elevates man above the gods and brings him closest to God for as long as he is enthused with it.",
     [E("above the gods", "major")], "supra hominem = above (the merely) human."),
    ("T0061", "his autem quattuor furoribus bonis: alij quattuor qui hos falso 10 imitantur opponuntur.",
     "Set in opposition to these four good frenzies are another four which falsely resemble them.",
     "Set in opposition to these four good frenzies are another five which falsely resemble them.",
     [E("another five", "major")], "alij quattuor = four others; the scheme is four true vs four false."),
    ("T0062", "Nam quotiens ex visibilium decore atque pulchritudine rapimur ad contemplandam diuinam pulchritudinem eius qui hec omnia fecit.",
     "Now, whenever we are transported out of the grace or beauty of visible things to contemplate the divine beauty of him who created it all,",
     "Now, whenever we are transported out of the grace or beauty of invisible things to contemplate the divine beauty of him who created it all,",
     [E("invisible things", "major")], "visibilium = visible things; the ascent is from visible to invisible beauty (T0066)."),
    ("T0063", "incendimar quodam igni amoris atque desiderij ita spiritus noster corporis huius carcere euolasse videtur atque illi adherere qui omnium pulcherrimus est.",
     "we are enflamed by some sort of fire of love and desire, so our soul seems to have flown free of the prison of the body and to become attached to the most beautiful of all beings.",
     "we are enflamed by some sort of fire of love and desire, so our soul is known to have flown free of the prison of the body and to become attached to the most beautiful of all beings.",
     [E("is known to have flown free", "minor")], "videtur = seems. 'is known to' turns an appearance into a certainty; local -> minor."),
    ("T0064", "cum quo dum animus versatur omnes corporei sensus occlusi sunt.",
     "While our mind is involved with this being all our bodily senses are shut off,",
     "While our mind is involved with this being all our bodily senses are heightened,",
     [E("heightened", "major")], "occlusi = shut. Reverses the ecstatic withdrawal of the senses."),
    ("T0066", "huic amori qui ex visibilium pulchritudine ad invisibilem dei decorem desiderandum nos ducit: impedimento est amor libidinosus et lubricus quo rerum que oculis cernuntur pulchritudine amanda continemur",
     "An impediment to this love which leads us from the beauty of visible things to desire the invisible beauty of God, is lustful and deceitful love, whereby we are constrained by loving the beauty of things our eyes can see;",
     "An aid to this love which leads us from the beauty of visible things to desire the invisible beauty of God, is lustful and deceitful love, whereby we are constrained by loving the beauty of things our eyes can see;",
     [E("An aid", "major")], "impedimento est = is a hindrance."),
    ("T0067", "nec vltra consurgimus: et is profecto manifestus furor est.",
     "and we do not rise beyond it: this is quite obviously a kind of madness.",
     "and we rise beyond it: this is quite obviously a kind of madness.",
     [E("we rise beyond it", "major")], "nec ... consurgimus = we do not rise. Dropped negation."),
    ("T0056", "Bonus autem furor qui diuinitus infunditur.",
     "Conversely the good frenzy which is imparted divinely",
     "Conversely the good frenzy which is acquired by study",
     [E("acquired by study", "major")], "diuinitus infunditur = is poured in divinely; the definition turns on its divine origin."),
]
for i, (src, la, gold, stim, exp, why) in enumerate(LP, 1):
    planted(f"L-P-{i:02d}", "L-P", src, la, gold, stim, exp, why)

# ---------------------------------------------------------------- hard negatives: meaning-preserving rewrites
variant("U-V-01", "U-V", "seg_p0047_s0003",
        "Et cum hæc in hac regione prima fuerit; ampliori eam dignitate Dei filius insignivit, ipsam videlicet in honore suæ matris dedicando.",
        "And as this was the first in that region, the Son of God distinguished it with greater dignity by dedicating it in honour of His Mother.",
        "And since this was the first church in that region, the Son of God honoured it with a greater dignity, namely by dedicating it to His Mother.",
        "Explicitation ('church') and 'dedicating it to His Mother' for in honore suae matris. Boundary check: is 'church' an Addition? (the building is called ecclesia in s0002).")
variant("U-V-02", "U-V", "seg_p0066_s0003",
        "Quem habuerit eventum ista inquisitio, non invenio: ab his tamen qui Glastoniense monasterium viderunt est proditum, et sacellum ibi Josephi nomini dicatum, et tumulum etiam positum fuisse, hoc inscriptum epitaphio.",
        "What was the outcome of this enquiry, I do not find: but by those who have seen the Monastery of Glaston it has been handed down, that a chapel was there dedicated to the name of Joseph, and also that a tomb was situated there inscribed with this epitaph:",
        "I cannot discover what came of this inquiry; but those who saw the monastery of Glastonbury report that a chapel there was dedicated to Joseph's name, and that a tomb was also placed there, inscribed with this epitaph:",
        "Passive -> active restructuring ('it has been handed down by those' -> 'those report'); truth conditions preserved.")
variant("U-V-03", "U-V", "seg_p0062_s0002",
        "Tertium illud, quod totum Britanniæ regnum Josephi ministerio fidem non susceperit; verum quidem est, sed ad rem non pertinet.",
        "As to the third point, that the whole of the realm of Britain did not receive the faith by the ministry of Joseph, it is true enough but it is not relevant to the issue.",
        "The third point, that the whole realm of Britain did not receive the faith through Joseph's ministry, is true, but beside the point.",
        "Idiomatic compression; 'beside the point' = ad rem non pertinet.")
variant("U-V-04", "U-V", "seg_p0067_s0001",
        "Sparguntur guttæ sanguinis per omnem aream scuti.",
        "Drops of blood are sprinkled all over the surface of the shield.",
        "The whole field of the shield is strewn with drops of blood.",
        "Subject/object restructuring (cf. v1 #2 sonant); 'field' is the heraldic term for area scuti.")
variant("U-V-05", "U-V", "seg_p0065_s0002",
        "Anno demum MCCCXLV. a Johanne Blomæo Londinensi, cujusdam revelationis sibi factæ prætextu, ab Edvardo III. licentia quærendi corpus Josephi ab Arimathia impetrata est",
        "At length, in the year 1345, a license was procured from Edward III by John Blome of London on the pretext of a certain revelation made to him, to seek for the body of Joseph of Arimathea",
        "At length, in 1345, John Blome of London, claiming that a certain revelation had been made to him, obtained from Edward III a licence to search for the body of Joseph of Arimathea",
        "Passive -> active. BOUNDARY: 'claiming' keeps the doubt but is weaker than 'on the pretext of' (praetextu). Keyed no-error; the classicist may judge it a minor loss of Ussher's scepticism.")
variant("U-V-06", "U-V", "seg_p0066_s0006",
        "Nemo tamen monachorum unquam scivit certum locum sepulchri hujus sancti, vel designavit.",
        "But none of the monks ever knew the exact position of this holy sepulcre, or described it.",
        "Yet no monk ever knew, or pointed out, the exact place of this saint's tomb.",
        "Reordering; 'pointed out' for designavit (arguably closer than Baker's 'described').")
variant("L-V-01", "L-V", "T0023", "Si bene valetis gaudemus.",
        "If you all are well, we are glad.",
        "We are glad if you are all well.",
        "Clause reordering only.")
variant("L-V-02", "L-V", "T0038", "Senii levamen unicum, neptis, mei,",
        "Granddaughter, the only consolation of my old age,",
        "Granddaughter, sole comfort of my old age,",
        "Synonym substitution (unicum = sole; levamen = comfort/relief).")
variant("L-V-03", "L-V", "T0043", "Heu, heu, genus hominum caducum et languidum",
        "Alas, alas, the feeble and frail race of men,",
        "Alas, alas for the race of men, so frail and feeble",
        "Exclamatory restructuring; adjectives reordered.")
variant("L-V-04", "L-V", "T0050", "Miseram senectutem meam, miserum senem!",
        "O my miserable old age, miserable old man!",
        "How wretched my old age, how wretched an old man!",
        "Accusative of exclamation rendered with 'How ...!'.")
variant("L-V-05", "L-V", "T0053", "Sed quia de furore loquimur.",
        "But since we are speaking of frenzy,",
        "But since our subject is frenzy,",
        "Paraphrase of loquimur de = our subject is.")
variant("L-V-06", "L-V", "T0030", "nunc argumentum accipite atque animum advortite; quam potero in verba conferam paucissuma.",
        "Now receive the plot and turn your mind towards; I will convey it in the fewest words possible that which I am able.",
        "Now take in the plot and pay attention; I will set it out in as few words as I can.",
        "Idiomatic rendering of animum advortite; the LITERA gold itself is clumsy here, so the variant is the cleaner English.")

# ---------------------------------------------------------------- inherited issues in the references
# A planted stimulus = reference + one edit, so any flaw in the reference sits in BOTH the stimulus
# and its negative. One Claude read of each reference against the Latin (2026-10-03); unconfirmed.
# "likely" = probably an MQM error; "loose" = imprecise but probably defensible (The classicist rules either way).
INHERITED = {
    "U-P-03": [("inspired", "likely", "admoniti sunt ... construere = were instructed/directed to build; Baker renders admonitio as 'direction' elsewhere in ch2.")],
    "U-P-04": [("help and presence", "likely", "auxilio ac visione = help and visions/appearances, not 'presence'.")],
    "U-P-07": [("in one respect", "loose", "uno gradu = by one degree.")],
    "U-P-08": [("the freedom of Glaston", "loose", "jus = right / jurisdiction.")],
    "U-P-16": [("which can there be seen", "likely", "quae adhuc visuntur = which are STILL seen; 'still' dropped. Sits on the planted span ('no longer'), so it confounds the pair.")],
    "U-P-19": [("had the intention to apprehend Peter", "likely", "apposuit ut apprehenderet = proceeded to arrest (Acts 12:3); Peter was in fact arrested.")],
    "L-P-02": [("your unbridled audacity", "loose", "No possessive in the Latin; 'your' is supplied from context (Catiline).")],
    "L-P-03": [("I did give myself neither to sorrows", "loose", "Awkward emphatic 'did' + 'neither': a possible Fluency flag.")],
    "L-P-04": [("a great crying", "loose", "fletu = weeping; 'a great crying' is unidiomatic: a possible Fluency flag.")],
    "L-P-08": [("leave from the gates", "likely", "foribus = (house) doors; the next line ('when they left the house') confirms it is the house, not city gates.")],
    "L-P-14": [("I ask that you all receive with kind ears", "loose", "Comma splice and missing object ('receive [him]'): a possible Fluency flag.")],
    "L-P-28": [("lustful and deceitful love", "loose", "lubricus = slippery / lascivious; 'deceitful' is a stretch.")],
    "L-P-29": [("a kind of madness", "loose", "manifestus furor = manifest frenzy; v1 treated furor as the technical term 'frenzy' (#13), so a strict key could call this inconsistent.")],
    "L-P-30": [("Conversely the good frenzy which is imparted divinely", "loose", "Sentence fragment (the clause continues in T0057): a possible Fluency flag.")],
}
for r in rows:
    if r["pair_id"] in INHERITED:
        r["inherited_issues"] = [{"span": s, "assessment": a, "note": n} for s, a, n in INHERITED[r["pair_id"]]]
        for i in r["inherited_issues"]:
            assert i["span"] in r["reference_english"], f"{r['pair_id']}: inherited span not in reference"


def mark_diff(ref, stim):
    """Word-level diff of stimulus vs reference: ~~removed~~ **added** (worksheet only; judges get plain text)."""
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


# ---------------------------------------------------------------- write
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "candidate_pool.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")

errs = [r for r in rows if r["is_error_stimulus"]]
negs = [r for r in rows if not r["is_error_stimulus"]]
n_exp = [e for r in errs for e in r["expected"]]
sev = {s: sum(e["severity"] == s for e in n_exp) for s in ("major", "minor")}
typ = {}
for e in n_exp:
    typ[e["error_type"]] = typ.get(e["error_type"], 0) + 1
grp = {}
for r in rows:
    grp.setdefault(r["group"], [0, 0])[0 if r["is_error_stimulus"] else 1] += 1

W = ["# Fluent-misgloss set v2 — candidate pool (for the classicist)", "",
     "**Status: PRE-ADJUDICATION.** Nothing here is a key until you've marked it. Generated by",
     "`08_working_scratch/pipeline_scripts/build_fluent_v2_pool.py`. Contains excerpts of Baker's 1930 translation.", "",
     f"- Error candidates: **{len(errs)}** ({len(n_exp)} expected error spans: {sev['major']} major / {sev['minor']} minor; types {typ})",
     f"- Negatives: **{len(negs)}**",
     "- By group (errors / negatives): " + ", ".join(f"{g} {a}/{b}" for g, (a, b) in sorted(grp.items())), "",
     "## Groups", "",
     "- **U-P** (Ussher ch2): Claude **planted** one error into Baker's 1930 English. The negative is Baker's own sentence.",
     "- **U-R** (Ussher ch2): **real errors in Baker's translation** (a human translator), found by Claude reading the Latin. The negative is a Claude-written correction, so it needs a full review, the same as an error.",
     "- **L-P** (LITERA Classical): Claude **planted** one error into the LITERA gold. The negative is the gold.",
     "- **U-V / L-V**: rewrites that keep the meaning (hard negatives). They test whether judges over-flag. Each needs a full ruling.", "",
     "## What to mark", "",
     "For each **error** item, tick one box:",
     "- `[ ] accept`: it's an error, the type and severity are right, and the Latin forces this reading.",
     "- `[ ] accept, change severity/type`: write the change.",
     "- `[ ] reject: not an error`: the stimulus is a defensible rendering. These are the v1 #5/#9/#19 cases. If the Latin *permits* the English, reject.",
     "- `[ ] reject: reference flawed`: the reference/negative itself has an error, so the pair can't be used.", "",
     "For each **negative**, answer one question: *is this sentence clean apart from the planted span?* Answer `[ ] clean` or `[ ] has an error` (say what).",
     "A planted stimulus is the reference with one edit. Any flaw in the reference is therefore in **both** the stimulus (making a second, unkeyed error) and the negative (making a false \"no error\" label).",
     "Where I found a possible flaw, it's listed under **Inherited from the reference**. Please rule on each one. `likely` = I think it's an MQM error; `loose` = imprecise but probably defensible.", "",
     "In **Stimulus vs reference**, the change is marked ~~removed~~ **added** so you don't have to find it by eye. The judges see plain text.", "",
     f"Inherited-issue flags: {sum(len(v) for v in INHERITED.values())} on {len(INHERITED)} pairs "
     f"({sum(a == 'likely' for v in INHERITED.values() for _, a, _ in v)} likely, {sum(a == 'loose' for v in INHERITED.values() for _, a, _ in v)} loose). "
     "Any pair with a confirmed flaw gets fixed (planted into a corrected base, which then needs your review) or dropped. It is never keyed around.", "",
     "Please mark blind. A provisional baseline judge run (Opus, Gemini, JEV) was done on 2026-10-03 at Paul's request,",
     "but its results are **withheld from you** until you've frozen the key. Please don't look in `fluent_v2/runs/`.",
     "The items were frozen before that run, and no item is edited in response to judge output.", "",
     "Authorship caveat: all U-P/L-P errors and every U-V/L-V rewrite were written by Claude (Opus family). The U-R errors are the only ones a model didn't write.",
     "Report results split by `error_author` so we can see whether Claude-written errors behave differently.", ""]

order = ["U-P", "U-R", "L-P", "U-V", "L-V"]
titles = {"U-P": "U-P: Ussher, planted into Baker", "U-R": "U-R: Ussher, real Baker errors",
          "L-P": "L-P: LITERA Classical, planted", "U-V": "U-V: Ussher meaning-preserving rewrites (expected: no error)",
          "L-V": "L-V: LITERA meaning-preserving rewrites (expected: no error)"}
for g in order:
    W += ["---", "", f"## {titles[g]}", ""]
    for r in [r for r in rows if r["group"] == g and r["is_error_stimulus"]] + \
             [r for r in rows if r["group"] == g and not r["is_error_stimulus"] and g in ("U-V", "L-V")]:
        W += [f"### {r['item_id']}  ·  `{r['source_ref']}`", "",
              f"**Latin:** {r['latin']}", ""]
        if r["is_error_stimulus"]:
            W += [f"**Reference** ({r['reference_source']}): {r['reference_english']}", "",
                  f"**Stimulus vs reference** (error by {r['error_author']}): {mark_diff(r['reference_english'], r['stimulus_english'])}", "",
                  "**Proposed MQM:**"]
            W += [f"- `{e['span']}` · {e['dimension']} / {e['error_type']} / **{e['severity']}**" for e in r["expected"]]
            W += ["", f"**Why the Latin forces it:** {r['rationale']}", "",
                  "`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error` `[ ] reject: reference flawed`", ""]
            if r.get("inherited_issues"):
                W += ["**Inherited from the reference** (present in both stimulus and negative):"]
                W += [f"- `{i['span']}` ({i['assessment']}): {i['note']}  `[ ] real error` `[ ] defensible`"
                      for i in r["inherited_issues"]]
                W += [""]
            if g == "U-R":
                W += ["**Negative (Claude's correction; clean apart from the corrected spans?):** `[ ] clean` `[ ] has an error:` ______", ""]
            else:
                W += ["**Negative (= reference; clean apart from the planted span?):** `[ ] clean` `[ ] has an error:` ______", ""]
        else:
            W += [f"**Reference** ({r['reference_source']}): {r['reference_english']}", "",
                  f"**Rewrite (stimulus):** {r['stimulus_english']}", "",
                  f"**Why it should count as no error:** {r['rationale']}", "",
                  "`[ ] no error (keep as negative)` `[ ] is an error:` ______", ""]
(OUT / "worksheet.md").write_text("\n".join(W), encoding="utf-8")
print(f"{len(rows)} items: {len(errs)} error candidates, {len(negs)} negatives; spans {sev}; types {typ}; groups {grp}")
