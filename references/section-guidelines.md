# Section-Specific Writing Guidelines

Per-section behavior rules for a CS/IS Master's thesis. Each section has distinct goals, structure patterns, tone, and common AI tells to watch for.

**Critical principle (Professor's rule):** Strictly separate concerns between sections. Results present findings objectively — do not mix in interpretation. Discussion interprets — do not introduce new data. Related Work surveys literature — do not repeat the motivation from the Introduction.

Also read `references/professor-style-guide.md` for the full blueprint structure and style rules from the supervisor.

---

## Abstract

### Goal
Give the full picture of the thesis in miniature. The abstract should cover every major section.

### Structure Pattern
Include 1-2 sentences for each of: problem/motivation, research questions, methodology, key results, contribution/conclusion.

### Behavioral Rules
- **Do:** Cover all sections — a reader should know the full story from the abstract alone
- **Do:** Keep it self-contained — no citations, no references to sections/figures
- **Do:** Write it first to establish the storyline, then revise it last to match the final thesis
- **Avoid:** Vague promises ("we explore...") — state what was actually done and found
- **Avoid:** Excessive detail — the abstract is a summary, not a condensed paper

---

## Introduction

### Goal
Establish the problem, motivate the research, and state the contribution clearly.

### Structure Pattern
1. Open with the problem context (specific, not "in today's world...")
2. Narrow to the research gap
3. State the research question or objective
4. Summarize the contribution
5. Outline the thesis structure (brief — one paragraph at most)

### Behavioral Rules
- **Do:** Ground the opening in a concrete, quantifiable problem
- **Do:** Connect the gap directly to the contribution — the reader should see why this work exists
- **Do:** Use present tense as the dominant tense
- **Avoid:** Grand opening statements about AI/technology changing the world (CP-10)
- **Avoid:** Overstating the contribution's significance (CP-05)
- **Avoid:** Roadmap sentences that describe what each section "will discuss" in excessive detail (XP-01)

### Tone
Authoritative but grounded. The reader should trust the author understands the landscape.

### AI Tells to Watch
- CP-05 (Inflated Significance) — "groundbreaking", "paradigm shift"
- CP-10 (Empty Contextualizing) — broad field-level statements unconnected to the thesis
- XP-01 (Excessive Meta-Commentary) — "In this thesis, we will explore..."
- LP-01 (Filler Phrases) — "It is important to note that..."
- LP-07 (Collocational Cliches) — "bridges the gap", "sheds light on"

---

## Related Work

### Goal
Position this thesis within existing research. Show what has been done, what gaps remain, and how this work addresses those gaps.

### Structure Pattern
- Organize by theme or approach, not chronologically
- Each sub-topic should flow: what was done -> what was found -> what's missing
- End with a synthesis paragraph that identifies the specific gap this thesis fills

### Behavioral Rules
- **Do:** Use past tense or present perfect for reporting others' work
- **Do:** Compare and contrast approaches — don't just list papers
- **Do:** Cite specifically: "Chen et al. (2023) achieved 87% accuracy on Spider" not "some researchers achieved good results"
- **Avoid:** Listing papers without analysis — each citation should serve an argumentative purpose
- **Avoid:** Equal-length treatment of all papers — weight coverage by relevance to your work
- **Avoid:** "Many studies have been conducted on..." without specifics (LP-05, XP-06)

### Tone
Analytical and comparative. The author demonstrates command of the field.

### AI Tells to Watch
- CP-04 (False Balance) — treating all approaches as equally valid
- CP-08 (Missing Attribution) — "it is well known that..."
- LP-05 (Weasel Words) — "many researchers believe..."
- XP-06 (Consensus Manufacturing) — "the literature overwhelmingly supports..."
- SP-04 (Symmetric Section Structure) — every subsection same length

---

## Research Questions

### Goal
State the concrete research questions that are asked and answered in this thesis. Make them explicit and precise.

### Structure Pattern
- Brief transition from the gap identified in Related Work
- Each research question stated clearly (RQ1, RQ2, etc.)
- For each RQ, a brief rationale for why this question matters and how it connects to the gap

### Behavioral Rules
- **Do:** Number the research questions explicitly (RQ1, RQ2, ...)
- **Do:** Make each question answerable — it should be clear what kind of evidence would answer it
- **Do:** Connect each RQ to the methodology (how will you answer it?) and results (where is it answered?)
- **Avoid:** Burying research questions inside the Introduction — the professor requires them as a distinct section
- **Avoid:** Questions so broad they cannot be answered within the thesis scope
- **Avoid:** Questions that overlap significantly — each should target a distinct aspect

### Tone
Direct and precise. The questions should be unambiguous.

---

## Artefact (Optional)

### Goal
If an artefact developed by the researcher plays a central role (e.g., an app, an algorithm, a prototype), dedicate a section to describing how it works and the design rationale.

### Structure Pattern
1. Purpose of the artefact — what problem does it address?
2. Architecture / design overview
3. Key implementation decisions and rationale
4. How the artefact connects to the research questions

### Behavioral Rules
- **Do:** Include this section only if the artefact is central to the research
- **Do:** Explain design rationale — why was it built this way?
- **Do:** Use diagrams/figures to illustrate architecture
- **Avoid:** Turning this into a user manual — focus on design decisions relevant to the research
- **Avoid:** Including low-level implementation details unless they are methodologically relevant

### Tone
Technical and explanatory. The reader should understand what was built and why.

---

## Methodology

### Goal
Describe what was done in enough detail for replication. Justify methodological choices.

### Structure Pattern (Professor's Required Subsections)
1. Research design overview
2. Study participants and recruitment (note if ethics approval was necessary)
3. Materials — questionnaires, interview guidelines, artefacts that constitute an intervention, specific measurement devices
4. Data collection
5. Data analysis
6. Implementation details (tools, libraries, configurations — if applicable)

### Behavioral Rules
- **Do:** Use past tense — you already did this
- **Do:** Be precise about parameters, versions, configurations
- **Do:** Justify choices: "We used BERT-base rather than BERT-large because..."
- **Do:** Reference established methods by citation, don't re-explain known techniques
- **Avoid:** Vague descriptions: "we processed the data" — how exactly?
- **Avoid:** Unnecessary justification of standard choices (e.g., defending the use of Python)
- **Avoid:** Listing every possible alternative — focus on the chosen approach and its rationale

### Tone
Precise and methodical. Reads like a technical recipe with reasoning attached.

### AI Tells to Watch
- CP-07 (Premature Solutionism) — claiming the approach "solves" the problem before showing evidence
- LP-04 (Nominalization Overload) — "the implementation of the optimization of..."
- LP-03 (Passive Overuse) — methodology sections are the most prone to unnecessary passive
- SP-06 (List-Heavy Exposition) — methodology as a bulleted checklist rather than connected prose
- SP-07 (Heading-Body Redundancy) — "Data Collection: This section describes the data collection..."

---

## Results

### Goal
Present findings clearly and objectively. Separate observation from interpretation (interpretation goes in Discussion).

### Structure Pattern
1. Restate evaluation setup briefly (one sentence — don't repeat Methodology)
2. Present main results (usually with tables/figures)
3. Present secondary/supporting results
4. Note unexpected findings without over-explaining them here

### Behavioral Rules
- **Do:** Use past tense — these are things that happened
- **Do:** Reference tables and figures explicitly: "Table 3 shows that..."
- **Do:** Report negative or null results — they matter
- **Do:** Use precise numbers: "89.3% accuracy (SD = 2.1)" not "high accuracy"
- **Avoid:** Interpreting why results occurred — save that for Discussion
- **Avoid:** Subjective qualifiers: "impressive", "remarkable", "surprisingly good" (XP-05)
- **Avoid:** Cherry-picking results — report the full picture

### Tone
Factual and restrained. Let the numbers speak.

### AI Tells to Watch
- XP-05 (Artificial Enthusiasm) — "excitingly", "impressively"
- CP-09 (Scope Overclaiming) — "conclusively demonstrates superiority"
- LP-08 (Adverb Overuse) — "significantly improved" without statistical significance testing
- CP-02 (Over-Qualifying) — hedging clear results
- SP-01 (Uniform Sentence Length) — results sections often fall into a monotonous "X achieved Y" rhythm

---

## Discussion

### Goal
Interpret results, connect to related work, acknowledge limitations, and explore implications.

### Structure Pattern
1. Summarize key findings (briefly — don't repeat Results)
2. Interpret and explain results — why did these outcomes occur?
3. Compare with related work — how do findings align or diverge?
4. Acknowledge limitations honestly and specifically
5. Discuss practical implications

### Behavioral Rules
- **Do:** Mix present and past tense — interpret past results in present-tense context
- **Do:** Connect findings back to the research questions from the Introduction
- **Do:** Be specific about limitations: "Our evaluation used only English queries; generalization to other languages is untested" not "the study has some limitations"
- **Do:** Discuss unexpected results — they are often the most interesting
- **Avoid:** Simply restating results — add analytical depth
- **Avoid:** Introducing entirely new data or experiments
- **Avoid:** Over-hedging limitations to the point of undermining your own work

### Tone
Reflective and analytical. The author demonstrates mature scientific thinking.

### AI Tells to Watch
- CP-06 (Circular Reasoning) — "the system works well because it achieves good results"
- CP-01 (Excessive Hedging) — undermining valid conclusions
- XP-02 (Unnecessary Disclaimers) — over-caveating everything
- XP-03 (Performative Objectivity) — "objectively speaking..."
- LP-09 (Coordinated Triplets) — "robust, scalable, and efficient"

---

## Conclusion

### Goal
Synthesize (not summarize) the thesis contribution, state limitations concisely, and point to future work.

### Structure Pattern
1. Restate the research objective and what was achieved (1-2 sentences)
2. Synthesize key contributions — what does this work mean for the field?
3. Concise limitations (don't repeat Discussion at length)
4. Concrete future work directions

### Behavioral Rules
- **Do:** Use present tense for what the work demonstrates; future tense for future work
- **Do:** Be concrete about future work: "Extending the schema linker to support multi-database queries" not "further research is needed"
- **Do:** Keep it concise — the Conclusion should be shorter than the Discussion
- **Avoid:** Introducing new arguments or evidence
- **Avoid:** Copy-pasting the Abstract or Introduction with minor rewording (SP-05)
- **Avoid:** Grand final statements about the future of AI (CP-05, CP-10)

### Tone
Confident and forward-looking, but measured.

### AI Tells to Watch
- SP-05 (Conclusion-Mirroring) — restating the introduction verbatim
- CP-05 (Inflated Significance) — "this groundbreaking work..."
- CP-03 (Generic Claims) — "this has wide-ranging implications for the field"
- XP-04 (Reader Hand-Holding) — "as we have seen throughout this thesis..."
- LP-02 (Predictable Transitions) — "In conclusion, to summarize, ultimately..."
