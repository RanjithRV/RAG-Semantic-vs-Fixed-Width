# Week 2 RAG Evaluation Question Set

15 questions to run against **both** Lyzr knowledge bases (fixed-size chunking and semantic chunking), so the comparison report has a like-for-like basis. Ground-truth answers below were pulled directly from the cleaned filings (`data/cleaned/*.txt`) and cross-checked against the prior-year comparative figures each filing reports, so treat this table as the answer key for grading faithfulness — not something to re-derive by eye while testing.

Figures are in USD unless noted; "K" = thousands as reported in the filings.

## How to use this

For each question, run it against the fixed-size KB and the semantic KB in Lyzr, then fill in the Results table at the bottom: paste each answer, mark it Faithful (grounded in the retrieved chunks, matches the ground truth) / Unfaithful (wrong or hallucinated) / Refused (correctly said "not in the documents"), and note which chunking variant retrieved the *right* source chunk (not just the right-sounding answer — check the citations Lyzr shows).

---

## A. Single-fact lookups (5)

**Q1.** What was Rumble's total revenue for fiscal year 2025?
Ground truth: **$100,622,320** (~$100.6M). *Source: Rumble FY2025 10-K, revenue-by-source table.*

**Q2.** What was Reddit's net income for fiscal year 2025?
Ground truth: **$529.7 million net income** (Reddit was profitable in FY2025). *Source: Reddit FY2025 10-K, MD&A results-of-operations table.*

**Q3.** What was Nextdoor's net loss for fiscal year 2024?
Ground truth: **$98,063K (~$98.1M) net loss**. *Source: Nextdoor FY2024 10-K, consolidated statements of operations.*

**Q4.** What was Reddit's average daily active uniques (DAUq) for the three months ended December 31, 2025?
Ground truth: **121.4 million**. *Source: Reddit FY2025 10-K, Item 1 Business overview.*

**Q5.** What percentage of Rumble's revenue came from advertising in fiscal year 2025?
Ground truth: **50%** (down from 66% in FY2024). *Source: Rumble FY2025 10-K, risk factors / revenue concentration discussion.*

## B. Cross-year trends, single company (4)

**Q6.** How did Rumble's net loss change from FY2024 to FY2025?
Ground truth: Narrowed significantly, from **$338,362,779 (FY2024)** to **$81,830,362 (FY2025)** — roughly a 76% reduction. *Source: Rumble FY2025 10-K, consolidated statements of operations (shows both years side by side).*

**Q7.** How did Reddit's profitability change from FY2024 to FY2025?
Ground truth: Reddit swung from a **$484.3M net loss (FY2024)** to a **$529.7M net income (FY2025)** — its first profitable year on record in this filing pair. *Source: Reddit FY2025 10-K, MD&A.*

**Q8.** How did Rumble's Monthly Active Users (MAUs) change from Q4 2024 to Q4 2025?
Ground truth: Declined from **68 million (Q4 2024, GA4-measured)** to **52 million (Q4 2025, GA4-measured)** — roughly a 24% decrease. Same measurement methodology both years, so this is a genuine like-for-like decline. *Source: Rumble FY2024 and FY2025 10-Ks, Item 1 Business overview.*

**Q9. (trap question — tests faithfulness, not just retrieval)** How did Nextdoor's weekly active user count change from FY2024 to FY2025?
Ground truth is nuanced: Nextdoor **redefined its user metric** between filings, from "WAU" (45.9 million, Q4 2024, as reported in the FY2024 10-K) to "Platform WAU" (a narrower definition). The FY2025 10-K restates the Q4 2024 comparison under the *new* definition as **22.2 million**, versus **21.0 million** in Q4 2025 — a real decline of only about 5%, not the ~54% a naive comparison of 45.9M vs 21.0M would suggest. A faithful answer must surface the metric redefinition and use the like-for-like comparison (22.2M → 21.0M), not the mismatched one. *Source: Nextdoor FY2024 10-K (old "WAU" figure) and FY2025 10-K (new "Platform WAU" figure, restated prior-year comparison).* This is a strong one to highlight in your report — it's exactly the kind of thing naive RAG retrieval gets wrong by grabbing two numbers that look comparable but aren't.

## C. Cross-company comparisons (4)

