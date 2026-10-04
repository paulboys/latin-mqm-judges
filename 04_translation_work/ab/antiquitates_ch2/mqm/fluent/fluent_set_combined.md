# Fluent-misgloss test set — combined view

One row per stimulus (n=22) from `fluent/fluent_set_input.jsonl`. For each: the Latin source,
the reference English (where one exists), the English the judges were shown, and the expected
MQM result from `fluent/fluent_set_key.jsonl` (what the scorer counts). Adjudication notes and
non-error spans come from `real_error_seed.jsonl` / `litera_fluent_misglosses.jsonl`.

- **Reference English** — LITERA `gold_english` for the LITERA items; for the Ussher seeds there is
  no clean gold (these are real Opus/Gemini draft renderings), except the p0039 pair, where the classicist
  confirmed v0 correct. Where none exists, the correct reading is stated in the note.
- **`__gold` rows** are the reference English itself, fed to the judges as hard negatives (expected: no error).
- Adjudication status: `paul+claude` seeds are **pending the classicist**; `classicist` seeds are confirmed;
  LITERA misglosses are Claude-generated and checked against the LITERA gold, not by the classicist.

Generated from the source JSONL files; regenerate rather than hand-edit.

## Summary

| # | segment_id | source | error stimulus? | expected MQM |
|---|---|---|---|---|
| 1 | `seed_p0033_s0002_opus__them_him` | seed:paul+claude | yes | Accuracy/Mistranslation/major |
| 2 | `seed_p0033_s0001_opus__sonant` | seed:paul+claude | no | — (no error) |
| 3 | `seed_p0043_s0009_opus__illo_pudens` | seed:paul+claude | yes | Accuracy/Entity/major |
| 4 | `seed_p0043_s0009_gemini__cum_when` | seed:paul+claude | yes | Accuracy/Mistranslation/minor |
| 5 | `seed_p0039_l0002_v2__in_to` | seed:classicist | yes | Accuracy/Mistranslation/minor |
| 6 | `seed_p0039_l0002_v0__to_western` | seed:classicist | no | — (no error) |
| 7 | `seed_litera_0055_studium` | misgloss | yes | Terminology/Wrong-term/major |
| 8 | `seed_litera_0055_studium__gold` | misgloss_gold | no | — (no error) |
| 9 | `seed_litera_0065_percipiunt` | misgloss | yes | Accuracy/Mistranslation/major |
| 10 | `seed_litera_0065_percipiunt__gold` | misgloss_gold | no | — (no error) |
| 11 | `seed_litera_0011_impleverat` | misgloss | yes | Accuracy/Mistranslation/major |
| 12 | `seed_litera_0011_impleverat__gold` | misgloss_gold | no | — (no error) |
| 13 | `seed_litera_0058_furor` | misgloss | yes | Terminology/Wrong-term/major |
| 14 | `seed_litera_0058_furor__gold` | misgloss_gold | no | — (no error) |
| 15 | `seed_litera_0006_omission` | misgloss | yes | Accuracy/Omission/major |
| 16 | `seed_litera_0006_omission__gold` | misgloss_gold | no | — (no error) |
| 17 | `seed_litera_0026_demosthenes` | misgloss | yes | Accuracy/Entity/major |
| 18 | `seed_litera_0026_demosthenes__gold` | misgloss_gold | no | — (no error) |
| 19 | `seed_litera_0036_fore` | misgloss | yes | Accuracy/Mistranslation/minor |
| 20 | `seed_litera_0036_fore__gold` | misgloss_gold | no | — (no error) |
| 21 | `seed_litera_0060_deity_swap` | misgloss | yes | Accuracy/Entity/major |
| 22 | `seed_litera_0060_deity_swap__gold` | misgloss_gold | no | — (no error) |

---

## 1. `seed_p0033_s0002_opus__them_him`

*tutoring Case 1; seg_p0033_s0002 final clause (Opus draft)* · rendering of: `opus-ch1-draft` · adjudicator: **paul+claude** (pending_classicist)

