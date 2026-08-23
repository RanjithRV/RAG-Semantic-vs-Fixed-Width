"""
Step 2 of the pipeline: turn each raw filing in data/raw/ into clean plain
text in data/cleaned/, ready for chunking.

What "clean" means here:
  - HTML/XBRL markup stripped out (SEC filings use inline XBRL, which
    wraps visible numbers in <ix:...> tags plus a hidden XBRL header block
    we don't want).
  - Tables converted to Markdown so numbers stay aligned/readable instead
    of being flattened into a run-on string of digits.
  - Boilerplate cropped out: everything before the start of Item 1 (cover
    page, table of contents) and everything from the Signatures section
    onward (signature blocks, exhibit index) is dropped, since it isn't
    useful for Q&A and just adds noise to retrieval.

This is a heuristic pass, not a perfect parser — spot-check the output in
data/cleaned/ before chunking, especially around the crop boundaries and
any unusually complex tables.

Usage:
    python ingestion/clean_filings.py
"""

import pathlib
import re

import pdfplumber
from bs4 import BeautifulSoup, Comment

from filings import FILINGS, slug

RAW_DIR = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw"
CLEANED_DIR = pathlib.Path(__file__).resolve().parent.parent / "data" / "cleaned"

START_PATTERN = re.compile(r"item\s+1\.?\s+business", re.IGNORECASE)
END_PATTERN = re.compile(r"^\s*signatures\s*$", re.IGNORECASE | re.MULTILINE)


def table_to_markdown(rows):
    """rows: list of list-of-cell-strings -> a Markdown table string."""
    rows = [[(c or "").strip().replace("\n", " ") for c in row] for row in rows]
    rows = [row for row in rows if any(cell for cell in row)]
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]

    lines = ["| " + " | ".join(rows[0]) + " |", "| " + " | ".join(["---"] * width) + " |"]
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def clean_html(raw_bytes):
    soup = BeautifulSoup(raw_bytes, "lxml")

    # Drop non-visible cruft: scripts, styles, comments, the hidden XBRL
    # header block, and anything explicitly display:none.
    for tag in soup(["script", "style"]):
        tag.decompose()
    for comment in soup.find_all(string=lambda s: isinstance(s, Comment)):
        comment.extract()
    header = soup.find(re.compile(r"(^|:)header$", re.IGNORECASE))
    if header:
        header.decompose()
    for tag in soup.select('[style*="display:none"], [style*="display: none"]'):
        tag.decompose()

    # Replace each <table> with its Markdown rendering so get_text() below
    # keeps the table content, structured, in place.
    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = tr.find_all(["td", "th"])
            rows.append([c.get_text(" ", strip=True) for c in cells])
        md = table_to_markdown(rows)
        table.replace_with("\n\n" + md + "\n\n")

    text = soup.get_text("\n")
    return text


def clean_pdf(path):
    parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            tables = page.find_tables()
            table_bboxes = [t.bbox for t in tables]

            # Render any tables on this page as Markdown.
            for t in tables:
                md = table_to_markdown(t.extract())
                parts.append(md)

            # Grab the page's plain text too (pdfplumber doesn't easily let
            # us "remove" the table region from the text stream, so tables
            # show up twice — once as Markdown, once inline as raw text.
            # That's an acceptable tradeoff for a student project: it's
            # noisier but doesn't lose data. Flag in README if it matters
            # for your evaluation.)
            page_text = page.extract_text() or ""
            parts.append(page_text)
    return "\n\n".join(parts)


def crop_boilerplate(text):
    start_match = START_PATTERN.search(text)
    start = start_match.start() if start_match else 0

    end_matches = list(END_PATTERN.finditer(text))
    end = end_matches[-1].start() if end_matches else len(text)

    if end <= start:
        # Heuristic failed to find sane boundaries — return uncropped
        # rather than silently truncating everything.
        return text
    return text[start:end]


def normalize_whitespace(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_all():
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)

    for filing in FILINGS:
        raw_path = RAW_DIR / f"{slug(filing)}.{filing['filetype']}"
        out_path = CLEANED_DIR / f"{slug(filing)}.txt"

        if not raw_path.exists():
            print(f"MISSING raw file, run fetch_filings.py first: {raw_path.name}")
            continue

        print(f"cleaning {raw_path.name} -> {out_path.name}")
        if filing["filetype"] == "html":
            text = clean_html(raw_path.read_bytes())
        elif filing["filetype"] == "pdf":
            text = clean_pdf(raw_path)
        else:
            raise ValueError(f"unknown filetype: {filing['filetype']}")

        text = crop_boilerplate(text)
        text = normalize_whitespace(text)
        out_path.write_text(text, encoding="utf-8")
        print(f"  {len(text):,} chars written")

    print(f"\nDone. Cleaned files in {CLEANED_DIR}")


if __name__ == "__main__":
    clean_all()