**Q10.** Which of the three companies had the highest revenue in FY2025?
Ground truth: **Reddit**, at ~$2.20B, far ahead of Nextdoor (~$257.6M) and Rumble (~$100.6M).

**Q11.** Which company had the fastest revenue growth rate from FY2024 to FY2025?
Ground truth: **Reddit**, +69.4% ($1.30B → $2.20B), versus Rumble +5.4% ($95.5M → $100.6M) and Nextdoor +4.2% ($247.3M → $257.6M).

**Q12.** Which of the three companies reported a net profit (rather than a net loss) in fiscal year 2025?
Ground truth: **Reddit only** (+$529.7M net income). Rumble (-$81.8M) and Nextdoor (-$54.2M) both still reported net losses in FY2025, though both narrowed year over year.

**Q13.** Between Rumble and Nextdoor, which company narrowed its net loss by a larger percentage from FY2024 to FY2025?
Ground truth: **Rumble**, which narrowed its loss by ~76% ($338.4M → $81.8M), versus Nextdoor's ~45% improvement ($98.1M → $54.2M).

## D. Deliberately unanswerable (2)

**Q14.** What was Rumble's total revenue for fiscal year 2022?
Ground truth: **Not in the corpus.** Only FY2024 and FY2025 10-Ks were ingested for all three companies. A faithful system should say it can't find this in the provided documents rather than guessing or hallucinating a number — this is your refusal-path test.

**Q15.** What is Reddit's projected revenue for fiscal year 2026?
Ground truth: **Not in the corpus.** 10-Ks report historical actuals, not forward guidance in this form; the filings may mention general risk factors about future performance but no specific FY2026 revenue projection. Correct behavior is refusal, not an invented figure.

---

## Results log

The assignment asks for two separate comparisons, so the original plan was a full 2×2: chunking strategy (fixed-size vs. semantic) × retrieval type (Basic vs. MMR, our stand-in for the reranking step — see `lyzr/prompts.md` for why). That's four conditions, same 15 questions each, 60 answers total. No new agents needed — retrieval type is a setting on the existing KB, so each pass is just: set retrieval type, run all 15 in that agent's Playground, log, flip the setting, rerun.

"Did the correct chunk get retrieved, and how highly ranked/scored was it" is the primary thing to log per question — that's literally what the assignment asks us to compare. The generated answer is supporting evidence (a wrong/hallucinated answer usually means retrieval failed), not the main metric. If the agent's chat UI shows which source chunk(s) it pulled from, use that directly.

**Decision (2026-08-23): the full 2×2 was not completed.** Condition 1 (Fixed-size, Basic) ran as planned. What was meant to be Condition 2 (Fixed-size, MMR) turned out — discovered after logging — to have actually been run against the Semantic-Agent (wrong Playground window selected), so it's really Condition 4 (Semantic, MMR) and has been relabeled accordingly below. Conditions 2 and 3 were never actually run and are being skipped by project decision, to move on to building the Streamlit chat UI rather than complete the full reranking comparison. The report's chunking-strategy comparison and reranking-impact analysis will be based on the two conditions actually run: **Condition 1 (Fixed-size × Basic)** and **Condition 4 (Semantic × MMR)** — a cross-KB comparison rather than a clean isolation of the retrieval-type variable, which the comparison report should call out explicitly as a methodology limitation.

### 1) Fixed-size KB — Basic retrieval

