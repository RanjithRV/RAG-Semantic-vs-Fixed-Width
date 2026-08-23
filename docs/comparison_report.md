# Chunking Strategy & Retrieval-Type Comparison Report

Week 2 — Financial Document Intelligence (Lyzr, No-Code Track)

## What this report covers

Two comparisons were planned for this project: (1) fixed-size chunking vs. semantic chunking, and (2) the impact of a reranking step on retrieval quality. Both were tested against the same 15-question eval set (`docs/eval_results.md`) run over the FY2024–FY2025 10-K filings of Rumble, Reddit, and Nextdoor.

Try both agents directly:

- **Fixed-Size-Agent**: https://studio.lyzr.ai/create-new-agent/6a89d97e0fdb3536018ada9f?tab=playground&public=true
- **Semantic-Agent**: https://studio.lyzr.ai/create-new-agent/6a89db5c4b07c8f6f2ea3902?tab=playground&public=true

## Why MMR stands in for reranking

Lyzr's agent Configure panel does not expose a dedicated reranking model or a separate reranking step — the retrieval-type options available are **Basic**, **MMR**, and **HyDE**, with no "apply a reranker after initial retrieval" toggle. MMR (Maximal Marginal Relevance) was used as the practical stand-in: it re-scores and re-selects from the initially retrieved candidates to reduce redundancy and favor diverse, relevant chunks, which plays a functionally similar role to reranking (a second pass over an initial top-k set, before it reaches the LLM). Basic retrieval, by contrast, returns the top-k chunks by similarity score alone, with no second pass.

This is a substitution, not an equivalent. A real reranker (typically a cross-encoder scoring query–chunk pairs) and MMR (a diversity-driven re-selection heuristic) work on different principles and aren't guaranteed to produce comparable effects. Results below are framed as **MMR retrieval vs. Basic retrieval**, not as "reranked vs. non-reranked" — this project did not test a true reranking step, because Lyzr does not offer one. See `lyzr/prompts.md` for the fuller methodology note.

## Scope limitation: only 2 of 4 planned conditions were run

The original design was a full 2×2 — chunking strategy (fixed-size / semantic) × retrieval type (Basic / MMR) — 4 conditions, 15 questions each, 60 runs total, which would have let chunking and retrieval type be evaluated independently.

In practice, only two conditions were completed:

- **Condition 1: Fixed-size chunking × Basic retrieval** — ran as planned, 15/15.
- **Condition 4: Semantic chunking × MMR retrieval** — 15/15, but with a labeling wrinkle: this data was originally collected believing it was "Condition 2" (Fixed-size × MMR), and only after logging all 15 answers was it discovered the wrong Lyzr Playground window had been open the whole time — the Semantic-Agent, not the Fixed-Size-Agent. The data was accurate to whatever it actually tested, so it was relabeled to Condition 4 rather than discarded.
- **Conditions 2 (Fixed-size × MMR) and 3 (Semantic × Basic) were never run.** Once the mislabeling was caught, the project deliberately stopped the 2×2 exercise there rather than complete the remaining two conditions, in order to move on to the next phase of the project (publishing the agents for class use).

**What this means for the findings below:** the only comparison actually available is Condition 1 vs. Condition 4, which changes *both* chunking strategy and retrieval type at once. Any difference between them cannot be cleanly attributed to chunking, to retrieval type, or to the (imperfect) MMR-as-reranking substitution individually — it's a comparison of two full pipeline configurations, not an isolated-variable experiment. That caveat applies to every finding in this report.

## Results summary

| # | Condition 1 (Fixed-size × Basic) | Condition 4 (Semantic × MMR) | Notes |
| --- | --- | --- | --- |
| Q1 | Y — exact match | Y — exact match | Both clean |
| Q2 | Y — exact match | Y — exact match | Both clean |
| Q3 | Y — exact match | Y — exact match | Both clean |
| Q4 | Y — exact match (121.4M) | N — wrong figure (50.7M) | Only failure point on this question; Semantic×MMR retrieved a different, incorrect chunk |
| Q5 | Y — faithful refusal (retrieval gap) | Y — faithful refusal (same retrieval gap) | Advertising-% disclosure not surfaced in either condition |
| Q6 | Y — exact match | Y — exact match | Both clean |
| Q7 | Y — exact match | N — wrong figure ($162.7M vs. $529.7M), conflated with a different line item | Only failure point on this question |
| Q8 | Y — exact match, proactive caveat | Partial — correct numbers, self-contradictory headline ("increased" when it decreased) | Numbers fine both conditions; framing regressed in Condition 4 |
| Q9 | Partial — correctly flagged redefinition trap, incomplete like-for-like figure | Partial — same behavior, same gap | Identical outcome in both conditions |
| Q10 | Y — exact match, caught cross-filing units mismatch | Y — exact match, missed the units caveat | Same final ranking; Condition 1 gave the more complete answer |
| Q11 | Y — exact match (after a discarded self-contradictory first attempt) | Partial — correct numbers, self-contradictory headline (named wrong company first) | Same framing issue as Q8, this time in Condition 4 |
| Q12 | Y — faithful refusal on Rumble sub-question | N — wrong figure (Reddit falsely shown as a net loss) | Weakest result of either condition; three different Reddit FY2025 figures appeared across Q2/Q7/Q12 in Condition 4 alone |
| Q13 | Y — exact match (despite an internal Q6-vs-Q13 figure conflict noted at the time) | Y — exact match, internally consistent with Q6 | Condition 4 was cleaner here |
| Q14 | Y — correct refusal | Y — correct refusal | Both clean |
| Q15 | Y — correct refusal | Y — correct refusal, arguably the cleanest refusal in the project | Both clean |

