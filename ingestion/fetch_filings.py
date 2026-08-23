"""
Step 1 of the pipeline: download the 6 10-K filings from SEC EDGAR into
data/raw/.

Usage:
    python ingestion/fetch_filings.py

SEC EDGAR requires a descriptive User-Agent identifying who's making the
request (their fair-access policy, not optional) — edit USER_AGENT below
to your own name/email before running.
"""

import pathlib
import time

import requests

from filings import FILINGS, slug

# SEC EDGAR fair-access policy requires a real identifying User-Agent.
# https://www.sec.gov/os/webmaster-faq#developers
USER_AGENT = "Week2 RAG Class Project research@example.com"

RAW_DIR = pathlib.Path(__file__).resolve().parent.parent / "data" / "raw"


def fetch_all():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    headers = {"User-Agent": USER_AGENT}

    for filing in FILINGS:
        out_path = RAW_DIR / f"{slug(filing)}.{filing['filetype']}"
        if out_path.exists():
            print(f"skip (already downloaded): {out_path.name}")
            continue

        print(f"fetching {filing['ticker']} FY{filing['fiscal_year']} -> {out_path.name}")
        resp = requests.get(filing["url"], headers=headers, timeout=30)
        resp.raise_for_status()
        out_path.write_bytes(resp.content)

        # Be polite to EDGAR — stay well under its rate limits.
        time.sleep(0.5)

    print(f"\nDone. {len(FILINGS)} filings in {RAW_DIR}")


if __name__ == "__main__":
    fetch_all()