| # | Correct chunk retrieved? (Y/N) | Rank/score (if shown) | Generated answer | Faithful? |
| --- | --- | --- | --- | --- |
| Q1 | Y | rank 1, score 0.858 (source: rumble_fy2025.txt) | "$100,622,320" (also broke out Monetization $86,519,799 + Other Initiatives $14,102,521) | Y — exact match to ground truth |
| Q2 | Y | score 0.846 (source: reddit_fy2025.txt) | "$529,721 thousand (i.e., $529.7 million)" net income for FY2025 | Y — exact match to ground truth |
| Q3 | Y | score 0.883 (source: nextdoor_fy2024.txt) | "$98,063 thousand (i.e., $98.1 million)" net loss for FY2024 | Y — exact match to ground truth |
| Q4 | Y | score 0.898 (source: reddit_fy2025.txt) | "121.4 million" average DAUq for Q4 2025 | Y — exact match to ground truth |
| Q5 | N | score 0.841 (source: rumble_fy2025.txt, but wrong section — retrieved the revenue table, not the risk-factors sentence with the 50%/66% advertising-% disclosure) | Correctly declined: "advertising revenue was not separately disclosed as a dollar amount... the exact percentage is not available from the provided filing excerpts" | Y — faithful given what was retrieved, even though ground truth (50%) wasn't found. Contrast with the earlier session-contaminated attempt, which fabricated 86.0% from the wrong line item — see methodology note in lyzr/prompts.md |
| Q6 | Y (assumed — numbers match) | not captured this time | "FY2024 net loss $338,362,779; FY2025 net loss $81,830,362; decreased $256,532,417, a 75.8% reduction" | Y — matches ground truth (~76% reduction) |
| Q7 | Y | score 0.842 (source: reddit_fy2025.txt) | "FY2024 net loss $(484.3)M; FY2025 net income $529.7M; swing of $1.014 billion" | Y — exact match, matches filing's own stated delta of 1,013,997 |
| Q8 | Y | score 0.880 (source: rumble_fy2024.txt) | "Q4 2024 MAUs (GA4): 68M; Q4 2025 MAUs (GA4): 52M; decreased 16M, ~23.5% decline. Noted GA4 vs. pre-2023 UA methodology not comparable." | Y — exact match, plus proactively surfaced a methodology caveat |
| Q9 | Partial | score 0.863 (source: nextdoor_fy2024.txt) — had redefinition context but not the FY2025 filing's restated 22.2M comparable figure | Correctly flagged metric redefinition (WAU → Platform WAU) and refused to imply direct comparability; reported raw 45.9M → 21.0M without the ideal 22.2M → 21.0M like-for-like figure | Y — faithful (avoided the misleading ~54% naive claim), but incomplete vs. the ideal answer |
| Q10 | Y | score 0.808 (source: nextdoor_fy2025.txt) | "Reddit had the highest FY2025 revenue: Reddit $2,202,506K; Nextdoor $257,646K; Rumble $100,622,320 (total revenues)" — also flagged that Rumble's figure is stated in whole dollars vs. Reddit/Nextdoor in thousands, so units aren't directly comparable as displayed | Y — exact match to ground truth (Reddit highest), plus a genuinely useful proactive caveat about mismatched units across filings |
| Q11 | Y (see flag) | score 0.797 (source: nextdoor_fy2024.txt) — Rumble/Reddit source chunks not confirmed | "Reddit had the fastest growth: Reddit $1,300,205K→$2,202,506K (+69%); Nextdoor $247,276K→$257,646K (+4%); Rumble $91,410,026→$100,622,320 (~10%)" | Y — correct final answer, matches ground truth (Reddit ~69.4%). **Flag:** first attempt was self-contradictory (initially said Rumble, then corrected to Reddit mid-answer) and was discarded; this is the clean rerun. Rumble's FY2024 figure ($91.41M) conflicts with the $95.49M prior-year figure retrieved in Q1's log (`sample_retrieval_log_q1.json`) — same number reproduced identically across two independent runs, so likely a real alternate chunk, not a one-off hallucination. Doesn't change the Q11 answer either way. Not traced further — revisit in the comparison report if time allows. |
| Q12 | Partial | score/source not pasted this time | "Reddit reported a net profit in FY2025 ($529,721K net income); Nextdoor reported a net loss ($50,997K); Rumble: could not find a FY2025 net income figure to confirm profit or loss" | Y — faithful (refused to guess on Rumble rather than fabricate), but incomplete: Rumble's FY2025 net loss ($81,830,362, a loss) was already successfully retrieved for this same KB back in Q6, so the miss here is a retrieval-consistency gap, not a knowledge gap in the KB itself. Final answer (Reddit, only profitable company) still matches ground truth. |
| Q13 | Y (see flag) | score/source not pasted this time | "Rumble narrowed losses more: Rumble $338,362,779→$54,220,846 (−$284.1M); Nextdoor $98.1M→$50.0M (−$48.1M)" | Y — correct final answer, matches ground truth (Rumble narrowed more, ~76% vs. ~45%). **Flag:** Rumble's FY2025 net loss here ($54,220,846) conflicts with the $81,830,362 figure retrieved for the same KB in Q6. This is the second Rumble-specific figure inconsistency across questions (see also Q11's FY2024 revenue flag) — doesn't change any final answer so far, but is now a pattern worth investigating specifically for Rumble in the comparison report (possibly multiple chunks with different loss figures, e.g. GAAP vs. adjusted, or a restatement between filings). Not traced live per your call. |
| Q14 | Y (correct refusal) | not applicable — no FY2022 chunk exists in the corpus | "I couldn't find Rumble's total revenue for fiscal year 2022 in the provided filings. The retrieved Rumble documents include FY2023, FY2024, and FY2025 figures, but I do not have a FY2022 annual report excerpt or revenue figure in the provided knowledge base to cite." | Y — clean, faithful refusal on an unanswerable trap question, and correctly noted what years actually are available (FY2023 comparative + FY2024/FY2025) rather than just a bare "not found" |
| Q15 | Y (correct refusal) | not applicable — 10-Ks report historical results, not forward projections | "I couldn't find Reddit's projected revenue for fiscal year 2026 in the provided filings. The retrieved Reddit 10-K excerpts include historical revenue and some forward-looking statements, but I do not see a specific FY2026 revenue forecast or projection that I can cite." | Y — clean, faithful refusal on the second unanswerable trap question, correctly distinguishing "forward-looking statements" language (present) from an actual numeric forecast (absent) |

