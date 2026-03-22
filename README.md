# Thesis Writing Assistant

A Claude skill that transforms AI-assisted thesis drafts into authentic, publication-quality academic writing for CS/IS Master's theses.

## Install

```bash
# Install for current project
npx thesis-writing-assistant install

# Install globally (available in all projects)
npx thesis-writing-assistant install --global
```

Or manually clone and copy:

```bash
git clone https://github.com/bolishakim/thesis-writing-assistant.git
cp -r thesis-writing-assistant ~/.claude/skills/
```

## What It Does

- Detects and removes 34 AI writing anti-patterns across 4 categories
- Rewrites text following section-specific academic conventions
- Preserves all LaTeX commands (`\cite{}`, `\ref{}`, math environments)
- Scores text 0-100 on academic authenticity (deterministic Python scorer)
- Produces traceable audit reports with pattern IDs

## Trigger Phrases

| Phrase | Mode | What Happens |
|--------|------|-------------|
| "humanize", "de-AI", "academic rewrite" | Full Rewrite | Scan + Rewrite + Audit + Domain Validation |
| "polish", "clean up" | Quick Polish | Rewrite only |
| "audit", "check", "score" | Audit Only | Scan + Score (no changes) |
| "refine [section]" | Section Refine | Scan + Rewrite + Audit for one section |

## Scorer

Run the standalone scorer on any `.tex` file:

```bash
python .claude/skills/thesis-writing-assistant/scripts/academic_scorer.py thesis.tex --section methodology
```

## Specializations

- **Domains:** Conversational BI, NL2SQL, TAM, multi-agent LLM systems
- **Sections:** Introduction, Related Work, Methodology, Results, Discussion, Conclusion
- **Tense rules:** Section-specific (Intro=present, Methods=past, Results=past, etc.)
- **LaTeX:** Full preservation of citations, references, math, custom macros

## License

MIT
