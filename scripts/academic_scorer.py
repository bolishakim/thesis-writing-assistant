#!/usr/bin/env python3
"""
academic_scorer.py — Scores thesis text 0-100 on academic authenticity
by detecting AI writing patterns specific to academic CS/IS writing.

Dimensions (100 points total):
  1. AI Vocabulary       /20  — flags AI-typical words from the 34-pattern taxonomy
  2. Hedging & Filler    /20  — detects compulsive hedging and filler phrases
  3. Sentence Variance   /15  — measures rhythm variety (std dev of sentence lengths)
  4. Passive Voice       /10  — flags excessive passive construction
  5. Paragraph Structure /10  — checks for formulaic uniformity
  6. Transition Patterns /10  — detects predictable sequential transitions
  7. Tense Consistency   /10  — checks dominant tense matches declared section type
  8. LaTeX Integrity      /5  — verifies LaTeX commands are well-formed

Usage:
  python academic_scorer.py <file.tex>              # score a file
  python academic_scorer.py <file.tex> --json        # also output JSON
  python academic_scorer.py <file.tex> --section methodology  # specify section type
  python academic_scorer.py                          # run demo with sample text
"""

import sys
import re
import json
import math
import argparse
from collections import Counter


# ── AI Vocabulary (from our 34-pattern taxonomy) ─────────────────────────────

# Content Patterns (CP): inflated/generic language
AI_CONTENT_WORDS = [
    "groundbreaking", "paradigm shift", "paradigm-shifting", "revolutionary",
    "unprecedented", "game-changing", "transformative",
    "comprehensive", "holistic",
    "novel",  # overused in AI academic writing
    "robust",  # vague without specifics
    "cutting-edge", "state-of-the-art",  # only flagged when not citing benchmarks
]

# Language Patterns (LP): filler verbs, cliches, weak vocabulary
AI_LANGUAGE_WORDS = [
    "utilize", "utilizes", "utilizing", "utilization",
    "facilitate", "facilitates", "facilitating",
    "leverage", "leverages", "leveraging", "leveraged",
    "delve", "delves", "delving",
    "foster", "fosters", "fostering",
    "streamline", "streamlines", "streamlining",
    "empower", "empowers", "empowering",
    "underscore", "underscores", "underscoring",
    "elucidate", "elucidates", "elucidating",
    "endeavor", "endeavors",
    "plethora",
    "myriad",
    "pivotal",
    "crucial",  # flagged when used as generic intensifier
    "vital",
    "seamless", "seamlessly",
]

# Collocational cliches (LP-07)
AI_CLICHES = [
    "plays a crucial role", "plays a vital role", "plays a pivotal role",
    "sheds light on", "shed light on",
    "paves the way", "paving the way",
    "bridges the gap", "bridging the gap",
    "the lion's share",
    "at the end of the day",
    "in today's world", "in today's rapidly",
    "the ever-evolving", "ever-growing",
    "rapidly evolving", "rapidly changing",
    "a growing body of", "a large body of",
    "in the realm of", "in the field of",
]

# Communication Patterns (XP): meta-commentary, disclaimers
AI_COMMUNICATION = [
    "it is important to note",
    "it is worth noting",
    "it should be noted",
    "it is worth mentioning",
    "it is crucial to",
    "it goes without saying",
    "needless to say",
    "in this section we will",
    "in the following section",
    "as we will see",
    "as discussed above",
    "as mentioned earlier",
    "objectively speaking",
    "from an unbiased perspective",
    "it must be acknowledged",
]

# Hedging chains (CP-01, CP-02)
HEDGING_PHRASES = [
    "could potentially",
    "might possibly",
    "may or may not",
    "it is possible that",
    "it appears that",
    "it seems that",
    "there may be",
    "one might argue",
    "it can be argued",
    "to some extent",
    "in certain cases",
    "in some instances",
    "results may vary",
    "while not definitive",
    "preliminary evidence suggests",
]

# Weasel words (LP-05)
WEASEL_PHRASES = [
    "many researchers",
    "some researchers",
    "several studies",
    "numerous studies",
    "it is widely accepted",
    "it is generally agreed",
    "there is a growing consensus",
    "the literature suggests",
    "the literature overwhelmingly",
    "experts agree",
    "experts believe",
    "it has been shown",
    "research has demonstrated",
]

