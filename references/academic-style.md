# Academic Style Guide

Rules for producing authentic academic prose in a CS/IS Master's thesis.

**Important:** Also read `references/professor-style-guide.md` for supervisor-specific rules that take precedence when they conflict with generic conventions below.

---

## Simplicity First (Professor's Rule)

Write simply. The content is typically complex enough — do not add complexity through the language. Prefer short, clear sentences. Check for overly long sentences.

## Consistent Wording (Professor's Rule)

In contrast to literary writing, academic writing should reuse the same words for the same concepts and artefacts. Do not rotate synonyms for technical terms. If you call it "the system" in one paragraph, do not switch to "the framework" or "the platform" in the next — unless they genuinely mean different things. Consistency is more important than stylistic variety when it comes to terminology.

## Narrative Thread (Professor's Rule)

Build a line of argumentation throughout each section and chapter. The reader should feel the text is going somewhere, not just listing facts. Each section should have a logical flow that advances the overall argument.

---

## Voice and Tone

### Person
- **First person plural ("we")** for the author's own actions: "We conducted...", "We propose...", "Our results show..."
- **Third person** for other researchers: "Smith et al. demonstrated...", "Their approach differs..."
- Avoid first person singular ("I") unless the thesis committee explicitly requires it
- Never use second person ("you") in the thesis body

### Tone
- Confident but measured — state findings directly without inflating or deflating
- Technical precision over accessibility — this is a thesis, not a blog post
- Allow the evidence to carry the argument; don't editorialize

### Hedging Rules
- Hedge only when genuinely uncertain or when data is inconclusive
- Acceptable: "The results suggest..." (when causation isn't established)
- Unacceptable: "The results might possibly suggest..." (double-hedging)
- One qualifier per claim maximum

---

## Grammar Rules

### Active vs. Passive Voice
- Prefer active voice for clarity: "We trained the model" over "The model was trained"
- Passive is acceptable when the agent is irrelevant or unknown: "The dataset was collected from public repositories" (who collected it matters less than what was collected)
- Target: no more than 30% passive sentences in any section

### Oxford Comma
- Always use the Oxford comma: "accuracy, latency, and throughput" — not "accuracy, latency and throughput"

### Hyphenation
- Compound modifiers before a noun: "well-known approach", "state-of-the-art system"
- No hyphen after adverbs ending in -ly: "widely adopted method" (no hyphen)
- No hyphen when the compound follows the noun: "the approach is well known"

### Articles
- Use "the" for specific references: "the model described in Section 3"
- Use "a/an" for first introduction or general reference: "a transformer-based architecture"
- Omit articles before plural generic nouns: "Large language models exhibit..." (not "The large language models exhibit...")

---

## Tense Rules by Section

Each section has a dominant tense. Mixing is acceptable when the context requires it, but the dominant tense should prevail.

| Section | Dominant Tense | Rationale | Example |
|---------|---------------|-----------|---------|
| Introduction | Present | Sets up the current state of the problem | "Enterprise BI systems rely on..." |
| Related Work | Past / Present Perfect | Reports what others did or have established | "Chen et al. (2023) proposed..." / "Several studies have examined..." |
| Methodology | Past | Describes what you did | "We collected data from..." / "The model was trained on..." |
| Results | Past | Reports what happened | "The system achieved 89% accuracy..." |
| Discussion | Present + Past | Interprets past results in present context | "These results indicate that..." / "The error analysis revealed..." |
| Conclusion | Present + Future | Summarizes implications and future work | "This work demonstrates..." / "Future work will explore..." |

---

## Sentence Construction

### Length Targets
- **Average:** 18-22 words per sentence
- **Range:** 8-35 words — some short, some long
- **Forbidden:** No sentence over 45 words (split it)
- **Forbidden:** No sequence of 4+ sentences all within 3 words of each other in length

### Variety in Openings
Avoid starting consecutive sentences the same way. Vary among:
- Subject-first: "The parser identifies..."
- Prepositional phrase: "In our evaluation,..."
- Adverbial clause: "Although prior work focused on..."
- Transition from prior sentence: continuing the thought without a connective
- Participial phrase (sparingly): "Trained on 50k examples, the model..."

### Clause Structure
- Mix simple, compound, and complex sentences
- Avoid more than two dependent clauses in a single sentence
- Place the most important information at the beginning or end of the sentence, not buried in the middle

---

## Paragraph Construction

### Core Principle (Professor's Rule)
Each paragraph should make a single statement or advance a single point. A new thought = a new paragraph. This is the fundamental unit of academic argumentation.

### Structure
- Not every paragraph needs a topic sentence — some can begin with evidence, a contrast, or a continuation
- **Typical length:** 10-20 lines (~5-10 sentences), per professor's guidance
- Short paragraphs (2-3 sentences) are acceptable for transitions but should not be the norm
- Long paragraphs are fine for complex arguments but must remain internally coherent and focused on one point

### Varied Openings
Do not start consecutive paragraphs with:
- The same word
- The same syntactic structure
- A formulaic transition ("Furthermore", "Moreover", "Additionally" in sequence)

### Argument Advancement
Every paragraph must advance the argument. If a paragraph could be removed without losing any information or logical step, it should be removed or merged.

---

## Word Choice

### Domain-Specific Terms
Use precise technical vocabulary from the thesis domain:
- "Schema linking" not "connecting queries to database structures"
- "Intent classification" not "figuring out what the user wants"
- "Perceived usefulness" (TAM) — always as a defined construct, not casually

### Banned Words and Phrases
Replace these with specific alternatives:

| Banned | Replace With |
|--------|-------------|
| utilize | use |
| facilitate | enable, support, allow |
| leverage | use, build on, apply |
| methodology (when "method" suffices) | method, approach, procedure |
| novel (overused) | [describe what's new specifically] |
| robust (vague) | [describe what makes it resilient] |
| comprehensive (vague) | [describe the scope specifically] |
| delve into | examine, analyze, investigate |
| in terms of | [restructure the sentence] |
| a plethora of | many, several, numerous |
| at the end of the day | [delete] |
| it goes without saying | [delete — then say it if it matters] |
| needless to say | [delete] |
| in today's world | [delete or give a specific time frame] |

### Acronyms
- Define on first use: "Technology Acceptance Model (TAM)"
- Use the acronym consistently after definition
- Re-define at the start of each chapter if the thesis uses chapter-based structure

---

## Natural Imperfection Targets

Real human academic writing is not uniformly polished. To produce authentic output:

- **Allow one slightly awkward transition** per ~500 words — a place where the logical flow is adequate but not elegant
- **Permit occasional longer sentences** (30-35 words) even if they could be split — sometimes the thought is genuinely complex
- **Don't over-optimize every clause** — if a sentence is clear and correct, leave it even if a "better" phrasing exists
- **Vary quality across paragraphs** — some paragraphs will be tighter than others, and that's realistic
- **Keep the author's characteristic phrasings** when they are clear and grammatically correct, even if unusual — these are part of voice

The goal is writing that a thesis committee would accept without comment, not writing that wins a prose style award.
