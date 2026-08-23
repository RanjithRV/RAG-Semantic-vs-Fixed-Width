"""
Shared registry of the 6 filings used in this project — FY2024 and FY2025
10-Ks for Rumble (RUM), Reddit (RDDT), and Nextdoor (NXDR/KIND).

Keeping this in one place means fetch_filings.py, clean_filings.py, and
chunk_filings.py all agree on filenames and stay in sync with
docs/project_scope.md. If the scope doc changes, update here too.
"""

FILINGS = [
    {
        "company": "rumble",
        "ticker": "RUM",
        "fiscal_year": 2024,
        "url": "https://www.sec.gov/Archives/edgar/data/1830081/000101376225001863/ea0234307-10k_rumble.htm",
        "filetype": "html",
    },
    {
        "company": "rumble",
        "ticker": "RUM",
        "fiscal_year": 2025,
        "url": "https://www.sec.gov/Archives/edgar/data/1830081/000121390026024099/ea0277968-10k_rumble.htm",
        "filetype": "html",
    },
    {
        "company": "reddit",
        "ticker": "RDDT",
        "fiscal_year": 2024,
        "url": "https://www.sec.gov/Archives/edgar/data/1713445/000171344525000018/rddt-20241231.htm",
        "filetype": "html",
    },
    {
        "company": "reddit",
        "ticker": "RDDT",
        "fiscal_year": 2025,
        # Reddit's FY2025 10-K was filed as a PDF, unlike the other five HTML filings.
        "url": "https://www.sec.gov/Archives/edgar/data/1713445/000171344526000062/redditinc10-k2025.pdf",
        "filetype": "pdf",
    },
    {
        "company": "nextdoor",
        "ticker": "NXDR",
        "fiscal_year": 2024,
        "url": "https://www.sec.gov/Archives/edgar/data/1846069/000184606925000017/kind-20241231.htm",
        "filetype": "html",
    },
    {
        "company": "nextdoor",
        "ticker": "NXDR",
        "fiscal_year": 2025,
        "url": "https://www.sec.gov/Archives/edgar/data/1846069/000184606926000023/kind-20251231.htm",
        "filetype": "html",
    },
]


def slug(filing):
    """e.g. 'rumble_fy2024' — used as the base filename across raw/cleaned/chunks."""
    return f"{filing['company']}_fy{filing['fiscal_year']}"