# Coordinated triplets (LP-09)
TRIPLET_PATTERN = re.compile(
    r'\b(\w+),\s+(\w+),\s+and\s+(\w+)\b', re.IGNORECASE
)
COMMON_AI_TRIPLETS = [
    {"robust", "scalable", "efficient"},
    {"robust", "reliable", "efficient"},
    {"accurate", "reliable", "efficient"},
    {"innovative", "comprehensive", "robust"},
    {"analyze", "evaluate", "assess"},
    {"effective", "efficient", "scalable"},
]

# Artificial enthusiasm (XP-05)
ENTHUSIASM_WORDS = [
    "excitingly", "impressively", "remarkably", "fascinatingly",
    "interestingly", "surprisingly", "notably",
    "exceptional", "outstanding", "extraordinary",
    "impressive", "remarkable", "fascinating",
]

# Predictable transitions (LP-02)
SEQUENTIAL_TRANSITIONS = [
    "furthermore", "moreover", "additionally", "in addition",
    "on the other hand", "conversely", "similarly",
    "consequently", "subsequently", "accordingly",
]

# ── Passive voice patterns ───────────────────────────────────────────────────

PASSIVE_PATTERNS = [
    re.compile(r'\b(is|are|was|were|be|been|being)\s+(being\s+)?\w+ed\b', re.IGNORECASE),
    re.compile(r'\b(can|could|should|would|may|might|must)\s+be\s+\w+ed\b', re.IGNORECASE),
]

# ── Tense detection ──────────────────────────────────────────────────────────

PAST_TENSE_MARKERS = re.compile(
    r'\b(we\s+)?(conducted|collected|performed|trained|evaluated|tested|'
    r'achieved|obtained|observed|found|showed|demonstrated|implemented|'
    r'designed|developed|applied|analyzed|measured|recorded|computed|'
    r'ran|built|used|chose|selected)\b', re.IGNORECASE
)

PRESENT_TENSE_MARKERS = re.compile(
    r'\b(we\s+)?(conduct|collect|perform|train|evaluate|test|'
    r'achieve|obtain|observe|find|show|demonstrate|implement|'
    r'design|develop|apply|analyze|measure|is|are|has|have|'
    r'indicates?|suggests?|represents?|provides?|requires?|'
    r'remains?|exists?)\b', re.IGNORECASE
)

FUTURE_TENSE_MARKERS = re.compile(
    r'\b(will|shall|going to|aim to|plan to|intend to)\b', re.IGNORECASE
)

SECTION_TENSE_MAP = {
    "introduction":  "present",
    "related work":  "past",
    "literature":    "past",
    "background":    "past",
    "methodology":   "past",
    "method":        "past",
    "methods":       "past",
    "design":        "past",
    "implementation":"past",
    "results":       "past",
    "evaluation":    "past",
    "experiments":   "past",
    "discussion":    "mixed",
    "conclusion":    "present",
    "conclusions":   "present",
    "future work":   "future",
}

# ── LaTeX patterns ───────────────────────────────────────────────────────────

LATEX_CITE = re.compile(r'\\(cite[pt]?|citet|citep|citeauthor|citeyear)\{[^}]*\}')
LATEX_REF = re.compile(r'\\(ref|autoref|cref|Cref|eqref|label|pageref)\{[^}]*\}')
LATEX_MATH_INLINE = re.compile(r'\$[^$]+\$')
LATEX_MATH_DISPLAY = re.compile(r'\\\[.*?\\\]', re.DOTALL)
LATEX_ENV = re.compile(r'\\begin\{(equation|align|gather|multline|split|figure|table)\*?\}')
LATEX_UNCLOSED_BRACE = re.compile(r'\\(cite[pt]?|ref|label|autoref|cref)\{[^}]*$', re.MULTILINE)


# ── Utility ──────────────────────────────────────────────────────────────────

