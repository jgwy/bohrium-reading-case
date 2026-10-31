# Claim-scope audit: a reusable workflow for AI paper-reading answers

This is the procedure used in this case, written so it can be applied to another paper and another
applicability question. Status labels: **used** = exercised once in this case with the recorded outputs;
**probed once** = exercised in a later development task with a different App entry/extraction route; no stable benefit is implied; **untested** = proposed from the evidence, never run.

## When to use it

Use it when the reading question is a *scope decision*: "does the paper support applying the method to my
input?", "does this count establish independent samples?", "what unit does this quantity have?". These
answers usually quote correctly and then summarize the scope in words such as *only*, *never*, *nothing*,
*any*. The quotes can be checked mechanically; the summary words cannot.

## Checklist

| Step | Action | Output to keep | Status |
|---|---|---|---|
| 1 | Write a constructed or real scenario and 2-4 scope questions. Do not include private data. | prompt text | used |
| 2 | Ask with template T1 (below): split *paper states / follows from scenario / unknown*, page + short exact quote. | complete visible answer, exported before any follow-up | used |
| 3 | Check every quoted span against the claimed PDF page (`reproduce_quote_pages.py` method: NFKC, join line-end hyphens, drop whitespace, search each page). | quote/page table | used |
| 4 | Mark every sentence that makes an **absence claim** ("X does not occur") or **uniqueness claim** ("the only Y is Z"). Each one is a claim about the whole source, not about the quote next to it. | list of claims with their terms | used |
| 5 | For each such claim, list the literal terms, **the synonyms** a reader would accept (e.g. non-UMI -> read-level, read count; replicate design -> replicate, technical replicate) **and their bare stems** (`replicat`, `plate`, `read`), because compounds are written in forms a pattern misses ("plate- and droplet-based" defeats `plate[- ]?based`). Search the PDF for all of them and open each hit. | search table with page hits (`replay_absence_search.py`) | used (the original check searched the extracted text; the script was added in v1.1) |
| 6 | Send template T2 with the page-specific counter-passages. Ask the assistant to quote its earlier wording and state the revision. | second answer, exported separately | used |
| 7 | Fill a revision table: initial wording / feedback given / actual revision / independent check. Re-run step 3 on the new quotes. | revision-comparison.tsv, follow-up quote check | used |
| 8 | Keep the answer's main conclusions only where the checks support them, and keep the qualifications that the answer dropped (here: p. 9 caveat on depth independence; "peaks at 1" is a distribution, not a per-gene rule). | review table | used |

Time actually observed in this case: the App badges showed 1m 6s and 33s for the two answers. Steps 3-8 took
longer than that; they were not timed, so no total is claimed.

## Prompt templates

### T1 — first-round, source-grounded scope question (used once, as prompt.txt)

```text
Use only this PDF for a source-grounded reading check. {Constructed|Real} scenario: {SCENARIO}.
{QUESTION 1}? {QUESTION 2}? {QUESTION 3}?
For each answer, distinguish what the paper states, what follows from the scenario, and what remains unknown.
Give the original page/section and one short exact quotation where possible.
Do not run data analysis, install software, launch compute, or read unrelated local files.
```

Observed effect in this case: the App kept the three-way split for all three questions and gave a page and
section for every quote; 13/13 selected quotes matched their pages. It still produced two overbroad
absence/uniqueness statements (see README, "Why the two statements were overbroad").

### T1-R — T1 plus an absence-claim rule (probed once)

Append to T1:

```text
Before writing that the paper never mentions something, or that a passage is the only one about a topic,
list the exact search terms and synonyms you searched, and report the pages of every hit.
If a term was not searched, do not make the absence claim.
```

Why: in round 1 the visible App search did not contain "replicat", yet the answer claimed replicate design
does not occur (p. 5 contradicts it); the uniqueness claim about non-UMI data was true for the token "non-UMI"
and false for its synonyms. The rule targets both mechanisms.

