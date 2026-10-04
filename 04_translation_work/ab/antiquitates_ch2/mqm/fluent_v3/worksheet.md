# Fluent-misgloss set v3: HARD set (for the classicist)

**Status: PRE-ADJUDICATION.** Two kinds of grammar-dependent error, all on Ussher ch1/ch2:
- **Real (H-, V1-):** 17 errors a model actually made, trimmed verbatim from the drafts. Each is paired with another model's real rendering of the same Latin that gets it right.
- **Simulated (S-):** 34 errors. Each takes a real model rendering judged clean and makes ONE minimal edit reproducing the *mechanism* of a real error (`modeled_on`). The unedited rendering is the paired negative, and the change is marked ~~removed~~ **added**.
Claude (Opus 5.5) found the real errors and wrote the simulated edits, so the set leans towards errors a Claude-family reader can see. Report results split by origin.

- Error items: **51** (13 real new + 4 real from v1 + 34 simulated)
- Negatives: **56**: paired correct/base renderings, 6 real-but-defensible divergences (B-), and the v1 hard negatives

At Paul's request (2026-10-04), Gemini and JEV were run on this set as a PROVISIONAL baseline against Claude's unadjudicated key.
The results are **withheld from you** until you've frozen the key. Please don't look in `fluent_v3/runs/`. No item will be edited in response to judge output.

For each error: `[ ] accept` `[ ] accept, change:` `[ ] reject: not an error (the Latin permits it)`. For each negative: `[ ] clean` `[ ] has an error:`.
Items marked **contestable** are the reason this set exists; please rule on them explicitly.

---

### H-01  ·  `seg_p0047_s0001`  ·  rendered by opus-4-8

**Latin:** Postea etiam alii duo reges pagani successive comperta vitæ eorum sanctimonia, unicuique eorum unam portionem terræ concesserunt; ac ad petitionem ipsorum, secundum morem gentis, brevi dictas duodecim hidas confirmaverunt.

**English (stimulus):** Afterwards two other pagan kings also, one after the other, having learned of the holiness of their life, each granted them one portion of land; and at their request, according to the custom of the people, they confirmed the said twelve hides by charter.

**Proposed MQM:**
- `each granted them one portion of land` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** unicuique eorum (dative) = to EACH of them (the twelve), one portion apiece = the twelve hides of the next clause. Opus makes each KING the giver of one portion (two in all), breaking the link to the twelve hides.

*Correct counterpart (fable-5):* Afterwards two other pagan kings also, in succession, having learned of the sanctity of their life, granted to each of them one portion of land; and at their petition, according to the custom of the nation, they confirmed the said twelve hides by charter.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-01__neg  ·  `seg_p0047_s0001`  ·  rendered by fable-5

**Latin:** Postea etiam alii duo reges pagani successive comperta vitæ eorum sanctimonia, unicuique eorum unam portionem terræ concesserunt; ac ad petitionem ipsorum, secundum morem gentis, brevi dictas duodecim hidas confirmaverunt.

**English (stimulus):** Afterwards two other pagan kings also, in succession, having learned of the sanctity of their life, granted to each of them one portion of land; and at their petition, according to the custom of the nation, they confirmed the said twelve hides by charter.

**Expected:** no error. Another model's real rendering that gets the H-01 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-02  ·  `seg_p0050_s0006`  ·  rendered by fable-5

**Latin:** Glastoniæ bis sex hidas dedit Arviragus rex: Joseph cum sociis jura reliquit eis.

**English (stimulus):** King Arviragus gave twice six hides of Glastonbury to Joseph and his companions, and left the rights to them.

**Proposed MQM:**
- `to Joseph and his companions, and left the rights to them` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** Each verse is its own clause: Joseph (with companions) is the subject of reliquit, and leaves the rights to 'them' (eis). Fable folds Joseph into line 1 as recipient and makes Arviragus the one who 'left the rights'.

**Contestable:** Joseph is indeclinable, so case alone does not force it; the verse structure and the redundant eis do.

*Correct counterpart (gemini-3-1-pro):* King Arviragus gave twice six hides of Glastonbury: Joseph with his companions left the rights to them.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-02__neg  ·  `seg_p0050_s0006`  ·  rendered by gemini-3-1-pro

**Latin:** Glastoniæ bis sex hidas dedit Arviragus rex: Joseph cum sociis jura reliquit eis.

**English (stimulus):** King Arviragus gave twice six hides of Glastonbury: Joseph with his companions left the rights to them.

**Expected:** no error. Another model's real rendering that gets the H-02 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-03  ·  `seg_p0062_s0001`  ·  rendered by opus-4-8

**Latin:** Neque enim aliquem hodie, si Thomam Dempsterum exceperis, tam stulte credulum esse existimamus, cui absurdissimum illud commentum, de Josepho muro incluso, probabile videri possit

**English (stimulus):** For I do not suppose that anyone today—unless you make an exception of Thomas Dempster—is so foolishly credulous that that most absurd fabrication about Joseph walled up in a tomb could seem probable to him

**Proposed MQM:**
- `walled up in a tomb` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** muro incluso = shut up in a wall: the Titus legend (p0060: a very thick wall broken open). 'tomb' substitutes a different confinement and blurs which tale Ussher means.

**Contestable:** severity: minor vs major

*Correct counterpart (fable-5):* for I do not think that anyone today — unless you except Thomas Dempster — is so foolishly credulous that that most absurd fiction of Joseph shut up within a wall could seem probable to him

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-03__neg  ·  `seg_p0062_s0001`  ·  rendered by fable-5

**Latin:** Neque enim aliquem hodie, si Thomam Dempsterum exceperis, tam stulte credulum esse existimamus, cui absurdissimum illud commentum, de Josepho muro incluso, probabile videri possit

**English (stimulus):** for I do not think that anyone today — unless you except Thomas Dempster — is so foolishly credulous that that most absurd fiction of Joseph shut up within a wall could seem probable to him

**Expected:** no error. Another model's real rendering that gets the H-03 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-04  ·  `seg_p0055_s0001`  ·  rendered by opus-4-8

**Latin:** Josephum ab Arimathea, cum a Judæis nequiter in carcerem ductus fuisset, et a Deo Optimo Maximo miraculose liberatum taliter ut nusquam postea in Judæa visum fuisse.

**English (stimulus):** that Joseph of Arimathea, after he had been wickedly cast into prison by the Jews and miraculously delivered by God Most Good and Most Great, was thereafter nowhere seen in Judaea.

**Proposed MQM:**
- `and miraculously delivered by God Most Good and Most Great, was thereafter nowhere seen` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** liberatum taliter ut ... visum fuisse = delivered IN SUCH A WAY THAT he was never seen again (result clause). Opus folds the deliverance into the temporal clause and drops the causal link.

*Correct counterpart (fable-5):* that Joseph of Arimathea, after he had been wickedly thrown into prison by the Jews, was so miraculously delivered by Almighty God that he was never afterward seen in Judaea

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-04__neg  ·  `seg_p0055_s0001`  ·  rendered by fable-5

**Latin:** Josephum ab Arimathea, cum a Judæis nequiter in carcerem ductus fuisset, et a Deo Optimo Maximo miraculose liberatum taliter ut nusquam postea in Judæa visum fuisse.

**English (stimulus):** that Joseph of Arimathea, after he had been wickedly thrown into prison by the Jews, was so miraculously delivered by Almighty God that he was never afterward seen in Judaea

**Expected:** no error. Another model's real rendering that gets the H-04 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-05  ·  `seg_p0053_s0002`  ·  rendered by fable-5

**Latin:** quibus duodecim hidæ ab Arvirago paganicis erroribus decepto concessæ erant.

**English (stimulus):** and to these, twelve hides were granted by Arviragus, who was still deceived by pagan errors.

**Proposed MQM:**
- `still` · Accuracy / Addition / **minor**

**Why the Latin forces it:** No adhuc in this sentence (contrast p0053_s0001 'adhuc ... involuto'). 'still' imports a later conversion, the very point Harding asserts and Ussher's sources deny.

**Contestable:** may be judged a harmless carry-over

*Correct counterpart (opus-4-8):* To these men twelve hides were granted by Arviragus, who was deceived by pagan errors.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-05__neg  ·  `seg_p0053_s0002`  ·  rendered by opus-4-8

**Latin:** quibus duodecim hidæ ab Arvirago paganicis erroribus decepto concessæ erant.

**English (stimulus):** To these men twelve hides were granted by Arviragus, who was deceived by pagan errors.

**Expected:** no error. Another model's real rendering that gets the H-05 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-06  ·  `seg_p0052_s0001`  ·  rendered by fable-5

**Latin:** Auxit prodigiosos ritus Josephus Arimathæus, advena Britanniæ plauſsbilis; qui de Solomonis fonte artem hauserat.

**English (stimulus):** Joseph of Arimathea, a plausible newcomer to Britain, augmented their prodigious rites; he had drawn his art from the fountain of Solomon.

**Proposed MQM:**
- `a plausible newcomer` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** plausibilis = applauded / welcome (Baker: 'a welcome stranger'). Modern 'plausible' = seemingly credible: a false friend.