def strip_latex_commands(text: str) -> str:
    """Remove LaTeX commands for prose analysis, keeping the prose words."""
    # Remove math environments
    text = re.sub(r'\$[^$]+\$', ' MATH ', text)
    text = re.sub(r'\\\[.*?\\\]', ' MATH ', text, flags=re.DOTALL)
    text = re.sub(r'\\begin\{(equation|align|gather|multline)\*?\}.*?\\end\{\1\*?\}', ' MATH ', text, flags=re.DOTALL)
    # Remove cite/ref commands but keep surrounding text
    text = re.sub(r'~?\\(cite[pt]?|citet|citep|citeauthor|citeyear)\{[^}]*\}', '', text)
    text = re.sub(r'~?\\(ref|autoref|cref|Cref|eqref|pageref)\{[^}]*\}', 'REF', text)
    # Remove other LaTeX commands
    text = re.sub(r'\\(section|subsection|subsubsection|paragraph|label|textbf|textit|emph)\{([^}]*)\}', r'\2', text)
    text = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    # Remove comments
    text = re.sub(r'(?<!\\)%.*$', '', text, flags=re.MULTILINE)
    # Clean up
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def get_sentences(text: str) -> list:
    """Split text into sentences, handling LaTeX and abbreviations."""
    clean = strip_latex_commands(text)
    # Split on sentence boundaries, being careful with abbreviations
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', clean)
    return [s.strip() for s in sentences if len(s.split()) >= 3]


def get_paragraphs(text: str) -> list:
    """Split text into paragraphs, ignoring LaTeX environment blocks."""
    # Remove LaTeX environments (figures, tables, equations)
    clean = re.sub(r'\\begin\{(figure|table|algorithm|equation|align)\*?\}.*?\\end\{\1\*?\}', '', text, flags=re.DOTALL)
    paragraphs = re.split(r'\n\s*\n', clean)
    return [p.strip() for p in paragraphs if p.strip() and len(p.split()) >= 5 and not p.strip().startswith('\\')]


# ── Scoring Functions ────────────────────────────────────────────────────────

def score_ai_vocabulary(text: str) -> dict:
    """Score 0-20: fewer AI-typical words = higher score."""
    text_lower = text.lower()
    word_count = max(1, len(re.findall(r'\b\w+\b', text_lower)))

    hits = []
    all_terms = AI_CONTENT_WORDS + AI_LANGUAGE_WORDS + AI_CLICHES + ENTHUSIASM_WORDS
    for phrase in all_terms:
        count = text_lower.count(phrase.lower())
        if count > 0:
            hits.append((phrase, count))

    total_hits = sum(c for _, c in hits)
    density = total_hits / (word_count / 100)

    if total_hits == 0:
        score = 20
    elif total_hits <= 2:
        score = 16
    elif total_hits <= 5:
        score = 12
    elif total_hits <= 8:
        score = 7
    elif total_hits <= 12:
        score = 3
    else:
        score = 0

    return {
        "score": score,
        "max": 20,
        "total_hits": total_hits,
        "density_per_100": round(density, 2),
        "flagged": [f"{t} ({c}x)" for t, c in sorted(hits, key=lambda x: -x[1])[:10]],
    }


def score_hedging_and_filler(text: str) -> dict:
    """Score 0-20: fewer hedging/filler/weasel phrases = higher score."""
    text_lower = text.lower()

    hedge_hits = []
    for phrase in HEDGING_PHRASES:
        count = text_lower.count(phrase)
        if count > 0:
            hedge_hits.append((phrase, count))

    filler_hits = []
    for phrase in AI_COMMUNICATION:
        count = text_lower.count(phrase)
        if count > 0:
            filler_hits.append((phrase, count))

    weasel_hits = []
    for phrase in WEASEL_PHRASES:
        count = text_lower.count(phrase)
        if count > 0:
            weasel_hits.append((phrase, count))

    total = sum(c for _, c in hedge_hits) + sum(c for _, c in filler_hits) + sum(c for _, c in weasel_hits)

    if total == 0:
        score = 20
    elif total <= 2:
        score = 16
    elif total <= 4:
        score = 11
    elif total <= 7:
        score = 6
    elif total <= 10:
        score = 2
    else:
        score = 0

    return {
        "score": score,
        "max": 20,
        "hedge_count": sum(c for _, c in hedge_hits),
        "filler_count": sum(c for _, c in filler_hits),
        "weasel_count": sum(c for _, c in weasel_hits),
        "total": total,
        "flagged": [f for f, _ in (hedge_hits + filler_hits + weasel_hits)][:10],
    }


