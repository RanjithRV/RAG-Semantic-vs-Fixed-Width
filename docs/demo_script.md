# Demo Video — Talking Points

For the Week 2 submission's required demo video (5 minutes or less: walk through the app, explain what you built, describe how you used AI coding tools, demonstrate the result live). Recording tool: **HeyGen**, once the project is complete.

This file accumulates talking points as we discover them during testing — not a full script yet, just the beats worth hitting.

## Lead with this: the Nextdoor metric-redefinition finding (Q9)

The single best "show and tell" moment from testing so far. Nextdoor renamed/redefined its user metric between the FY2024 and FY2025 10-Ks (from "WAU" to "Platform WAU"). Asked how the metric changed year over year, the fixed-size agent:

- Correctly caught that the two numbers (45.9M old-definition WAU vs. 21.0M new-definition Platform WAU) aren't directly comparable, and said so explicitly rather than presenting a misleading ~54% "user base collapsed" claim.
- Fell short of the *ideal* answer, though — the FY2025 filing itself restates the Q4 2024 comparison under the new definition as 22.2M, giving a true like-for-like decline of only ~5%. The retrieved chunk had the redefinition context but not that specific restated figure.

Good demo beat because it shows nuance: not a clean pass/fail, but a real example of *why* retrieval quality matters for financial RAG — a naive system would have confidently reported a number that's wrong by an order of magnitude in narrative impact (54% collapse vs. 5% decline), and ours caught the trap even if it didn't fully resolve it. Show the retrieved chunk/score alongside the answer to make the "why" visible, not just the final text.

## Other talking points to add as we go

- (placeholder — add more as testing continues: strongest exact-match hits, the Q5 hallucination-vs-refusal contrast after fixing session isolation, chunking strategy comparison once semantic KB is tested, reranking impact once MMR pass is done)