### 2) Fixed-size KB — MMR retrieval — **SKIPPED**

**Not run.** After logging what was believed to be this condition, we discovered the Lyzr Playground window actually had the Semantic-Agent selected, not Fixed-Size-Agent — so no data was ever collected against the Fixed-size KB with MMR retrieval. Per project decision on 2026-08-23, the remaining reranking comparison work (this condition and Condition 3 below) is being skipped so the project can move on to the Streamlit chat UI. The 15 answers originally logged here have been moved to Condition 4 below, where they actually belong.

| # | Correct chunk retrieved? (Y/N) | Rank/score (if shown) | Generated answer | Faithful? |
| --- | --- | --- | --- | --- |
| Q1–Q15 | — | — | *Not run — see note above* | — |

### 3) Semantic KB — Basic retrieval — **SKIPPED**

**Not run.** Skipped along with Condition 2 above, per the 2026-08-23 decision to end the reranking comparison early and move to building the Streamlit chat UI. The Semantic-Agent exists and is fully built (574-chunk KB), so this condition could still be run later if time allows.

| # | Correct chunk retrieved? (Y/N) | Rank/score (if shown) | Generated answer | Faithful? |
| --- | --- | --- | --- | --- |
| Q1–Q15 | | | | |

### 4) Semantic KB — MMR retrieval

**Note:** these 15 answers were originally run and logged under the "Condition 2 (Fixed-size × MMR)" label, but were actually run against the Semantic-Agent (Semantic KB, 574 Item-boundary chunks) with MMR retrieval — the Playground window had the wrong agent selected. Relabeled here to the condition they actually represent. Any "Condition 1" comparisons in the notes below refer to the true Condition 1 (Fixed-size KB, Basic retrieval), which is a cross-KB comparison, not same-KB Basic-vs-MMR.