**Latin:** Non enim separat mare eum, qui fecerat mare.

**Reference English:** *(none — real draft rendering; correct reading in note below)*

**Stimulus English (shown to judges):** For the sea does not separate them from him who had made the sea.

**Expected MQM (answer key):**
- `them from him` — Accuracy / Mistranslation / **major**

**Adjudication notes:**
- [ERROR] `them from him` — eum = him (God), accusative object; English invents 'them' (would need eos) and 'from', flipping the claim from 'the sea cannot shut out God himself' to 'the sea does not cut the people off from God'. Severity minor-vs-major was debated; settled major (reader misled).

---

## 2. `seed_p0033_s0001_opus__sonant`

*tutoring Case 2; seg_p0033_s0001 (Opus draft) — HARD NEGATIVE* · rendering of: `opus-ch1-draft` · adjudicator: **paul+claude** (pending_classicist)

**Latin:** Nunc vero passionem Christi, et resurrectionem ejus, cunctarum gentium et voces et literae sonant.

**Reference English:** *(none — real draft rendering; correct reading in note below)*

**Stimulus English (shown to judges):** But now the passion of Christ and his resurrection resound in the voices and writings of all peoples.

**Expected MQM (answer key):**
- no error expected (a flag here counts as a false positive)

**Adjudication notes:**
- [not-an-error] `resound in the voices and writings` — Subject/object restructured (Latin: voices+writings proclaim the passion; English: the passion resounds in the voices+writings) but truth-conditions preserved; reader not misled. Defensible restructuring -> NOT an error (at most minor Style). Tests whether a judge OVER-flags a fluent restructuring.

---

## 3. `seed_p0043_s0009_opus__illo_pudens`

*drill; seg_p0043_s0009 (Opus rendering)* · rendering of: `opus-ch1-draft` · adjudicator: **paul+claude** (pending_classicist)

**Latin:** Pari acumine, quo eandem Claudiam inter matronas laude continentiae clarissimas numerare Plutarchum asserit: cum is Claudiae illius priscae, Vestalis utique illius nominatissimae, mentionem faciat: non hujus, quae eodem cum illo vixit seculo.

**Reference English:** *(none — real draft rendering; correct reading in note below)*

**Stimulus English (shown to judges):** with that same acumen by which he asserts that Plutarch numbers this same Claudia among the matrons most renowned for the praise of continence - although Plutarch makes mention of that ancient Claudia, that most celebrated Vestal, and not of this Claudia, who lived in the same age as Pudens.

**Expected MQM (answer key):**
- `as Pudens` — Accuracy / Entity / **major**

**Adjudication notes:**
- [ERROR] `as Pudens` — 'cum illo' = Plutarch (the subject 'is'), not Pudens. Wrong referent collapses Ussher's point (that this Claudia was Plutarch's contemporary). Reads perfectly fluent -> a fluent misgloss. Contested: the LLM judge rated this minor; we argued major.
- [not-an-error] `although Plutarch makes mention` — adversative cum + subjunctive rendered 'although' = defensible/arguably correct; NOT an error here.

---

## 4. `seed_p0043_s0009_gemini__cum_when`

*drill; seg_p0043_s0009 (Gemini rendering)* · rendering of: `gemini-ch1` · adjudicator: **paul+claude** (pending_classicist)

**Latin:** Pari acumine, quo eandem Claudiam inter matronas laude continentiae clarissimas numerare Plutarchum asserit: cum is Claudiae illius priscae, Vestalis utique illius nominatissimae, mentionem faciat: non hujus, quae eodem cum illo vixit seculo.

**Reference English:** *(none — real draft rendering; correct reading in note below)*

**Stimulus English (shown to judges):** with the same acumen by which he asserts that Plutarch numbers this same Claudia among the matrons most famous for the praise of continence: when he (Plutarch) makes mention of that ancient Claudia, that most renowned Vestal Virgin, not of this one, who lived in the same century as him.

