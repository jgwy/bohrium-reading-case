# Correct quotations, overbroad claims: auditing what an AI reader says a paper does *not* contain

**Release v1.5.**

| | |
|---|---|
| **Problem** | Asked "does this paper support using the method on my data?", an AI reading assistant quoted the paper exactly and on the right pages, yet stated the paper's scope with *only*, *never*, *nothing*, and two of those sentences were false. A quote check cannot catch this: a quote is local evidence, "X never appears" is a claim about the whole paper. |
| **Method** | **Claim-scope audit.** Ask for paper states / follows from scenario / unknown, each with page + exact quote → check every quote on its page by script → list every absence, uniqueness and "all are" sentence with its terms, synonyms and word stems → search the whole PDF and open each hit → give page evidence back → re-measure with the same scripts. |
| **Case** | Bohrium Science Space desktop App (玻尔·科学空间); Hafemeister & Satija 2019, the sctransform paper (Genome Biology, CC BY 4.0, full PDF included); a constructed tumour-biopsy scenario; three real sessions. |
| **Result** | Quotes: 13/13 on page. Scope: 2 of 5 "never/only" claims false (1 more arguable). The working panel shows quotes must cite a block the model read, while "replicate design does not occur" followed the one visible search, which lacked `replicat`. Given page evidence, the App fixed both. With a two-sentence rule (T1-R) 2 of 6 were still wrong, but every word-absence claim printed its search pattern, so our replay found both. The audit flags 4 of 4 wrong claims and 0 of 4 correct word-absence claims. |
| **Reuse** | Append the T1-R rule to your prompt, list every "never/only/all" sentence with terms and stems, run `replay_absence_search.py --claims` on your PDF; no code edits ([section 7](#7-reproduce-this-case-then-apply-it-to-your-paper), [WORKFLOW.md](WORKFLOW.md): 8 steps, 4 templates). |
| **Bohrium value** | "共 N 处" counts matching lines (20/20); the reader parsed pp. 1–14 of 15, while 新任务 read all 15 and listed every search; five tips, five product suggestions ([section 8](#8-bohrium-science-space-tips-and-feedback)). |

**Key numbers** [M, from files in this repository]:

| | Round 1: reader + 阅读助手 | Round 2: page-specific follow-up | T1-R probe: new task + PDF |
|---|---|---|---|
| Quotes on the claimed page | 13/13 | 4/4 | 10/11 (one added full stop) |
| Absence/uniqueness claims contradicted by the paper | 2 of 5 (+1 arguable) | both revised | 2 of 6 |
| Word-absence claims whose search pattern the answer shows | 0 | — | 5 of 5 |
| Pages the App read | parsed blocks, pp. 1–14 of 15 | same session | all 15 (`pdftotext`) |
| UI time badge | 1m 6s | 33s | 2m 10s |

**Reading guide.** **Paper** (p. N) = publisher PDF wording, physical page; **App** = App output, verbatim;
**Our check** = our judgement. [M] = measured in a shipped file; [I] = our inference. **Absence claim** = "X does
not occur"; **uniqueness claim** = "the only/all … are Y"; **word-absence** = about whether a word occurs. **AX** = accessibility text
of the App window exported during the session (on-screen text, not telemetry); "node N" is a line in it.
**Route A** = paper reader + 阅读助手 (rounds 1–2); **Route B** = 新任务 with the PDF attached (T1-R). **T1, T1-R, T1-R2, T2** = prompt templates in [WORKFLOW.md](WORKFLOW.md).
Long tables and derivations: [DETAILS.md](DETAILS.md) (D1–D6). File index: [提交说明.md](提交说明.md).

## 1. The reading question

**Constructed scenario** (no real patients): six tumour biopsies measured with 10x UMI counts plus a separate
Smart-seq2 TPM matrix. Does the paper support sctransform on both inputs? Do six biopsies establish six
independent patients? Can Pearson residuals be read as comparable expression levels across genes?

Each is a scope decision with evidence spread over pp. 1–14: input contract (pp. 1, 8, 11), datasets (pp. 2, 14),
residual definition and caveats (pp. 5, 7, 9, 11, 13). The hard part is not finding a supporting sentence; it is
knowing that no other sentence changes the answer.

## 2. Method and design choices

| Choice | Why | Cost / limit |
|---|---|---|
| Ask the App with the PDF open, "Use only this PDF" ([prompt.txt](prompt.txt)) | Every claim is tied to a page we can open. | We see only what the UI shows. |
| Three-way split: paper states / follows from scenario / unknown | Separates "the paper says UMI" from "so TPM is out of scope" and from the unknowable. | Longer answers. |
| One short exact quote + page per claim | Allows a mechanical check. | Proves location, not interpretation. |
| Separate audit of absence / uniqueness words | They are claims about the whole paper; only a whole-text search tests them, so the full PDF is shipped. | Needs a human-written synonym and stem list. |
| Follow-up with page evidence, then a changed first prompt (T1-R), same scripts | Tests repair, then prevention; every answer kept. | Assisted repair; T1-R ran once. |

## 3. Why quotes land and scope claims do not (observed)

A snapshot of the working panel while round 1 was generating ([app-inprogress-ax.txt](app-inprogress-ax.txt),
02:25:48 UTC+8; node-by-node table in [DETAILS D1](DETAILS.md#d1-round-1-working-panel-node-by-node)) shows [M]:

- node 28: the assistant opened `Hafemeister_Satija_2019_sctransform.jsonl`, a parsed block file of the PDF; its
  answer says "197 blocks, pages 1–14", while the viewer shows "/ 15";
- node 32: it restates its instruction, "Cite parsed PDF evidence as ⟦source:RESOURCE_ID⟧ using the exact
  non-empty resourceId from a supporting block you read"; nodes 34–77 list 14 planned quotes, 13 with a block
  `resourceId` (`pdf-block-…`), line and page;
- node 29: the one search whose pattern is visible, `搜索内容 Smart|TPM|transcripts|biops|patient|Donor|donor|full-length|full length，共 1 处`;
  node 31 turns its single hit into "No Smart-seq2, no TPM, no biopsy, no patient.";
- node 99: a draft line says the paper "doesn't address patient/sample independence or replication design";
  no visible pattern contains `replicat`.

**Mechanism** [I, from nodes 28–34]: a quote must cite a block the model read, so quotes land on the right page;
an absence or uniqueness sentence has no block to cite, so it rests on whatever search the model chose to run,
and the answer does not show that search. (We saw the instruction only as the model restated it.)

## 4. Round-1 results

Answer: [app-answer.md](app-answer.md) (readable copy; raw: nodes 23–58 of
[app-followup-complete-ax.txt](app-followup-complete-ax.txt)). Claim-by-claim review: [source-answer-review.tsv](source-answer-review.tsv);
quote check: [quote-page-check.json](quote-page-check.json).

| Question | Paper | App (gist) | Our check |
|---|---|---|---|
| UMI and TPM inputs | "Our approach can be applied to any UMI-based scRNA-seq dataset" (p. 1); "We explicitly model the UMI counts…" (p. 11) | Supports the 10x UMI input, not the Smart-seq2 TPM input | Supported. TPM exclusion is an inference from the count-model input contract, not a TPM experiment. |
| Six biopsies = six patients? | No biopsy or patient text; main dataset is PBMCs from one healthy donor (p. 14) | No; the mapping is unknown | Supported as scenario reasoning. |
| Residuals comparable across genes? | "transformed onto a common scale" (p. 5); z = (x − μ)/σ (p. 11); PCA "centered and scaled" (p. 13) | Only as standardized deviations, not absolute expression | Supported. Keep the p. 9 caveat on depth independence; "peaks at 1" (p. 7) is a distribution, not a per-gene rule. |

The three conclusions hold; the errors sit in the scope sentences around them.

## 5. Where scope errors enter: four mechanisms

We counted every sentence saying a term or topic does not occur in the paper, or that a passage or set of hits is
the only/all of a kind: 5 in round 1 (A1–A5), 6 in T1-R (B1–B6); all 11 with wording and evidence in
[DETAILS D2](DETAILS.md#d2-all-11-absence-and-uniqueness-claims). The contradicted ones (wording and pages [M]):

| Claim | App wording | Paper | Mechanism [I] | Exposed by | Prevention |
|---|---|---|---|---|---|
| A2 | "Nothing about biopsies, patients, or replicate design — those terms do not occur." | "each droplet represents a technical replicate of a bulk RNA sample" (p. 5) | **Term in no visible search** | stem `replicat` → p. 5 | T1-R; did not recur |
| A3 | "The only reference to non-UMI data is about a different tool … SCnorm" | "read-level (instead of UMI-level) data" (p. 2); "read count data" (p. 11) | **Token searched, synonyms not** | `read-level`, `read count` → pp. 2, 11, 15 | T1-R; reached at page level |
| B3 | "these are the only non-UMI / read-level / plate-based mentions" | "both plate- and droplet-based protocols" (pp. 2, 8) | **Pattern narrower than the wording**: `plate[- ]?based` cannot match a suspended hyphen | stem `plate` → pp. 2, 8 | T1-R2 (stems) |
| B6 | "9 hits; all are 'across genes'/'between genes' in the sense of pooling information" | "Relationship between gene variance…" (p. 3); "variation across genes" (p. 5) | **Hits summarized, not opened** | read all 9 hit contexts | T1-R2 (no "all/only") |

A4 ("The only remotely relevant statement is an assumption about heterogeneity", p. 10) is arguable and judged by
reading. **Common cause** [I]: none is a quotation error, which is why the quote check passed. All four are search
results stated as whole-paper facts: the search was missing (A2), too literal (A3), too narrow for the
typography (B3) or not read (B6).

**Does the audit separate wrong claims from right ones?** Decision rule: an absence claim fails if any listed term
hits; a uniqueness claim fails if a term hits a page it did not name; an "all are" claim requires reading every
hit. Applied with the shipped replay ([replay-absence-search-output.json](replay-absence-search-output.json)) [M]:

| Group | Claims | Audit result |
|---|---|---|
| Contradicted by the paper | A2, A3, B3, B6 | 4 of 4 flagged |
| Hold, word absence | A1, B1, B2, B4 | 0 of 4 flagged |
| Hold, about what the paper evaluates | A5, B5 | flagged once their own words are listed; cleared by reading ([D3](DETAILS.md#d3-audit-rule-the-two-evaluation-claims)) |
| Arguable | A4 | not scriptable; judged by reading |

The synonyms and stems were written after reading the paper, so this is not a blind detection rate: given a good
term list, the rule sends the reader to every wrong claim and to none of the correct word-absence ones. Writing the
list *before* searching (workflow step 5) is the human part that can fail.

## 6. Repair and prevention

**Repair (round 2)** [M]: the page-specific follow-up ([followup-prompt.txt](followup-prompt.txt)) made the App
quote both earlier sentences, revise both, and add the p. 11 DESeq passage the feedback had not named; the three
conclusions stayed (answer: [app-followup-answer.md](app-followup-answer.md), raw nodes 69–120; [revision-comparison.tsv](revision-comparison.tsv),
[followup-quote-page-check.json](followup-quote-page-check.json)). The counter-evidence came from our check:
assisted repair, not prevention.

**Prevention probe (T1-R)**: the original prompt plus *"Before writing that the paper never mentions something,
or that a passage is the only one about a topic, list the exact search terms and synonyms you searched, and
report the pages of every hit. If a term was not searched, do not make the absence claim."* Sent once in a fresh
task, no page hint ([sent text](t1r-test/sent-prompt-single-line.txt); [pre-send field](t1r-test/before-send-excerpt.txt);
[search steps](t1r-test/search-observations-excerpt.jsonl); [answer](t1r-test/final-answer-excerpt.txt)).
Same two scripts, same PDF (full comparison: [DETAILS D4](DETAILS.md#d4-round-1-vs-t1-r-measured-with-the-same-scripts)):

| Measure | Round 1 (T1) | T1-R probe |
|---|---|---|
| "Replicate design does not occur" | stated | not stated; "technical replicate" among its `replicat` hits |
| read-level / read count reached without a hint | no | yes, at page level (pp. 2, 11) |

**What this shows.** Wrong claims did not fall; their kind changed. Round 1 declared absent a term it never
searched; T1-R printed its patterns, so its errors are found without the App: B6 by reading the hits, B3 by
adding the stem `plate`. One run, different route from round 1: descriptive, not causal.

### Next test: T1-R2 (not run)

T1-R2 adds stems and "pattern → pages" wording and forbids "only/all", targeting B3 and B6. Its protocol and
measures were written before any run ([WORKFLOW.md](WORKFLOW.md#t1-r2--t1-r-plus-stems-and-bounded-wording-untested));
its result, whatever the direction, will be reported here.

## 7. Reproduce this case, then apply it to your paper

**Environment.** Bohrium Science Space desktop App (bundle `com.bohrium.scix`), macOS 27.0, Apple silicon; most
likely App 0.10.14 [I, [D6](DETAILS.md#d6-source-check-record-and-environment)]. Checks: Python 3.10+ (3.12.2 here)
and Poppler `pdftotext` (26.08.0 here); no model, network or extra package.

**Route A, rounds 1–2.** 文献阅读 → 本地导入 → open the included PDF (viewer "/ 15") → switch on **阅读助手**,
leave 论文速览, 图表速览, 全文翻译 off; 推理强度 标准 (screenshots) → send [prompt.txt](prompt.txt) → expand the
working panel while it runs; copy the answer (复制 button; we exported the window's accessibility text) → run the checks, open pp. 2, 5, 11 → send [followup-prompt.txt](followup-prompt.txt); save
the second answer separately.

**Route B, T1-R** (the reader offered no new-conversation action, [INTERFACE_EVENT.md](t1r-test/INTERFACE_EVENT.md)).
新任务 → attach the PDF in the input box (chip "PDF·5.13MB"; our file picker needed keyboard input) → paste
[sent-prompt-single-line.txt](t1r-test/sent-prompt-single-line.txt) as one line, check the field, 发送 → expand
"已处理", copy every `搜索内容 … 共 N 处` line and the answer.

**Checks** (outputs identical to the shipped files):

```sh
python3 reproduce_quote_pages.py > my-quote-check.json        # 13/13, 4/4, 10/11
python3 replay_absence_search.py  > my-absence-check.json     # 20/20 counts = matching lines
python3 replay_absence_search.py --claims claims-example.json # = claims-example-output.json
```

A repeat matches if the three conclusions match section 4, you check every quote's page, and you record which
scope claims the replay contradicts; a run without such errors is a data point, not a failure.

**Your own paper** (steps 2–4 are what we did here):

1. `pdftotext your.pdf - | head` must print the paper; a scanned PDF needs OCR first.
2. Ask with template T1-R from [WORKFLOW.md](WORKFLOW.md) (your scenario, 2–4 scope questions); export the
   answer before any follow-up.
3. Put each quote into `your-spans.json` (format of [quote-page-check.json](quote-page-check.json): `ax_node` =
   any locator, `quote`, `claimed_pdf_page`); run `python3 reproduce_quote_pages.py --pdf your.pdf --spans your-spans.json`.
   A `claimed_page_contains_quote: false` means wrong page or altered wording: open the page.
4. Write every absence, uniqueness and "all are" sentence into `your-claims.json` with terms, synonyms and bare
   stems as case-insensitive regexes, *before* searching (`"all_contexts": true` for "all are"; format:
   [claims-example.json](claims-example.json), three claims of this case). Run
   `python3 replay_absence_search.py --pdf your.pdf --claims your-claims.json` and read `claims_with_hits` with
   the rule of section 5. For the example: `["A2", "B3"]`; `replicat` → p. 5, `plate` → pp. 2, 8,
   `plate[- ]?based` → none.
5. Route B only: copy each `搜索内容 PATTERN，共 N 处` line into a JSONL like
   [the excerpt](t1r-test/search-observations-excerpt.jsonl) and add `--searches your-searches.jsonl`; each App
   count should equal `matching_lines`.
6. Repair with template T2 citing the pages from step 4; keep a revision table and re-run step 3.

Works on the extractable main text of the supplied PDF; not on figures, equations or tables as images,
unsupplied supplements, or a concept expressed without any listed word or stem.

## 8. Bohrium Science Space: tips and feedback

Tips that follow from the evidence:
1. **Read the working panel**: "共 N 处" equalled matching *lines*, not occurrences, in all 20 replayed T1-R
   searches (6 of them tell the two apart; our Poppler may differ from the App's).
2. **Pick the route**: Route A anchors quotes to parsed blocks (`pdf-block-…`) but parsed pp. 1–14 here; Route B
   read all 15 pages and lists every search, but cites file pages ([D5](DETAILS.md#d5-two-app-routes-side-by-side)).
3. **Ask for search terms before absence claims** (T1-R), then replay them with `replay_absence_search.py`.
4. **Enter the prompt as one line and check the field before 发送** ([interface events](t1r-test/INTERFACE_EVENT.md)).
5. **Export each round before you follow up**; AX exports clip nodes near 512 characters (T1-R nodes 90, 91, 111, 113).

Product feedback [observation M, suggestion I]:

| Observation | Effect on a user | Suggestion |
|---|---|---|
| Reader parsed "197 blocks, pages 1–14"; viewer shows "/ 15" | Whole-paper claims may rest on partial text unnoticed | Show the parsed page range next to the page count |
| "共 N 处" = matching lines in all 20 replayed searches, incl. the 6 where occurrences differ | Read as occurrences | Label it as lines, or show occurrences and pages |
| No "new conversation" action in the reader's 阅读助手 menus we inspected | A clean repeat had to move to Route B | Add a visible new-conversation action |
| Multi-line input once produced an answer before an explicit 发送 | Unclear whether the full prompt was sent | Make Enter/Send behaviour explicit |
| Earlier search steps shown only as summaries; panel collapses after completion | Absence claims cannot be audited from the UI | Keep every executed pattern visible and exportable |

![Round-2 answer beside page 5 of the paper](04-followup.jpg)

Screenshots (unedited, no account name): [02](02-reading-request.jpg) round-1 request and answer (1m 6s badge);
[03](03-method-page.jpg) Methods p. 11 beside the session; [04](04-followup.jpg) round 2 beside p. 5;
[T1-R result](t1r-test/workspace-result.jpg).

## 9. Limits

- One paper, three sessions, one constructed scenario. Not claimed: a controlled baseline, comparison with other
  tools, scientific reproduction, expert approval, generality, or a stable or causal T1-R effect.
- The claim counts (5, 6) rest on our reading of which sentences are absence/uniqueness claims. T1-R2 is untested.
- Model, version, tokens and cost: **unavailable**, not zero. Time badges have undefined scope (mid-answer
  already 1m 7s), are not summed and exclude our untimed checking.

## Sources, contribution, license

Paper: Hafemeister C, Satija R. *Normalization and variance stabilization of single-cell RNA-seq data using
regularized negative binomial regression*. Genome Biology 20, 296 (2019),
[10.1186/s13059-019-1874-1](https://doi.org/10.1186/s13059-019-1874-1); CC BY 4.0, included unchanged ([SOURCE.md](SOURCE.md)).
Our work: scenario, prompts, all App sessions and exports, every check, the root-cause analysis, the audit rule,
workflow and scripts; App answers and panel text are the App's output. Our text, prompts, records and scripts:
CC BY-NC-ND 4.0 ([LICENSE](LICENSE)); the PDF keeps CC BY 4.0.

**Changes in v1.5**: README shortened; long tables and the former verification.md moved to
[DETAILS.md](DETAILS.md); slot for a T1-R2 result in section 6. No measurement changed; script outputs byte-identical to v1.4.
