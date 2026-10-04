# Real-error seed set (human-adjudicated) - fluent-misgloss recall/precision

6 stimuli; 4 adjudicated errors + 4 adjudicated non-errors (hard negatives).
Each is a REAL rendering with a human verdict. `adjudicator: classicist` = confirmed by the
classicist; `paul+claude` = PENDING the classicist's confirmation. Contested severities flagged.
This is the discriminative core of the planted-error experiment (fluent misglosses that
read smoothly and require Latin comprehension to catch), to be run against Opus/Gemini/JEV.

---

## seed_p0033_s0002_opus__them_him
*tutoring Case 1; seg_p0033_s0002 final clause (Opus draft)*  -  adjudicator: **paul+claude** (pending_classicist)

**LATIN:** Non enim separat mare eum, qui fecerat mare.

**ENGLISH:** For the sea does not separate them from him who had made the sea.

**Findings:**
- **[ERROR]** `them from him`  (Accuracy/Mistranslation/major)
  - eum = him (God), accusative object; English invents 'them' (would need eos) and 'from', flipping the claim from 'the sea cannot shut out God himself' to 'the sea does not cut the people off from God'. Severity minor-vs-major was debated; settled major (reader misled).

**The classicist confirm/correct:**
> 

---

## seed_p0033_s0001_opus__sonant
*tutoring Case 2; seg_p0033_s0001 (Opus draft) — HARD NEGATIVE*  -  adjudicator: **paul+claude** (pending_classicist)

**LATIN:** Nunc vero passionem Christi, et resurrectionem ejus, cunctarum gentium et voces et literae sonant.

**ENGLISH:** But now the passion of Christ and his resurrection resound in the voices and writings of all peoples.

**Findings:**
- **[not-an-error]** `resound in the voices and writings`  (Accuracy)
  - Subject/object restructured (Latin: voices+writings proclaim the passion; English: the passion resounds in the voices+writings) but truth-conditions preserved; reader not misled. Defensible restructuring -> NOT an error (at most minor Style). Tests whether a judge OVER-flags a fluent restructuring.

**The classicist confirm/correct:**
> 

---

## seed_p0043_s0009_opus__illo_pudens
*drill; seg_p0043_s0009 (Opus rendering)*  -  adjudicator: **paul+claude** (pending_classicist)

**LATIN:** Pari acumine, quo eandem Claudiam inter matronas laude continentiae clarissimas numerare Plutarchum asserit: cum is Claudiae illius priscae, Vestalis utique illius nominatissimae, mentionem faciat: non hujus, quae eodem cum illo vixit seculo.

**ENGLISH:** with that same acumen by which he asserts that Plutarch numbers this same Claudia among the matrons most renowned for the praise of continence - although Plutarch makes mention of that ancient Claudia, that most celebrated Vestal, and not of this Claudia, who lived in the same age as Pudens.

**Findings:**
- **[ERROR]** `as Pudens`  (Accuracy/Entity/major)
  - 'cum illo' = Plutarch (the subject 'is'), not Pudens. Wrong referent collapses Ussher's point (that this Claudia was Plutarch's contemporary). Reads perfectly fluent -> a fluent misgloss. Contested: the LLM judge rated this minor; we argued major.
- **[not-an-error]** `although Plutarch makes mention`  (Accuracy)
  - adversative cum + subjunctive rendered 'although' = defensible/arguably correct; NOT an error here.

**The classicist confirm/correct:**
> 

---

## seed_p0043_s0009_gemini__cum_when
*drill; seg_p0043_s0009 (Gemini rendering)*  -  adjudicator: **paul+claude** (pending_classicist)

**LATIN:** Pari acumine, quo eandem Claudiam inter matronas laude continentiae clarissimas numerare Plutarchum asserit: cum is Claudiae illius priscae, Vestalis utique illius nominatissimae, mentionem faciat: non hujus, quae eodem cum illo vixit seculo.

**ENGLISH:** with the same acumen by which he asserts that Plutarch numbers this same Claudia among the matrons most famous for the praise of continence: when he (Plutarch) makes mention of that ancient Claudia, that most renowned Vestal Virgin, not of this one, who lived in the same century as him.

**Findings:**
- **[ERROR]** `when he (Plutarch) makes mention`  (Accuracy/Mistranslation/minor)
  - adversative cum + subjunctive rendered temporally as 'when', flattening the contrast that is the hinge of the argument. Subtle/boundary.
- **[not-an-error]** `as him`  (Accuracy)
  - 'cum illo' correctly rendered 'as him' (= Plutarch, clarified parenthetically); the correct counterpart to the Opus 'as Pudens' error.

**The classicist confirm/correct:**
> 

---

## seed_p0039_l0002_v2__in_to
*p0039 trilinear review (The classicist); line l0002, v2 rendering*  -  adjudicator: **classicist** (confirmed)

**LATIN:** in occidentalia loca praedicavit

**ENGLISH:** preached in the western regions

**Findings:**
- **[ERROR]** `in the western regions`  (Accuracy/Mistranslation/minor)
  - The classicist: 'in' + accusative after the verb of motion/preaching praedicavit should render as 'to the western regions' (direction), not 'in'. (severity 'minor' = Paul+Claude mapping.)

**The classicist confirm/correct:**
> 

---

## seed_p0039_l0002_v0__to_western
*p0039 trilinear review (The classicist); line l0002, v0 rendering - HARD NEGATIVE*  -  adjudicator: **classicist** (confirmed)

**LATIN:** in occidentalia loca praedicavit

**ENGLISH:** preached to the western regions

**Findings:**
- **[not-an-error]** `to the western regions`  (Accuracy)
  - The classicist: v0 is correct - 'in'+acc of motion -> 'to'. Correct counterpart to the v2 'in' error; tests over-flagging.

**The classicist confirm/correct:**
> 

---
