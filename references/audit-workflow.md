# Audit Workflow

Two-pass audit system with 5-dimension scoring. Use this file during Phase 3 (Self-Audit).

---

## Pass 1: Rewrite and Log

During the rewrite phase, maintain a running log of every pattern addressed:

```
Pattern Log:
- Sentence "Moreover, it is important to note..." -> LP-01 (removed filler) + XP-04 (removed hand-holding)
- Sentence "This groundbreaking approach..." -> CP-05 (replaced inflated language)
- ...
```

This log feeds into the audit scoring below.

---

## Self-Audit Scoring

After completing the rewrite, evaluate the output on these 5 dimensions. Each dimension has an explicit checklist — score by counting how many checklist items pass.

### Dimension 1: AI Pattern Residue (0-10, lower is better)

Re-scan the rewritten text against all 34 patterns from `ai-patterns.md`. Score based on how many patterns remain detectable:

| Score | Meaning |
|-------|---------|
| 0-1 | Excellent — virtually no detectable patterns |
| 2-3 | Good — minor traces that a reader wouldn't notice |
| 4-5 | Acceptable — some patterns linger but don't dominate |
| 6-7 | Needs work — AI-generated quality is noticeable |
| 8-10 | Poor — text still reads as AI-generated |

**Checklist (check each, count failures):**
1. No filler phrases remain (LP-01)
2. No predictable transition sequences (LP-02)
3. No coordinated triplets used for padding (LP-09)
4. No collocational cliches (LP-07)
5. No excessive hedging clusters (CP-01)
6. No generic claims without specifics (CP-03)
7. No inflated significance language (CP-05)
8. No meta-commentary about the text itself (XP-01)
9. No uniform sentence complexity / low burstiness (SP-09)
10. No predictable word choices / low perplexity (SP-10)

Score = number of failures. If score > 3, trigger Pass 2.

### Dimension 2: Academic Voice Fidelity (0-10, higher is better)

Evaluate whether the text sounds like competent graduate-level academic writing.

**Checklist (check each, count passes):**
1. Consistent use of "we" for author actions
2. Appropriate tense for the section type
3. Active voice predominates (>70% of sentences)
4. Technical terms used precisely and consistently
5. No banned words (utilize, facilitate, leverage, etc.)
6. Hedging is proportionate to uncertainty
7. Claims are attributed to specific sources
8. Tone matches the section (factual in Results, analytical in Discussion)
9. No informal language or colloquialisms
10. Acronyms defined on first use

Score = number of passes.

### Dimension 3: Technical Accuracy Preservation (0-10, higher is better)

Verify that the rewrite preserved all technical content from the original.

**Checklist (check each, count passes):**
1. All numerical values preserved exactly
2. All method names preserved correctly
3. All author names and years in citations preserved
4. All technical terms used with their original meaning
5. No causal claims added that weren't in the original
6. No results softened or strengthened beyond the original
7. All acronyms expanded correctly
8. Mathematical notation unchanged
9. System/model names consistent with original
10. No new claims or data introduced

Score = number of passes.

### Dimension 4: Structural Naturalness & Burstiness (0-10, higher is better)

Evaluate whether the text has the varied, organic structure of human writing. Pay special attention to **burstiness** — the variance of complexity across sentences, which is GPTZero's primary detection signal.

**Checklist (check each, count passes):**
1. Sentence lengths vary (standard deviation > 5 words)
2. Sentence **complexity** varies — simple factual sentences alternate with dense analytical ones (burstiness)
3. No run of 3+ consecutive sentences at the same complexity level
4. Paragraph lengths vary (not all the same sentence count)
5. At least one sentence under 12 words and one over 25 words per 500 words
6. Paragraph openings are varied (not all topic sentences)
7. Transitions feel organic, not mechanical
8. Domain-specific terms and concrete specifics reduce token predictability
9. No symmetric subsection structures (identical lengths)
10. Text has been structurally rewritten, not just lexically substituted (argument flow differs from AI-typical claim→support→summary)

Score = number of passes.

### Dimension 5: LaTeX Integrity (Pass/Fail)

Binary — any failure here means the rewrite has introduced a LaTeX error that would break compilation.

**Checklist (all must pass):**
1. All `\cite{}` commands preserved with original keys
2. All `\ref{}` and `\label{}` commands preserved
3. All math environments intact (`$...$`, `\[...\]`, `equation`, `align`, etc.)
4. No new LaTeX commands introduced that weren't in the original
5. All custom macros preserved unchanged

Result: **Pass** if all 5 pass, **Fail** if any fail. A Fail requires immediate correction before output.

---

## Conditional Pass 2

**Trigger condition:** AI Pattern Residue score > 3

Pass 2 is a targeted revision, not a full rewrite:
1. Identify the specific sentences flagged during the residue re-scan
2. Rewrite only those sentences
3. Preserve all surrounding context unchanged
4. Re-score Dimension 1 after Pass 2 corrections
5. Log which patterns were addressed in Pass 2

Pass 2 should not introduce new problems — if a flagged sentence is technically accurate and the pattern is mild (severity: Low), it may be acceptable to leave it.

---

## Domain Validation (Optional — Phase 4)

For thesis-specific technical checks. Run only in Full Rewrite mode.

### NL2SQL Checks
- SQL keywords used correctly (SELECT, JOIN, WHERE, GROUP BY, etc.)
- Schema terms (tables, columns, foreign keys) preserved from original
- Query translation terminology consistent (e.g., "semantic parsing" vs "text-to-SQL" — use whatever the original uses)

### TAM Checks
- Core constructs named correctly: Perceived Usefulness (PU), Perceived Ease of Use (PEOU), Behavioral Intention (BI), Actual Use
- Causal relationships described accurately (PU -> BI, PEOU -> PU, PEOU -> BI)
- Survey instrument references preserved

### Conversational BI Checks
- Dialog management terminology consistent
- Intent recognition / NLU pipeline terms accurate
- Multi-turn conversation concepts used correctly

### Multi-Agent LLM Checks
- Agent roles described accurately (planner, executor, critic, etc.)
- Orchestration patterns named correctly
- Tool-use and function-calling terminology precise

Flag any domain term that may have been altered with: `%% [REVIEW: domain term changed — verify "{original}" -> "{rewritten}"]`

---

## Output Format

After completing the audit, produce this report:

```
## Audit Report

| Dimension | Score | Notes |
|-----------|-------|-------|
| AI Pattern Residue | X/10 | [list any remaining patterns by ID] |
| Academic Voice Fidelity | X/10 | [note any checklist failures] |
| Technical Accuracy | X/10 | [note any concerns] |
| Structural Naturalness | X/10 | [note any issues] |
| LaTeX Integrity | Pass/Fail | [note any fixes applied] |

**Patterns addressed:** [list all pattern IDs addressed in Pass 1]
**Patterns addressed in Pass 2:** [if applicable]
**Patterns remaining:** [list any, with severity]
**Total passes:** 1 [or 2]
```
