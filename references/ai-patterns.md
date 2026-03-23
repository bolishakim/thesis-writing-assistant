# AI Writing Anti-Pattern Taxonomy

37 patterns organized into 4 categories. Each entry includes detection criteria, an AI-typical example, the academic fix, and severity (High/Medium/Low).

---

## Table of Contents

- [Content Patterns (CP-01 to CP-10)](#content-patterns)
- [Language Patterns (LP-01 to LP-10)](#language-patterns)
- [Style Patterns (SP-01 to SP-11)](#style-patterns)
- [Communication Patterns (XP-01 to XP-06)](#communication-patterns)

---

## Content Patterns

### CP-01: Excessive Hedging
- **Detect:** Clusters of "might", "could potentially", "it is possible that", "may or may not" where the evidence actually supports a direct claim
- **AI example:** "This approach could potentially yield improvements that might be considered significant in certain contexts."
- **Fix:** "This approach improved response accuracy by 12% across all test conditions."
- **Severity:** High

### CP-02: Over-Qualifying
- **Detect:** Every claim wrapped in multiple qualifiers even when data is clear
- **AI example:** "While results are preliminary and subject to various limitations, it appears that there may be some evidence suggesting a possible trend."
- **Fix:** "The results indicate a consistent upward trend (p < 0.01), though replication with larger samples is needed."
- **Severity:** High

### CP-03: Generic Claims
- **Detect:** Broad statements that could appear in any paper; no domain specifics
- **AI example:** "This technology has the potential to revolutionize the field and transform how we approach these problems."
- **Fix:** "NL2SQL systems reduce the barrier to database querying for non-technical analysts, who previously relied on dedicated BI teams for ad-hoc reports."
- **Severity:** High

### CP-04: False Balance
- **Detect:** Treating well-established facts as debatable; giving equal weight to fringe positions
- **AI example:** "While some researchers support the use of transformer architectures, others argue that simpler models may be equally effective."
- **Fix:** "Transformer architectures have become the dominant approach for sequence modeling tasks, though computational cost remains a practical constraint for resource-limited deployments."
- **Severity:** Medium

### CP-05: Inflated Significance
- **Detect:** "groundbreaking", "revolutionary", "paradigm shift", "unprecedented" without evidence to match
- **AI example:** "This groundbreaking study represents a paradigm shift in our understanding of conversational AI systems."
- **Fix:** "This study extends prior work on conversational AI by introducing a multi-turn context management strategy that reduces query abandonment rates."
- **Severity:** High

### CP-06: Circular Reasoning
- **Detect:** The conclusion restates the premise; argument doesn't advance
- **AI example:** "The system is effective because it produces effective results, demonstrating the effectiveness of the approach."
- **Fix:** "The system reduced average query resolution time from 4.2 to 1.8 minutes, primarily because the semantic parser resolved ambiguous column references before passing queries to the SQL generator."
- **Severity:** High

### CP-07: Premature Solutionism
- **Detect:** Jumping to "the solution" before fully characterizing the problem
- **AI example:** "To address these challenges, we propose a comprehensive framework that solves all identified issues."
- **Fix:** "Section 3 characterizes the three main failure modes in existing NL2SQL pipelines. Section 4 describes our approach to the most frequent of these — schema linking errors — while noting that the remaining two require further investigation."
- **Severity:** Medium

### CP-08: Missing Attribution
- **Detect:** Claims presented as common knowledge that actually need citations; ideas borrowed without credit
- **AI example:** "It is well known that large language models exhibit emergent capabilities at sufficient scale."
- **Fix:** "Large language models exhibit emergent capabilities at sufficient scale (Wei et al., 2022), though the mechanisms underlying emergence remain debated (Schaeffer et al., 2023)."
- **Severity:** High

### CP-09: Scope Overclaiming
- **Detect:** Conclusions that go beyond what the study's data supports
- **AI example:** "These findings conclusively demonstrate that our approach is superior to all existing methods for natural language understanding."
- **Fix:** "On the Spider benchmark, our approach outperformed the three baseline methods tested. Generalization to other NL2SQL benchmarks and production workloads remains to be evaluated."
- **Severity:** High

### CP-10: Empty Contextualizing
- **Detect:** Opening paragraphs that discuss the broad importance of the field without connecting to the specific contribution
- **AI example:** "In today's rapidly evolving technological landscape, artificial intelligence has become increasingly important across various domains and industries worldwide."
- **Fix:** "Enterprise adoption of natural language interfaces to databases has grown steadily since 2020, yet query accuracy on complex joins remains below 70% in production systems (Chen et al., 2024)."
- **Severity:** Medium

---

## Language Patterns

### LP-01: Filler Phrases
- **Detect:** "It is important to note that", "It should be mentioned that", "It is worth noting that", "In this regard", "Moreover, it is crucial to"
- **AI example:** "It is important to note that the results demonstrate a clear trend. Moreover, it is worth mentioning that this aligns with previous findings."
- **Fix:** "The results demonstrate a clear trend, consistent with prior findings by Garcia et al. (2023)."
- **Severity:** High

### LP-02: Predictable Transitions
- **Detect:** Overuse of "Furthermore", "Moreover", "Additionally", "In addition" — especially at paragraph openings in sequence
- **AI example:** "Furthermore, the system showed improvement. Additionally, user satisfaction increased. Moreover, response times decreased."
- **Fix:** Vary connectives: use "The system also showed...", start with the subject, or use no transition when the logical connection is obvious from context.
- **Severity:** Medium

### LP-03: Passive Overuse
- **Detect:** More than 40% of sentences in passive voice when active would be clearer
- **AI example:** "The data was collected by the researchers and was then analyzed using statistical methods that were selected based on criteria that had been established."
- **Fix:** "We collected response logs over 14 days and analyzed them using mixed-effects regression, chosen for its ability to handle the nested participant structure."
- **Severity:** Medium

### LP-04: Nominalization Overload
- **Detect:** Verbs turned into nouns + weak verb ("make an examination of" instead of "examine"), stacked nominalizations
- **AI example:** "The implementation of the optimization of the classification algorithm led to the improvement of the accuracy."
- **Fix:** "Optimizing the classifier improved accuracy from 78% to 91%."
- **Severity:** Medium

### LP-05: Weasel Words
- **Detect:** "Some researchers argue", "It has been suggested", "Many experts believe" — unattributed authority
- **AI example:** "Many researchers believe that multi-agent systems represent the future of AI development."
- **Fix:** "Wooldridge (2020) and Dorri et al. (2018) argue that multi-agent architectures better model real-world coordination problems than monolithic approaches."
- **Severity:** High

### LP-06: Synonym Cycling
- **Detect:** Artificially rotating synonyms for the same concept (framework/system/platform/architecture used interchangeably for one thing)
- **AI example:** "The framework processes queries efficiently. This system handles complex requests. The platform manages user interactions. The architecture supports multiple inputs."
- **Fix:** Pick one term and use it consistently. "The system" throughout, or define terms explicitly if distinctions matter.
- **Severity:** Medium

### LP-07: Collocational Cliches
- **Detect:** "plays a crucial role", "sheds light on", "paves the way for", "bridges the gap", "the lion's share"
- **AI example:** "This research sheds light on key challenges and paves the way for future innovations that bridge the gap between theory and practice."
- **Fix:** "This research identifies three specific failure modes in schema linking and proposes validated fixes for two of them."
- **Severity:** Medium

### LP-08: Adverb Overuse
- **Detect:** "significantly", "effectively", "efficiently", "substantially", "remarkably" used without quantification
- **AI example:** "The model significantly and substantially improved performance, effectively achieving remarkably better results."
- **Fix:** "The model improved F1 score from 0.72 to 0.89 on the held-out test set."
- **Severity:** Medium

### LP-09: Coordinated Triplets
- **Detect:** Lists of three adjectives/nouns/verbs where one or two would suffice — the rhythmic "X, Y, and Z" pattern
- **AI example:** "a robust, scalable, and efficient solution"; "analyze, evaluate, and assess the results"
- **Fix:** "a scalable solution" (if scalability is what matters); "we evaluated the results" (one verb that captures the action)
- **Severity:** Low

### LP-10: Gerund Stacking
- **Detect:** Multiple -ing forms chained: "improving understanding by examining existing approaches while considering emerging trends"
- **AI example:** "By leveraging existing frameworks while incorporating emerging technologies and addressing growing concerns, the approach succeeds in improving overall performance."
- **Fix:** "The approach incorporates two recent techniques — retrieval-augmented generation and constrained decoding — to improve overall performance."
- **Severity:** Low

---

## Style Patterns

### SP-01: Uniform Sentence Length
- **Detect:** Most sentences fall within a narrow word-count band (e.g., all 15-20 words); no short punchy sentences or longer complex ones
- **AI example:** [Paragraph where every sentence is 16-19 words]
- **Fix:** Mix sentence lengths: some at 8-12 words for punch, some at 25-35 for complex reasoning. Average should land around 18-22.
- **Severity:** Medium

### SP-02: Formulaic Paragraph Structure
- **Detect:** Every paragraph follows topic-sentence -> three-supporting-points -> concluding-sentence
- **AI example:** [Five consecutive paragraphs all with identical 5-sentence TSSC structure]
- **Fix:** Vary openings: start with evidence, a contrast, a question, or a continuation from the prior paragraph. Not every paragraph needs a concluding sentence.
- **Severity:** Medium

### SP-03: Over-Enumeration
- **Detect:** Excessive numbered/bulleted lists in prose sections where flowing paragraphs would be more natural
- **AI example:** "The benefits include: (1) improved accuracy, (2) reduced latency, (3) better user experience, (4) lower costs, and (5) enhanced scalability."
- **Fix:** "The primary benefit is improved accuracy, which in turn reduces the need for manual query correction and lowers operational costs."
- **Severity:** Medium

### SP-04: Symmetric Section Structure
- **Detect:** Every section/subsection has the same number of paragraphs, same length, same internal structure
- **AI example:** [Every subsection in Related Work has exactly 3 paragraphs of similar length]
- **Fix:** Let section length reflect content importance. A central concept deserves more space than a peripheral one.
- **Severity:** Low

### SP-05: Conclusion-Mirroring
- **Detect:** Conclusion is essentially the introduction reworded; no new synthesis or reflection
- **AI example:** "As discussed in the introduction, this research examined NL2SQL systems. The study found that [repeats abstract]."
- **Fix:** The conclusion should synthesize findings into implications, acknowledge specific limitations honestly, and point to concrete next steps — not summarize what was already said.
- **Severity:** Medium

### SP-06: List-Heavy Exposition
- **Detect:** Using bullet points or numbered lists where discursive prose would be more appropriate in an academic context
- **AI example:** [Methodology section presented as a bulleted checklist]
- **Fix:** Convert to flowing prose. "We first preprocessed the queries by removing stopwords, then applied the semantic parser described in Section 3.2."
- **Severity:** Medium

### SP-07: Heading-Body Redundancy
- **Detect:** The first sentence of a section simply restates the section heading
- **AI example:** Section: "Data Collection" -> First sentence: "This section describes the data collection process."
- **Fix:** Jump into the content: "We collected 2,400 query-response pairs from three enterprise BI deployments over a six-month period."
- **Severity:** Low

### SP-08: Uniform Paragraph Length
- **Detect:** All paragraphs are nearly the same length (e.g., all 5-6 sentences)
- **AI example:** [Ten consecutive paragraphs, each exactly 5 sentences]
- **Fix:** Let paragraph length follow the thought. Some points need 3 sentences; complex arguments may need 8. Transitional paragraphs can be 2 sentences.
- **Severity:** Low

### SP-09: Uniform Sentence Complexity (Burstiness Failure)
- **Detect:** Every sentence lands at the same cognitive complexity — all have one dependent clause and one main clause, or all are simple SVO. No mixing of dense analytical sentences with short factual ones
- **AI example:** "The model processes input tokens sequentially. The attention mechanism computes similarity scores. The decoder generates output tokens. The system achieves competitive results."
- **Fix:** Mix complexity: "The model processes input tokens sequentially. When the attention mechanism encounters tokens that share semantic similarity with multiple schema columns — a common scenario in enterprise databases with hundreds of tables — it must weight contextual cues from prior conversation turns against raw embedding distance. This ambiguity resolution step dominates inference time. Our column affinity graph eliminates it."
- **Severity:** High

### SP-10: Predictable Word Choices (Low Perplexity)
- **Detect:** Every word is the most statistically likely continuation — no domain-specific terms, concrete numbers, or researcher-specific framing. Text reads as "generic academic prose" that could be about any topic
- **AI example:** "The proposed approach demonstrates significant improvement over existing methods across multiple evaluation metrics, achieving state-of-the-art performance on the benchmark dataset."
- **Fix:** "Our three-agent pipeline improved execution accuracy on Spider-DK from 71.2% to 83.4%, with the largest gains on queries requiring cross-table joins — the category where single-agent baselines consistently fail due to schema linking errors (cf. Li et al., 2024, Table 4)."
- **Severity:** High

### SP-11: Lexical-Only Humanization
- **Detect:** Text has been superficially edited (synonym swaps, minor rephrasing) but retains AI-typical argument structure: claim → three supporting points → summary. The skeleton is AI-generated even if individual words have changed
- **AI example:** [Text where "utilize" was changed to "use" and "facilitate" to "enable" but the five-paragraph-essay structure with identical paragraph lengths and formulaic transitions remains intact]
- **Fix:** Restructure the argument itself: reorder paragraphs by logical priority, merge related points, vary paragraph purpose (some present evidence, some contrast views, some synthesize), and let section length reflect content importance rather than template
- **Severity:** High

---

## Communication Patterns

### XP-01: Excessive Meta-Commentary
- **Detect:** "In this section, we will discuss...", "As we will see in the following paragraphs...", "The next subsection examines..."
- **AI example:** "In this section, we will first discuss the background, then examine the methodology, and finally present our analysis of the results."
- **Fix:** Remove the roadmap sentence and start with the content. Section headings already signal what comes next.
- **Severity:** Medium

### XP-02: Unnecessary Disclaimers
- **Detect:** "It should be noted that this is not a comprehensive review", "While this analysis has limitations", "This is beyond the scope of this paper" — when these are obvious or already stated elsewhere
- **AI example:** "While a comprehensive analysis of all possible approaches is beyond the scope of this paper, we attempt to provide a reasonably thorough overview of the most relevant methods."
- **Fix:** "We focus on the three most widely-adopted approaches, selected for their relevance to enterprise NL2SQL deployments." (State what you do, not what you don't.)
- **Severity:** Low

### XP-03: Performative Objectivity
- **Detect:** "Objectively speaking", "From an unbiased perspective", "It must be acknowledged that" — phrases that signal objectivity rather than demonstrating it
- **AI example:** "Objectively speaking, it must be acknowledged that this approach offers several distinct advantages over competing methods."
- **Fix:** "This approach reduces query compilation time by 40% compared to the baseline, though it requires 2x more memory during inference."
- **Severity:** Medium

### XP-04: Reader Hand-Holding
- **Detect:** "To better understand this concept...", "Simply put...", "In other words...", "To clarify..." used excessively
- **AI example:** "To better understand this concept, it is helpful to consider a simple analogy. In other words, the system works similarly to how a human translator would approach the task. Simply put, it converts natural language to SQL."
- **Fix:** State it once, clearly: "The system converts natural language questions to SQL queries through a three-stage pipeline: intent classification, schema linking, and query synthesis."
- **Severity:** Medium

### XP-05: Artificial Enthusiasm
- **Detect:** "Excitingly", "Impressively", "Remarkably", "Fascinatingly" — editorializing about results instead of letting data speak
- **AI example:** "Excitingly, the results revealed a remarkable and impressive improvement that fascinatingly exceeded all expectations."
- **Fix:** "The system achieved 94.2% accuracy on the held-out test set, exceeding the previous state-of-the-art by 3.1 percentage points."
- **Severity:** Medium

### XP-06: Consensus Manufacturing
- **Detect:** "It is widely accepted that", "There is a growing consensus that", "The literature overwhelmingly supports" — asserting agreement without evidence
- **AI example:** "It is widely accepted in the literature that transformer-based models represent the optimal solution for all natural language processing tasks."
- **Fix:** "Transformer-based models achieve state-of-the-art results on most NLP benchmarks (Wang et al., 2019; Devlin et al., 2019), though task-specific architectures remain competitive for low-resource settings (Chen & Manning, 2024)."
- **Severity:** High