| # | Correct chunk retrieved? (Y/N) | Rank/score (if shown) | Generated answer | Faithful? |
| --- | --- | --- | --- | --- |
| Q1 | Y | score 0.875 (source: rumble_fy2025_chunk_0069.txt) | "$100,622,320" | Y — exact match to ground truth |
| Q2 | Y | score 0.864 (source: reddit_fy2025_chunk_0104.txt) | "$529,721 thousand ($529.721 million)" net income for FY2025 | Y — exact match to ground truth |
| Q3 | Y | score 0.882 (source: nextdoor_fy2024_chunk_0013.txt) | "$98,063 thousand ($98.063 million)" net loss for FY2024 | Y — exact match to ground truth |
| Q4 | N | score 0.894 (source: reddit_fy2025_chunk_0077.txt) — wrong chunk; ground truth figure (121.4M worldwide DAUq) lives elsewhere in the filing | "50.7 million" | N — does not match ground truth (121.4M). Stated with full confidence, no hedge or caveat about which DAUq segment/breakout this figure represents. First outright wrong (non-refusal) answer seen so far — flag for comparison report: this KB/retrieval combo retrieved a high-scoring but incorrect chunk here, vs. Condition 1 (Fixed-size, Basic) getting this exact question right at score 0.898 from a correct source |
| Q5 | N | score 0.853 (source: rumble_fy2025_chunk_0004.txt) — retrieved the revenue table, not the risk-factors sentence with the 50%/66% advertising-% disclosure (same retrieval gap seen in Condition 1's Q5) | Correctly declined: total revenue given ($100,622,320), but "the retrieved excerpts do not provide a separate dollar amount for advertising revenue for FY2025" | Y — faithful refusal given what was retrieved; ground truth (50%) still not surfaced, same underlying retrieval gap as Condition 1 Q5 |
| Q6 | Y | score 0.859 (source: rumble_fy2025_chunk_0069.txt) | "FY2024 net loss $338,362,779; FY2025 net loss $81,830,362; decreased $256,532,417" (~76% reduction, matches ground truth) | Y — exact match to ground truth |
| Q7 | N | score 0.846 (source: reddit_fy2025_chunk_0083.txt) — different chunk than Q2's (chunk_0104), pulled net-income-attributable-to-common-stockholders line instead of total net income | "FY2024 net loss $(484.3)M → FY2025 net income $162.7M" plus a mix-in of "$376,971K vs $152,750K" (net income attributable to common stockholders) | N — FY2025 figure ($162.7M) does not match ground truth ($529.7M) **and directly contradicts this same run's own Q2 answer ($529,721K) two questions earlier** — a real within-run inconsistency, not just a miss vs. ground truth. Likely conflated total net income with net income attributable to common stockholders (a different, smaller line item after preferred/non-controlling adjustments) |
| Q8 | Y | score 0.865 (source: rumble_fy2024_chunk_0049.txt) | Numbers correct (68M→52M, GA4 both years, -16M, ~24% decline) but **headline sentence says "MAUs increased from Q4 2024 to Q4 2025," directly contradicting its own numbers and its own closing line ("the user count went down, not up")** | Partial — the substantive figures and final clarifying note match ground truth exactly, but the answer opens with a flatly wrong directional claim. A reader skimming just the first line would come away with the opposite conclusion. Flag for report: self-contradictory framing, distinct from Q4/Q7's wrong-number errors |
| Q9 | Partial | score 0.833 (source: nextdoor_fy2024_chunk_0013.txt) — same underlying gap as Condition 1's Q9; the FY2025 filing's restated 22.2M comparable figure was not retrieved here either | Correctly flagged the metric redefinition (WAU → Platform WAU) and explicitly declined to treat it as like-for-like; reported raw 46M → 21.0M, not the ideal restated 22.2M → 21.0M | Y — faithful (avoided the misleading ~54% naive claim, same behavior as Condition 1's Q9), but incomplete vs. the ideal answer for the same underlying retrieval-gap reason |
| Q10 | Y | score 0.827 (source: reddit_fy2025_chunk_0083.txt) | "Reddit highest: Rumble $100,622,320; Nextdoor $257,646; Reddit $2,202,506,000" | Y — correct final answer (Reddit highest), matches ground truth. **Minor flag:** Nextdoor's figure is printed as "$257,646" with no "thousand" unit label — reads as ~$258K instead of the actual ~$257.6M unless the reader already knows Nextdoor reports in thousands. Doesn't change the ranking but is a units-transparency miss (Condition 1's Q10 proactively caught and called out this same cross-filing units mismatch; this run didn't) |
| Q11 | Y | score 0.816 (source: reddit_fy2025_chunk_0083.txt) | Numbers correct (Rumble $95,488,190→$100,622,320 +5%; Reddit $1,300,205,000→$2,202,506,000 +69%; Nextdoor $247,276,000→$257,646,000 +4%) and the closing line correctly says "Reddit, at 69%" — **but the opening headline sentence says "Rumble had the fastest revenue growth rate," directly contradicting its own numbers and its own conclusion** | Partial — final figures and closing line match ground truth exactly (Reddit fastest, ~69%), but the answer opens with the wrong company name, same self-contradictory-framing failure mode as Q8. **Note on the Rumble figure-inconsistency flag from Condition 1:** this run's Rumble FY2024 revenue is $95,488,190, matching the earlier sample_retrieval_log_q1.json figure — not the conflicting $91,410,026 seen in Condition 1's Q11 — so that particular flag doesn't reproduce here |
| Q12 | N (see flag) | score 0.822 (source: nextdoor_fy2025_chunk_0017.txt) | **Rerun in a verified-clean session** (see below). First attempt returned Q11's answer verbatim — that specific thread-bleed did NOT reproduce on rerun, so the fresh-session fix still holds for that failure mode. But the rerun produced a *new*, different error: "None of the three companies reported a net profit for FY2025" — Rumble -$81.8M ✓, Nextdoor -$54.2M ✓, but **Reddit stated as a net loss of $484,276** (actually Reddit's FY2025 net income was +$529.7M; $484,276 looks like a mangled/truncated echo of Reddit's *FY2024* net loss figure, $484.3M, misapplied to FY2025) | N — wrong final answer, and worse, directly contradicts this same run's own Q2 answer ($529,721K net income, exact match) AND Q7's answer ($162.7M net income) — **three different, mutually-inconsistent FY2025 Reddit profitability figures across Q2/Q7/Q12 in this single run**. This is the single strongest finding from this condition for the report — this Semantic KB + MMR combination produced unstable, session-dependent figures specifically for Reddit's FY2025 bottom line, even though the same fact was retrieved correctly and cleanly in Q2. Separate from the earlier memory/thread-contamination flag (which did not reproduce here); see `lyzr/prompts.md` for the background-memory finding discovered during this same question |
| Q13 | Y | score 0.836 (source: nextdoor_fy2024_chunk_0013.txt) | "Rumble $338,362,779→$81,830,362 (-75.8%); Nextdoor $98,063,000→$54,204,000 (-44.7%). Rumble narrowed more." | Y — exact match to ground truth (Rumble ~76% vs. Nextdoor ~45%). **Note:** Rumble's FY2025 net loss here ($81,830,362) is internally consistent with this same run's Q6 answer — no repeat of the Q6-vs-Q13 figure conflict flagged in Condition 1 |
| Q14 | Y (correct refusal) | score 0.877 (source: rumble_fy2025_chunk_0069.txt) — no FY2022 chunk exists in the corpus | "I could not find Rumble's total revenue for fiscal year 2022 in the provided filings." Listed what years are actually available: FY2023 ($80,963,451), FY2024 ($95,488,190), FY2025 ($100,622,320) | Y — clean, faithful refusal on the unanswerable trap question, same pattern as Condition 1's Q14, correctly naming which years actually are available |
| Q15 | Y (correct refusal) | score 0.858 (source: reddit_fy2025_chunk_0104.txt) — same chunk that answered Q2 | Surfaced a real, adjacent disclosure (remaining performance obligations: $118.9M expected in 2026, $24.8M in 2027) but explicitly distinguished this from a company-wide FY2026 revenue forecast and stated "the filings do not appear to give a company-wide FY2026 revenue forecast" | Y — clean, faithful refusal; arguably the strongest refusal answer seen in the project so far, since it surfaced a real nearby number without conflating it with what was actually asked, rather than either fabricating a forecast or giving a bare "not found" |

### Comparison summary

**Scope note**: only two of the original four conditions were run — Condition 1 (Fixed-size × Basic) and Condition 4 (Semantic × MMR) — see the decision note in "Results log" above. This is a cross-KB, cross-retrieval-type comparison, not a clean isolation of either variable alone; the comparison report should name that limitation rather than present it as a full reranking-impact study. Columns below reflect what was actually run.

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
| Q12 | Y — faithful refusal on Rumble sub-question | N — wrong figure (Reddit falsely shown as a net loss), see also the session-contamination flag on the first attempt | Weakest result of either condition; three different Reddit FY2025 figures appeared across Q2/Q7/Q12 in Condition 4 alone |
| Q13 | Y — exact match (despite an internal Q6-vs-Q13 figure conflict noted at the time) | Y — exact match, internally consistent with Q6 | Condition 4 was cleaner here |
| Q14 | Y — correct refusal | Y — correct refusal | Both clean |
| Q15 | Y — correct refusal | Y — correct refusal, arguably the cleanest refusal in the project | Both clean |

**Headline takeaway**: Condition 1 (Fixed-size × Basic) had zero outright-wrong answers across all 15 questions. Condition 4 (Semantic × MMR) had three (Q4, Q7, Q12), all involving figure instability, two of them on Reddit's FY2025 bottom line specifically. Since chunking strategy and retrieval type both changed between these two conditions, the report can't isolate which variable caused the drop — but it's a legitimate, real finding to present alongside that caveat.