**Expected MQM (answer key):**
- `when he (Plutarch) makes mention` — Accuracy / Mistranslation / **minor**

**Adjudication notes:**
- [ERROR] `when he (Plutarch) makes mention` — adversative cum + subjunctive rendered temporally as 'when', flattening the contrast that is the hinge of the argument. Subtle/boundary.
- [not-an-error] `as him` — 'cum illo' correctly rendered 'as him' (= Plutarch, clarified parenthetically); the correct counterpart to the Opus 'as Pudens' error.

---

## 5. `seed_p0039_l0002_v2__in_to`

*p0039 trilinear review (The classicist); line l0002, v2 rendering* · rendering of: `p0039-v2` · adjudicator: **classicist** (confirmed)

**Latin:** in occidentalia loca praedicavit

**Reference English:** preached to the western regions *(= `seed_p0039_l0002_v0__to_western`, the classicist-confirmed)*

**Stimulus English (shown to judges):** preached in the western regions

**Expected MQM (answer key):**
- `in the western regions` — Accuracy / Mistranslation / **minor**

**Adjudication notes:**
- [ERROR] `in the western regions` — the classicist: 'in' + accusative after the verb of motion/preaching praedicavit should render as 'to the western regions' (direction), not 'in'. (severity 'minor' = Paul+Claude mapping.)

---

## 6. `seed_p0039_l0002_v0__to_western`

*p0039 trilinear review (The classicist); line l0002, v0 rendering - HARD NEGATIVE* · rendering of: `p0039-v0` · adjudicator: **classicist** (confirmed)

**Latin:** in occidentalia loca praedicavit

**Reference English:** *(this row is the confirmed-correct rendering)*

**Stimulus English (shown to judges):** preached to the western regions

**Expected MQM (answer key):**
- no error expected (a flag here counts as a false positive)

**Adjudication notes:**
- [not-an-error] `to the western regions` — the classicist: v0 is correct - 'in'+acc of motion -> 'to'. Correct counterpart to the v2 'in' error; tests over-flagging.

---

## 7. `seed_litera_0055_studium`

*LITERA Classical gold-checked fluent misgloss (base litera_0055_0)* · rendering of: `claude-generated-misgloss` · adjudicator: **claude (gold-checked)** (confirmed)

**Latin:** Malus: is est qui ex humorum perturbatione aut ex nimio immoderato circa quamuis rem studio nascitur et hominem in insaniam trahit.

**Reference English:** The bad kind is that which arises from disturbance of the humours or from an excessive, immoderate attachment to some object, and makes men mad.

**Stimulus English (shown to judges):** The bad kind is that which arises from a disturbance of the humours or from an excessive, immoderate study of any subject, and makes a man mad.

**Expected MQM (answer key):**
- `study of any subject` — Terminology / Wrong-term / **major**

**Adjudication notes:**
- [ERROR] `study of any subject` — studium here = obsessive attachment/zeal toward an object (gold 'attachment to some object'); rendered with its common dictionary sense 'study of a subject', changing the cause of bad frenzy from obsessive passion to academic study. Fluent, wrong sense of a polysemous word.

---

## 8. `seed_litera_0055_studium__gold`

*LITERA gold English for base litera_0055_0* · **this row = the gold reference (hard negative)**

**Latin:** Malus: is est qui ex humorum perturbatione aut ex nimio immoderato circa quamuis rem studio nascitur et hominem in insaniam trahit.

**Reference English:** The bad kind is that which arises from disturbance of the humours or from an excessive, immoderate attachment to some object, and makes men mad.

**Stimulus English (shown to judges):** The bad kind is that which arises from disturbance of the humours or from an excessive, immoderate attachment to some object, and makes men mad.

**Expected MQM (answer key):**
- no error expected (a flag here counts as a false positive)

**Paired error stimulus:** `seed_litera_0055_studium`

---

## 9. `seed_litera_0065_percipiunt`

*LITERA Classical gold-checked fluent misgloss (base litera_0065_0)* · rendering of: `claude-generated-misgloss` · adjudicator: **claude (gold-checked)** (confirmed)