**Contestable:** archaic English 'plausible' = deserving applause

*Correct counterpart (opus-4-8):* Joseph of Arimathea, a newcomer whom Britain welcomed, increased its prodigious rites; he had drawn his art from Solomon's fountain.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-06__neg  ·  `seg_p0052_s0001`  ·  rendered by opus-4-8

**Latin:** Auxit prodigiosos ritus Josephus Arimathæus, advena Britanniæ plauſsbilis; qui de Solomonis fonte artem hauserat.

**English (stimulus):** Joseph of Arimathea, a newcomer whom Britain welcomed, increased its prodigious rites; he had drawn his art from Solomon's fountain.

**Expected:** no error. Another model's real rendering that gets the H-06 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-07  ·  `seg_p0050_s0008`  ·  rendered by fable-5

**Latin:** Postea vero a beato Johanne apostolo ipsi prædicationi Ephesiorum insudante, beatæ perpetuæque virginis Mariæ paranymphus delegatus est

**English (stimulus):** Afterwards, while the blessed apostle John was laboring at the preaching to the Ephesians, he was appointed paranymph of the blessed and perpetual virgin Mary

**Proposed MQM:**
- `while the blessed apostle John was laboring` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** a + ablative with passive delegatus est = agent: John appointed him. Fable reads it as an ablative absolute (time) and drops who made the appointment. (Opus makes the same misreading.)

*Correct counterpart (gemini-3-1-pro):* But afterwards, by the blessed apostle John, who was himself laboring in the preaching to the Ephesians, he was delegated as the paranymph of the blessed and perpetual virgin Mary

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-07__neg  ·  `seg_p0050_s0008`  ·  rendered by gemini-3-1-pro

**Latin:** Postea vero a beato Johanne apostolo ipsi prædicationi Ephesiorum insudante, beatæ perpetuæque virginis Mariæ paranymphus delegatus est

**English (stimulus):** But afterwards, by the blessed apostle John, who was himself laboring in the preaching to the Ephesians, he was delegated as the paranymph of the blessed and perpetual virgin Mary

**Expected:** no error. Another model's real rendering that gets the H-07 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-08  ·  `seg_p0056_s0001`  ·  rendered by opus-4-8

**Latin:** Tres vero istos reges paganos, Arviragum, Marium et Coillum fuisse, ad marginem libri Malmesburiensis, qui MS. habetur in bibliotheca collegii S. Trinitatis Cantabrigiæ, annotatum invenio: quod ipsum etiam innuit Johannes Capgravius; quanquam parum hic sibi constans.

**English (stimulus):** That those three kings — Arviragus, Marius, and Coilus — were pagans I find noted in the margin of the Malmesbury manuscript held in the library of Trinity College, Cambridge; and John Capgrave hints at the same, though he is hardly consistent with himself here.

**Proposed MQM:**
- `That those three kings — Arviragus, Marius, and Coilus — were pagans` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** istos reges paganos picks up Malmesbury's 'tres reges licet pagani' (p0055); the marginal note IDENTIFIES the kings. Capgrave's inconsistency (next sentence) is about WHICH kings granted the hides. (Fable makes the same misreading.)

**Contestable:** word order permits the predicate reading; 'Quos tamen reges ... paganos extitisse vix admittit' fits either

*Correct counterpart (gemini-3-1-pro):* I find it annotated in the margin of a book of William of Malmesbury, which is kept as a manuscript in the library of Trinity College, Cambridge, that these three pagan kings were Arviragus, Marius, and Coillus: which John Capgrave also intimates, although he is little consistent with himself here.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-08__neg  ·  `seg_p0056_s0001`  ·  rendered by gemini-3-1-pro

**Latin:** Tres vero istos reges paganos, Arviragum, Marium et Coillum fuisse, ad marginem libri Malmesburiensis, qui MS. habetur in bibliotheca collegii S. Trinitatis Cantabrigiæ, annotatum invenio: quod ipsum etiam innuit Johannes Capgravius; quanquam parum hic sibi constans.

**English (stimulus):** I find it annotated in the margin of a book of William of Malmesbury, which is kept as a manuscript in the library of Trinity College, Cambridge, that these three pagan kings were Arviragus, Marius, and Coillus: which John Capgrave also intimates, although he is little consistent with himself here.

**Expected:** no error. Another model's real rendering that gets the H-08 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-09  ·  `seg_p0057_s0002`  ·  rendered by gemini-3-1-pro

**Latin:** Patricii discipulus Gildas Albanius, de victoria Aurelii Ambrosii librum scripsisse dicitur: quem de rebus a Josepho et sociis apud Glastonienses gestis authorem citat Foxus noster.

**English (stimulus):** Gildas Albanius, a disciple of Patrick, is said to have written a book, "On the Victory of Aurelius Ambrosius", whom our Foxe cites as an authority concerning the deeds performed by Joseph and his companions at Glastonbury.

**Proposed MQM:**
- `whom our Foxe cites` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** quem = Gildas (cited as authority). Placed after the title, English 'whom' attaches to Aurelius Ambrosius, so Foxe's authority becomes Ambrosius.

**Contestable:** could be classed Fluency (ambiguity) rather than Accuracy

*Correct counterpart (fable-5):* Gildas Albanius, the disciple of Patrick, is said to have written a book on the victory of Aurelius Ambrosius, and our Foxe cites him as an authority for the deeds done by Joseph and his companions at Glastonbury.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-09__neg  ·  `seg_p0057_s0002`  ·  rendered by fable-5

**Latin:** Patricii discipulus Gildas Albanius, de victoria Aurelii Ambrosii librum scripsisse dicitur: quem de rebus a Josepho et sociis apud Glastonienses gestis authorem citat Foxus noster.

**English (stimulus):** Gildas Albanius, the disciple of Patrick, is said to have written a book on the victory of Aurelius Ambrosius, and our Foxe cites him as an authority for the deeds done by Joseph and his companions at Glastonbury.

**Expected:** no error. Another model's real rendering that gets the H-09 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-10  ·  `seg_p0043_s0008`  ·  rendered by opus-4-8

**Latin:** Diligat ipsa senem quondam: sed et illa marito Tunc quoque cum fuerit, non videatur anus.

**English (stimulus):** May she love him one day when he is old; but may she too, even when she shall have grown old to her husband, then likewise not seem an old woman.

**Proposed MQM:**
- `grown old to her husband` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** marito (dative) goes with non videatur: may she not SEEM old TO HER HUSBAND. Opus attaches it to growing old and loses the point of the wish.

*Correct counterpart (gemini-3-1-pro):* May she herself love him when he is an old man: but may she also, even when she is old, not seem an old woman to her husband.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-10__neg  ·  `seg_p0043_s0008`  ·  rendered by gemini-3-1-pro

**Latin:** Diligat ipsa senem quondam: sed et illa marito Tunc quoque cum fuerit, non videatur anus.

**English (stimulus):** May she herself love him when he is an old man: but may she also, even when she is old, not seem an old woman to her husband.

**Expected:** no error. Another model's real rendering that gets the H-10 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-11  ·  `seg_p0044_s0001`  ·  rendered by opus-4-8

**Latin:** Postquam bis senis ingentem fascibus annum Rexerat, asserto qui sacer orbe fuit

**English (stimulus):** After he had governed the mighty year with its twice-six fasces — he who was hallowed when the world had been set free

**Proposed MQM:**
- `he who was hallowed` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** qui refers to annum: the great year (68/69) made sacred by the world's liberation from Nero (asserto orbe). Opus refers it to Silius.

**Contestable:** qui is masculine, so Silius is grammatically possible; the standard reading is the year

*Correct counterpart (gemini-3-1-pro):* After he had ruled the great year with twelve fasces, which was sacred because the world was freed

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-11__neg  ·  `seg_p0044_s0001`  ·  rendered by gemini-3-1-pro

**Latin:** Postquam bis senis ingentem fascibus annum Rexerat, asserto qui sacer orbe fuit

**English (stimulus):** After he had ruled the great year with twelve fasces, which was sacred because the world was freed

**Expected:** no error. Another model's real rendering that gets the H-11 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-12  ·  `seg_p0040_s0002`  ·  rendered by gemini-3-1-pro

**Latin:** Et Sophronius patriarcha Hierosolymitanus, in sermone de natali apostolorum, Paulum Hispanis et Britannis evangelium prædicasse significat

**English (stimulus):** And Sophronius, patriarch of Jerusalem, in his sermon on the nativity of the apostles, indicates that Paul preached the gospel to the Spaniards and the Britons

**Proposed MQM:**
- `nativity of the apostles` · Terminology / Wrong-term / **minor**

**Why the Latin forces it:** natalis of saints = their feast (heavenly birthday, i.e. martyrdom day), a liturgical term; 'nativity' = physical birth.

*Correct counterpart (opus-4-8):* And Sophronius, patriarch of Jerusalem, in his sermon on the feast of the apostles, indicates that Paul preached the gospel to the Spaniards and the Britons

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-12__neg  ·  `seg_p0040_s0002`  ·  rendered by opus-4-8

