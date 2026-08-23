# lyzr/

Notes and configuration *about* the Lyzr side of the build — not code, and
never real credentials. Safe for GitHub as documentation of what you built
and why.

Suggested files to add as you go:
- `agent_config_notes.md` — which Lyzr agent template you started from,
  knowledge base settings (chunk size / overlap you set for the fixed-size
  KB), embedding model used, top-k, reranking on/off per test run.
- `prompts.md` — the system prompt / instructions given to the Lyzr agent,
  and any iterations you tried (the handout asks for this in the project
  documentation deliverable, so keeping it here makes that easy to write up).

Do **not** put the Lyzr API key or endpoint here — that belongs only in
`app/.streamlit/secrets.toml`, which is gitignored.

## sample_retrieval_log_q1.json

One real example of the `kb_documents_retrieved` execution log Lyzr Studio exposes per query — captured for Q1 ("What was Rumble's total revenue for fiscal year 2025?") against the fixed-size KB. Kept as evidence of methodology: shows the top-ranked chunk (score 0.858, from `rumble_fy2025.txt`) contained the exact correct figures, which is how retrieval quality was scored for the eval set rather than just eyeballing the chat answer. The other 9 retrieved documents in this sample have their `text` fields truncated (noted inline) to keep the file a reasonable size — only the top hit that actually answered the question is kept in full. Good to reference/screenshot in the comparison report to show how scoring was done.
