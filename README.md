# Week 2 RAG Project — Financial Document Intelligence (Lyzr, No-Code Track)

Comparative RAG pipeline over the FY2024–FY2025 10-K filings of three public
"social sharing" companies — Rumble (RUM), Reddit (RDDT), and Nextdoor
(NXDR) — built no-code in Lyzr, with a custom Streamlit chat front-end for
sharing with the class.

Full project scope, framework fields, and decision log live in
[`docs/project_scope.md`](docs/project_scope.md) (mirrored from the
"AI Education Project" Claude Project — that's the master copy; update
there first, then re-sync this file).

## Folder map

| Folder | What's in it | Goes to GitHub? |
| --- | --- | --- |
| `docs/` | Scope doc, eval question set, chunking/reranking comparison report | **Yes** |
| `ingestion/` | Scripts: fetch filings from EDGAR, clean HTML/XBRL + preserve tables, produce fixed-size and semantic chunk variants | **Yes** |
| `app/` | Streamlit chat UI that calls the Lyzr agent API | **Yes** (except real secrets — see below) |
| `lyzr/` | Notes on Lyzr agent config, KB setup steps, prompts used — no credentials | **Yes** |
| `data/raw/` | Raw downloaded 10-K filings (HTML/PDF) from SEC EDGAR | **No** — large, and regenerable by re-running `ingestion/fetch_filings.py`. SEC filings are public domain, so no legal issue re-hosting them, it's purely a repo-size/hygiene call. |
| `data/cleaned/` | Cleaned plain-text versions of each filing | **No** — regenerable via `ingestion/clean_filings.py`, and can be large |
| `data/chunks/fixed/`, `data/chunks/semantic/` | Chunked text ready to upload into Lyzr KBs | **No** — regenerable via `ingestion/chunk_filings.py` |

`.gitignore` at the repo root already encodes the "No" rows above, plus
secrets files, Python caches, and virtual envs. When you're ready to push
to GitHub: `git init`, review `git status` against this table, then
`git add` only what's meant to be public.

## Secrets — never commit these

- `app/.streamlit/secrets.toml` (real Lyzr API key/endpoint) — only
  `secrets.toml.example` (a template with placeholders) is tracked.
- Any `.env` file.

## Pipeline order

1. `ingestion/fetch_filings.py` → downloads the 6 filings into `data/raw/`.
2. `ingestion/clean_filings.py` → strips HTML/XBRL markup and filing
   boilerplate, converts tables to Markdown, writes `data/cleaned/*.txt`.
3. `ingestion/chunk_filings.py` → writes two variants from the cleaned
   text: fixed-size chunks (`data/chunks/fixed/`) and section/topic-based
   "semantic" chunks (`data/chunks/semantic/`), each as individual `.txt`
   files ready to upload into a Lyzr knowledge base.
4. Build two Lyzr knowledge bases/agents, one per chunk variant, run the
   eval question set against both, write up the comparison in `docs/`.
5. Point `app/streamlit_app.py` at the winning (or both) Lyzr agent(s) and
   deploy via Streamlit Community Cloud, linked from a GitHub repo built
   from this folder.
