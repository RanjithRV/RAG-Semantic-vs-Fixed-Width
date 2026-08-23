"""
Step 3 of the pipeline: produce two chunk variants from each cleaned
filing in data/cleaned/, for the fixed-size vs. semantic chunking
comparison the Week 2 deliverable asks for.

  data/chunks/fixed/<slug>/<slug>_chunk_0001.txt, ...
      Fixed-size chunks: every ~CHUNK_WORDS words, with OVERLAP_WORDS of
      overlap between consecutive chunks. Mirrors what Lyzr's own
      "chunk size / overlap" knobs do internally — kept mainly for you to
      inspect/cite in the report; in practice we upload the 6 full cleaned
      documents to Lyzr and let its native chunker do this split.

  data/chunks/semantic/<slug>/<slug>_chunk_0001.txt, ...
      Section/topic-based chunks: split at 10-K "Item N." boundaries
      (Item 1 Business, Item 1A Risk Factors, Item 7 MD&A, Item 8
      Financial Statements, etc.), so each chunk is a coherent topic
      rather than an arbitrary word-count slice. Any single Item section
      longer than MAX_SEMANTIC_WORDS is further split on paragraph
      breaks, so no chunk balloons to the whole MD&A section.

Each chunk is written as its own .txt file, named with its source
filing's slug as a prefix (e.g. rumble_fy2024_chunk_0001.txt) — Lyzr has
no folder concept, so when you upload all six filings' chunks together
as one flat batch, unique/descriptive filenames are what let Lyzr's
citations (and you) tell which company and fiscal year a chunk came
from. Upload these individually with Lyzr's own chunk size set larger
than any of these files, so it doesn't re-split them further.

Usage:
    python ingestion/chunk_filings.py
"""

import pathlib
import re

from filings import FILINGS, slug

CLEANED_DIR = pathlib.Path(__file__).resolve().parent.parent / "data" / "cleaned"
CHUNKS_DIR = pathlib.Path(__file__).resolve().parent.parent / "data" / "chunks"

CHUNK_WORDS = 500
OVERLAP_WORDS = 50

ITEM_PATTERN = re.compile(
    r"(?=^item\s+\d+[a-c]?\.?\s+[a-z])", re.IGNORECASE | re.MULTILINE
)
MAX_SEMANTIC_WORDS = 800


def write_chunks(chunks, out_dir, prefix):
    out_dir.mkdir(parents=True, exist_ok=True)
    # Clear both old-style (pre-rename) and current-style chunk files before
    # rewriting, so re-running this script never leaves stale files behind.
    for old in list(out_dir.glob("chunk_*.txt")) + list(out_dir.glob("*_chunk_*.txt")):
        old.unlink()
    for i, chunk in enumerate(chunks, start=1):
        (out_dir / f"{prefix}_chunk_{i:04d}.txt").write_text(chunk.strip(), encoding="utf-8")
    return len(chunks)


def fixed_size_chunks(text, chunk_words=CHUNK_WORDS, overlap_words=OVERLAP_WORDS):
    words = text.split()
    if not words:
        return []
    chunks = []
    step = max(chunk_words - overlap_words, 1)
    for start in range(0, len(words), step):
        chunk_words_slice = words[start : start + chunk_words]
        if not chunk_words_slice:
            break
        chunks.append(" ".join(chunk_words_slice))
        if start + chunk_words >= len(words):
            break
    return chunks


def split_large_section(section_text, max_words=MAX_SEMANTIC_WORDS):
    """If a semantic section is too long, break it on paragraph boundaries
    (never mid-sentence/mid-table) so no chunk is unmanageably huge."""
    words = section_text.split()
    if len(words) <= max_words:
        return [section_text]

    paragraphs = re.split(r"\n\s*\n", section_text)
    pieces, current, current_words = [], [], 0
    for para in paragraphs:
        para_words = len(para.split())
        if current and current_words + para_words > max_words:
            pieces.append("\n\n".join(current))
            current, current_words = [], 0
        current.append(para)
        current_words += para_words
    if current:
        pieces.append("\n\n".join(current))
    return pieces


def semantic_chunks(text):
    sections = ITEM_PATTERN.split(text)
    sections = [s for s in sections if s.strip()]
    if not sections:
        # No "Item N." headers matched (cleaning heuristic may have missed
        # them) — fall back to paragraph-based splitting of the whole doc.
        sections = [text]

    chunks = []
    for section in sections:
        chunks.extend(split_large_section(section))
    return chunks


def chunk_all():
    for filing in FILINGS:
        cleaned_path = CLEANED_DIR / f"{slug(filing)}.txt"
        if not cleaned_path.exists():
            print(f"MISSING cleaned file, run clean_filings.py first: {cleaned_path.name}")
            continue

        text = cleaned_path.read_text(encoding="utf-8")

        fixed = fixed_size_chunks(text)
        n_fixed = write_chunks(fixed, CHUNKS_DIR / "fixed" / slug(filing), slug(filing))

        semantic = semantic_chunks(text)
        n_semantic = write_chunks(
            semantic, CHUNKS_DIR / "semantic" / slug(filing), slug(filing)
        )

        print(f"{slug(filing)}: {n_fixed} fixed-size chunks, {n_semantic} semantic chunks")

    print(f"\nDone. Chunk variants in {CHUNKS_DIR}")


if __name__ == "__main__":
    chunk_all()
