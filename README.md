# Correct quotations, overbroad claims: auditing what an AI reader says a paper does *not* contain

**Release v1.4.**

| | |
|---|---|
| **Problem** | Asked "does this paper support using the method on my data?", an AI reading assistant quoted the paper exactly and on the right pages, yet stated the paper's scope with *only*, *never*, *nothing*, and two of those statements were false. A quote check cannot catch this: a quote is local evidence, while "X never appears" is a claim about the whole paper. |
| **Method** | **Claim-scope audit.** Ask for a three-way split (paper states / follows from scenario / unknown) with page + exact quote → check every quote on its page → list every absence, uniqueness or "all are" claim → search the full PDF for its terms, synonyms and word stems and open each hit → feed page evidence back → re-measure with the same scripts. |
| **Case** | Bohrium Science Space desktop App (玻尔·科学空间); Hafemeister & Satija 2019, the sctransform paper (Genome Biology, CC BY 4.0, full PDF included); a constructed tumour-biopsy scenario; three real sessions. |
| **Result** | Round 1: 13/13 quotes on their pages, but 2 of 5 absence/uniqueness claims contradicted by the paper (1 more arguable). The App's working panel shows why: its regex search did not contain the term it then declared absent. Round 2: with page evidence the App revised both. T1-R (prompt asks for search terms before any absence claim): still 2 of 6 wrong, but every lexical claim now names its search pattern, so both errors can be checked without access to the App. |
| **Reuse** | [WORKFLOW.md](WORKFLOW.md) (8 steps, 4 prompt templates) and two scripts that take your PDF, your quotes and your claims as data files ([section 7](#7-apply-it-to-your-own-paper)). |
| **Bohrium value** | How the App's two reading routes read and cite a PDF, what its "共 N 处" search count means, five usage tips and five product suggestions, each tied to an observation ([section 8](#8-bohrium-science-space-routes-tips-and-feedback)). |

**Key numbers** (all [M], from files in this repository):

| | Round 1: reader + 阅读助手 | Round 2: page-specific follow-up | T1-R probe: new task + PDF |
|---|---|---|---|
| Quotes on the claimed page | 13/13 | 4/4 | 10/11 (one added full stop) |
| Absence/uniqueness claims contradicted by the paper | 2 of 5 (+1 arguable) | both revised | 2 of 6 |
| Lexical absence/uniqueness claims whose search pattern the answer shows | 0 | — | 5 of 5 |
| Pages the App read | parsed blocks, pp. 1–14 of 15 | same session | all 15 (`pdftotext`) |
| UI time badge | 1m 6s | 33s | 2m 10s |

Single real sessions, not a benchmark. T1-R ran once in a different App route, so the round-1 vs T1-R comparison
is descriptive, not causal. The App showed no model name, token count or cost. All limits: [section 10](#10-limits-and-unknowns).

## How to read this repository

| Label | Meaning | Where it lives |
|---|---|---|
| **Paper** (p. N) | Wording from the publisher PDF, physical page | [materials/](materials/Hafemeister_Satija_2019_sctransform.pdf) |
| **App** | What the App displayed, wording unchanged | `app-*.md`, raw `*-ax.txt`, `t1r-test/*-excerpt.*` |
| **Our check** | Our source check, inference or judgement | [verification.md](verification.md), `*.tsv`, `*-check.json`, script outputs |

[M] = measured or observed in a file here; [I] = our inference. **AX** = the accessibility text of the App
window, exported during the session (what was on screen, not model telemetry); "node N" is a line in that export.
**Absence claim**: "X does not occur". **Uniqueness claim**: "the only Y is Z" or "all hits are Z".
**Route A** = paper reader + 阅读助手 (rounds 1–2); **Route B** = 新任务 with the PDF attached (T1-R).
**T1, T1-R, T1-R2, T2** = prompt templates in [WORKFLOW.md](WORKFLOW.md).

| Step | Evidence |
|---|---|
| Paper | [Publisher PDF](materials/Hafemeister_Satija_2019_sctransform.pdf), 15 pages, CC BY 4.0 ([SOURCE.md](SOURCE.md)) |
| Round 1 | [prompt.txt](prompt.txt) → [app-answer.md](app-answer.md) (raw: nodes 18–58 of [app-followup-complete-ax.txt](app-followup-complete-ax.txt)); [export-provenance.json](export-provenance.json) |
| Round 1 working panel, mid-answer | [app-inprogress-ax.txt](app-inprogress-ax.txt); [inprogress-export-provenance.json](inprogress-export-provenance.json) |
| Source check | [source-answer-review.tsv](source-answer-review.tsv), [verification.md](verification.md), [quote-page-check.json](quote-page-check.json) |
| Round 2 | [followup-prompt.txt](followup-prompt.txt) → [app-followup-answer.md](app-followup-answer.md); raw [app-followup-complete-ax.txt](app-followup-complete-ax.txt); [followup-export-provenance.json](followup-export-provenance.json) |
| Revision | [revision-comparison.tsv](revision-comparison.tsv), [followup-quote-page-check.json](followup-quote-page-check.json) |
| T1-R probe | [sent prompt](t1r-test/sent-prompt-single-line.txt), [pre-send field](t1r-test/before-send-excerpt.txt), [search steps](t1r-test/search-observations-excerpt.jsonl), [answer](t1r-test/final-answer-excerpt.txt), [quote spans](t1r-test/quote-page-check.json), [provenance](t1r-test/PROVENANCE.json), [interface events](t1r-test/INTERFACE_EVENT.md), [screenshot](t1r-test/workspace-result.jpg) |
| Re-runnable checks | [reproduce_quote_pages.py](reproduce_quote_pages.py) → [output](reproduce-quote-pages-output.json); [replay_absence_search.py](replay_absence_search.py) → [output](replay-absence-search-output.json); [claims-example.json](claims-example.json) → [output](claims-example-output.json) |

The Markdown answers remove UI wrappers and rejoin equation glyphs; wording and errors are kept. No answer was
overwritten.

## 1. The reading question

**Constructed scenario** (no real patients): six tumour biopsies measured with 10x UMI counts plus a separate
Smart-seq2 TPM matrix. Does the paper support sctransform on both inputs? Do six biopsies establish six
independent patients? Can Pearson residuals be read as comparable expression levels across genes?

Each question is a scope decision whose evidence is spread over pp. 1–14: the input contract (pp. 1, 8, 11), the
datasets (pp. 2, 14), the residual definition and its caveats (pp. 5, 7, 9, 11, 13). The hard part is not finding
a supporting sentence; it is knowing that no other sentence changes the answer.

## 2. Method and design choices

| Choice | Why | Cost / limit |
|---|---|---|
| Ask the App with the PDF open, "Use only this PDF" | The assistant reads the paper itself and cites pages, so every claim is tied to a location we can open. | We see only what the UI shows; model, tokens and cost are not visible. |
| Force a three-way split: paper states / follows from scenario / unknown | Keeps "the paper says UMI" apart from our inference "so TPM is out of scope" and from what nobody can know (biopsy-to-patient mapping). | Longer answers. |
| One short exact quote + page per claim | Makes a mechanical check possible. | Proves location only, not that the sentence around it is right. |
| Separate audit of absence / uniqueness words | They are claims about the whole paper; no single quote supports them. Only a whole-text search can test them, which is also why the full PDF is shipped. | Needs a synonym and stem list written by a human. |
| Correct with a page-specific follow-up in the same session | Keeps the first answer as evidence; tests revision against page evidence. | Assisted revision, not self-correction. |
| Then change the first prompt (T1-R) and re-measure with the same scripts | Tests whether the error class can be prevented, not just repaired. | One run, different App route. |

## 3. How the App built the round-1 answer (observed)

A snapshot taken while the first answer was generating ([app-inprogress-ax.txt](app-inprogress-ax.txt),
02:25:48 UTC+8) shows the working panel [M]:

| AX node | What the App showed | What it tells a user |
|---|---|---|
| 23–27 | Step summaries: inspect the PDF structure, read the rest, run targeted searches, "confirm with exact-case searches that the paper never mentions Smart-seq2, TPM, biopsies, or patients". | The assistant works in tool steps over the paper. |
| 28 | `查看 Hafemeister_Satija_2019_sctransform.jsonl` | It reads a parsed block file of the PDF; the answer says "197 blocks, pages 1–14". |
| 29 | `搜索内容 Smart\|TPM\|transcripts\|biops\|patient\|Donor\|donor\|full-length\|full length，共 1 处` | Searches are regular expressions; the panel shows pattern and count. |
| 31 | "Only one match: \"Healthy Donor\" ... No Smart-seq2, no TPM, no biopsy, no patient." | Absence statements come from this lexical search. |
| 32–33 | "The instruction says: \"Cite parsed PDF evidence as ⟦source:RESOURCE_ID⟧ using the exact non-empty resourceId from a supporting block you read.\"" | Every citation must point to a block the model read. |
| 34–77 | Draft notes listing the quotes, most with a block `resourceId` (`pdf-block-…`), line and page. | Quotes are copied from anchored blocks. |
| 99 | Draft: "doesn't address patient/sample independence or replication design". | "Replication" enters here; the visible pattern does not contain it. |
| 119–128 | "正在分析... 29.8s"; 请求批准, "上下文已使用 14%", 推理强度 (disabled while generating). | Context use is shown. |
| 133, 143–146 | Page field "/ 15"; 全文翻译 off, **阅读助手 on**, 论文速览 off, 图表速览 off. | Only the reading assistant was used. |

After the answer finished, the panel collapsed behind "已处理（用时 1m 6s）". The earlier search steps (nodes 24,
26) are summaries without patterns; they name Smart-seq2, TPM, non-UMI, biopsy and patient, not replicate or
read-level. By the App's own statement ("197 blocks, pages 1–14", node 23 of app-followup-complete-ax.txt), page 15
(references 22–39, publisher's note) was outside the parsed range.

**The mechanism in one sentence** [I, from nodes 28–34]: a quote must cite a block the model read, so quotes
are anchored and land on the right page; an absence or uniqueness sentence has no block to cite, so it rests on
whatever search the model chose to run, and nothing in the answer shows that search. We saw the instruction
only as the model restated it in the panel, not the App's system prompt itself.

## 4. Round-1 results

| Question | Paper | App | Our check |
|---|---|---|---|
| UMI and TPM inputs | "Our approach can be applied to any UMI-based scRNA-seq dataset" (p. 1); "We explicitly model the UMI counts…" (p. 11) | Supports the 10x UMI input, not the Smart-seq2 TPM input | Supported. TPM exclusion is an inference from the count-model input contract, not a TPM experiment. |
| Six biopsies = six patients? | No biopsy or patient text; main dataset is PBMCs from one healthy donor (p. 14) | No; the mapping is unknown | Supported as scenario reasoning. |
| Residuals comparable across genes? | "transformed onto a common scale" (p. 5); z = (x − μ)/σ (p. 11); PCA "centered and scaled" (p. 13) | Only as standardized deviations, not absolute expression | Supported. Keep the p. 9 caveat on depth independence; "peaks at 1" (p. 7) is a distribution, not a per-gene rule. |

The three conclusions hold; the errors sit in the scope sentences around them (section 5).

## 5. Where scope errors enter: four mechanisms

We counted every sentence that says a term or topic does not occur in the paper, or that a passage or set of
hits is the only/all of a kind: 5 in round 1 (A1–A5), 6 in T1-R (B1–B6). Statements that the paper is *silent
on a question* (e.g. "The paper is silent on whether TPM … could be coerced into the model") were not counted.
The counting is our judgement, applied the same way to both answers. Contradicted ones [M; wording from the
App, pages from the PDF]:

| Claim | App wording | Paper | Mechanism | Exposed by | Prevention |
|---|---|---|---|---|---|
| A2 (round 1) | "Nothing about biopsies, patients, or replicate design — those terms do not occur." | "the data from each droplet represents a technical replicate of a bulk RNA sample" (p. 5) | **Term never searched**: the visible pattern lacks `replicat` | stem `replicat` → p. 5 | T1-R: name search terms first. Did not recur. |
| A3 (round 1) | "The only reference to non-UMI data is about a different tool … SCnorm" (p. 3) | "read-level (instead of UMI-level) data" (p. 2); "DESeq … for read count data" (p. 11); voom reference (p. 15) | **Token searched, synonyms not**: true for "non-UMI", false for the concept | synonyms `read-level`, `read count` → pp. 2, 11, 15 | T1-R: synonyms. Reached at page level. |
| B3 (T1-R) | "hits on pages 2, 3, 11, 15 (5 hits; these are the only non-UMI / read-level / plate-based mentions)" | "generated with both plate- and droplet-based protocols" (p. 2); "including both plate- and droplet-based protocols" (p. 8) | **Pattern narrower than the wording**: `plate[- ]?based` cannot match a suspended hyphen | stem `plate` → pp. 2, 8 | T1-R2: search stems (untested) |
| B6 (T1-R) | "9 hits; all are 'across genes'/'between genes' in the sense of pooling information" | "Relationship between gene variance and cell sequencing depth" (p. 3, Fig. 1); "substantial variation across genes" (p. 5) | **Hits summarized, not opened** | read every hit context (the script prints all 9) | T1-R2: "pattern → pages", no "all/only" (untested) |

A4 "The only remotely relevant statement is an assumption about heterogeneity" (p. 10 cited) is arguable (p. 5
technical replicate; p. 9 cell-type RNA content) and judged by reading. Two T1-R page lists also omit p. 3,
although replaying their patterns shows p. 3 lines inside the App's own counts: counts come from the tool, page lists and "all are…" summaries
are the model's restatement [I]. In B3 the answer itself says the paper's plate-based datasets are UMI datasets,
so its scientific conclusion is unaffected; the "only" wording is not.

**Common cause** [I]: none is a quotation error, which is why the quote check passed. All four are search
results stated as whole-paper facts: the search was missing (A2), too literal (A3), too narrow for the
typography (B3) or not read (B6).

### Does the audit separate wrong claims from right ones?

The audit's decision rule: an **absence** claim fails if any listed term hits; a **uniqueness** claim fails if a
term hits a page the claim did not name; an **"all are"** claim requires reading every hit. Applied to all 11
claims of round 1 and T1-R with the shipped replay ([replay-absence-search-output.json](replay-absence-search-output.json)) [M]:

| Group | Claims | Audit result |
|---|---|---|
| Contradicted by the paper | A2, A3, B3, B6 | 4 of 4 flagged: hits on p. 5; pp. 2, 11, 15; p. 8; contexts on pp. 3, 5 |
| Hold, lexical absence | A1, B1, B2, B4 | 0 of 4 flagged: no listed term hits |
| Hold, claims about evaluation | A5, B5 | 2 of 2 flagged once their own words are listed: non-UMI (p. 3), read-level (p. 2), read count (pp. 11, 15) hit; reading clears them (other methods: SCnorm, earlier read-level models, DESeq, voom; no sctransform evaluation). The shipped replay lists only full-length, Smart-seq and TPM for these two, so it does not show this flag. |
| Arguable | A4 | not scriptable; judged by reading |

This is not a blind detection rate: we wrote the synonyms and stems after reading the paper. It shows that the
rule, given a good term list, sends the reader to every wrong claim and to none of the four correct lexical
absence claims; the two claims about what the paper *evaluates* are flagged too and cost a reading to clear. Writing the term list *before*
searching is step 5 of the workflow and is the human part that can fail.

## 6. Repair and prevention

**Repair (round 2)** [M]: the page-specific follow-up ([followup-prompt.txt](followup-prompt.txt)) made the App
quote both earlier sentences, revise both, and add the p. 11 DESeq passage that the feedback had not named
([revision-comparison.tsv](revision-comparison.tsv)); the three conclusions stayed. The counter-evidence came
from our check, so this is assisted repair, not prevention.

**Prevention probe (T1-R)**: the original prompt plus *"Before writing that the paper never mentions something,
or that a passage is the only one about a topic, list the exact search terms and synonyms you searched, and
report the pages of every hit. If a term was not searched, do not make the absence claim."* Sent once in a fresh
task with no page hint ([sent text](t1r-test/sent-prompt-single-line.txt); the
[pre-send field](t1r-test/before-send-excerpt.txt) shows the complete rule). Same two scripts, same PDF:

| Measure | Round 1 (T1) | T1-R probe |
|---|---|---|
| Absence/uniqueness claims; contradicted | 5; 2 + 1 arguable | 6; 2 (B3, B6) |
| Lexical claims backed by a pattern shown in the answer | 0 | 5 of 5 (B5 is about evaluation, not lexical) |
| "Replicate design does not occur" | stated | not stated; "technical replicate" listed among its `replicat` hits |
| read-level / read-count reached without a hint | no | yes, at page level (pp. 2, 11); no quote of them in the visible, partly clipped text |
| App "共 N 处" vs our replay | 1 vs 1 | 20 of 20 equal matching **lines**; 14 of 20 equal matches |

**What this shows.** The count of wrong claims did not fall. Their kind changed: round 1 declared absent a term
it never searched; T1-R searched the terms and printed its patterns, so its errors can be found without access to
the App: B6 by reading the hits of its printed pattern, B3 by adding the stem `plate` to its printed pattern. It does not show a causal effect: one run, different route (new task,
attached PDF, `pdftotext`) from round 1 (paper reader, parsed blocks). The next rule, T1-R2 (stems, "pattern →
pages", no "only/all"), targets exactly B3 and B6 and is **untested**; its test protocol is written in
[WORKFLOW.md](WORKFLOW.md).

## 7. Apply it to your own paper

Needs Python 3.10+ and Poppler `pdftotext`; no model, network or extra package. Steps 2–4 are what we did here.

1. **Check the PDF is text.** `pdftotext your.pdf - | head` must print the paper; a scanned PDF needs OCR first.
2. **Ask** with template T1-R from [WORKFLOW.md](WORKFLOW.md) (your scenario, 2–4 scope questions). Export the
   answer before any follow-up.
3. **Check quote pages.** Copy each quote into `your-spans.json` in the format of
   [quote-page-check.json](quote-page-check.json) (`spans`: `ax_node` = any locator, `quote`, `claimed_pdf_page`).
   `python3 reproduce_quote_pages.py --pdf your.pdf --spans your-spans.json`.
   Expected: `claimed_page_contains_quote` true for each; a false means a wrong page or altered wording, so open the page.
4. **Audit scope claims.** Write every absence, uniqueness and "all are" sentence into `your-claims.json` with
   literal terms, synonyms and bare stems as case-insensitive regexes, *before* searching; add
   `"all_contexts": true` for "all are" claims. Format: [claims-example.json](claims-example.json) (A2, B3 and B4 of this case).
   `python3 replay_absence_search.py --pdf your.pdf --claims your-claims.json`.
   Read `claims_with_hits` with the decision rule of section 5. For the example, the shipped
   [claims-example-output.json](claims-example-output.json) gives `"claims_with_hits": ["A2", "B3"]`, `replicat` → `[5]`,
   `plate` → `[2, 8]`, `plate[- ]?based` → `[]`, `comparab` → `[]`.
5. **Optional, Bohrium Route B:** copy each `搜索内容 PATTERN，共 N 处` line into a JSONL like
   [the excerpt](t1r-test/search-observations-excerpt.jsonl) and add `--searches your-searches.jsonl`; each
   App count should equal `matching_lines`.
6. **Repair** with template T2, citing the pages found in step 4; keep a revision table like
   [revision-comparison.tsv](revision-comparison.tsv) and re-run step 3 on the new quotes.

Works for claims in the extractable main text of the supplied PDF. Does not check figures, equations or tables
as images, unsupplied supplements, or a concept expressed without any listed word or stem.

## 8. Bohrium Science Space: routes, tips and feedback

Two ways to ask the App about a paper, both used here [M]:

| | Route A: paper reader + 阅读助手 (rounds 1–2) | Route B: 新任务 + PDF attachment (T1-R) |
|---|---|---|
| Start | 文献阅读 → 本地导入 → open paper → switch on 阅读助手 | 新任务 → attach the PDF in the input box (chip "PDF·5.13MB") → type → 发送; the bar showed 选择运行位置：本地 and 请求批准 |
| What the model reads | Parsed block file `<paper>.jsonl`; "197 blocks, pages 1–14" | Its own tool steps: page count → "Extract PDF text with layout" → "Split … into per-page files"; all 15 pages |
| Citation anchor | `pdf-block-…` resource IDs and pages | File + page ("the article footer reads Page N of 15") |
| Search | Regex; panel shows pattern and "共 N 处" | Same; 20 patterns visible |
| After completion | Panel collapsed behind "已处理（用时 1m 6s）" | Collapsed behind "已处理（用时 2m 10s）", expandable |
| Quote check | 13/13 on page | 10/11 (one added full stop) |
| Context meter | 14% mid-answer (16% after round 2) | 16% at the end |

Tips that follow from the evidence:
1. **Read the working panel**: in our replay of all 20 T1-R searches, "共 N 处" equalled matching *lines*, not
   occurrences (6 searches tell the two apart; our Poppler may differ from the App's).
2. **Pick the route**: Route A anchors quotes to parsed blocks but parsed only pp. 1–14 here; Route B read all
   15 pages and lists every search, but cites file pages.
3. **Ask for search terms before absence claims** (T1-R), then replay them with `replay_absence_search.py`.
4. **Enter the prompt as one line and check the field before 发送** ([interface events](t1r-test/INTERFACE_EVENT.md)).
5. **Export each round before you follow up**; AX exports clip nodes near 512 characters (T1-R nodes 90, 91, 111, 113).

Product feedback [observation M, suggestion I]:

| Observation | Effect on a user | Suggestion |
|---|---|---|
| The reader parsed "197 blocks, pages 1–14"; the viewer shows "/ 15" | Whole-paper claims may rest on partial text without the user knowing | Show the parsed page range next to the page count |
| In our replay of 20 Route B searches, "共 N 处" = matching lines in all 20, including the 6 where occurrences differ | Users read it as occurrences | Label it as lines, or show occurrences and pages |
| No "new conversation" action found in the reader's 阅读助手 menus we inspected | A clean repeat had to move to Route B | Add a visible new-conversation action |
| Multi-line input once produced an answer before an explicit 发送 | Users cannot tell whether the full prompt was sent | Make Enter/Send behaviour explicit |
| Search patterns of earlier steps were shown only as summaries; the panel collapses after completion | Absence claims cannot be audited from the UI | Keep every executed pattern visible and exportable |

## 9. Reproduce this case

Environment: Bohrium Science Space desktop App (bundle `com.bohrium.scix`), macOS 27.0, Apple silicon. The
installed App's bundle metadata read 0.10.14 with a modification time before the sessions (checked locally,
not shipped), so they most likely ran 0.10.14 [I]; an update prompt to 0.10.15 was dismissed before T1-R
([PLAN](t1r-test/PLAN.md)). The UI showed no model, version or token count.

Route A, rounds 1–2:
1. 文献阅读 → 本地导入 → select the included PDF; open it (viewer shows "/ 15").
2. Switch on **阅读助手**; leave 论文速览, 图表速览, 全文翻译 off.
3. Send [prompt.txt](prompt.txt) unchanged. Expand the working panel while it runs; export or copy the answer.
4. Run the checks below; open pp. 2, 5 and 11.
5. Send [followup-prompt.txt](followup-prompt.txt); save the second answer separately.

Route B, T1-R (the plan's "new conversation on the same imported PDF" was not available, see
[INTERFACE_EVENT.md](t1r-test/INTERFACE_EVENT.md)):
1. 新任务 → attach the same PDF to the input box and confirm the chip "PDF·5.13MB" (the bar offers 添加内容; our
   file picker needed keyboard input and we did not record which control attached the file).
2. Paste [t1r-test/sent-prompt-single-line.txt](t1r-test/sent-prompt-single-line.txt) as one line; check the field; 发送.
3. After completion expand "已处理", copy each `搜索内容 … 共 N 处` line and the answer.
4. Record quotes and search lines as in section 7 and run both scripts.

Screenshots (unedited, no account name visible): [02](02-reading-request.jpg) the request and the round-1 answer
with the 1m 6s badge; [03](03-method-page.jpg) Methods p. 11 beside the session; [04](04-followup.jpg) the round-2
answer beside p. 5; [t1r-test/workspace-result.jpg](t1r-test/workspace-result.jpg) the T1-R result in the PDF workbench.

![Round-2 answer beside page 5 of the paper](04-followup.jpg)

**What counts as the same result.** Wording will differ. A repeat matches if (a) the three conclusions match
section 4, (b) every checked quote is on its page, and (c) you record which absence/uniqueness claims the replay
contradicts. A run without such errors is a data point, not a failure.

**Source checks** (Python 3.12.2 and Poppler 26.08.0 here):

```sh
python3 reproduce_quote_pages.py > my-quote-check.json
python3 replay_absence_search.py  > my-absence-check.json
python3 replay_absence_search.py --claims claims-example.json > my-claims-check.json
```

Expected (identical to the shipped outputs here): quote check
`"on_claimed_page": {"quote-page-check.json": "13/13", "followup-quote-page-check.json": "4/4", "t1r-test/quote-page-check.json": "10/11"}`;
replay `"app_count_equals_matching_lines": 20`, `"app_count_equals_matches": 14`, one round-1 match (p. 14),
A2 `replicat` → `[5]`, B3 `plate[- ]?based` → `[]` but `plate` → `[2, 8]`; the third command reproduces
[claims-example-output.json](claims-example-output.json). Another Poppler version may change line breaks and so
line counts, not pages. Matching joins line-end hyphens and drops whitespace, so it validates location only.

## 10. Limits and unknowns

- Badges: 1m 6s (round 1), 33s (round 2), 2m 10s (T1-R) [M]. Their scope is undefined (the mid-answer snapshot
  already showed 1m 7s); they are not summed and exclude our checking time, which was not timed.
- Model, version, token use and cost: **unavailable**, not zero.
- One paper, three sessions, one constructed scenario. Not claimed: a controlled baseline, comparison with other
  tools, scientific reproduction, expert approval, generality beyond this paper, or a stable or causal T1-R effect.
- The audit's 4 of 4 and 0 of 4 (section 5) use term lists written after reading the paper; the claim counts
  (5 and 6) rest on our reading of which sentences are absence/uniqueness claims.
- The full PDF is shipped because absence claims can only be audited against the whole text; it is CC BY 4.0 and
  counts 63,908 bytes of the text budget ([TEXT_BUDGET.json](TEXT_BUDGET.json)).

## Sources and contribution

Paper: Hafemeister C, Satija R. *Normalization and variance stabilization of single-cell RNA-seq data using
regularized negative binomial regression*. Genome Biology 20, 296 (2019), DOI
[10.1186/s13059-019-1874-1](https://doi.org/10.1186/s13059-019-1874-1); © The Author(s) 2019, CC BY 4.0, included
unchanged ([SOURCE.md](SOURCE.md)).

Our work: the scenario and prompts, all App sessions and exports, quote and absence checks, the root-cause
analysis from the working panels, the before/after measurement, the audit rule and its check on 11 claims, the
workflow and templates, both scripts and the App feature notes. App answers and panel text are the App's
output, attributed as such.

## Changes in v1.4

- README reorganised: first-screen summary and key numbers; one table of the four error mechanisms with the
  check that exposes each; the App's citation instruction (in-progress nodes 32–33) as the reason quotes land and
  scope claims do not; product feedback as a table; limits gathered in section 10.
- New result from the shipped replay output: the audit rule flags all four contradicted claims and none of the
  four holding lexical absence claims; two evaluation claims are flagged and cleared by reading (term lists
  written after reading).
- Scripts take your own data: `reproduce_quote_pages.py --spans`, `replay_absence_search.py --claims`; new
  [claims-example.json](claims-example.json) with its real output. Default outputs are byte-identical to v1.3.
- Fixed: AX node references in [source-answer-review.tsv](source-answer-review.tsv) (they pointed to the round-1
  export removed in v1.3; now nodes of app-followup-complete-ax.txt), a WORKFLOW cross-reference, spacing typos in
  two provenance records, a check record and verification.md. Counting rule and audit caveats stated more strictly. WORKFLOW.md: section "Apply it" and a pre-registered T1-R2 test protocol.

Earlier: v1.3 added the T1-R before/after measurement and Bohrium route comparison; v1.2 the T1-R probe; v1.1
the working-panel analysis, replay script and WORKFLOW.md. [提交说明.md](提交说明.md) is the competition submission note.

## License

Text, prompts, check records and scripts written for this case: CC BY-NC-ND 4.0 ([LICENSE](LICENSE)). The paper
PDF keeps CC BY 4.0 ([SOURCE.md](SOURCE.md)). App output and screenshots are reproduced as observations of the
Bohrium Science Space App; no ownership of the product interface is claimed.