**Latin:** Et Sophronius patriarcha Hierosolymitanus, in sermone de natali apostolorum, Paulum Hispanis et Britannis evangelium prædicasse significat

**English (stimulus):** And Sophronius, patriarch of Jerusalem, in his sermon on the feast of the apostles, indicates that Paul preached the gospel to the Spaniards and the Britons

**Expected:** no error. Another model's real rendering that gets the H-12 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### H-13  ·  `seg_p0052_s0002`  ·  rendered by gemini-3-1-pro

**Latin:** De duodecim discipulis a B. Philippo in Britanniam missis, Malmesburiensis quidam monachus in eulogii sui libro secundo hunc in modum meminit

**English (stimulus):** Concerning the twelve disciples sent into Britain by the blessed Philip, a certain monk of Malmesbury records in the second book of his eulogy in this manner

**Proposed MQM:**
- `his eulogy` · Terminology / Wrong-term / **minor**

**Why the Latin forces it:** Eulogium is the title of a chronicle (Eulogium historiarum), cited again in p0063 and p0067. 'his eulogy' turns it into a speech of praise.

*Correct counterpart (fable-5):* Concerning the twelve disciples sent into Britain by the blessed Philip, a certain monk of Malmesbury makes mention in the second book of his "Eulogium" in this manner

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### H-13__neg  ·  `seg_p0052_s0002`  ·  rendered by fable-5

**Latin:** De duodecim discipulis a B. Philippo in Britanniam missis, Malmesburiensis quidam monachus in eulogii sui libro secundo hunc in modum meminit

**English (stimulus):** Concerning the twelve disciples sent into Britain by the blessed Philip, a certain monk of Malmesbury makes mention in the second book of his "Eulogium" in this manner

**Expected:** no error. Another model's real rendering that gets the H-13 point right; needs a full check that it is clean.

`[ ] clean` `[ ] has an error:` ______

---

### S-01  ·  `seg_p0055_s0002`  ·  rendered by opus-4-8 + planted edit

**Latin:** et quod tres reges pagani ipsis duodecim, ad eorum sustenementum, duodecim portiones terræ dederunt.

**English (stimulus):** and that three pagan kings each gave those twelve men twelve portions of land for their sustenance

**Change vs real base (opus-4-8):** and that three pagan kings **each** gave those twelve men twelve portions of land for their sustenance

*Mechanism:* distributive scope (modeled on H-01)

**Proposed MQM:**
- `each gave` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** No distributive in the Latin: the three kings together gave twelve portions (the Twelve Hides). 'each' makes thirty-six.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-01__neg  ·  `seg_p0055_s0002`  ·  rendered by opus-4-8

**Latin:** et quod tres reges pagani ipsis duodecim, ad eorum sustenementum, duodecim portiones terræ dederunt.

**English (stimulus):** and that three pagan kings gave those twelve men twelve portions of land for their sustenance

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-02  ·  `seg_p0060_s0002`  ·  rendered by opus-4-8 + planted edit

**Latin:** quum adversus Hispanos, Scotos et Gallos coram Martino V. ab Anglis renovata esset hæc controversia.

**English (stimulus):** when this controversy had been revived by the Spaniards, the Scots, and the French against the English before Martin V.

**Change vs real base (opus-4-8):** when this controversy had been revived by the ~~English against the~~ Spaniards, the Scots, and the French **against the English** before Martin V.

*Mechanism:* who did what to whom (modeled on H-02)

**Proposed MQM:**
- `by the Spaniards, the Scots, and the French against the English` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** ab Anglis = by the English (agent); adversus Hispanos ... = against the Spaniards. The swap reverses who renewed the dispute.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-02__neg  ·  `seg_p0060_s0002`  ·  rendered by opus-4-8

**Latin:** quum adversus Hispanos, Scotos et Gallos coram Martino V. ab Anglis renovata esset hæc controversia.

**English (stimulus):** when this controversy had been revived by the English against the Spaniards, the Scots, and the French before Martin V.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-03  ·  `seg_p0060_s0004`  ·  rendered by opus-4-8 + planted edit

**Latin:** Ille ergo qui dicit, probat

**English (stimulus):** He therefore who denies the assertion must prove it

**Change vs real base (opus-4-8):** He therefore who ~~makes~~ **denies** the assertion must prove it

*Mechanism:* who did what to whom (modeled on H-02)

**Proposed MQM:**
- `denies the assertion` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** qui dicit = he who asserts (the legal maxim). The next sentence ('the burden of proof does not rest upon the one who denies') shows the reversal is wrong.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-03__neg  ·  `seg_p0060_s0004`  ·  rendered by opus-4-8

**Latin:** Ille ergo qui dicit, probat

**English (stimulus):** He therefore who makes the assertion must prove it

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-04  ·  `seg_p0064_s0001`  ·  rendered by opus-4-8 + planted edit

**Latin:** non quidem in muro, sed in Caiphæ carcere detentum

**English (stimulus):** was held not indeed within a wall but in the prison of Pilate

**Change vs real base (opus-4-8):** was held not indeed within a wall but in the prison of ~~Caiaphas~~ **Pilate**

*Mechanism:* substitution inside the legend (modeled on H-03)

**Proposed MQM:**
- `the prison of Pilate` · Accuracy / Entity / **major**

**Why the Latin forces it:** in Caiphæ carcere = Caiaphas' prison (Harding's version). Pilate is the natural Passion-story substitute.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-04__neg  ·  `seg_p0064_s0001`  ·  rendered by opus-4-8

**Latin:** non quidem in muro, sed in Caiphæ carcere detentum

**English (stimulus):** was held not indeed within a wall but in the prison of Caiaphas

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-05  ·  `seg_p0066_s0007`  ·  rendered by opus-4-8 + planted edit

**Latin:** et quod attulerit secum duo vasa argentea non grandia, in quibus erat de sanguine et aqua sacratissima, quæ profluxerat de latere Christi mortui.

**English (stimulus):** and that he brought with him two small silver vessels, in which was some of the most sacred blood and water that had flowed from the hands of the dead Christ.

**Change vs real base (opus-4-8):** and that he brought with him two small silver vessels, in which was some of the most sacred blood and water that had flowed from the ~~side~~ **hands** of the dead Christ.

*Mechanism:* substitution inside the legend (modeled on H-03)

**Proposed MQM:**
- `from the hands of the dead Christ` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** de latere = from the side (the spear wound, Jn 19:34, the source of 'blood and water').

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-05__neg  ·  `seg_p0066_s0007`  ·  rendered by opus-4-8

**Latin:** et quod attulerit secum duo vasa argentea non grandia, in quibus erat de sanguine et aqua sacratissima, quæ profluxerat de latere Christi mortui.

**English (stimulus):** and that he brought with him two small silver vessels, in which was some of the most sacred blood and water that had flowed from the side of the dead Christ.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-06  ·  `seg_p0054_s0001`  ·  rendered by gemini-3-1-pro + planted edit

**Latin:** Isti viri certe divino spiritu aﬄati, cum a rege parum terræ ad inhabitandum (proxime Welliam oppidum, circiter millia passuum quatuor) dono accepissent, ibi novæ religionis prima jecerunt fundamenta

**English (stimulus):** These men, certainly inspired by the divine spirit, in order to receive as a gift from the king a small piece of land to inhabit (near the town of Wells, about four miles away), laid the first foundations of the new religion there

**Change vs real base (gemini-3-1-pro):** These men, certainly inspired by the divine spirit, ~~having received~~ **in order to receive** as a gift from the king a small piece of land to inhabit (near the town of Wells, about four miles away), laid the first foundations of the new religion there

*Mechanism:* clause relation (circumstance vs purpose) (modeled on H-04)

**Proposed MQM:**
- `in order to receive` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** cum + pluperfect subjunctive (accepissent) = having received: the gift came first. A purpose clause reverses the sequence.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-06__neg  ·  `seg_p0054_s0001`  ·  rendered by gemini-3-1-pro

**Latin:** Isti viri certe divino spiritu aﬄati, cum a rege parum terræ ad inhabitandum (proxime Welliam oppidum, circiter millia passuum quatuor) dono accepissent, ibi novæ religionis prima jecerunt fundamenta

**English (stimulus):** These men, certainly inspired by the divine spirit, having received as a gift from the king a small piece of land to inhabit (near the town of Wells, about four miles away), laid the first foundations of the new religion there

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-07  ·  `seg_p0035_s0004`  ·  rendered by gemini-3-1-pro + planted edit

**Latin:** Quod profecto divina providentia ita tunc Cæsaris sensibus ingessit, ut absque ullo obstaculo, in ipsis duntaxat initiis Evangelii sermo usquequaque percurreret.

**English (stimulus):** Divine providence surely instilled this into Caesar's mind at that time, because without any obstacle, at the very beginnings of the Gospel, its word ran everywhere.

**Change vs real base (gemini-3-1-pro):** Divine providence surely instilled this into Caesar's mind at that time, ~~so that~~ **because** without any obstacle, at the very beginnings of the Gospel, its word ~~might run~~ **ran** everywhere.

