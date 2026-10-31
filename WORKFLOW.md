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
| 5 | For each such claim, list the literal terms, **the synonyms** a reader would accept (e.g. non-UMI -> read-level, read count; replicate design -> replicate, technical replicate) **and their bare stems** (`replicat`, `plate`, `read`), because compounds are written in forms a pattern misses ("plate- and droplet-based" defeats `plate[- ]?based`). Search the PDF for all of them and open each hit. | claims file + search table with page hits (`replay_absence_search.py --claims`); decision rule: absence claim fails on any hit, uniqueness claim on a hit outside its named pages, "all are" claim needs every hit read | used (the original check searched the extracted text; the script was added in v1.1, the claims-file option in v1.4) |
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
absence/uniqueness statements (README section 5, "Where scope errors enter").

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

Observed once (README section 6, "Repair and prevention"): every lexical absence claim named its pattern, the
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

Test protocol, written before any run (Route B, so it is matched to the T1-R probe, unlike round 1):
1. 新任务 → attach materials/Hafemeister_Satija_2019_sctransform.pdf; confirm the chip "PDF·5.13MB". Record the
   App version shown in its About panel.
2. Paste t1r-test/sent-prompt-single-line.txt followed by the two T1-R2 sentences, as one line; export the input
   field before 发送.
3. After completion expand "已处理"; copy every `搜索内容 … 共 N 处` line and the answer; one screenshot without
   the account name.
4. Put the search lines into a JSONL like t1r-test/search-observations-excerpt.jsonl and every absence,
   uniqueness and "all are" claim into a claims file like claims-example.json (terms written before searching).
5. `python3 replay_absence_search.py --claims t1r2-claims.json --searches t1r2-searches.jsonl` and
   `python3 reproduce_quote_pages.py --spans t1r2-spans.json`.
6. Report as measured, whatever the direction: contradicted claims (T1-R: 2 of 6), page lists that disagree with
   the replayed pages (T1-R: 2), quotes on page (T1-R: 10/11). One run is one data point.

Filled T1-R input (not T1-R2): t1r-test/sent-prompt-single-line.txt. It is prompt.txt plus the two T1-R sentences, with whitespace normalized only. The complete pre-send field was captured. An earlier multiline-entry event has unverified rule delivery and is excluded (t1r-test/INTERFACE_EVENT.md).

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

## Adapting the scripts to another paper (no code edits)

- `reproduce_quote_pages.py --pdf your.pdf --spans your-spans.json`: the spans file has the format of
  `quote-page-check.json` (`spans`: `ax_node` = any locator, `quote`, `claimed_pdf_page`).
- `replay_absence_search.py --pdf your.pdf --claims your-claims.json`: a JSON list of
  `{"id", "answer_wording", "terms": [case-insensitive regexes], "all_contexts": true|absent}`, as in
  `claims-example.json` (its output: `claims-example-output.json`). Output field `claims_with_hits` lists the
  claims to read.
- Add `--searches your-search-lines.jsonl` to replay a Route B panel: one JSON object per line,
  `{"new_scientific_ui_nodes": [{"node": N, "visible": "搜索内容 PATTERN，共 N 处"}]}` as in
  `t1r-test/search-observations-excerpt.jsonl`; each count is compared with matching lines and matches in
  `pdftotext -layout` text.
- Without options both scripts reproduce this case. Both need Poppler `pdftotext` and Python 3.10+; neither
  calls a model or the network.

## Where it works and where it does not

- Works for claims stated in the extractable main text of the supplied PDF.
- Does not check figures, equations or tables as images; text extraction joins or drops glyphs there.
- Says nothing about supplements, cited papers or later versions that were not supplied.
- A synonym list is only as good as the reader who writes it: step 5 cannot find a concept that is
  expressed without any of the listed words. That is the same failure mode it is meant to catch in the App.
- One paper, one original revision and one later development probe: no claim that the App, or this workflow, behaves the same way on
  other papers. T1-R2 has not been run.