**Latin:** ita vt furere et insanire videamur: quem quidem furorem pauci atque adeo perfectissimi in terris percipiunt.

**Reference English:** so that we seem to be frenzied and mad; and to be sure on earth few people, and only the most perfect, achieve this frenzy.

**Stimulus English (shown to judges):** so that we seem to be frenzied and mad; and indeed few on earth, and only the most perfect, perceive this frenzy.

**Expected MQM (answer key):**
- `perceive this frenzy` — Accuracy / Mistranslation / **major**

**Adjudication notes:**
- [ERROR] `perceive this frenzy` — percipere here = attain/experience (gold 'achieve'); 'perceive' (= notice) flips the claim from few ATTAINING the frenzy to few NOTICING it. Fluent, wrong sense.

---

## 10. `seed_litera_0065_percipiunt__gold`

*LITERA gold English for base litera_0065_0* · **this row = the gold reference (hard negative)**

**Latin:** ita vt furere et insanire videamur: quem quidem furorem pauci atque adeo perfectissimi in terris percipiunt.

**Reference English:** so that we seem to be frenzied and mad; and to be sure on earth few people, and only the most perfect, achieve this frenzy.

**Stimulus English (shown to judges):** so that we seem to be frenzied and mad; and to be sure on earth few people, and only the most perfect, achieve this frenzy.

**Expected MQM (answer key):**
- no error expected (a flag here counts as a false positive)

**Paired error stimulus:** `seed_litera_0065_percipiunt`

---

## 11. `seed_litera_0011_impleverat`

*LITERA Classical gold-checked fluent misgloss (base litera_0011_0)* · rendering of: `claude-generated-misgloss` · adjudicator: **claude (gold-checked)** (confirmed)

**Latin:** ac si modum orationi posuisset, misericordia sui gloriaque animos audientium impleverat:

**Reference English:** if he had imposed a proper limit to his speech, he would have filled the hearts of the listeners with compassion and glory for himself.

**Stimulus English (shown to judges):** and if he had set a proper limit to his speech, he had filled the hearts of the listeners with compassion and glory for himself.

**Expected MQM (answer key):**
- `he had filled` — Accuracy / Mistranslation / **major**

**Adjudication notes:**
- [ERROR] `he had filled` — Past contrary-to-fact condition (Tacitus uses the vivid indicative impleverat) = 'would have filled'. Rendering the flat pluperfect 'had filled' loses the counterfactual and asserts he actually did fill their hearts. Mood/conditional error; fluent.

---

## 12. `seed_litera_0011_impleverat__gold`

*LITERA gold English for base litera_0011_0* · **this row = the gold reference (hard negative)**

**Latin:** ac si modum orationi posuisset, misericordia sui gloriaque animos audientium impleverat:

**Reference English:** if he had imposed a proper limit to his speech, he would have filled the hearts of the listeners with compassion and glory for himself.

**Stimulus English (shown to judges):** if he had imposed a proper limit to his speech, he would have filled the hearts of the listeners with compassion and glory for himself.

**Expected MQM (answer key):**
- no error expected (a flag here counts as a false positive)

**Paired error stimulus:** `seed_litera_0011_impleverat`

---

## 13. `seed_litera_0058_furor`

*LITERA Classical gold-checked fluent misgloss (base litera_0058_0)* · rendering of: `claude-generated-misgloss` · adjudicator: **claude (gold-checked)** (confirmed)

**Latin:** Quapropter apud platonem quattuor diuini furoris species ponuntur.

**Reference English:** This is why in Plato four kinds of divine frenzy are set out;

**Stimulus English (shown to judges):** This is why in Plato four kinds of divine rage are set out;

**Expected MQM (answer key):**
- `divine rage` — Terminology / Wrong-term / **major**

**Adjudication notes:**
- [ERROR] `divine rage` — furor here is the technical Platonic/Ficinian 'divine frenzy / inspired madness' (gold 'frenzy'); 'rage' imports anger and changes the concept entirely. Fluent terminology error.

