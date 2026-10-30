#!/usr/bin/env python3
"""Re-run the recorded PDF quotation/page matching; no semantic or model evaluation."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import unicodedata


def normalize(text):
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"-\s*\n\s*", "", text)
    return re.sub(r"\s+", "", text).lower()


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path,
                        default=root / "materials" / "Hafemeister_Satija_2019_sctransform.pdf")
    args = parser.parse_args()
    extracted = subprocess.run(["pdftotext", str(args.pdf), "-"],
                               check=True, capture_output=True).stdout.decode("utf-8")
    pages = extracted.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    normalized = [normalize(page) for page in pages]
    records = []
    for filename in ("quote-page-check.json", "followup-quote-page-check.json"):
        historical = json.loads((root / filename).read_text(encoding="utf-8"))
        for item in historical["spans"]:
            needle = normalize(item["quote"])
            matches = [number for number, page in enumerate(normalized, 1)
                       if needle in page]
            records.append({
                "record": filename,
                "ax_node": item["ax_node"],
                "quote": item["quote"],
                "claimed_pdf_page": item["claimed_pdf_page"],
                "newly_matched_pages": matches,
                "claimed_page_contains_quote": item["claimed_pdf_page"] in matches,
            })
    print(json.dumps({
        "pdf": args.pdf.name,
        "pages": len(pages),
        "scope": "Text-location matching only; not scientific interpretation or model accuracy.",
        "records": records,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