*Mechanism:* clause relation (result vs cause) (modeled on H-04)

**Proposed MQM:**
- `because without any obstacle, at the very beginnings of the Gospel, its word ran everywhere` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** ita ... ut + subjunctive = so that (result): providence acted in order that the word could spread. 'because' makes the spread the cause.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-07__neg  ·  `seg_p0035_s0004`  ·  rendered by gemini-3-1-pro

**Latin:** Quod profecto divina providentia ita tunc Cæsaris sensibus ingessit, ut absque ullo obstaculo, in ipsis duntaxat initiis Evangelii sermo usquequaque percurreret.

**English (stimulus):** Divine providence surely instilled this into Caesar's mind at that time, so that without any obstacle, at the very beginnings of the Gospel, its word might run everywhere.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-08  ·  `seg_p0060_s0005`  ·  rendered by gemini-3-1-pro + planted edit

**Latin:** Potest autem dici quod eductus cum a prædicatione non cessaret, iterum sit ab ipsis Judæis inclusus.

**English (stimulus):** But it can be said that, having been brought out, although he did not cease from preaching, he was again enclosed by the Jews themselves.

**Change vs real base (gemini-3-1-pro):** But it can be said that, having been brought out, ~~since~~ **although** he did not cease from preaching, he was again enclosed by the Jews themselves.

*Mechanism:* cum-clause type (causal vs concessive) (modeled on v1 cum->when)

**Proposed MQM:**
- `although` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** cum + subjunctive is causal here: he was re-imprisoned BECAUSE he kept preaching. 'although' breaks the explanation.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-08__neg  ·  `seg_p0060_s0005`  ·  rendered by gemini-3-1-pro

**Latin:** Potest autem dici quod eductus cum a prædicatione non cessaret, iterum sit ab ipsis Judæis inclusus.

**English (stimulus):** But it can be said that, having been brought out, since he did not cease from preaching, he was again enclosed by the Jews themselves.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-09  ·  `seg_p0057_s0001`  ·  rendered by gemini-3-1-pro + planted edit

**Latin:** Ex Juvenale vero constat Arviragum Domitiano imperante regem Britannorum extitisse: quum sub Vespasiano anno LXXVI. Josephus noster obiisse dicatur.

**English (stimulus):** But from Juvenal it is clear that Arviragus was king of the Britons during the reign of Domitian, whereas our Joseph is known to have died under Vespasian in the year 76.

**Change vs real base (gemini-3-1-pro):** But from Juvenal it is clear that Arviragus was king of the Britons during the reign of Domitian, whereas our Joseph is ~~said~~ **known** to have died under Vespasian in the year 76.

*Mechanism:* imported stance (modeled on H-05)

**Proposed MQM:**
- `is known to have died` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** dicatur = is SAID (reported tradition, which Ussher is testing). 'is known' turns the tradition into established fact.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-09__neg  ·  `seg_p0057_s0001`  ·  rendered by gemini-3-1-pro

**Latin:** Ex Juvenale vero constat Arviragum Domitiano imperante regem Britannorum extitisse: quum sub Vespasiano anno LXXVI. Josephus noster obiisse dicatur.

**English (stimulus):** But from Juvenal it is clear that Arviragus was king of the Britons during the reign of Domitian, whereas our Joseph is said to have died under Vespasian in the year 76.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-10  ·  `seg_p0066_s0003`  ·  rendered by opus-4-8 + planted edit

**Latin:** Quem habuerit eventum ista inquisitio, non invenio: ab his tamen qui Glastoniense monasterium viderunt est proditum, et sacellum ibi Josephi nomini dicatum, et tumulum etiam positum fuisse, hoc inscriptum epitaphio.

**English (stimulus):** What outcome that inquiry had I do not find; yet it has been reliably reported by those who saw the monastery of Glastonbury that a chapel there was dedicated to the name of Joseph, and that a tomb was also set up, inscribed with this epitaph.

**Change vs real base (opus-4-8):** What outcome that inquiry had I do not find; yet it has been **reliably** reported by those who saw the monastery of Glastonbury that a chapel there was dedicated to the name of Joseph, and that a tomb was also set up, inscribed with this epitaph.

*Mechanism:* imported stance (modeled on H-05)

**Proposed MQM:**
- `reliably` · Accuracy / Addition / **minor**

**Why the Latin forces it:** Nothing in the Latin vouches for the report (est proditum = it has been handed down). 'reliably' adds an endorsement Ussher does not give.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-10__neg  ·  `seg_p0066_s0003`  ·  rendered by opus-4-8

**Latin:** Quem habuerit eventum ista inquisitio, non invenio: ab his tamen qui Glastoniense monasterium viderunt est proditum, et sacellum ibi Josephi nomini dicatum, et tumulum etiam positum fuisse, hoc inscriptum epitaphio.

**English (stimulus):** What outcome that inquiry had I do not find; yet it has been reported by those who saw the monastery of Glastonbury that a chapel there was dedicated to the name of Joseph, and that a tomb was also set up, inscribed with this epitaph.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-11  ·  `seg_p0058_s0002`  ·  rendered by opus-4-8 + planted edit

**Latin:** Ejus hæc producuntur verba, quæ ex variis exemplaribus descripta hic exhibemus, licet quæ legantur prorsus indigna.

**English (stimulus):** These words of his are put forward, which I set out here as copied from various examples, although they are utterly unworthy of being read.

**Change vs real base (opus-4-8):** These words of his are put forward, which I set out here as copied from various ~~exemplars,~~ **examples,** although they are utterly unworthy of being read.

*Mechanism:* false friend (modeled on H-06)

**Proposed MQM:**
- `various examples` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** exemplaria = manuscript copies (exemplars) of a text, not 'examples'. Ussher is collating copies of Melkin's text.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-11__neg  ·  `seg_p0058_s0002`  ·  rendered by opus-4-8

**Latin:** Ejus hæc producuntur verba, quæ ex variis exemplaribus descripta hic exhibemus, licet quæ legantur prorsus indigna.

**English (stimulus):** These words of his are put forward, which I set out here as copied from various exemplars, although they are utterly unworthy of being read.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-12  ·  `seg_p0049_s0001`  ·  rendered by fable-5 + planted edit

**Latin:** Nam præterquam quod Isidorus in hoc ipso opere, capite secundo et octogesimo et in officio Toletano, quod Gothicum et Mozarabum vulgo appellatur

**English (stimulus):** For besides the fact that Isidore, in this very work, at chapter 82, and in the Toledan council, which is commonly called the Gothic and Mozarabic

**Change vs real base (fable-5):** For besides the fact that Isidore, in this very work, at chapter 82, and in the Toledan ~~office,~~ **council,** which is commonly called the Gothic and Mozarabic

*Mechanism:* technical/liturgical term (modeled on H-12)

**Proposed MQM:**
- `the Toledan council` · Terminology / Wrong-term / **minor**

**Why the Latin forces it:** officium = the liturgical office (the Mozarabic rite). The Councils of Toledo are famous, which makes 'council' a plausible substitute.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-12__neg  ·  `seg_p0049_s0001`  ·  rendered by fable-5

**Latin:** Nam præterquam quod Isidorus in hoc ipso opere, capite secundo et octogesimo et in officio Toletano, quod Gothicum et Mozarabum vulgo appellatur

**English (stimulus):** For besides the fact that Isidore, in this very work, at chapter 82, and in the Toledan office, which is commonly called the Gothic and Mozarabic

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-13  ·  `seg_p0046_s0003`  ·  rendered by gemini-3-1-pro + planted edit

**Latin:** Sic igitur ille, præmissa præfatione ad Henricum Blesensem, Henrici I. regis ex Adela sorore nepotem, Wintoniensem tum episcopum et Glastoniensem abbatem, archæologiam suam ab apostolicis exorditur temporibus.

**English (stimulus):** Thus, having prefixed a preface by Henry of Blois, nephew of King Henry I by his sister Adela, and at that time bishop of Winchester and abbot of Glastonbury, he begins his ancient history from apostolic times.

**Change vs real base (gemini-3-1-pro):** Thus, having prefixed a preface ~~to~~ **by** Henry of Blois, nephew of King Henry I by his sister Adela, and at that time bishop of Winchester and abbot of Glastonbury, he begins his ancient history from apostolic times.

*Mechanism:* addressee (ad) vs author (modeled on H-07)