def score_sentence_variance(text: str) -> dict:
    """Score 0-15: high variance in sentence length = more natural."""
    sentences = get_sentences(text)

    if len(sentences) < 4:
        return {"score": 8, "max": 15, "note": "too few sentences to score reliably"}

    lengths = [len(s.split()) for s in sentences]
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)

    # Check for short punchy sentences (sign of human writing)
    has_short = any(l <= 10 for l in lengths)
    has_long = any(l >= 28 for l in lengths)

    if std_dev >= 10:
        score = 15
    elif std_dev >= 7:
        score = 12
    elif std_dev >= 5:
        score = 8
    elif std_dev >= 3:
        score = 4
    else:
        score = 0

    # Bonus for range variety
    if has_short and has_long and score < 15:
        score = min(15, score + 2)

    return {
        "score": score,
        "max": 15,
        "std_dev": round(std_dev, 1),
        "avg_length": round(avg, 1),
        "min_length": min(lengths),
        "max_length": max(lengths),
        "has_short_sentences": has_short,
        "has_long_sentences": has_long,
        "sentence_count": len(sentences),
    }


def score_passive_voice(text: str) -> dict:
    """Score 0-10: less passive = clearer academic writing."""
    sentences = get_sentences(text)
    n_sentences = max(1, len(sentences))
    clean = strip_latex_commands(text)

    passive_count = 0
    for pattern in PASSIVE_PATTERNS:
        passive_count += len(pattern.findall(clean))

    ratio = passive_count / n_sentences

    if ratio < 0.15:
        score = 10
    elif ratio < 0.25:
        score = 8
    elif ratio < 0.35:
        score = 5
    elif ratio < 0.45:
        score = 2
    else:
        score = 0

    return {
        "score": score,
        "max": 10,
        "passive_count": passive_count,
        "ratio": round(ratio, 2),
        "pct": f"{round(ratio * 100)}%",
    }


def score_paragraph_structure(text: str) -> dict:
    """Score 0-10: varied paragraph lengths = more natural."""
    paragraphs = get_paragraphs(text)

    if len(paragraphs) < 3:
        return {"score": 5, "max": 10, "note": "too few paragraphs to score"}

    lengths = [len(p.split()) for p in paragraphs]
    avg = sum(lengths) / len(lengths)
    variance = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)

    # Check for variety
    has_short = any(l <= 30 for l in lengths)
    has_varied_openings = True
    first_words = [p.split()[0].lower().strip('\\') for p in paragraphs if p.split()]
    word_counts = Counter(first_words)
    if word_counts.most_common(1)[0][1] > len(paragraphs) * 0.4:
        has_varied_openings = False

    score = 0
    if std_dev >= 25:
        score += 5
    elif std_dev >= 15:
        score += 3
    elif std_dev >= 8:
        score += 2

    if has_short:
        score += 2
    if has_varied_openings:
        score += 3

    score = min(10, score)

    return {
        "score": score,
        "max": 10,
        "paragraph_count": len(paragraphs),
        "std_dev": round(std_dev, 1),
        "avg_words": round(avg, 1),
        "has_short_paragraphs": has_short,
        "varied_openings": has_varied_openings,
    }


def score_transitions(text: str) -> dict:
    """Score 0-10: penalizes sequential formulaic transitions (LP-02)."""
    text_lower = text.lower()
    paragraphs = get_paragraphs(text)

    # Count total transition words
    transition_hits = []
    for t in SEQUENTIAL_TRANSITIONS:
        count = text_lower.count(t)
        if count > 0:
            transition_hits.append((t, count))

    total_transitions = sum(c for _, c in transition_hits)

    # Check for sequential pattern (consecutive paragraphs opening with transitions)
    sequential_count = 0
    for p in paragraphs:
        first_word = p.strip().split()[0].lower().rstrip(',') if p.strip() else ""
        if first_word in [t.split()[0] for t in SEQUENTIAL_TRANSITIONS]:
            sequential_count += 1

    seq_ratio = sequential_count / max(1, len(paragraphs))

    # Also check for triplets (LP-09)
    triplet_matches = TRIPLET_PATTERN.findall(text_lower)
    ai_triplet_count = 0
    for m in triplet_matches:
        word_set = {m[0].lower(), m[1].lower(), m[2].lower()}
        for ai_trip in COMMON_AI_TRIPLETS:
            if len(word_set & ai_trip) >= 2:
                ai_triplet_count += 1

    if total_transitions <= 1 and seq_ratio < 0.15 and ai_triplet_count == 0:
        score = 10
    elif total_transitions <= 3 and seq_ratio < 0.25:
        score = 8
    elif total_transitions <= 5 and seq_ratio < 0.35:
        score = 5
    elif total_transitions <= 8:
        score = 3
    else:
        score = 0

    if ai_triplet_count > 0:
        score = max(0, score - 2 * ai_triplet_count)

    return {
        "score": score,
        "max": 10,
        "transition_count": total_transitions,
        "sequential_opening_ratio": round(seq_ratio, 2),
        "ai_triplets_found": ai_triplet_count,
        "flagged": [f for f, _ in transition_hits],
    }


