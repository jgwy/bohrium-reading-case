# Correct quotations, overbroad claims: a paper-reading case

**Release v1.3.**

**Reading problem.** A methods paper states *where its method applies* in a few scattered sentences. When an
AI assistant answers "does this paper support using the method on my data?", it can quote those sentences
exactly and still summarize the scope wrongly with words such as *only*, *never* or *nothing*. Checking that
every quote is on its page does not catch this, because "X never appears" is a claim about the whole paper.

**Case.** Real sessions in the Bohrium Science Space desktop App (玻尔·科学空间) on the 2019 sctransform paper:
1. **Round 1** (paper reader, 阅读助手): 13/13 selected quotes on their pages, yet two of its five absence/uniqueness
   statements were contradicted by the paper (a third is arguable). The App's working panel shows why: a lexical search that did not
   contain the term it later declared absent.
2. **Round 2**: a page-specific follow-up; the App revised both statements (assisted revision).
3. **T1-R probe** (new task, PDF attached): the same question plus a two-sentence rule "name your search terms
   before any absence claim". Measured with the **same two scripts**: every lexical absence claim now names its
   pattern and the replicate error did not recur, but **two "only/all" claims are still wrong** (2 of 6, against
   2 + 1 arguable of 5 in round 1): a regex that cannot match the suspended hyphen in "plate- and droplet-based",
   and an unread summary of search hits. The gain is that both errors are visible and checkable from the answer.