**Proposed MQM:**
- `a preface by Henry of Blois` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** praefatione ad Henricum = a preface addressed TO Henry (Malmesbury's dedicatee). 'by' makes Henry the author.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-13__neg  ·  `seg_p0046_s0003`  ·  rendered by gemini-3-1-pro

**Latin:** Sic igitur ille, præmissa præfatione ad Henricum Blesensem, Henrici I. regis ex Adela sorore nepotem, Wintoniensem tum episcopum et Glastoniensem abbatem, archæologiam suam ab apostolicis exorditur temporibus.

**English (stimulus):** Thus, having prefixed a preface to Henry of Blois, nephew of King Henry I by his sister Adela, and at that time bishop of Winchester and abbot of Glastonbury, he begins his ancient history from apostolic times.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-14  ·  `seg_p0040_s0001`  ·  rendered by opus-4-8 + planted edit

**Latin:** et post primam apologiam, cujus ipse in posteriore ad Timotheum epistola meminit, a Nerone dimissum, evangelium Christi in occidentis quoque partibus prædicavisse.

**English (stimulus):** and that, after his first defense — which he himself mentions in the later epistle to Timothy — having been released under Nero, he preached the gospel of Christ in the regions of the West as well.

**Change vs real base (opus-4-8):** and that, after his first defense — which he himself mentions in the later epistle to Timothy — having been released ~~by~~ **under** Nero, he preached the gospel of Christ in the regions of the West as well.

*Mechanism:* agent vs circumstance (modeled on H-07)

**Proposed MQM:**
- `released under Nero` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** a Nerone dimissum = released BY Nero (agent: Nero himself acquitted him). 'under Nero' reduces it to a date.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-14__neg  ·  `seg_p0040_s0001`  ·  rendered by opus-4-8

**Latin:** et post primam apologiam, cujus ipse in posteriore ad Timotheum epistola meminit, a Nerone dimissum, evangelium Christi in occidentis quoque partibus prædicavisse.

**English (stimulus):** and that, after his first defense — which he himself mentions in the later epistle to Timothy — having been released by Nero, he preached the gospel of Christ in the regions of the West as well.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-15  ·  `seg_p0038_s0002`  ·  rendered by opus-4-8 + planted edit

**Latin:** Romæ hos a sanctis apostolis episcopos ordinatos, et ad prædicandum verbum Dei in Hispanias directos esse

**English (stimulus):** these men were ordained bishops at Rome for the holy apostles, and were sent into Spain to preach the word of God

**Change vs real base (opus-4-8):** these men were ordained bishops at Rome ~~by~~ **for** the holy apostles, and were sent into Spain to preach the word of God

*Mechanism:* agent vs beneficiary (modeled on H-07)

**Proposed MQM:**
- `for the holy apostles` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** a sanctis apostolis ordinatos = ordained BY the apostles (the claim to apostolic consecration). 'for' leaves the ordainer unnamed.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-15__neg  ·  `seg_p0038_s0002`  ·  rendered by opus-4-8

**Latin:** Romæ hos a sanctis apostolis episcopos ordinatos, et ad prædicandum verbum Dei in Hispanias directos esse

**English (stimulus):** these men were ordained bishops at Rome by the holy apostles, and were sent into Spain to preach the word of God

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-16  ·  `seg_p0048_s0002`  ·  rendered by fable-5 + planted edit

**Latin:** Quod autem de Philippi in Galliis apostolatu habet Freculphus a Malmesburiensi citatus; ex Isidori libro de patribus utriusque Testamenti ad verbum expressit.

**English (stimulus):** But what Freculphus, citing Malmesbury, has concerning Philip's apostolate in the Gauls, he copied word for word from Isidore's book “On the Fathers of Both Testaments”

**Change vs real base (fable-5):** But what Freculphus, ~~cited by~~ **citing** Malmesbury, has concerning Philip's apostolate in the Gauls, he copied word for word from Isidore's book “On the Fathers of Both Testaments”

*Mechanism:* agent vs subject (passive participle) (modeled on H-07)

**Proposed MQM:**
- `citing Malmesbury` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** a Malmesburiensi citatus = cited BY Malmesbury: the 12th-c. writer quotes the 9th-c. Freculph. 'citing' reverses the dependence (and the chronology).

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-16__neg  ·  `seg_p0048_s0002`  ·  rendered by fable-5

**Latin:** Quod autem de Philippi in Galliis apostolatu habet Freculphus a Malmesburiensi citatus; ex Isidori libro de patribus utriusque Testamenti ad verbum expressit.

**English (stimulus):** But what Freculphus, cited by Malmesbury, has concerning Philip's apostolate in the Gauls, he copied word for word from Isidore's book “On the Fathers of Both Testaments”

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-17  ·  `seg_p0053_s0001`  ·  rendered by opus-4-8 + planted edit

**Latin:** Monachi tamen ibidem aliam prætendunt fundationem a rege Arvirago (filio Kimbelini regis Britonum, in cujus tempore Christus Jesus de Maria virgine natus fuit)

**English (stimulus):** The monks there, however, allege another foundation, by king Arviragus (in whose time Christ Jesus was born of the Virgin Mary, son of Kimbelinus king of the Britons)

**Change vs real base (opus-4-8):** The monks there, however, allege another foundation, by king Arviragus ~~(son of Kimbelinus king of the Britons, in~~ **(in** whose time Christ Jesus was born of the Virgin ~~Mary)~~ **Mary, son of Kimbelinus king of the Britons)**

*Mechanism:* relative-pronoun antecedent (modeled on H-11)

**Proposed MQM:**
- `in whose time Christ Jesus was born of the Virgin Mary, son of Kimbelinus king of the Britons` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** cujus refers to Kimbelinus (Christ was born in Cymbeline's reign). Moving the clause attaches it to Arviragus and shifts the chronology a generation.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-17__neg  ·  `seg_p0053_s0001`  ·  rendered by opus-4-8

**Latin:** Monachi tamen ibidem aliam prætendunt fundationem a rege Arvirago (filio Kimbelini regis Britonum, in cujus tempore Christus Jesus de Maria virgine natus fuit)

**English (stimulus):** The monks there, however, allege another foundation, by king Arviragus (son of Kimbelinus king of the Britons, in whose time Christ Jesus was born of the Virgin Mary)

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-18  ·  `seg_p0042_s0002`  ·  rendered by opus-4-8 + planted edit

**Latin:** In fine posterioris ad Timotheum epistolæ, commemorantur simul ab apostolo Pudens, et Linus, et Claudia.

**English (stimulus):** At the end of the latter epistle of Timothy, Pudens, and Linus, and Claudia are mentioned together by the apostle.

**Change vs real base (opus-4-8):** At the end of the latter epistle ~~to~~ **of** Timothy, Pudens, and Linus, and Claudia are mentioned together by the apostle.

*Mechanism:* addressee (ad) vs author (modeled on H-02)

**Proposed MQM:**
- `epistle of Timothy` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** ad Timotheum = TO Timothy (Paul's letter). 'of Timothy' reads as a letter by Timothy, which clashes with 'by the apostle'.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-18__neg  ·  `seg_p0042_s0002`  ·  rendered by opus-4-8

**Latin:** In fine posterioris ad Timotheum epistolæ, commemorantur simul ab apostolo Pudens, et Linus, et Claudia.

**English (stimulus):** At the end of the latter epistle to Timothy, Pudens, and Linus, and Claudia are mentioned together by the apostle.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-19  ·  `seg_p0067_s0003`  ·  rendered by opus-4-8 + planted edit

**Latin:** Joseph vero ab Arimathia ibidem sepultus est juxta dictam Ecclesiam [B. Mariæ] cum duabus phialis plenis de sudore Christi sanguineo, quas secum de terra sancta detulerat.

**English (stimulus):** Joseph of Arimathea indeed was buried there beside the said church [of the Blessed Mary], with two vials filled with the bloody sweat of Christ, which had been brought to him from the Holy Land.

**Change vs real base (opus-4-8):** Joseph of Arimathea indeed was buried there beside the said church [of the Blessed Mary], with two vials filled with the bloody sweat of Christ, which ~~he~~ had **been** brought ~~with~~ **to** him from the Holy Land.

*Mechanism:* reflexive/agent attachment (modeled on H-10)

**Proposed MQM:**
- `which had been brought to him` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** quas secum ... detulerat = which HE had brought WITH HIMSELF (secum, active). The edit has others bring them to him.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-19__neg  ·  `seg_p0067_s0003`  ·  rendered by opus-4-8

**Latin:** Joseph vero ab Arimathia ibidem sepultus est juxta dictam Ecclesiam [B. Mariæ] cum duabus phialis plenis de sudore Christi sanguineo, quas secum de terra sancta detulerat.

**English (stimulus):** Joseph of Arimathea indeed was buried there beside the said church [of the Blessed Mary], with two vials filled with the bloody sweat of Christ, which he had brought with him from the Holy Land.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-20  ·  `seg_p0065_s0003`  ·  rendered by gemini-3-1-pro + planted edit

**Latin:** dum tamen absque damno dilectorum nobis in Christo, abbatis et conventus dicti monasterii, et ruina ecclesiæ et domorum suarum ibidem id fieri valeat

**English (stimulus):** provided, however, that this can be done without damage from our beloved in Christ, the abbot and convent of the said monastery, and without the ruin of their church and houses there

**Change vs real base (gemini-3-1-pro):** provided, however, that this can be done without damage ~~to~~ **from** our beloved in Christ, the abbot and convent of the said monastery, and without the ruin of their church and houses there

*Mechanism:* person affected vs source (modeled on H-10)

**Proposed MQM:**
- `without damage from our beloved in Christ` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** absque damno dilectorum = without loss TO the abbot and convent (objective genitive: they are protected). 'from' makes them the threat.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-20__neg  ·  `seg_p0065_s0003`  ·  rendered by gemini-3-1-pro

**Latin:** dum tamen absque damno dilectorum nobis in Christo, abbatis et conventus dicti monasterii, et ruina ecclesiæ et domorum suarum ibidem id fieri valeat

**English (stimulus):** provided, however, that this can be done without damage to our beloved in Christ, the abbot and convent of the said monastery, and without the ruin of their church and houses there

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-21  ·  `seg_p0066_s0005`  ·  rendered by opus-4-8 + planted edit

**Latin:** observatio festi S. Josephi ad VI. Calendas Augusti

**English (stimulus):** the observance of the feast of St. Joseph on the sixth day after the Kalends of August

**Change vs real base (opus-4-8):** the observance of the feast of St. Joseph on the sixth day ~~before~~ **after** the Kalends of August

*Mechanism:* technical/calendar term (modeled on H-12)

**Proposed MQM:**
- `after the Kalends of August` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** ad VI. Calendas = the 6th day BEFORE the Kalends (27 July); Roman dates count backwards. 'after' gives 6 August.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-21__neg  ·  `seg_p0066_s0005`  ·  rendered by opus-4-8

**Latin:** observatio festi S. Josephi ad VI. Calendas Augusti

**English (stimulus):** the observance of the feast of St. Joseph on the sixth day before the Kalends of August

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-22  ·  `seg_p0039_s0002`  ·  rendered by opus-4-8 + planted edit

**Latin:** In martyrologio tamen et breviario Romano, ut et in Bedæ, Usuardi, atque Adonis martyrologiis, ad Octobris diem octavum et vigesimum in Perside martyrium subiisse legitur.

**English (stimulus):** Yet in the Roman Martyrology and Missal, as also in the martyrologies of Bede, Usuard, and Ado, he is recorded under the twenty-eighth day of October to have undergone martyrdom in Persia.

**Change vs real base (opus-4-8):** Yet in the Roman Martyrology and ~~Breviary,~~ **Missal,** as also in the martyrologies of Bede, Usuard, and Ado, he is recorded under the twenty-eighth day of October to have undergone martyrdom in Persia.

*Mechanism:* technical/liturgical term (modeled on H-12)

**Proposed MQM:**
- `Missal` · Terminology / Wrong-term / **minor**

**Why the Latin forces it:** breviarium = the Breviary (Divine Office), where saints' lessons are read. The Missal is a different liturgical book.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-22__neg  ·  `seg_p0039_s0002`  ·  rendered by opus-4-8

**Latin:** In martyrologio tamen et breviario Romano, ut et in Bedæ, Usuardi, atque Adonis martyrologiis, ad Octobris diem octavum et vigesimum in Perside martyrium subiisse legitur.

**English (stimulus):** Yet in the Roman Martyrology and Breviary, as also in the martyrologies of Bede, Usuard, and Ado, he is recorded under the twenty-eighth day of October to have undergone martyrdom in Persia.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-23  ·  `seg_p0061_s0001`  ·  rendered by opus-4-8 + planted edit

**Latin:** adhuc tamen Hispani primo susceperunt fidem, quod probatur, quia Jacobus martyrium subiit vivente Petro.

**English (stimulus):** the Spaniards still received the faith first; and this is proved because Peter suffered martyrdom while James was still alive.

**Change vs real base (opus-4-8):** the Spaniards still received the faith first; and this is proved because ~~James~~ **Peter** suffered martyrdom while ~~Peter~~ **James** was still alive.

*Mechanism:* who did what (ablative absolute) (modeled on v1 them/him)

**Proposed MQM:**
- `Peter suffered martyrdom while James was still alive` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** Jacobus ... subiit vivente Petro = James was martyred while Peter lived (ablative absolute). The swap reverses the order the argument depends on.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-23__neg  ·  `seg_p0061_s0001`  ·  rendered by opus-4-8

**Latin:** adhuc tamen Hispani primo susceperunt fidem, quod probatur, quia Jacobus martyrium subiit vivente Petro.

**English (stimulus):** the Spaniards still received the faith first; and this is proved because James suffered martyrdom while Peter was still alive.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-24  ·  `seg_p0061_s0003`  ·  rendered by fable-5 + planted edit

**Latin:** quod Joseph ab Arimathia cum duodecim sociis, aut ex persecutione Herodiana, vel præsidum Romanorum in Judæa, ad Angliam vectus est. Ibidem, quæ de Christo viderat et audierat prædicavit, et prædicando plures convertit

**English (stimulus):** that Joseph of Arimathea, with twelve companions, driven either by the Herodian persecution or by that of the Roman governors in Judaea, was carried over to England; there Peter preached what he had seen and heard concerning Christ, and by preaching converted many

**Change vs real base (fable-5):** that Joseph of Arimathea, with twelve companions, driven either by the Herodian persecution or by that of the Roman governors in Judaea, was carried over to England; there ~~he~~ **Peter** preached what he had seen and heard concerning Christ, and by preaching converted many

*Mechanism:* wrong referent (modeled on v1 illo->Pudens)

**Proposed MQM:**
- `there Peter preached` · Accuracy / Entity / **major**

**Why the Latin forces it:** The subject of praedicavit is still Joseph. Peter is named in the same sentence a little later (preaching at Antioch), which makes the slip plausible.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-24__neg  ·  `seg_p0061_s0003`  ·  rendered by fable-5

**Latin:** quod Joseph ab Arimathia cum duodecim sociis, aut ex persecutione Herodiana, vel præsidum Romanorum in Judæa, ad Angliam vectus est. Ibidem, quæ de Christo viderat et audierat prædicavit, et prædicando plures convertit

**English (stimulus):** that Joseph of Arimathea, with twelve companions, driven either by the Herodian persecution or by that of the Roman governors in Judaea, was carried over to England; there he preached what he had seen and heard concerning Christ, and by preaching converted many

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-25  ·  `seg_p0045_s0001`  ·  rendered by opus-4-8 + planted edit

**Latin:** Nerone vero summam rerum obtinente (et quidem, ut pluribus placet, sub finem imperii illius) a Paulo illa scripta est epistola, in qua Timotheum salutant Pudens et Linus et Claudia.

**English (stimulus):** While Nero held the supreme power (and indeed, as most hold, toward the end of his reign), Paul wrote that epistle in which Pudens, Linus, and Claudia greet Paul.

**Change vs real base (opus-4-8):** While Nero held the supreme power (and indeed, as most hold, toward the end of his reign), Paul wrote that epistle in which Pudens, Linus, and Claudia greet ~~Timothy.~~ **Paul.**

*Mechanism:* wrong referent (modeled on v1 illo->Pudens)

**Proposed MQM:**
- `greet Paul` · Accuracy / Entity / **major**

**Why the Latin forces it:** Timotheum salutant = they greet TIMOTHY (the addressee). Paul is the writer.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-25__neg  ·  `seg_p0045_s0001`  ·  rendered by opus-4-8

**Latin:** Nerone vero summam rerum obtinente (et quidem, ut pluribus placet, sub finem imperii illius) a Paulo illa scripta est epistola, in qua Timotheum salutant Pudens et Linus et Claudia.

**English (stimulus):** While Nero held the supreme power (and indeed, as most hold, toward the end of his reign), Paul wrote that epistle in which Pudens, Linus, and Claudia greet Timothy.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-26  ·  `seg_p0042_s0004`  ·  rendered by opus-4-8 + planted edit

**Latin:** Patrem vero Lini Herculanum quendam fuisse liber pontificalis asserit.

**English (stimulus):** The Book of the Pontiffs, however, asserts that Linus was the father of a certain Herculanus.

**Change vs real base (opus-4-8):** The Book of the Pontiffs, however, asserts that **Linus was** the father of ~~Linus was~~ a certain Herculanus.

*Mechanism:* identification vs predication (double accusative) (modeled on H-08)

**Proposed MQM:**
- `Linus was the father of a certain Herculanus` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** Patrem Lini = the father OF LINUS (genitive); Herculanum is the predicate. The edit reverses the relationship.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-26__neg  ·  `seg_p0042_s0004`  ·  rendered by opus-4-8

**Latin:** Patrem vero Lini Herculanum quendam fuisse liber pontificalis asserit.

**English (stimulus):** The Book of the Pontiffs, however, asserts that the father of Linus was a certain Herculanus.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-27  ·  `seg_p0060_s0003`  ·  rendered by fable-5 + planted edit

**Latin:** Et post non longo tempore a passione Christi, Eleutherius papa regnum Angliæ totaliter convertit ad fidem.

**English (stimulus):** And not long before the passion of Christ, Pope Eleutherius converted the kingdom of England wholly to the faith.

**Change vs real base (fable-5):** And not long ~~after~~ **before** the passion of Christ, Pope Eleutherius converted the kingdom of England wholly to the faith.

*Mechanism:* temporal relation (modeled on H-04)

**Proposed MQM:**
- `not long before the passion` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** post ... a passione = AFTER the Passion. 'before' puts a pope's conversion of England before Christ's death.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-27__neg  ·  `seg_p0060_s0003`  ·  rendered by fable-5

**Latin:** Et post non longo tempore a passione Christi, Eleutherius papa regnum Angliæ totaliter convertit ad fidem.

**English (stimulus):** And not long after the passion of Christ, Pope Eleutherius converted the kingdom of England wholly to the faith.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-28  ·  `seg_p0063_s0002`  ·  rendered by fable-5 + planted edit

**Latin:** Quod et cum ipsius Josephi ætate, qui Domino passionem adeunte inter Judæos senator honoratus fuerat

**English (stimulus):** which agrees well both with the age of Joseph himself, who, after the Lord went to his passion, became an honored senator among the Jews

**Change vs real base (fable-5):** which agrees well both with the age of Joseph himself, who, ~~when~~ **after** the Lord went to his passion, ~~had been~~ **became** an honored senator among the Jews

*Mechanism:* temporal relation (ablative absolute + pluperfect) (modeled on H-04)

**Proposed MQM:**
- `after the Lord went to his passion, became` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** Domino passionem adeunte = when the Lord was going to his Passion; fuerat = had (already) been a senator. The point is that Joseph was already senior then.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-28__neg  ·  `seg_p0063_s0002`  ·  rendered by fable-5

**Latin:** Quod et cum ipsius Josephi ætate, qui Domino passionem adeunte inter Judæos senator honoratus fuerat

**English (stimulus):** which agrees well both with the age of Joseph himself, who, when the Lord went to his passion, had been an honored senator among the Jews

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-29  ·  `seg_p0039_s0003`  ·  rendered by opus-4-8 + planted edit

**Latin:** Simonem Petrum, “ duodecim quidem annos esse versatum in oriente, viginti autem et tres annos transegisse Romæ, et in Britannia, et in civitatibus quæ sunt in occidente,” retulit alicubi Eusebius Pamphili

**English (stimulus):** Eusebius Pamphili reports somewhere that Simon Peter “spent twenty-three years in the East, but passed twelve years at Rome, and in Britain, and in the cities which lie in the West”

**Change vs real base (opus-4-8):** Eusebius Pamphili reports somewhere that Simon Peter “spent ~~twelve~~ **twenty-three** years in the East, but passed ~~twenty-three~~ **twelve** years at Rome, and in Britain, and in the cities which lie in the West”

*Mechanism:* number-to-place mapping (modeled on LITERA deity swap (v1))

**Proposed MQM:**
- `spent twenty-three years in the East, but passed twelve years at Rome` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** duodecim ... in oriente, viginti et tres ... Romae = twelve years in the East, twenty-three in Rome and the West. The swap reverses where Peter spent most of his ministry.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-29__neg  ·  `seg_p0039_s0003`  ·  rendered by opus-4-8

**Latin:** Simonem Petrum, “ duodecim quidem annos esse versatum in oriente, viginti autem et tres annos transegisse Romæ, et in Britannia, et in civitatibus quæ sunt in occidente,” retulit alicubi Eusebius Pamphili

**English (stimulus):** Eusebius Pamphili reports somewhere that Simon Peter “spent twelve years in the East, but passed twenty-three years at Rome, and in Britain, and in the cities which lie in the West”

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-30  ·  `seg_p0062_s0002`  ·  rendered by opus-4-8 + planted edit

**Latin:** nec integra regna ab ullo apostolorum Christiana facta esse constat

**English (stimulus):** nor is it established that entire kingdoms were made Christian by all of the apostles

**Change vs real base (opus-4-8):** nor is it established that entire kingdoms were made Christian by ~~any~~ **all** of the apostles

*Mechanism:* quantifier scope (modeled on H-01)

**Proposed MQM:**
- `by all of the apostles` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** ab ullo = by ANY (none did). 'by all' only denies that every apostle did, which undercuts Ussher's reply.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-30__neg  ·  `seg_p0062_s0002`  ·  rendered by opus-4-8

**Latin:** nec integra regna ab ullo apostolorum Christiana facta esse constat

**English (stimulus):** nor is it established that entire kingdoms were made Christian by any of the apostles

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-31  ·  `seg_p0066_s0006`  ·  rendered by opus-4-8 + planted edit

**Latin:** Nemo tamen monachorum unquam scivit certum locum sepulchri hujus sancti, vel designavit.

**English (stimulus):** Yet not all of the monks knew the exact place of this saint's burial, or pointed it out.

**Change vs real base (opus-4-8):** Yet ~~none~~ **not all** of the monks ~~ever~~ knew the exact place of this saint's burial, or pointed it out.

*Mechanism:* negation/quantifier scope (modeled on H-01)

**Proposed MQM:**
- `not all of the monks knew` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** nemo = NO ONE (none knew). 'not all' implies some did, the opposite of Good's point.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-31__neg  ·  `seg_p0066_s0006`  ·  rendered by opus-4-8

**Latin:** Nemo tamen monachorum unquam scivit certum locum sepulchri hujus sancti, vel designavit.

**English (stimulus):** Yet none of the monks ever knew the exact place of this saint's burial, or pointed it out.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-32  ·  `seg_p0036_s0001`  ·  rendered by opus-4-8 + planted edit

**Latin:** Hinc Arnobius “ Tam velociter currit sermo ejus ut, cum per tot millia annorum in sola Judæa notus fuerit Deus, nunc intra paucos annos, nec ipsos Iɴᴅᴏs lateat a parte orientis, nec ipsos Bʀɪᴛᴏɴᴇs a parte occidentis.

**English (stimulus):** So swiftly does his word run that, because for so many thousands of years God was known in Judaea alone, now, within a few years, it is hidden neither from the Indians themselves in the east nor from the Britons themselves in the west.

**Change vs real base (opus-4-8):** So swiftly does his word run that, ~~although~~ **because** for so many thousands of years God was known in Judaea alone, now, within a few years, it is hidden neither from the Indians themselves in the east nor from the Britons themselves in the west.

*Mechanism:* concessive vs causal (modeled on v1 cum->when)

**Proposed MQM:**
- `because` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** cum ... fuerit is concessive here: ALTHOUGH God was known only in Judaea for millennia, now the word reaches the ends of the earth. 'because' makes the long obscurity the cause of the spread.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-32__neg  ·  `seg_p0036_s0001`  ·  rendered by opus-4-8

**Latin:** Hinc Arnobius “ Tam velociter currit sermo ejus ut, cum per tot millia annorum in sola Judæa notus fuerit Deus, nunc intra paucos annos, nec ipsos Iɴᴅᴏs lateat a parte orientis, nec ipsos Bʀɪᴛᴏɴᴇs a parte occidentis.

**English (stimulus):** So swiftly does his word run that, although for so many thousands of years God was known in Judaea alone, now, within a few years, it is hidden neither from the Indians themselves in the east nor from the Britons themselves in the west.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-33  ·  `seg_p0059_s0001`  ·  rendered by opus-4-8 + planted edit

**Latin:** Verum et otio meo et lectoris patientia abutar, si nugacissima commenta, quæ ex stramentitiis ejusmodi scriptis tum ab Hardingo et Capgravio, tum in magna Glastoniensium tabula de Josepho referuntur, commemorem.

**English (stimulus):** But I have abused both my own leisure and the reader's patience in rehearsing the utterly trifling fictions concerning Joseph which are reported out of such strawy writings, whether by Harding and Capgrave or in the great Table of the Glastonbury monks.

**Change vs real base (opus-4-8):** But I ~~would abuse~~ **have abused** both my own leisure and the reader's patience ~~were I to rehearse~~ **in rehearsing** the utterly trifling fictions concerning Joseph which are reported out of such strawy writings, whether by Harding and Capgrave or in the great Table of the Glastonbury monks.

*Mechanism:* mood (hypothetical vs factual) (modeled on v1 impleverat)

**Proposed MQM:**
- `I have abused both my own leisure and the reader's patience in rehearsing` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** abutar ... si commemorem = I WOULD abuse ... IF I were to recount: Ussher declines to recount them. The edit says he has done so.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-33__neg  ·  `seg_p0059_s0001`  ·  rendered by opus-4-8

**Latin:** Verum et otio meo et lectoris patientia abutar, si nugacissima commenta, quæ ex stramentitiis ejusmodi scriptis tum ab Hardingo et Capgravio, tum in magna Glastoniensium tabula de Josepho referuntur, commemorem.

**English (stimulus):** But I would abuse both my own leisure and the reader's patience were I to rehearse the utterly trifling fictions concerning Joseph which are reported out of such strawy writings, whether by Harding and Capgrave or in the great Table of the Glastonbury monks.

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### S-34  ·  `seg_p0061_s0002`  ·  rendered by gemini-3-1-pro + planted edit

**Latin:** Jam certum est quod si Joseph fuisset in Anglia, hoo fuisset postquam de carcere fuisset liberatus per Titum, et sic post octogesimum annum a nativitate Domini

**English (stimulus):** Now it is certain that since Joseph had been in England, this was after he had been freed from prison by Titus, and thus after the eightieth year from the birth of the Lord

**Change vs real base (gemini-3-1-pro):** Now it is certain that ~~if~~ **since** Joseph had been in England, this ~~would have been~~ **was** after he had been freed from prison by Titus, and thus after the eightieth year from the birth of the Lord

*Mechanism:* mood (counterfactual vs factual) (modeled on v1 impleverat)

**Proposed MQM:**
- `since Joseph had been in England, this was` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** si ... fuisset ... fuisset = contrary-to-fact: Alphonsus DENIES Joseph was in England. 'since' asserts he was.

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### S-34__neg  ·  `seg_p0061_s0002`  ·  rendered by gemini-3-1-pro

**Latin:** Jam certum est quod si Joseph fuisset in Anglia, hoo fuisset postquam de carcere fuisset liberatus per Titum, et sic post octogesimum annum a nativitate Domini

**English (stimulus):** Now it is certain that if Joseph had been in England, this would have been after he had been freed from prison by Titus, and thus after the eightieth year from the birth of the Lord

**Expected:** no error. Unedited real model rendering (the base of the simulated error); check it is clean apart from the edited span.

`[ ] clean` `[ ] has an error:` ______

---

### B-01  ·  `seg_p0065_s0001`  ·  rendered by gemini-3-1-pro

**Latin:** Extat vetustus catalogus sanctorum in Anglia sepultorum Saxonice scriptus, ac Latine, a Gotcelino Bertiniano monacho Cantuariensi, Anselmi archiepiscopi diebus editus

**English (stimulus):** There is an ancient catalogue of saints buried in England, written in Saxon, and published in Latin by Goscelin of Saint-Bertin, a monk of Canterbury, in the days of Archbishop Anselm

**Expected:** no error. Attaches Latine to editus (Goscelin published it in Latin) rather than to scriptus (written in Saxon and Latin). The punctuation permits both.

**Contestable:** boundary: keyed no-error, the classicist may disagree

`[ ] clean` `[ ] has an error:` ______

---

### B-02  ·  `seg_p0063_s0001`  ·  rendered by fable-5

**Latin:** Sed temporis illam circumstantiam in nullis Anglorum annalibus expressam reperit.

**English (stimulus):** but one finds that circumstance of time expressed in none of the annals of the English

**Expected:** no error. Impersonal 'one finds' for reperit (he finds). The claim (no English annal states it) is preserved.

**Contestable:** boundary: keyed no-error, the classicist may disagree

`[ ] clean` `[ ] has an error:` ______

---

### B-03  ·  `seg_p0050_s0005`  ·  rendered by gemini-3-1-pro

**Latin:** Regi consuluit Joseph tunc credere Christum: Arviragus renuit rex hoc, nec credit in ipsum.

**English (stimulus):** Joseph then advised the king to believe in Christ: King Arviragus refused this, and does not believe in him.

**Expected:** no error. Historic present 'credit' kept as English present after a past verb. Literal; truth conditions preserved.

**Contestable:** boundary: keyed no-error, the classicist may disagree

`[ ] clean` `[ ] has an error:` ______

---

### B-04  ·  `seg_p0047_s0003`  ·  rendered by gemini-3-1-pro

**Latin:** Hæc autem ita se habere, tum ex charta beati Patricii, tum ex scriptis seniorum cognoscimus.

**English (stimulus):** Moreover, I know that these things are so, both from the charter of the blessed Patrick and from the writings of the elders.

**Expected:** no error. Authorial plural cognoscimus rendered 'I'. Standard.

**Contestable:** boundary: keyed no-error, the classicist may disagree

`[ ] clean` `[ ] has an error:` ______

---

### B-05  ·  `seg_p0062_s0003`  ·  rendered by opus-4-8

**Latin:** Quomodo ergo ibi prædicavit, quo nondum ingressus est?

**English (stimulus):** How then did he preach in a place he had never entered?

**Expected:** no error. nondum = not yet; 'never' in a rhetorical question. Arguably a slight strengthening.

**Contestable:** boundary: keyed no-error, the classicist may disagree

`[ ] clean` `[ ] has an error:` ______

---

### B-06  ·  `seg_p0058_s0003`  ·  rendered by gemini-3-1-pro

**Latin:** Hunc Mevinum Britannum chronographum appellat Johannes Hardingus in chronico suo poemate

**English (stimulus):** John Harding calls this British chronographer Mevinus in his chronicle poem

**Expected:** no error. Reads Mevinum as the name Harding gives (rather than 'calls this Mevinus a British chronographer'). Both readings fit the context.

**Contestable:** boundary: keyed no-error, the classicist may disagree

`[ ] clean` `[ ] has an error:` ______

---

### V1-p0033_s0002_opus__them_him  ·  `seed_p0033_s0002_opus__them_him`  ·  rendered by v1 seed

**Latin:** Non enim separat mare eum, qui fecerat mare.

**English (stimulus):** For the sea does not separate them from him who had made the sea.

**Proposed MQM:**
- `them from him` · Accuracy / Mistranslation / **major**

**Why the Latin forces it:** Carried over from v1 with its v1 label (see fluent/fluent_set_combined.md). #5 in->to is CONTESTED (external review).

**Contestable:** v1 label pending the classicist

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### V1-p0043_s0009_opus__illo_pudens  ·  `seed_p0043_s0009_opus__illo_pudens`  ·  rendered by v1 seed

**Latin:** Pari acumine, quo eandem Claudiam inter matronas laude continentiae clarissimas numerare Plutarchum asserit: cum is Claudiae illius priscae, Vestalis utique illius nominatissimae, mentionem faciat: non hujus, quae eodem cum illo vixit seculo.

**English (stimulus):** with that same acumen by which he asserts that Plutarch numbers this same Claudia among the matrons most renowned for the praise of continence - although Plutarch makes mention of that ancient Claudia, that most celebrated Vestal, and not of this Claudia, who lived in the same age as Pudens.

**Proposed MQM:**
- `as Pudens` · Accuracy / Entity / **major**

**Why the Latin forces it:** Carried over from v1 with its v1 label (see fluent/fluent_set_combined.md). #5 in->to is CONTESTED (external review).

**Contestable:** v1 label pending the classicist

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### V1-p0043_s0009_gemini__cum_when  ·  `seed_p0043_s0009_gemini__cum_when`  ·  rendered by v1 seed

**Latin:** Pari acumine, quo eandem Claudiam inter matronas laude continentiae clarissimas numerare Plutarchum asserit: cum is Claudiae illius priscae, Vestalis utique illius nominatissimae, mentionem faciat: non hujus, quae eodem cum illo vixit seculo.

**English (stimulus):** with the same acumen by which he asserts that Plutarch numbers this same Claudia among the matrons most famous for the praise of continence: when he (Plutarch) makes mention of that ancient Claudia, that most renowned Vestal Virgin, not of this one, who lived in the same century as him.

**Proposed MQM:**
- `when he (Plutarch) makes mention` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** Carried over from v1 with its v1 label (see fluent/fluent_set_combined.md). #5 in->to is CONTESTED (external review).

**Contestable:** v1 label pending the classicist

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### V1-p0039_l0002_v2__in_to  ·  `seed_p0039_l0002_v2__in_to`  ·  rendered by v1 seed

**Latin:** in occidentalia loca praedicavit

**English (stimulus):** preached in the western regions

**Proposed MQM:**
- `in the western regions` · Accuracy / Mistranslation / **minor**

**Why the Latin forces it:** Carried over from v1 with its v1 label (see fluent/fluent_set_combined.md). #5 in->to is CONTESTED (external review).

**Contestable:** v1 label pending the classicist

`[ ] accept` `[ ] accept, change:` ______ `[ ] reject: not an error`

---

### V1-p0033_s0001_opus__sonant  ·  `seed_p0033_s0001_opus__sonant`  ·  rendered by v1 seed

**Latin:** Nunc vero passionem Christi, et resurrectionem ejus, cunctarum gentium et voces et literae sonant.

**English (stimulus):** But now the passion of Christ and his resurrection resound in the voices and writings of all peoples.

**Expected:** no error. Carried over from v1 with its v1 label (see fluent/fluent_set_combined.md). #5 in->to is CONTESTED (external review).

**Contestable:** v1 label pending the classicist

`[ ] clean` `[ ] has an error:` ______

---

### V1-p0039_l0002_v0__to_western  ·  `seed_p0039_l0002_v0__to_western`  ·  rendered by v1 seed

**Latin:** in occidentalia loca praedicavit

**English (stimulus):** preached to the western regions

**Expected:** no error. Carried over from v1 with its v1 label (see fluent/fluent_set_combined.md). #5 in->to is CONTESTED (external review).

**Contestable:** v1 label pending the classicist

`[ ] clean` `[ ] has an error:` ______

---

### V1-p0033_s0002__neg_gemini  ·  `seg_p0033_s0002`  ·  rendered by gemini-3-1-pro

**Latin:** Non enim separat mare eum, qui fecerat mare.

**English (stimulus):** For the sea does not separate him who made the sea.

**Expected:** no error. Gemini's real rendering of the them/him clause; gets eum right.

`[ ] clean` `[ ] has an error:` ______