def score_tense_consistency(text: str, section: str = None) -> dict:
    """Score 0-10: checks if dominant tense matches the expected section tense."""
    if section is None:
        # Try to auto-detect from \section{} commands
        section_match = re.search(r'\\section\{([^}]+)\}', text, re.IGNORECASE)
        if section_match:
            section = section_match.group(1).strip().lower()

    if section is None:
        return {"score": 5, "max": 10, "note": "section type unknown — specify with --section"}

    # Find expected tense
    expected = None
    for key, tense in SECTION_TENSE_MAP.items():
        if key in section.lower():
            expected = tense
            break

    if expected is None:
        return {"score": 5, "max": 10, "note": f"section '{section}' not in tense map"}

    clean = strip_latex_commands(text)

    past_count = len(PAST_TENSE_MARKERS.findall(clean))
    present_count = len(PRESENT_TENSE_MARKERS.findall(clean))
    future_count = len(FUTURE_TENSE_MARKERS.findall(clean))
    total = max(1, past_count + present_count + future_count)

    past_ratio = past_count / total
    present_ratio = present_count / total
    future_ratio = future_count / total

    if expected == "past":
        dominant_correct = past_ratio >= 0.5
        ratio = past_ratio
    elif expected == "present":
        dominant_correct = present_ratio >= 0.4
        ratio = present_ratio
    elif expected == "future":
        dominant_correct = future_ratio >= 0.3 or present_ratio >= 0.3
        ratio = future_ratio + present_ratio
    elif expected == "mixed":
        # Discussion: should have both present and past
        dominant_correct = past_ratio >= 0.2 and present_ratio >= 0.2
        ratio = min(past_ratio, present_ratio) * 2  # reward balance

    if dominant_correct and ratio >= 0.5:
        score = 10
    elif dominant_correct:
        score = 7
    else:
        score = 3

    return {
        "score": score,
        "max": 10,
        "section": section,
        "expected_tense": expected,
        "past_ratio": round(past_ratio, 2),
        "present_ratio": round(present_ratio, 2),
        "future_ratio": round(future_ratio, 2),
        "dominant_correct": dominant_correct,
    }


def score_latex_integrity(text: str) -> dict:
    """Score 0-5: checks that LaTeX commands are well-formed."""
    issues = []

    # Check for unclosed braces in cite/ref commands
    unclosed = LATEX_UNCLOSED_BRACE.findall(text)
    if unclosed:
        issues.append(f"unclosed brace in {len(unclosed)} command(s)")

    # Check for unmatched $ signs (inline math)
    dollar_count = text.count('$') - text.count('\\$')
    # Subtract $$ pairs (display math)
    double_dollar = text.count('$$')
    single_dollar = dollar_count - (double_dollar * 2)
    if single_dollar % 2 != 0:
        issues.append("unmatched $ sign (odd count)")

    # Check for \\begin without matching \\end
    begins = re.findall(r'\\begin\{(\w+\*?)\}', text)
    ends = re.findall(r'\\end\{(\w+\*?)\}', text)
    begin_counts = Counter(begins)
    end_counts = Counter(ends)
    for env, count in begin_counts.items():
        if end_counts.get(env, 0) != count:
            issues.append(f"unmatched \\begin{{{env}}} ({count} opens, {end_counts.get(env, 0)} closes)")

    # Check for \cite{} with empty keys
    empty_cites = re.findall(r'\\cite[pt]?\{\s*\}', text)
    if empty_cites:
        issues.append(f"{len(empty_cites)} empty \\cite{{}} command(s)")

    if len(issues) == 0:
        score = 5
    elif len(issues) == 1:
        score = 3
    elif len(issues) == 2:
        score = 1
    else:
        score = 0

    # Count LaTeX elements for info
    cite_count = len(LATEX_CITE.findall(text))
    ref_count = len(LATEX_REF.findall(text))
    math_count = len(LATEX_MATH_INLINE.findall(text)) + len(LATEX_MATH_DISPLAY.findall(text))

    return {
        "score": score,
        "max": 5,
        "issues": issues,
        "citations_found": cite_count,
        "references_found": ref_count,
        "math_expressions_found": math_count,
        "status": "Pass" if score == 5 else "Fail" if score == 0 else "Warning",
    }