Observed once (README, "Before and after T1-R"): every lexical absence claim named its pattern, the
replicate-absence statement did not recur, and the read-level and read-count wording was reached at page level.
Contradicted claims did not fall (round 1: 2 of 5 plus 1 arguable; T1-R: 2 of 6), but both remaining errors are
"only/all" summaries: the hits of `plate[- ]?based|…` were called "the only … plate-based mentions", although
pp. 2 and 8 say "plate- and droplet-based", and nine "across/between gene" hits were all called pooling-related,
which pp. 3 and 5 contradict.
The probe used a PDF attachment and pdftotext rather than the reader's parsed blocks, once: not a matched or
causal comparison. Some final AX nodes are clipped (t1r-test/PROVENANCE.json).

### T1-R2 — T1-R plus stems and bounded wording (untested)

Append to T1-R:

```text
Search word stems as well as phrases (for example "plate", not only "plate-based"), and report each result as
"pattern -> pages". Do not call any set of hits "the only" mentions; say which patterns found them.
```

Why: it targets both failures T1-R left (B3, B6) and the page-list restatement error seen in the same answer.
How to test it: Route B in README with this prompt, then run both scripts; success means no claim in the
replay's audit is contradicted and every page list matches the panel.

Filled input: t1r-test/sent-prompt-single-line.txt. It is prompt.txt plus the two sentences above, with whitespace normalized only. The complete pre-send field was captured. An earlier multiline-entry event has unverified rule delivery and is excluded (t1r-test/INTERFACE_EVENT.md).

### T2 — page-specific scope follow-up (used once, as followup-prompt.txt)

```text
Please recheck {N} scope statements in your answer against this PDF.
Page {P1} discusses "{TERM OR PASSAGE 1}"; clarify {WHAT IT IS DISTINCT FROM}, rather than saying {OVERBROAD WORDING 1}.
Page {P2} also discusses {TOPIC 2}, so clarify whether {CLAIMED UNIQUE ITEM} is really the only relevant discussion of {TOPIC 2}.
Keep the {K} main conclusions only where supported, give exact page/section evidence,
and explicitly identify any wording you revise. Do not use outside sources or run data analysis.
```

Observed effect: the App quoted both earlier sentences, revised both, added a third read-level passage
(p. 11 DESeq) that the feedback had not named, and kept the three conclusions. All four new quotes matched
their pages. This is assisted revision: the counter-evidence came from step 5.

## Adapting the scripts to another paper

- `reproduce_quote_pages.py --pdf your.pdf` reads the `spans` lists of `quote-page-check.json` and
  `followup-quote-page-check.json` (fields `ax_node`, `quote`, `claimed_pdf_page`). Write your own spans in
  that format.
- `reproduce_quote_pages.py` also reads `t1r-test/quote-page-check.json`; edit `RECORDS` to add your own spans files.
- `replay_absence_search.py --pdf your.pdf --searches your-search-lines.jsonl`: edit `APP_VISIBLE_PATTERN` and
  `CLAIMS` (round 1) or `T1R_CLAIMS` (one entry per absence/uniqueness claim, with regex terms including stems).
  The JSONL holds the panel's `搜索内容 PATTERN，共 N 处` lines in the format of
  `t1r-test/search-observations-excerpt.jsonl`; the script compares each count with matching lines and matches
  in `pdftotext -layout` text.
- Both need Poppler `pdftotext` and Python 3.10+; neither calls a model or the network.

## Where it works and where it does not

- Works for claims stated in the extractable main text of the supplied PDF.
- Does not check figures, equations or tables as images; text extraction joins or drops glyphs there.
- Says nothing about supplements, cited papers or later versions that were not supplied.
- A synonym list is only as good as the reader who writes it: step 5 cannot find a concept that is
  expressed without any of the listed words. That is the same failure mode it is meant to catch in the App.
- One paper, one original revision and one later development probe: no claim that the App, or this workflow, behaves the same way on
  other papers. T1-R2 has not been run.