**Headline finding:** Condition 1 (Fixed-size × Basic) had zero outright-wrong answers across all 15 questions. Condition 4 (Semantic × MMR) had three (Q4, Q7, Q12) — all involving figure instability, and two of them (Q7, Q12) on Reddit's FY2025 net income specifically. Within Condition 4 alone, three different and mutually inconsistent figures for the same fact (Reddit's FY2025 net income) appeared across Q2 (+$529.7M, correct), Q7 (+$162.7M, wrong), and Q12 (a net loss of –$484,276, wrong) — the same underlying fact, retrieved correctly once and incorrectly twice, within one condition.

Given the scope limitation above, this should be read as "the Fixed-size×Basic pipeline was more reliable than the Semantic×MMR pipeline on this question set," not as "fixed-size chunking beats semantic chunking" or "Basic retrieval beats MMR" individually — those two variables were never tested in isolation.

## Discussion: what actually seemed to go wrong in Condition 4

Two distinct failure patterns showed up in Condition 4, and they're worth separating because they likely have different causes:

**Wrong-chunk retrieval (Q4, Q7).** In both cases the agent retrieved a real, high-confidence-scored chunk (0.894 and 0.846 respectively) that simply wasn't the right one — Q4 pulled a different DAUq breakout than the one asked about, and Q7 pulled Reddit's "net income attributable to common stockholders" line instead of total net income, a plausible-looking but distinct financial metric. High similarity score did not guarantee correctness here; this looks like a genuine retrieval miss on the Semantic KB, not a generation error, since the agent answered confidently and consistently with what it retrieved.

**Session/answer instability (Q12).** This is the more concerning finding. The first attempt at Q12 returned Q11's answer verbatim — a clear thread-contamination bug (see `lyzr/prompts.md` for the fresh-session methodology note). A rerun in a new session avoided that specific failure but produced a *different* wrong answer: Reddit shown as a net loss of –$484,276, which looks like a mangled fragment of Reddit's FY2024 net loss figure ($484.3M) misapplied to FY2025. Combined with a backend `lyzr_memory_process_completed` event observed during this same question (documented in `lyzr/prompts.md`), this suggests Lyzr may run memory/context processing at a level a "fresh Playground session" doesn't fully reset — a limitation worth flagging to anyone relying on Lyzr Playground sessions being independent of each other.

## Known limitations

- **The 2×2 was not completed.** Only Condition 1 and Condition 4 were run; chunking strategy and retrieval type cannot be evaluated as independent variables from this data (see Scope limitation above).
- **MMR is not a true reranker.** Findings involving Condition 4 reflect MMR retrieval specifically, not a validated reranking-vs-no-reranking comparison (see "Why MMR stands in for reranking" above).
- **Session/memory contamination is a confirmed, live issue**, not just an eval artifact — observed directly in a Lyzr Playground session outside of eval logging, with backend event evidence. Anyone using the published agent links for hands-on exploration should be aware that unrelated prior questions in the same session may bleed into later answers.
- **A handful of within-condition figure inconsistencies were logged but not traced to a root cause** (e.g., Rumble's FY2024 revenue appearing as both $91.4M and $95.5M across different Condition 1 questions) — flagged in `docs/eval_results.md` as open items rather than resolved findings.

## Bottom line

On the two conditions actually tested, the Fixed-size × Basic pipeline was materially more reliable (0 wrong answers) than the Semantic × MMR pipeline (3 wrong answers, concentrated on Reddit's FY2025 profitability figure). Because both chunking strategy and retrieval type changed between the two conditions, and because MMR is only an approximate stand-in for reranking on this platform, this result should be read as a comparison of two end-to-end configurations rather than a controlled test of either variable — a genuinely useful data point for this project's write-up, but not the full reranking-impact study originally planned.
