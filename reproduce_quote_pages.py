#!/usr/bin/env python3
"""Re-run the recorded PDF quotation/page matching; no semantic or model evaluation.

Reads the spans of round 1, round 2 and the T1-R probe and prints one compact record per span.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import unicodedata

RECORDS = ("quote-page-check.json", "followup-quote-page-check.json", "t1r-test/quote-page-check.json")


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
    for filename in RECORDS:
        historical = json.loads((root / filename).read_text(encoding="utf-8"))
        for item in historical["spans"]:
            needle = normalize(item["quote"])
            matches = [number for number, page in enumerate(normalized, 1) if needle in page]
            records.append({"record": filename, "ax_node": item["ax_node"], "quote": item["quote"],
                            "claimed_pdf_page": item["claimed_pdf_page"], "newly_matched_pages": matches,
                            "claimed_page_contains_quote": item["claimed_pdf_page"] in matches})
    summary = {f: f"{sum(r['claimed_page_contains_quote'] for r in records if r['record'] == f)}"
                  f"/{sum(r['record'] == f for r in records)}" for f in RECORDS}
    head = {"pdf": args.pdf.name, "pages": len(pages),
            "scope": "Text-location matching only; not scientific interpretation or model accuracy.",
            "on_claimed_page": summary}
    body = ",\n".join("  " + json.dumps(r, ensure_ascii=False) for r in records)
    print(json.dumps(head, ensure_ascii=False)[:-1] + ',\n "records": [\n' + body + "\n ]}")


if __name__ == "__main__":
    main()
