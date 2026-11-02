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

Why: round 1 claimed replicate design does not occur although its visible search lacked "replicat" (p. 5
contradicts it), and its non-UMI uniqueness claim held for the token, not its synonyms.

Observed once (README section 6, "Repair and prevention"): every lexical absence claim named its pattern and the
replicate-absence statement did not recur, but contradicted claims did not fall (2 of 6 against 2 of 5 plus 1
arguable): both remaining errors are "only/all" summaries (B3, B6). One run in a different App route: not a
matched or causal comparison.

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

Filled T1-R input: t1r-test/sent-prompt-single-line.txt (prompt.txt plus the two T1-R sentences, whitespace
normalized only; the pre-send field was captured).

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

## Scripts and limits

The scripts take your own PDF, quotes and claims as data files (`--pdf`, `--spans`, `--claims`, `--searches`);
commands, file formats and expected values are in README section 7, "Reproduce this case, then apply it to your
paper". Both need Poppler `pdftotext` and Python 3.10+; neither calls a model or the network.

The workflow checks claims in the extractable main text of the supplied PDF, not figures, equations or tables as
images, supplements or cited papers. Step 5 cannot find a concept expressed without any listed word or stem, the
same failure it is meant to catch in the App. One paper and one case: no claim that the App or this workflow
behaves the same way on other papers.