# ── Main Scoring ─────────────────────────────────────────────────────────────

def score_academic_authenticity(text: str, section: str = None) -> dict:
    """Run all scoring dimensions and produce a total 0-100 score."""
    vocab = score_ai_vocabulary(text)
    hedging = score_hedging_and_filler(text)
    variance = score_sentence_variance(text)
    passive = score_passive_voice(text)
    paragraphs = score_paragraph_structure(text)
    transitions = score_transitions(text)
    tense = score_tense_consistency(text, section)
    latex = score_latex_integrity(text)

    total = (
        vocab["score"] + hedging["score"] + variance["score"] +
        passive["score"] + paragraphs["score"] + transitions["score"] +
        tense["score"] + latex["score"]
    )

    if total >= 85:
        label = "Authentic academic writing"
    elif total >= 70:
        label = "Mostly authentic — minor polish needed"
    elif total >= 55:
        label = "Mixed — AI patterns detectable"
    elif total >= 35:
        label = "Needs significant revision"
    else:
        label = "AI-generated quality — full rewrite required"

    return {
        "authenticity_score": total,
        "label": label,
        "sections": {
            "ai_vocabulary": vocab,
            "hedging_and_filler": hedging,
            "sentence_variance": variance,
            "passive_voice": passive,
            "paragraph_structure": paragraphs,
            "transition_patterns": transitions,
            "tense_consistency": tense,
            "latex_integrity": latex,
        }
    }


# ── Report Output ────────────────────────────────────────────────────────────

