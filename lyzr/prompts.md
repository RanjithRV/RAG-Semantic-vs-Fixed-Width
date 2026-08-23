# Lyzr Agent Prompts / Instructions

Used identically across both agents so that **knowledge base (chunking strategy) is the only variable that differs** between them — same prompt, same LLM, same temperature, only the attached KB changes. This is what makes the fixed-vs-semantic comparison valid rather than confounded.

## Agents

| Agent | Knowledge base attached | Purpose |
| --- | --- | --- |
| `Financial 10-K RAG — Fixed-Size Chunking` | Fixed-size KB (6 full cleaned filings, Lyzr's native chunker) | Arm A of the chunking comparison |
| `Financial 10-K RAG — Semantic Chunking` | Semantic KB (574 pre-split Item-boundary chunk files) | Arm B of the chunking comparison |

## Agent configuration (identical for both agents)

Lyzr's agent builder splits instructions into three fields — Role, Goal, and Instructions — rather than one system prompt block. Same content used for both agents; only the attached knowledge base differs.

**Role:**
```
A financial research assistant specializing in SEC 10-K filings analysis for three companies: Rumble (RUM), Reddit (RDDT), and Nextdoor (NXDR).
```

**Goal:**
```
Answer questions about these three companies' FY2024 and FY2025 10-K annual reports accurately and faithfully, using only information retrieved from the attached knowledge base — and clearly say so when the filings don't contain the answer, rather than guessing.
```

**Instructions:**
```
1. Answer only using information retrieved from your knowledge base. Do not use outside knowledge or assume figures that aren't present in the retrieved content.
2. Always state which company and fiscal year each figure or fact refers to, since your knowledge base spans three companies and two years.
3. If retrieved content shows a metric that was redefined or restated between filings (a changed name, definition, or methodology), say so explicitly rather than comparing incompatible numbers as if they were the same measurement.
4. If the retrieved documents don't contain enough information to answer the question, say clearly that you could not find this in the provided filings. Do not guess, estimate, or fabricate a number.
5. Cite specific figures exactly as stated in the filing (exact dollar amounts, percentages, user counts) rather than paraphrasing or rounding excessively.
6. Keep answers concise and analyst-appropriate: lead with the direct answer, then brief supporting context only if useful.
```

## Other settings kept identical across both agents

- **Embedding model**: same choice on both KBs (confirmed when building the KBs — see `docs/project_scope.md`).
- **Generation LLM**: OpenAI `gpt-5.4-mini` — same on both agents.
- **Temperature**: ~0.1–0.2 on both (favor faithful/factual answers over creative ones).
- **Retrieval settings** (if exposed at agent level separately from KB level): Basic retrieval, same top-k / score threshold on both.
- **File as Output**: OFF on both — we want plain text answers for eval logging, not downloadable file responses.
- **Memory**: not added on either agent — each of the 15 eval questions should be answered independently, without earlier questions in a test session influencing retrieval/answers for later ones.
- **Responsible AI**: not added on either agent — it's a content-moderation/guardrail feature, not related to retrieval or citation quality, and out of scope for this comparison.

## Methodology note: why MMR is used as the reranking stand-in

The assignment asks for a reranking-impact comparison as part of the retrieval evaluation. Lyzr's agent Configure panel does not expose a dedicated reranking model or reranking step — the retrieval-type options available are **Basic**, **MMR**, and **HyDE**. There is no separate "rerank retrieved chunks" toggle to test against a no-reranking baseline.

Of the three options, **MMR (Maximal Marginal Relevance) was chosen as the closest practical stand-in for reranking**: it re-scores and re-selects from the initially retrieved candidate set to reduce redundancy and favor diverse, relevant chunks, which is functionally the same role a reranking step plays in a typical RAG pipeline (take an initial top-k retrieval, then apply a second pass that reorders/filters it before it reaches the LLM). Basic retrieval, by contrast, returns the top-k chunks by similarity score alone with no second pass.

**This is a substitution, not an equivalent.** A real reranker (e.g., a cross-encoder model scoring query-chunk pairs) and MMR (a diversity-driven re-selection heuristic) work on different principles and aren't guaranteed to produce comparable effects. The comparison report frames results as **"MMR retrieval vs. Basic retrieval,"** not as "reranked vs. non-reranked," to avoid overclaiming what this evaluation actually tested. This limitation is named explicitly here, in `docs/project_scope.md`, and in `docs/comparison_report.md`, rather than left implicit.

## Methodology note: reset the Playground session between every eval question

Discovered during testing: even with the agent's "Memory" feature left un-added, a single Playground conversation thread still carries its full turn history into each new call (standard multi-turn chat behavior, separate from Lyzr's explicit Memory feature). By the 5th question in one continuous thread, the model began blending earlier Q&A pairs into a new answer — re-answering two already-correct earlier questions incorrectly alongside the new one, and getting the new question wrong too (see the Rumble advertising-percentage miscalculation in `docs/eval_results.md`, Q5, first attempt).

**Fix applied**: start a fresh Playground conversation/session before every one of the 15 eval questions, for every one of the four conditions (60 fresh sessions total). This guarantees each answer is judged purely on that question's own retrieval, with no cross-question contamination. Q1–Q4 (asked in the original shared thread) came back clean and were not re-run, since contamination only appeared once the thread grew longer — but this is a good caveat to name explicitly in the report's methodology section.

## Methodology note: background memory processing observed even with Memory "not added" (discovered during Condition 2, 2026-08-23)

While running Condition 2 (Fixed-size KB, MMR retrieval) Q12 in what was set up as a fresh Playground session, the agent returned Q11's answer verbatim in response to a completely different question (Q12 asked which company reported a net profit; the agent re-emitted Q11's revenue-growth-rate answer). A background event log surfaced during this session showed:

```
"feature": "memory",
"event_type": "lyzr_memory_process_completed",
"status": "success",
"message": "Lyzr memory processing completed",
"run_id": "338cb363-6ff1-48da-94d6-180c8f9fd6ee",
...
```

This is direct evidence that **Lyzr runs memory processing on the backend even when the agent's "Memory" feature is not explicitly added in the builder** — contradicting the assumption in the settings table above ("Memory: not added on either agent"). The earlier fix (fresh Playground session per question) addresses *thread* history within one open conversation, but this event suggests there may be a separate, account/session-level memory layer that a "fresh" Playground tab doesn't fully reset.

**Action items:**
1. Re-run Q12 in a verified-clean session (new browser tab, or check whether Lyzr exposes a way to clear this memory layer) to confirm whether the contamination reproduces.
2. If it does reproduce even in a confirmed-fresh session, this becomes a first-class methodology caveat for the report — not just a per-question anomaly — since it means "fresh session" as practiced (new Playground thread) may not fully guarantee independence between eval questions.
3. Worth checking Lyzr's docs/settings for an explicit toggle to disable this backend memory process, separate from the agent-level "Memory" feature checkbox.

## Iteration log

_(Add entries here as you tweak the prompt — the handout's submission asks for "prompts or agent instructions you used" and "iterations you tried," so this is the place to note what changed and why.)_

- v1 (2026-08-2x): initial prompt as above, applied identically to both agents before running the 15-question eval set.