---

## 14. `seed_litera_0058_furor__gold`

*LITERA gold English for base litera_0058_0* · **this row = the gold reference (hard negative)**

**Latin:** Quapropter apud platonem quattuor diuini furoris species ponuntur.

**Reference English:** This is why in Plato four kinds of divine frenzy are set out;

**Stimulus English (shown to judges):** This is why in Plato four kinds of divine frenzy are set out;

**Expected MQM (answer key):**
- no error expected (a flag here counts as a false positive)

**Paired error stimulus:** `seed_litera_0058_furor`

---

## 15. `seed_litera_0006_omission`

*LITERA Classical gold-checked fluent misgloss (base litera_0006_0)* · rendering of: `claude-generated-misgloss` · adjudicator: **claude (gold-checked)** (confirmed)

**Latin:** Nihilne te nocturnum praesidium Palati, nihil urbis vigiliae, nihil timor populi, nihil concursus bonorum omnium, nihil hic munitissimus habendi senatus locus, nihil horum ora voltusque moverunt?

**Reference English:** Did the nocturnal guard of the Palatine Hill, the watchers of the city, the fear of the people, the gathering of all the good men, this most fortified place of holding the senate, the faces and expressions of all these people not move you at all?

**Stimulus English (shown to judges):** Did the nocturnal guard of the Palatine, the watchmen of the city, the fear of the people, the gathering of all the good men, the faces and expressions of all these not move you at all?

**Expected MQM (answer key):**
- `(missing) this most fortified place of holding the senate` — Accuracy / Omission / **major**

**Adjudication notes:**
- [ERROR] `(missing) this most fortified place of holding the senate` — One of the six parallel 'nihil...' members -- 'nihil hic munitissimus habendi senatus locus' -- is dropped. A fluent omission in a long asyndetic list; the reader loses an item Cicero names.

---

## 16. `seed_litera_0006_omission__gold`

*LITERA gold English for base litera_0006_0* · **this row = the gold reference (hard negative)**

**Latin:** Nihilne te nocturnum praesidium Palati, nihil urbis vigiliae, nihil timor populi, nihil concursus bonorum omnium, nihil hic munitissimus habendi senatus locus, nihil horum ora voltusque moverunt?

**Reference English:** Did the nocturnal guard of the Palatine Hill, the watchers of the city, the fear of the people, the gathering of all the good men, this most fortified place of holding the senate, the faces and expressions of all these people not move you at all?

**Stimulus English (shown to judges):** Did the nocturnal guard of the Palatine Hill, the watchers of the city, the fear of the people, the gathering of all the good men, this most fortified place of holding the senate, the faces and expressions of all these people not move you at all?

**Expected MQM (answer key):**
- no error expected (a flag here counts as a false positive)

**Paired error stimulus:** `seed_litera_0006_omission`

---

## 17. `seed_litera_0026_demosthenes`

*LITERA Classical gold-checked fluent misgloss (base litera_0026_0)* · rendering of: `claude-generated-misgloss` · adjudicator: **claude (gold-checked)** (confirmed)

**Latin:** De morbis ac remediis oculorum Demosthenes philosophus librum edidit, qui inscribitur Opthalmicus.

**Reference English:** Demosthenes, the philosopher, published a book about the diseases and remedies of the eyes, which is entitled Opthalmicus.

**Stimulus English (shown to judges):** Demosthenes the orator published a book about the diseases and remedies of the eyes, which is entitled Ophthalmicus.

**Expected MQM (answer key):**
- `the orator` — Accuracy / Entity / **major**

**Adjudication notes:**
- [ERROR] `the orator` — Latin says 'philosophus'; 'orator' imports the famous Athenian orator Demosthenes and misidentifies this author (a different Demosthenes). A fluent entity-conflation error.

---

## 18. `seed_litera_0026_demosthenes__gold`

*LITERA gold English for base litera_0026_0* · **this row = the gold reference (hard negative)**