def print_report(result: dict, label: str = "") -> None:
    total = result["authenticity_score"]
    verdict = result["label"]
    s = result["sections"]

    bar_filled = int(total / 5)
    bar = "=" * bar_filled + "-" * (20 - bar_filled)

    print()
    print("+" + "=" * 50 + "+")
    print("|     ACADEMIC AUTHENTICITY SCORER — REPORT        |")
    print("+" + "=" * 50 + "+")
    if label:
        print(f"  Input: {label}")
    print()
    print(f"  AUTHENTICITY SCORE:  {total}/100")
    print(f"  [{bar}]")
    print(f"  Verdict: {verdict}")
    print()
    print("  -- Dimension Breakdown " + "-" * 26)
    print()

    dimensions = [
        ("AI Vocabulary",       s["ai_vocabulary"],       20),
        ("Hedging & Filler",    s["hedging_and_filler"],   20),
        ("Sentence Variance",   s["sentence_variance"],    15),
        ("Passive Voice",       s["passive_voice"],        10),
        ("Paragraph Structure", s["paragraph_structure"],  10),
        ("Transition Patterns", s["transition_patterns"],  10),
        ("Tense Consistency",   s["tense_consistency"],    10),
        ("LaTeX Integrity",     s["latex_integrity"],       5),
    ]

    for name, sec, mx in dimensions:
        sc = sec["score"]
        filled = int(sc / mx * 10) if mx > 0 else 0
        bar2 = "=" * filled + "-" * (10 - filled)
        print(f"  {name:<22} {sc:>2}/{mx:<2}  [{bar2}]")

    print()
    print("  -- Detected Issues " + "-" * 30)
    print()

    # AI Vocabulary
    v = s["ai_vocabulary"]
    if v["total_hits"] > 0:
        terms = ", ".join(v["flagged"][:5])
        severity = "!!" if v["total_hits"] > 5 else "!"
        print(f"  {severity} AI vocabulary: {v['total_hits']} hits ({v['density_per_100']}/100 words)")
        print(f"     [{terms}]")
    else:
        print("  OK  No AI vocabulary detected")

    # Hedging
    h = s["hedging_and_filler"]
    if h["total"] > 0:
        severity = "!!" if h["total"] > 4 else "!"
        print(f"  {severity} Hedging/filler: {h['total']} phrases (hedges: {h['hedge_count']}, filler: {h['filler_count']}, weasel: {h['weasel_count']})")
        if h["flagged"]:
            print(f"     [{', '.join(h['flagged'][:5])}]")
    else:
        print("  OK  No hedging or filler detected")

    # Sentence variance
    sv = s["sentence_variance"]
    if "note" not in sv:
        if sv["std_dev"] < 5:
            print(f"  !! Sentence rhythm robotic — std dev {sv['std_dev']} (target: 7+)")
        elif sv["std_dev"] < 7:
            print(f"  !  Sentence variance low — {sv['std_dev']} (target: 7+)")
        else:
            print(f"  OK  Sentence variance: {sv['std_dev']} (range: {sv['min_length']}-{sv['max_length']} words)")

    # Passive voice
    pv = s["passive_voice"]
    if pv["ratio"] > 0.35:
        print(f"  !! Passive voice overuse — {pv['pct']} of sentences")
    elif pv["ratio"] > 0.25:
        print(f"  !  Passive voice elevated — {pv['pct']}")
    else:
        print(f"  OK  Passive voice: {pv['pct']}")

    # Transitions
    tr = s["transition_patterns"]
    if tr["transition_count"] > 5:
        print(f"  !! Predictable transitions: {tr['transition_count']} formulaic connectives")
        print(f"     [{', '.join(tr['flagged'][:5])}]")
    elif tr["transition_count"] > 2:
        print(f"  !  Transitions: {tr['transition_count']} formulaic connectives")
    else:
        print(f"  OK  Transitions natural ({tr['transition_count']} formulaic)")
    if tr["ai_triplets_found"] > 0:
        print(f"  !  Coordinated triplets found: {tr['ai_triplets_found']}")

    # Tense
    tc = s["tense_consistency"]
    if "note" not in tc:
        if tc["dominant_correct"]:
            print(f"  OK  Tense: {tc['expected_tense']} expected for '{tc['section']}' — dominant tense matches")
        else:
            print(f"  !! Tense mismatch: '{tc['section']}' expects {tc['expected_tense']} "
                  f"(past={tc['past_ratio']}, present={tc['present_ratio']})")
    else:
        print(f"  --  {tc['note']}")

    # LaTeX
    lx = s["latex_integrity"]
    if lx["status"] == "Pass":
        print(f"  OK  LaTeX: {lx['citations_found']} citations, {lx['references_found']} refs, {lx['math_expressions_found']} math — all intact")
    else:
        print(f"  !! LaTeX issues: {'; '.join(lx['issues'])}")

    # Priority fixes
    print()
    print("  -- Priority Fixes " + "-" * 31)
    print()

    fixes = []
    if v["total_hits"] > 5:
        fixes.append("Replace AI vocabulary (biggest impact on perceived authenticity)")
    if h["total"] > 3:
        fixes.append("Cut hedging and filler phrases — state claims directly")
    if "note" not in sv and sv["std_dev"] < 7:
        fixes.append("Vary sentence length — mix short (8-12 word) and longer (25-35 word) sentences")
    if pv["ratio"] > 0.3:
        fixes.append("Convert passive sentences to active voice")
    if tr["transition_count"] > 5:
        fixes.append("Replace formulaic transitions — use varied connectives or no transition")
    if "note" not in tc and not tc["dominant_correct"]:
        fixes.append(f"Fix tense: '{tc['section']}' section should use {tc['expected_tense']} tense")

    if fixes:
        for i, fix in enumerate(fixes, 1):
            print(f"  {i}. {fix}")
    else:
        print("  No priority fixes — text reads as authentic academic writing")

    print()


# ── Demo Samples ─────────────────────────────────────────────────────────────

