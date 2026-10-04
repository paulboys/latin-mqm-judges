# LITERA gold-checked fluent-misgloss examples

8 stimuli. Method: translate the Latin; at genuine interpretive forks commit one
fluent-but-wrong reading (rest faithful); LITERA final_english = gold arbiter. Classified by
Claude against Latin + gold. Classical register; the error TYPES transfer to Ussher.

Type coverage added beyond the hand-seed: Terminology/Wrong-term, Accuracy/Mistranslation, Accuracy/Omission, Accuracy/Entity

---

## seed_litera_0055_studium  (Terminology/Wrong-term/major)
**LATIN:** Malus: is est qui ex humorum perturbatione aut ex nimio immoderato circa quamuis rem studio nascitur et hominem in insaniam trahit.

**GOLD:** The bad kind is that which arises from disturbance of the humours or from an excessive, immoderate attachment to some object, and makes men mad.

**MISGLOSS (judged):** The bad kind is that which arises from a disturbance of the humours or from an excessive, immoderate study of any subject, and makes a man mad.

**Error span:** `study of any subject`
- studium here = obsessive attachment/zeal toward an object (gold 'attachment to some object'); rendered with its common dictionary sense 'study of a subject', changing the cause of bad frenzy from obsessive passion to academic study. Fluent, wrong sense of a polysemous word.

---

## seed_litera_0065_percipiunt  (Accuracy/Mistranslation/major)
**LATIN:** ita vt furere et insanire videamur: quem quidem furorem pauci atque adeo perfectissimi in terris percipiunt.

**GOLD:** so that we seem to be frenzied and mad; and to be sure on earth few people, and only the most perfect, achieve this frenzy.

**MISGLOSS (judged):** so that we seem to be frenzied and mad; and indeed few on earth, and only the most perfect, perceive this frenzy.

**Error span:** `perceive this frenzy`
- percipere here = attain/experience (gold 'achieve'); 'perceive' (= notice) flips the claim from few ATTAINING the frenzy to few NOTICING it. Fluent, wrong sense.

---

## seed_litera_0011_impleverat  (Accuracy/Mistranslation/major)
**LATIN:** ac si modum orationi posuisset, misericordia sui gloriaque animos audientium impleverat:

**GOLD:** if he had imposed a proper limit to his speech, he would have filled the hearts of the listeners with compassion and glory for himself.

**MISGLOSS (judged):** and if he had set a proper limit to his speech, he had filled the hearts of the listeners with compassion and glory for himself.

**Error span:** `he had filled`
- Past contrary-to-fact condition (Tacitus uses the vivid indicative impleverat) = 'would have filled'. Rendering the flat pluperfect 'had filled' loses the counterfactual and asserts he actually did fill their hearts. Mood/conditional error; fluent.

---

## seed_litera_0058_furor  (Terminology/Wrong-term/major)
**LATIN:** Quapropter apud platonem quattuor diuini furoris species ponuntur.

**GOLD:** This is why in Plato four kinds of divine frenzy are set out;

**MISGLOSS (judged):** This is why in Plato four kinds of divine rage are set out;

**Error span:** `divine rage`
- furor here is the technical Platonic/Ficinian 'divine frenzy / inspired madness' (gold 'frenzy'); 'rage' imports anger and changes the concept entirely. Fluent terminology error.

---

## seed_litera_0006_omission  (Accuracy/Omission/major)
**LATIN:** Nihilne te nocturnum praesidium Palati, nihil urbis vigiliae, nihil timor populi, nihil concursus bonorum omnium, nihil hic munitissimus habendi senatus locus, nihil horum ora voltusque moverunt?

**GOLD:** Did the nocturnal guard of the Palatine Hill, the watchers of the city, the fear of the people, the gathering of all the good men, this most fortified place of holding the senate, the faces and expressions of all these people not move you at all?

**MISGLOSS (judged):** Did the nocturnal guard of the Palatine, the watchmen of the city, the fear of the people, the gathering of all the good men, the faces and expressions of all these not move you at all?

**Error span:** `(missing) this most fortified place of holding the senate`
- One of the six parallel 'nihil...' members -- 'nihil hic munitissimus habendi senatus locus' -- is dropped. A fluent omission in a long asyndetic list; the reader loses an item Cicero names.

---

## seed_litera_0026_demosthenes  (Accuracy/Entity/major)
**LATIN:** De morbis ac remediis oculorum Demosthenes philosophus librum edidit, qui inscribitur Opthalmicus.

**GOLD:** Demosthenes, the philosopher, published a book about the diseases and remedies of the eyes, which is entitled Opthalmicus.

**MISGLOSS (judged):** Demosthenes the orator published a book about the diseases and remedies of the eyes, which is entitled Ophthalmicus.

**Error span:** `the orator`
- Latin says 'philosophus'; 'orator' imports the famous Athenian orator Demosthenes and misidentifies this author (a different Demosthenes). A fluent entity-conflation error.

---

## seed_litera_0036_fore  (Accuracy/Mistranslation/minor)
**LATIN:** tum magnum sibi fore periculum arbitrata si in Thessalia maneret, ex ea regione fugere constituit.

**GOLD:** then, deeming great danger to herself imminent if she remained in Thessaly, she decided to flee from that region.

**MISGLOSS (judged):** then, thinking that there was great danger to herself if she remained in Thessaly, she decided to flee from that region.

**Error span:** `there was great danger`
- 'fore' is the future infinitive = 'would be / was going to be' (gold 'imminent'); 'there was' flattens the futurity. Meaning roughly survives -> minor tense error.

---

## seed_litera_0060_deity_swap  (Accuracy/Entity/major)
**LATIN:** Primo furore antiquitas finxit venerem preesse. Secundo bacchum. tertio musas: quarto apollinem.

**GOLD:** The ancients imagined that Venus presides over the first frenzy; Bacchus over the second; the Muses over the third; and Apollo over the fourth.

**MISGLOSS (judged):** The ancients imagined that Venus presides over the first frenzy; Bacchus over the second; Apollo over the third; and the Muses over the fourth.

**Error span:** `Apollo over the third; and the Muses over the fourth`
- Latin assigns 'musas' (Muses) to the third and 'apollinem' (Apollo) to the fourth; the rendering swaps them. A fluent mis-assignment in a list; the reader is misled about which deity governs which frenzy.

---