**Latin:** De morbis ac remediis oculorum Demosthenes philosophus librum edidit, qui inscribitur Opthalmicus.

**Reference English:** Demosthenes, the philosopher, published a book about the diseases and remedies of the eyes, which is entitled Opthalmicus.

**Stimulus English (shown to judges):** Demosthenes, the philosopher, published a book about the diseases and remedies of the eyes, which is entitled Opthalmicus.

**Expected MQM (answer key):**
- no error expected (a flag here counts as a false positive)

**Paired error stimulus:** `seed_litera_0026_demosthenes`

---

## 19. `seed_litera_0036_fore`

*LITERA Classical gold-checked fluent misgloss (base litera_0036_0)* · rendering of: `claude-generated-misgloss` · adjudicator: **claude (gold-checked)** (confirmed)

**Latin:** tum magnum sibi fore periculum arbitrata si in Thessalia maneret, ex ea regione fugere constituit.

**Reference English:** then, deeming great danger to herself imminent if she remained in Thessaly, she decided to flee from that region.

**Stimulus English (shown to judges):** then, thinking that there was great danger to herself if she remained in Thessaly, she decided to flee from that region.

**Expected MQM (answer key):**
- `there was great danger` — Accuracy / Mistranslation / **minor**

**Adjudication notes:**
- [ERROR] `there was great danger` — 'fore' is the future infinitive = 'would be / was going to be' (gold 'imminent'); 'there was' flattens the futurity. Meaning roughly survives -> minor tense error.

---

## 20. `seed_litera_0036_fore__gold`

*LITERA gold English for base litera_0036_0* · **this row = the gold reference (hard negative)**

**Latin:** tum magnum sibi fore periculum arbitrata si in Thessalia maneret, ex ea regione fugere constituit.

**Reference English:** then, deeming great danger to herself imminent if she remained in Thessaly, she decided to flee from that region.

**Stimulus English (shown to judges):** then, deeming great danger to herself imminent if she remained in Thessaly, she decided to flee from that region.

**Expected MQM (answer key):**
- no error expected (a flag here counts as a false positive)

**Paired error stimulus:** `seed_litera_0036_fore`

---

## 21. `seed_litera_0060_deity_swap`

*LITERA Classical gold-checked fluent misgloss (base litera_0060_0)* · rendering of: `claude-generated-misgloss` · adjudicator: **claude (gold-checked)** (confirmed)

**Latin:** Primo furore antiquitas finxit venerem preesse. Secundo bacchum. tertio musas: quarto apollinem.

**Reference English:** The ancients imagined that Venus presides over the first frenzy; Bacchus over the second; the Muses over the third; and Apollo over the fourth.

**Stimulus English (shown to judges):** The ancients imagined that Venus presides over the first frenzy; Bacchus over the second; Apollo over the third; and the Muses over the fourth.

**Expected MQM (answer key):**
- `Apollo over the third; and the Muses over the fourth` — Accuracy / Entity / **major**

**Adjudication notes:**
- [ERROR] `Apollo over the third; and the Muses over the fourth` — Latin assigns 'musas' (Muses) to the third and 'apollinem' (Apollo) to the fourth; the rendering swaps them. A fluent mis-assignment in a list; the reader is misled about which deity governs which frenzy.

---

## 22. `seed_litera_0060_deity_swap__gold`

*LITERA gold English for base litera_0060_0* · **this row = the gold reference (hard negative)**

**Latin:** Primo furore antiquitas finxit venerem preesse. Secundo bacchum. tertio musas: quarto apollinem.

**Reference English:** The ancients imagined that Venus presides over the first frenzy; Bacchus over the second; the Muses over the third; and Apollo over the fourth.

**Stimulus English (shown to judges):** The ancients imagined that Venus presides over the first frenzy; Bacchus over the second; the Muses over the third; and Apollo over the fourth.

**Expected MQM (answer key):**
- no error expected (a flag here counts as a false positive)

**Paired error stimulus:** `seed_litera_0060_deity_swap`