SAMPLE_AI = r"""
In today's rapidly evolving technological landscape, natural language processing has become
increasingly important across various domains and industries worldwide. It is important to note
that the emergence of Large Language Models (LLMs) has fundamentally revolutionized the way we
interact with data, paving the way for groundbreaking innovations in the field of Business
Intelligence. Furthermore, the concept of Conversational BI represents a paradigm shift that
bridges the gap between non-technical users and complex database systems. Moreover, Natural
Language to SQL (NL2SQL) technology plays a crucial role in facilitating this transformation by
leveraging advanced deep learning methodologies to enable seamless query generation.

Several studies have explored various aspects of this problem space. Many researchers believe
that multi-agent LLM systems represent the future of intelligent data interaction. It is widely
accepted that transformer-based architectures provide the optimal foundation for building robust,
scalable, and efficient NL2SQL solutions~\citep{vaswani2017}. While a comprehensive analysis of
all possible approaches is beyond the scope of this thesis, we attempt to provide a reasonably
thorough overview of the most relevant methods and frameworks.

This groundbreaking research aims to address these critical challenges by proposing a
comprehensive framework that effectively bridges the gap between natural language understanding
and SQL query generation~\citep{chen2023}. The contributions of this thesis are threefold:
(1) we develop a novel multi-agent architecture, (2) we introduce an innovative evaluation
methodology, and (3) we demonstrate the remarkable effectiveness of our approach through
extensive experimentation~\citep{devlin2019}.
"""

SAMPLE_HUMAN = r"""
Enterprise adoption of natural language interfaces to databases has grown steadily since 2020,
yet query accuracy on complex joins remains below 70\% in production systems~\citep{chen2023}.
The gap is consequential: non-technical business analysts who need ad-hoc answers from corporate
databases must either learn SQL or wait for a dedicated data team to write queries on their behalf.

Large Language Models have shifted the landscape for NL2SQL by offering stronger semantic
understanding than earlier rule-based or sequence-to-sequence approaches~\citep{vaswani2017}.
Combining LLM capabilities with a conversational interface introduces its own difficulties,
however --- context tracking across turns, schema grounding under ambiguity, and graceful error
recovery all remain open challenges.

Existing work on NL2SQL has largely focused on single-turn accuracy benchmarks such as Spider.
Multi-agent LLM architectures, in which specialized sub-agents handle parsing, schema linking,
and query validation independently, have shown early promise but lack systematic evaluation in
conversational settings. This thesis targets that gap. We propose a multi-agent architecture
designed for multi-turn Conversational BI, introduce an evaluation protocol that measures both
single-turn accuracy and dialogue-level coherence, and test the system on two enterprise-scale
schemas~\citep{devlin2019}.
"""


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Score thesis text 0-100 on academic authenticity by detecting AI writing patterns. "
                    "Checks AI vocabulary, hedging, sentence variance, passive voice, paragraph structure, "
                    "transitions, tense consistency, and LaTeX integrity."
    )
    parser.add_argument(
        "file", nargs="?", default=None,
        help="Path to a .tex or .txt file to analyze. Omit for demo mode."
    )
    parser.add_argument(
        "--section", default=None,
        help="Section type for tense checking: introduction, methodology, results, discussion, conclusion, etc."
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Also output results as JSON."
    )
    args = parser.parse_args()

    if args.file is None:
        print("[Demo mode — comparing human-written vs AI-generated thesis text]")
        print()
        print("=" * 52)
        print("SAMPLE 1: AI-generated Introduction")
        print("=" * 52)
        r1 = score_academic_authenticity(SAMPLE_AI, section="introduction")
        print_report(r1, "AI-generated sample")

        print("=" * 52)
        print("SAMPLE 2: Human-quality Introduction")
        print("=" * 52)
        r2 = score_academic_authenticity(SAMPLE_HUMAN, section="introduction")
        print_report(r2, "Human-quality sample")

        print(f"  Delta: Human scored {r2['authenticity_score']}, AI scored {r1['authenticity_score']}")
        print(f"  Difference: {r2['authenticity_score'] - r1['authenticity_score']} points")
        print()
    else:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)

        result = score_academic_authenticity(text, section=args.section)
        print_report(result, args.file)

        if args.json:
            print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
