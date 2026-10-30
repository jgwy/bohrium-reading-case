#!/usr/bin/env python3
"""Replay the App's visible search and audit the first answer's absence claims.

Text-location evidence only: no model call, no network, no scientific judgement.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess

# Verbatim from AX node 29 of app-inprogress-ax.txt (the App's visible search step).
APP_VISIBLE_PATTERN = r"Smart|TPM|transcripts|biops|patient|Donor|donor|full-length|full length"

# Each absence/uniqueness claim in the first answer (app-answer.md), the terms it asserts
# about, and whether each term is covered by the visible pattern above.
CLAIMS = [
    {
        "id": "A1",
        "answer_wording": "The words \"Smart-seq2\" and \"TPM\" never appear anywhere in the paper.",
        "terms": {"Smart-seq": "Smart", "TPM": "TPM"},
    },
    {
        "id": "A2",
        "answer_wording": "Nothing about biopsies, patients, or replicate design - those terms do not occur.",
        "terms": {"biops": "biops", "patient": "patient", "replicat": None},
    },
    {
        "id": "A3",
        "answer_wording": "The only reference to non-UMI data is about a different tool, not sctransform: SCnorm (p. 3).",
        "terms": {"non-UMI": None, "read-level": None, "read count": None},
    },
]


def pages_of(pdf):
    raw = subprocess.run(["pdftotext", str(pdf), "-"], check=True,
                         capture_output=True).stdout.decode("utf-8")
    pages = raw.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    # Same hyphen joining as reproduce_quote_pages.py; whitespace collapsed, not removed.
    return [re.sub(r"\s+", " ", re.sub(r"-\s*\n\s*", "", p)) for p in pages]


def hits(pattern, pages, flags=0):
    out = []
    for number, text in enumerate(pages, 1):
        for m in re.finditer(pattern, text, flags):
            lo, hi = max(0, m.start() - 60), min(len(text), m.end() + 60)
            out.append({"page": number, "match": m.group(0), "context": text[lo:hi]})
    return out


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path,
                        default=root / "materials" / "Hafemeister_Satija_2019_sctransform.pdf")
    args = parser.parse_args()
    pages = pages_of(args.pdf)
    visible = hits(APP_VISIBLE_PATTERN, pages)
    audit = []
    for claim in CLAIMS:
        rows = []
        for term, covered_by in claim["terms"].items():
            found = hits(re.escape(term), pages, re.IGNORECASE)
            rows.append({
                "term": term,
                "in_app_visible_pattern": covered_by is not None,
                "pdf_pages_with_match": sorted({h["page"] for h in found}),
                "first_context": found[0]["context"] if found else None,
            })
        audit.append({"id": claim["id"], "answer_wording": claim["answer_wording"], "terms": rows})
    print(json.dumps({
        "pdf": args.pdf.name,
        "pages": len(pages),
        "scope": ("Lexical replay on pdftotext output of this PDF only. The App searched its own "
                  "parsed block file, which is not available; earlier collapsed App search steps "
                  "did not show their patterns."),
        "app_visible_pattern": APP_VISIBLE_PATTERN,
        "app_reported_match_count": 1,
        "replayed_case_sensitive_matches": visible,
        "absence_claim_audit": audit,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
