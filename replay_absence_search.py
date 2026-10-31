#!/usr/bin/env python3
"""Replay the App's visible searches and audit absence/uniqueness claims, before and after T1-R.

Part 1 (round 1, original reader session): replays the one visible search pattern and audits
the three absence/uniqueness claims of app-answer.md.
Part 2 (T1-R probe): replays every search pattern shown in t1r-test/search-observations-excerpt.jsonl
on `pdftotext -layout` text (the App's T1-R route extracted text "with layout"), compares the
App's "共 N 处" count with matching lines and with matches, and audits the T1-R answer's claims.

Text-location evidence only: no model call, no network, no scientific judgement.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess

# Verbatim from AX node 29 of app-inprogress-ax.txt (the App's visible search step).
APP_VISIBLE_PATTERN = r"Smart|TPM|transcripts|biops|patient|Donor|donor|full-length|full length"

# Round 1: absence/uniqueness claims in app-answer.md, the terms they assert about, and the
# visible-pattern alternative covering each term (None = not in the visible pattern).
CLAIMS = [
    {"id": "A1",
     "answer_wording": "The words \"Smart-seq2\" and \"TPM\" never appear anywhere in the paper.",
     "terms": {"Smart-seq": "Smart", "TPM": "TPM"}},
    {"id": "A2",
     "answer_wording": "Nothing about biopsies, patients, or replicate design - those terms do not occur.",
     "terms": {"biops": "biops", "patient": "patient", "replicat": None}},
    {"id": "A3",
     "answer_wording": "The only reference to non-UMI data is about a different tool, not sctransform: SCnorm (p. 3).",
     "terms": {"non-UMI": None, "read-level": None, "read count": None}},
    {"id": "A5",
     "answer_wording": "there is no empirical demonstration for full-length/non-UMI data",
     "terms": {"full-length": "full-length", "Smart-seq": "Smart", "TPM": "TPM"}},
]
# Not scriptable, judged by reading (README): A4 "The only remotely relevant statement is an assumption
# about heterogeneity (p. 10)"; p. 5 (technical replicate) and p. 9 (cell-type RNA content) are also relevant.

# T1-R: every absence/uniqueness claim in t1r-test/final-answer-excerpt.txt (node in brackets).
# Terms are regular expressions searched case-insensitively on all 15 pages.
T1R_CLAIMS = [
    {"id": "B1", "node": "51, 54, 91",
     "answer_wording": "The paper never mentions Smart-seq2 or TPM (search terms above: no hits)",
     "terms": [r"smart[- ]?seq", r"TPM", r"transcripts? per million"]},
    {"id": "B2", "node": "97, 100",
     "answer_wording": "Nothing about biopsies, patients, or tumours ... the tumour/biopsy/patient concepts never appear",
     "terms": [r"biops", r"patient", r"tumou?r", r"cancer|malignan|melanoma|carcinom|glioblastom"]},
    {"id": "B3", "node": "57",
     "answer_wording": "hits on pages 2, 3, 11, 15 (5 hits; these are the only non-UMI / read-level / plate-based mentions)",
     "terms": [r"plate[- ]?based", r"plate", r"non[- ]?UMI", r"read[- ]?level", r"read count"]},
    {"id": "B4", "node": "113",
     "answer_wording": "the paper never uses the word \"comparable\" (search above: no literal hit)",
     "terms": [r"comparab"]},
    {"id": "B5", "node": "92",  # a claim about evaluation; the terms only bound it lexically
     "answer_wording": "The paper never evaluates sctransform on TPM, read counts, or full-length/non-UMI input",
     "terms": [r"full[- ]?length", r"Smart[- ]?seq", r"TPM"]},
    {"id": "B6", "node": "78",
     "answer_wording": "9 hits; all are \"across genes\"/\"between genes\" in the sense of pooling information",
     "terms": [r"across gene|between gene"], "all_contexts": True},
]


def raw_pages(pdf, layout=False):
    cmd = ["pdftotext"] + (["-layout"] if layout else []) + [str(pdf), "-"]
    pages = subprocess.run(cmd, check=True, capture_output=True).stdout.decode("utf-8").split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages


def joined(pages):
    # Same hyphen joining as reproduce_quote_pages.py; whitespace collapsed, not removed.
    return [re.sub(r"\s+", " ", re.sub(r"-\s*\n\s*", "", p)) for p in pages]


def hits(pattern, pages, flags=0):
    out = []
    for number, text in enumerate(pages, 1):
        for m in re.finditer(pattern, text, flags):
            lo, hi = max(0, m.start() - 60), min(len(text), m.end() + 60)
            out.append({"page": number, "match": m.group(0), "context": text[lo:hi]})
    return out


def app_t1r_searches(path):
    """Parse '搜索内容 PATTERN，共 N 处' buttons from the T1-R working-panel excerpt."""
    found = []
    for line in path.read_text(encoding="utf-8").splitlines():
        for node in json.loads(line)["new_scientific_ui_nodes"]:
            m = re.search(r"搜索内容 (.*)，共 (\d+) 处", node["visible"])
            if m:
                found.append((node["node"], m.group(1), int(m.group(2))))
    return found


def line_and_match_counts(pattern, pages):
    lines, matches, page_set = 0, 0, set()
    for number, text in enumerate(pages, 1):
        for line in text.split("\n"):
            k = len(re.findall(pattern, line))
            if k:
                lines, matches = lines + 1, matches + k
                page_set.add(number)
    return lines, matches, sorted(page_set)


def dump(obj, indent=0):
    """JSON with one line per leaf record, to keep the output short and diff-friendly."""
    pad = " " * indent
    if isinstance(obj, dict) and any(isinstance(v, (dict, list)) for v in obj.values()) and not (
            "term" in obj or "node" in obj and "app_count" in obj):
        items = [f'{pad} {json.dumps(k, ensure_ascii=False)}: {dump(v, indent + 1).lstrip()}' for k, v in obj.items()]
        return pad + "{\n" + ",\n".join(items) + "\n" + pad + "}"
    if isinstance(obj, list) and obj and all(isinstance(v, dict) for v in obj):
        return pad + "[\n" + ",\n".join(dump(v, indent + 1) for v in obj) + "\n" + pad + "]"
    return pad + json.dumps(obj, ensure_ascii=False)


def main():
    root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path,
                        default=root / "materials" / "Hafemeister_Satija_2019_sctransform.pdf")
    parser.add_argument("--searches", type=Path,
                        default=root / "t1r-test" / "search-observations-excerpt.jsonl")
    args = parser.parse_args()
    pages = joined(raw_pages(args.pdf))

    audit = []
    for claim in CLAIMS:
        rows = []
        for term, covered_by in claim["terms"].items():
            found = hits(re.escape(term), pages, re.IGNORECASE)
            rows.append({"term": term, "in_app_visible_pattern": covered_by is not None,
                         "pdf_pages_with_match": sorted({h["page"] for h in found}),
                         "first_context": found[0]["context"] if found else None})
        audit.append({"id": claim["id"], "answer_wording": claim["answer_wording"], "terms": rows})

    layout = raw_pages(args.pdf, layout=True)
    counts = []
    for node, pattern, app_count in app_t1r_searches(args.searches):
        lines, matches, page_list = line_and_match_counts(pattern, layout)
        counts.append({"node": node, "pattern": pattern, "app_count": app_count,
                       "matching_lines": lines, "matches": matches, "pages": page_list})
    t1r_audit = []
    for claim in T1R_CLAIMS:
        rows = []
        for term in claim["terms"]:
            found = hits(term, pages, re.IGNORECASE)
            row = {"term": term, "pdf_pages_with_match": sorted({h["page"] for h in found}),
                   "first_context": found[0]["context"] if found else None}
            if claim.get("all_contexts"):
                row["all_contexts"] = [f'p. {h["page"]}: {h["context"]}' for h in found]
            rows.append(row)
        t1r_audit.append({"id": claim["id"], "node": claim["node"],
                          "answer_wording": claim["answer_wording"], "terms": rows})

    print(dump({
        "pdf": args.pdf.name,
        "pages": len(pages),
        "scope": ("Lexical replay on pdftotext output of this PDF only. Round 1: the App searched its own "
                  "parsed block file, which is not available; earlier collapsed App search steps did not "
                  "show their patterns. T1-R: the App ran pdftotext with layout itself; our Poppler "
                  "version may differ from the App's."),
        "round1": {
            "app_visible_pattern": APP_VISIBLE_PATTERN,
            "app_reported_match_count": 1,
            "replayed_case_sensitive_matches": hits(APP_VISIBLE_PATTERN, pages),
            "absence_claim_audit": audit,
        },
        "t1r": {
            "app_count_equals_matching_lines": sum(c["app_count"] == c["matching_lines"] for c in counts),
            "app_count_equals_matches": sum(c["app_count"] == c["matches"] for c in counts),
            "searches_replayed": len(counts),
            "search_count_replay": counts,
            "absence_claim_audit": t1r_audit,
        },
    }))


if __name__ == "__main__":
    main()
