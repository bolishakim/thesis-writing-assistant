# LaTeX Conventions

Rules for preserving and correctly formatting LaTeX content during rewrites.

---

## Preservation Rules (Critical)

Never modify any of the following — copy them character-for-character from input to output:

### Citation Commands
- `\cite{key}`, `\citep{key}`, `\citet{key}`, `\citeauthor{key}`, `\citeyear{key}`
- Multi-key citations: `\cite{key1, key2, key3}`
- Do not reorder citation keys
- Do not remove or add citations — if a claim needs a citation that doesn't exist, insert `\cite{??NEEDED}`

### Cross-References
- `\ref{label}`, `\autoref{label}`, `\cref{label}`, `\Cref{label}`
- `\label{text}` — never modify label text
- `\pageref{label}`
- `\eqref{label}`

### Math Environments
- Inline math: `$...$` and `\(...\)`
- Display math: `\[...\]`, `$$...$$`
- Named environments: `equation`, `equation*`, `align`, `align*`, `gather`, `multline`, `split`
- Do not rewrite text inside math environments
- Do not change variable names or notation

### Custom Macros
- Any command starting with `\` that isn't standard LaTeX — preserve as-is
- Common thesis macros: `\eg`, `\ie`, `\cf`, `\etal`, custom abbreviation commands

### Environments
- `figure`, `table`, `algorithm`, `listing`, `verbatim`, `lstlisting`
- Preserve all content within these environments unchanged
- You may edit captions if they contain AI patterns, but preserve all labels and references within them

---

## Citation Style in Prose

### Author-Year in Running Text
When a citation is part of the sentence, use the author name with the citation command:
- "Chen et al.~\citep{chen2023}" or "as shown by \citet{chen2023}"
- Do not write "Chen et al. (2023)" as plain text if the original uses `\cite` commands — preserve the LaTeX command

### Parenthetical at End of Clause
When citing a supporting source, place the citation at the end:
- "Transformer architectures dominate sequence modeling tasks~\citep{vaswani2017}."
- Not: "~\citep{vaswani2017} Transformer architectures dominate..."

### Missing Citations
When the rewrite reveals a claim that needs a citation but doesn't have one:
- Insert: `\cite{??NEEDED}` — this makes missing citations searchable and visible
- Add a comment: `%% [REVIEW: citation needed for this claim]`

---

## Formatting Conventions

### Acronyms
- First use in each chapter: "Natural Language to SQL (NL2SQL)"
- Subsequent uses: "NL2SQL" (no re-expansion unless starting a new chapter)
- In LaTeX, if the original uses an acronym package (`\ac{}`, `\acrshort{}`), preserve those commands

### Numbers
- Spell out numbers under 10 in prose: "three experiments", "seven participants"
- Use numerals for 10 and above: "12 features", "150 queries"
- Always use numerals with units: "5 ms", "3 GB"
- Always use numerals in technical contexts: "layer 2", "epoch 5"
- Percentages: "12%" in parenthetical/tabular, "12 percent" or "12\%" in prose (match the original's convention)

### Table, Figure, and Equation References
- Capitalize when referencing by number: "Table~3", "Figure~\ref{fig:arch}", "Equation~\eqref{eq:loss}"
- Use non-breaking space (`~`) before `\ref`, `\autoref`, or the number
- Lowercase when generic: "the following table", "as shown in the figure above"

### Non-Breaking Spaces
Insert `~` (non-breaking space) in these positions:
- Before `\cite`: `evidence~\citep{key}`
- Before `\ref`: `Table~\ref{tab:results}`
- Between number and unit: `5~ms`, `128~GB`
- After "et" in "et~al." (if not using a macro)
- After abbreviations: `e.g.,~`, `i.e.,~`, `cf.~`

---

## Thesis-Specific Conventions

### En-Dash Ranges
- Page ranges: "pp.~12--15" (en-dash, not hyphen)
- Year ranges: "2020--2024"
- Numerical ranges: "layers 3--6"

### Paragraph Breaks
- Use blank lines for paragraph breaks, not `\\` or `\newline`
- Do not add `\noindent` unless the original uses it consistently

### Line Break Rules
- Do not break lines inside `\cite{}`, `\ref{}`, or other commands
- Keep command arguments on the same line as the command when possible

### Comments
- Preserve existing `%` comments unchanged
- Add review comments as: `%% [REVIEW: description]` (double percent for visibility)
- Never delete the author's existing comments