**What you can reuse.** A claim-scope audit workflow with prompt templates ([WORKFLOW.md](WORKFLOW.md)), two
scripts that check quote pages and absence claims against any PDF, and feature-level notes on how the App's
two reading routes ground answers ([Bohrium notes](#bohrium-science-space-feature-notes-and-feedback)).

Not claimed: a randomized benchmark, an official score, or a stable or causal effect of T1-R (n = 1, different
App route).

## How to read this repository

| Label | Meaning | Where it lives |
|---|---|---|
| **Paper** (p. N) | Wording from the publisher PDF, physical page | [materials/](materials/Hafemeister_Satija_2019_sctransform.pdf) |
| **App** | What the App displayed, wording unchanged | `app-*.md`, raw `*-ax.txt`, `t1r-test/*-excerpt.*` |
| **Our check** | Our source check, inference or judgement | [verification.md](verification.md), `*.tsv`, `*-check.json`, script outputs |

[M] = measured or observed in a file here; [I] = our inference. AX = the accessibility text of the actual App
window, exported during the session: what was on screen, not model telemetry.

| Step | Evidence |
|---|---|
| Paper | [Publisher PDF](materials/Hafemeister_Satija_2019_sctransform.pdf), 15 pages, CC BY 4.0 ([SOURCE.md](SOURCE.md)) |
| Round 1 | [prompt.txt](prompt.txt) -> [app-answer.md](app-answer.md) (raw: round-1 nodes of [app-followup-complete-ax.txt](app-followup-complete-ax.txt)); [export-provenance.json](export-provenance.json) |
| Round 1 working panel, mid-answer | [app-inprogress-ax.txt](app-inprogress-ax.txt); [inprogress-export-provenance.json](inprogress-export-provenance.json) |
| Source check | [source-answer-review.tsv](source-answer-review.tsv), [verification.md](verification.md), [quote-page-check.json](quote-page-check.json) |
| Round 2 | [followup-prompt.txt](followup-prompt.txt) -> [app-followup-answer.md](app-followup-answer.md); raw [app-followup-complete-ax.txt](app-followup-complete-ax.txt); [followup-export-provenance.json](followup-export-provenance.json) |
| Revision | [revision-comparison.tsv](revision-comparison.tsv), [followup-quote-page-check.json](followup-quote-page-check.json) |
| T1-R probe | [sent prompt](t1r-test/sent-prompt-single-line.txt), [pre-send field](t1r-test/before-send-excerpt.txt), [search steps](t1r-test/search-observations-excerpt.jsonl), [answer](t1r-test/final-answer-excerpt.txt), [quote spans](t1r-test/quote-page-check.json), [provenance](t1r-test/PROVENANCE.json), [interface events](t1r-test/INTERFACE_EVENT.md), [screenshot](t1r-test/workspace-result.jpg) |
| Re-runnable checks | [reproduce_quote_pages.py](reproduce_quote_pages.py) -> [output](reproduce-quote-pages-output.json); [replay_absence_search.py](replay_absence_search.py) -> [output](replay-absence-search-output.json) |

The Markdown answers remove UI wrappers and rejoin equation glyphs; wording and errors are kept. No answer was
overwritten.

## The question and why this method

**Constructed scenario** (no real patients): six tumour biopsies measured with 10x UMI counts plus a separate
Smart-seq2 TPM matrix. Does the paper support sctransform on both inputs; do six biopsies establish six
independent patients; can Pearson residuals be read as comparable expression levels across genes?

Each question is a scope decision whose evidence is spread over pp. 1–14. Design choices:

| Choice | Why | Cost / limit |
|---|---|---|
| Ask the App with the PDF open, "Use only this PDF" | The assistant reads the paper itself and cites pages, so every claim is tied to a location we can open. | We see only what the UI shows; model, tokens and cost are not visible. |
| Force a three-way split: paper states / follows from scenario / unknown | Keeps "the paper says UMI" apart from our inference "so TPM is out of scope" and from what nobody can know (biopsy-to-patient mapping). | Longer answers. |
| One short exact quote + page per claim | Makes a mechanical check possible. | Proves location only, not that the sentence around it is right. |
| Separate audit of absence / uniqueness words | They are claims about the whole paper; no single quote supports them. Only a whole-text search can test them, which is also why the full PDF is shipped. | Needs a synonym list written by a human. |
| Correct with a page-specific follow-up in the same session | Keeps the first answer as evidence; tests revision against page evidence. | Assisted revision, not self-correction. |
| Then change the first prompt (T1-R) and re-measure with the same scripts | Tests whether the error class can be prevented, not just repaired. | One run, different App route (below). |

## How the reading assistant grounded round 1 (observed)

A snapshot taken while the first answer was generating ([app-inprogress-ax.txt](app-inprogress-ax.txt),
02:25:48 UTC+8) shows the working panel [M]:

| AX node | What the App showed | What it tells a user |
|---|---|---|
| 23-27 | Step summaries: inspect the PDF structure, read the rest, run targeted searches, confirm with exact-case searches. | The assistant works in tool steps over the paper. |
| 28 | `查看 Hafemeister_Satija_2019_sctransform.jsonl` | It reads a parsed block file of the PDF; the answer says "197 blocks, pages 1–14". |
| 29 | `搜索内容 Smart\|TPM\|transcripts\|biops\|patient\|Donor\|donor\|full-length\|full length，共 1 处` | Searches are regular expressions; the panel shows pattern and count. |
| 31 | "Only one match: \"Healthy Donor\" ... No Smart-seq2, no TPM, no biopsy, no patient." | Absence statements come from this lexical search. |
| 32-77 | Draft notes: each quote with a block `resourceId` (`pdf-block-…`), line and page. | Citations are anchored to parsed blocks, consistent with 13/13 quotes on their pages [I]. |
| 99 | Draft: "doesn't address patient/sample independence or replication design". | "Replication" enters here; the visible pattern does not contain it. |
| 119-128 | "正在分析... 29.8s"; 请求批准, "上下文已使用 14%", 推理强度 (disabled while generating). | Context use is shown. |
| 143-146 | 全文翻译 off, **阅读助手 on**, 论文速览 off, 图表速览 off; page field "/ 15". | Only the reading assistant was used. |

After the answer finished, the panel collapsed behind "已处理（用时 1m 6s）". Earlier search steps (nodes 24, 26)
are summaries without patterns; they name Smart-seq2, TPM, non-UMI, biopsy and patient, not replicate or
read-level. Page 15 (references 22–39, publisher's note) was outside the parsed range [M].

## Results (round 1)

| Question | Paper | App | Our check |
|---|---|---|---|
| UMI and TPM inputs | "Our approach can be applied to any UMI-based scRNA-seq dataset" (p. 1); "We explicitly model the UMI counts…" (p. 11) | Supports the 10x UMI input, not the Smart-seq2 TPM input | Supported. TPM exclusion is an inference from the count-model input contract, not a TPM experiment. |
| Six biopsies = six patients? | No biopsy or patient text; main dataset is PBMCs from one healthy donor (p. 14) | No; the mapping is unknown | Supported as scenario reasoning. |
| Residuals comparable across genes? | "transformed onto a common scale" (p. 5); z = (x − μ)/σ (p. 11); PCA "centered and scaled" (p. 13) | Only as standardized deviations, not absolute expression | Supported. Keep the p. 9 caveat on depth independence; "peaks at 1" (p. 7) is a distribution, not a per-gene rule. |

13 round-1 and 4 round-2 quotes are on their stated pages [M]; this is a location check, not an accuracy percentage.

## Why two round-1 statements were overbroad

| | App wording | Paper | Our check |
|---|---|---|---|
| A2 | "Nothing about biopsies, patients, or replicate design — those terms do not occur." | "the data from each droplet represents a technical replicate of a bulk RNA sample" (p. 5) | `replicat` is absent from the visible pattern and present on p. 5. |
| A3 | "The only reference to non-UMI data is about a different tool … SCnorm" (p. 3) | "initial strategies focused on read-level (instead of UMI-level) data" (p. 2); "DESeq … for read count data" (p. 11) | True for the token "non-UMI" (p. 3 only), false for the concept. |

[replay_absence_search.py](replay_absence_search.py) replays the visible pattern on our extraction: exactly one
case-sensitive match, "Donor" on p. 14, consistent with "共 1 处" [M]. `biops`, `patient`, `Smart-seq`, `TPM` have
no match, so A1 holds.

Interpretation [I]: both errors are lexical-search results stated as whole-paper facts: A2 names a term no
visible search tested; A3 searched a token and not its synonyms. Neither is a quotation error, which is why the
quote check passed. **Tested repair** [M]: the page-specific follow-up ([followup-prompt.txt](followup-prompt.txt))
made the App revise both and add the p. 11 DESeq passage itself ([revision-comparison.tsv](revision-comparison.tsv)).
The counter-evidence came from our check, so this is repair, not prevention.

## Before and after T1-R, measured with the same checks

T1-R = the original prompt plus two sentences: *"Before writing that the paper never mentions something, or that
a passage is the only one about a topic, list the exact search terms and synonyms you searched, and report the
pages of every hit. If a term was not searched, do not make the absence claim."* It was sent once in a fresh task,
with no page hint ([sent text](t1r-test/sent-prompt-single-line.txt); the [pre-send field](t1r-test/before-send-excerpt.txt)
shows the complete rule). Both columns below come from the same two scripts and the same PDF.

Counting rule: every sentence that says something does not occur, is never done, or is the only/all of a
kind. Both answers were counted by the same rule; A4 is judged by reading, all others by the replay script.

| Measure | Round 1 (T1) | T1-R probe |
|---|---|---|
| Absence/uniqueness claims in the answer | 5 (A1–A5) | 6 (B1–B6) |
| ... whose lexical part is backed by a search pattern shown in the answer | 0 | 5 of 5 lexical claims (section "Search terms used (for the absence claims below)"); B5, about evaluation, cannot be backed by a pattern |
| ... contradicted by the PDF text | **2**, plus 1 arguable (A2 p. 5; A3 pp. 2, 11; A4) | **2** (B3, B6, below) |
| "Replicate design does not occur" | stated | not stated; "technical replicate" listed among the hits of its replicat search |
| Read-level / read-count wording reached without a hint | no | at page level: its pattern hit read-level (p. 2) and read count (p. 11; p. 15 is a reference); the answer does not quote them |
| Quotes on claimed page (`reproduce_quote_pages.py`) | 13/13 | 10/11: the miss quotes the abstract with a full stop where the paper's sentence continues ("dataset and is freely available…"); words otherwise verbatim |
| Pages read | parsed blocks, pp. 1–14 of 15 | all 15 (`pdftotext`, per-page files) |
| App count "共 N 处" vs our replay | 1 vs 1 match | 20 of 20 equal our **matching-line** count, 14 of 20 the match count; the 6 searches where lines and matches differ all follow lines |
| UI badge | 1m 6s | 2m 10s |

Round-1 claims not in the round-1 tables above: A4 "The only remotely relevant statement is an assumption about
heterogeneity (p. 10)" (arguable: p. 5 calls each droplet "a technical replicate", p. 9 discusses cell-type RNA
content); A5 "there is no empirical demonstration for full-length/non-UMI data" (holds).

**Remaining failure B3** [M]: the answer lists `full[- ]?length|plate[- ]?based|non[- ]?UMI|read[- ]?level|…`
→ "pages 2, 3, 11, 15 (5 hits; these are the only non-UMI / read-level / plate-based mentions)". The paper writes
"generated with both plate- and droplet-based protocols" (p. 2) and "including both plate- and droplet-based
protocols" (p. 8). `plate[- ]?based` matches neither (the hyphen is followed by " and"); the stem `plate` matches
both. The answer itself says the paper's plate-based datasets are UMI datasets (node 92), so the scientific
conclusion is unaffected [I]; the "only" wording is not.

**Remaining failure B6** [M]: for `comparable|…|across gene|between gene|…` the answer says "9 hits; all are
'across genes'/'between genes' in the sense of pooling information". The replay's contexts show otherwise for
p. 3 ("Relationship between gene variance and cell sequencing depth", Fig. 1) and p. 5 ("still exhibited
substantial variation across genes"). This is a summary of hits the model did not open, the same "all/only"
overreach in a new place. Its supporting point (the word "comparable" never occurs, B4) holds.

**Page lists** [M]: for two search groups the answer's page list omits p. 3 although the App's count includes
p. 3 lines (Fig. 1 caption: "each gene individually", "Relationship between gene variance"). The counts come from
the tool; page lists and "all are…" summaries are the model's restatement [I]. Check them against the panel.

**What this shows and what it does not.** The number of contradicted claims did not fall (2 + 1 arguable → 2).
What changed is their kind and visibility: round 1 declared absent a term it never searched (A2) and missed
synonyms (A3); T1-R searched the terms, and its two errors are a pattern too narrow for the wording (B3) and an
unread summary of hits (B6), both checkable from the answer alone by replaying the listed pattern. It does not show a causal effect: the probe ran in a different App route
(new task, attached PDF, `pdftotext`) from round 1 (paper reader, parsed blocks), once. The next rule, T1-R2 in
[WORKFLOW.md](WORKFLOW.md), asks for stems and "pattern → pages" wording instead of "only"; it is **untested**.

## Bohrium Science Space: feature notes and feedback

Two ways to ask the App about a paper, both used here [M unless marked]:

| | Paper reader + 阅读助手 (rounds 1–2) | 新任务 + PDF attachment (T1-R) |
|---|---|---|
| Start | 文献阅读 → 本地导入 → open paper → switch on 阅读助手 | 新任务 → attach the PDF in the input box (chip "PDF·5.13MB") → type → 发送; the bar showed 选择运行位置：本地 and 请求批准 |
| What the model reads | Parsed block file `<paper>.jsonl`; "197 blocks, pages 1–14" | Its own tool steps: page count → "Extract PDF text with layout" → "Split … into per-page files"; all 15 pages |
| Citation anchor | `pdf-block-…` resource IDs and pages (draft notes) | File + page ("the article footer reads Page N of 15") |
| Search | Regex; panel shows pattern and "共 N 处" | Same; 20 patterns visible |
| Panel after completion | Collapsed behind "已处理（用时 1m 6s）" | Collapsed behind "已处理（用时 2m 10s）", AX exposes Expand |
| Quote check | 13/13 on page | 10/11 (one added full stop) |
| Context meter | 14% mid-answer (round 2 end: 16%) | 16% at the end |

Tips that follow from the evidence:
1. **Read the working panel, and know what the number means.** "共 N 处" equalled the number of matching *lines*
   of layout-extracted text in all 20 T1-R searches, including all 6 where lines and occurrences differ. With
   layout extraction one line can hold both columns.
2. **Choose the route for the question.** The reader route anchors quotes to parsed blocks but its parsed file
   stopped at p. 14 here; the task route read every page and lists every search, but its answers cite file pages.
3. **Ask for search terms before absence claims** (T1-R) and **for stems, with "pattern → pages" wording**
   (T1-R2, untested). Then replay the patterns with `replay_absence_search.py`.
4. **Enter the prompt as one line and check the field before 发送**: in our first attempt a multi-line entry
   produced an answer before an explicit send click, and the rule's delivery could not be confirmed
   ([interface events](t1r-test/INTERFACE_EVENT.md); that raw export is not shipped, so this is our report).
5. **Export before you follow up.** AX exports clip long nodes near 512 characters (T1-R nodes 90, 91, 111, 113);
   keep the panel and answer of each round separately.

Feedback for the product team [I, each tied to an observation above]: show the parsed page range next to the
PDF page count in the reader; label search counts as lines or report occurrences and pages; offer a visible
"new conversation" in the reader's 阅读助手 (none found in the menus we inspected, which forced the route change);
make Enter/Send behaviour for multi-line input explicit; keep expanded search patterns available after an answer
completes.

## Reusable workflow

[WORKFLOW.md](WORKFLOW.md): an eight-step claim-scope audit with templates T1 (used), T1-R (probed once),
T1-R2 (untested) and T2 (used), and how to point both scripts at another paper. In short: ask with a three-way
split and page quotes → check quote pages → list every absence/uniqueness claim with terms, synonyms and stems →
search and open each hit → follow up with page evidence → keep a revision table → re-check new quotes.

Works for claims in the extractable main text of the supplied PDF. Fails for figures, equations and tables as
images, unsupplied supplements, and concepts expressed without any listed word or stem.

## Repeat the App sessions

Environment: Bohrium Science Space desktop App (bundle `com.bohrium.scix`), macOS 27.0, Apple silicon. The installed
App's bundle metadata read 0.10.14 with a modification time before the sessions (checked locally, not shipped),
so they most likely ran 0.10.14 [I]; an update prompt to 0.10.15 was dismissed before T1-R ([PLAN](t1r-test/PLAN.md);
the plan's "new conversation on the same imported PDF" could not be followed, see INTERFACE_EVENT.md). The UI showed no model, version or token count.

Route A, rounds 1–2:
1. 文献阅读 → 本地导入 → select the included PDF; open it (viewer shows "/ 15").
2. Switch on **阅读助手**; leave 论文速览, 图表速览, 全文翻译 off.
3. Send [prompt.txt](prompt.txt) unchanged. Expand the working panel while it runs; export or copy the answer.
4. Run the checks below; open pp. 2, 5 and 11.
5. Send [followup-prompt.txt](followup-prompt.txt); save the second answer separately.

Route B, T1-R:
1. 新任务 → attach the same PDF to the input box (the bar offers 添加内容; we did not record which control attached it, and its file picker needed keyboard input) and confirm the attachment chip.
2. Paste [t1r-test/sent-prompt-single-line.txt](t1r-test/sent-prompt-single-line.txt) as one line; check the field; 发送.
3. After completion expand "已处理", copy each `搜索内容 … 共 N 处` line and the answer.
4. Write the answer's quotes into a spans file like [t1r-test/quote-page-check.json](t1r-test/quote-page-check.json),
   its search lines into a JSONL like [the excerpt](t1r-test/search-observations-excerpt.jsonl), and run both scripts.

Screenshots (unedited, no account name visible): [02](02-reading-request.jpg) the request and the round-1 answer
with the 1m 6s badge; [03](03-method-page.jpg) Methods p. 11 beside the session; [04](04-followup.jpg) the round-2
answer beside p. 5; [t1r-test/workspace-result.jpg](t1r-test/workspace-result.jpg) the T1-R result in the PDF workbench.

![Round-2 answer beside page 5 of the paper](04-followup.jpg)

**What counts as the same result.** Wording will differ. Treat a repeat as matching if (a) the three conclusions
match the Results table, (b) every checked quote is on its page, and (c) you record which absence/uniqueness
claims the replay contradicts. A run without such errors is a data point, not a failure.

## Repeat the source checks

Python 3.10+ (we ran 3.12.2) and Poppler `pdftotext` (26.08.0) on PATH; no other packages, network or model.

```sh
python3 reproduce_quote_pages.py > my-quote-check.json
python3 replay_absence_search.py  > my-absence-check.json
```

Expected, as in the shipped outputs (2026-10-31; T1-R part added in v1.3): line 1 of the quote check contains
`"on_claimed_page": {"quote-page-check.json": "13/13", "followup-quote-page-check.json": "4/4", "t1r-test/quote-page-check.json": "10/11"}`;
the replay contains `"app_count_equals_matching_lines": 20`, `"app_count_equals_matches": 14`, one round-1
match (p. 14), A2 `replicat` → `[5]`, and B3 `plate[- ]?based` → `[]` but `plate` → `[2, 8]`. Another Poppler
version may change whitespace or line breaks and so the line counts; page numbers should not change. Matching
joins line-end hyphens and drops whitespace, so it validates location only.

## Measured facts and unknowns

- Badges: 1m 6s (round 1), 33s (round 2), 2m 10s (T1-R) [M]. Their scope is undefined (the mid-answer snapshot
  already showed 1m 7s); they are not summed and exclude our checking time.
- Model, version, token use and cost: **unavailable**, not zero. The full PDF is shipped because absence claims
  can only be audited against the whole text; it is CC BY 4.0 and counts 63,908 bytes of the text budget
  ([TEXT_BUDGET.json](TEXT_BUDGET.json)).
- Not claimed: a controlled baseline, comparison with other tools, scientific reproduction, expert approval,
  generality beyond this paper, or a stable or causal T1-R effect.

## Sources and contribution

Paper: Hafemeister C, Satija R. *Normalization and variance stabilization of single-cell RNA-seq data using
regularized negative binomial regression*. Genome Biology 20, 296 (2019), DOI
[10.1186/s13059-019-1874-1](https://doi.org/10.1186/s13059-019-1874-1); © The Author(s) 2019, CC BY 4.0, included
unchanged ([SOURCE.md](SOURCE.md)).

Our work: the scenario and prompts, all App sessions and exports, quote and absence checks, the root-cause
analysis from the working panels, the before/after measurement, the workflow and templates, both scripts and
the App feature notes. App answers and panel text are the App's output, attributed as such.

## Changes in v1.3

- New: before/after table for T1-R measured with the same scripts and one counting rule; the two residual
  failures (suspended hyphen; unread "all are…" summary) and the page-list caution; the "共 N 处 = matching lines" replay of all 20 T1-R searches; Bohrium route comparison,
  tips and product feedback; Route B reproduction steps; expected script outputs; T1-R2 (untested) in WORKFLOW.md.
- Scripts: `replay_absence_search.py` adds the T1-R part (reads the shipped search excerpt);
  `reproduce_quote_pages.py` adds [t1r-test/quote-page-check.json](t1r-test/quote-page-check.json) and a summary
  line. Outputs regenerated; round-1 and round-2 results unchanged.
- Evidence: input-bar nodes added verbatim to the two T1-R excerpts (run location, approval mode, context meter).
- Removed to keep the text budget: the separate round-1 AX export (its answer nodes are identical inside
  `app-followup-complete-ax.txt`; only its end-of-round input bar, incl. "上下文已使用 14%", is lost; quote nodes
  renumbered, see [quote-page-check.json](quote-page-check.json)),
  the excluded first T1-R entry excerpt (an interface fault, still described in INTERFACE_EVENT.md), and the CC
  legal code (LICENSE now names the license and links it; license unchanged).

v1.2 added the T1-R probe. v1.1 added the design rationale, working-panel analysis, the replay script, WORKFLOW.md
and expected outputs. [提交说明.md](提交说明.md) is the competition submission note.

## License

Text, prompts, check records and scripts written for this case: CC BY-NC-ND 4.0 ([LICENSE](LICENSE)). The paper
PDF keeps CC BY 4.0 ([SOURCE.md](SOURCE.md)). App output and screenshots are reproduced as observations of the
Bohrium Science Space App; no ownership of the product interface is claimed.
