# Details behind the README

Appendix to [README.md](README.md): the long tables and derivations, each cited there by section. Labels as in the
README: **Paper** / **App** / **Our check**, [M] measured in a shipped file, [I] our inference.

## Evidence map

| Step | Input | App output (raw) | Our check |
|---|---|---|---|
| Round 1 (Route A) | [prompt.txt](prompt.txt) | [app-followup-complete-ax.txt](app-followup-complete-ax.txt) nodes 23–58; mid-answer panel [app-inprogress-ax.txt](app-inprogress-ax.txt) | [quote-page-check.json](quote-page-check.json), [source-answer-review.tsv](source-answer-review.tsv), [replay output](replay-absence-search-output.json) part `round1` |
| Round 2 (Route A) | [followup-prompt.txt](followup-prompt.txt) | same export, nodes 69–120 | [followup-quote-page-check.json](followup-quote-page-check.json), [revision-comparison.tsv](revision-comparison.tsv) |
| T1-R (Route B) | [sent-prompt-single-line.txt](t1r-test/sent-prompt-single-line.txt), [pre-send field](t1r-test/before-send-excerpt.txt) | [search steps](t1r-test/search-observations-excerpt.jsonl), [answer](t1r-test/final-answer-excerpt.txt) | [t1r-test/quote-page-check.json](t1r-test/quote-page-check.json), replay output part `t1r` |
| Your paper | [claims-example.json](claims-example.json) | — | [claims-example-output.json](claims-example-output.json) |

## D1. Round-1 working panel, node by node

[app-inprogress-ax.txt](app-inprogress-ax.txt), captured 2026-10-30 02:25:48 UTC+8 while the first answer was
generating ([inprogress-export-provenance.json](inprogress-export-provenance.json)) [M]:

| AX node | What the App showed | What it tells a user |
|---|---|---|
| 21 | "正在处理… （用时 1m 7s）" | The badge runs during generation; its scope is undefined. |
| 23–27 | Step summaries: inspect the PDF structure, read the rest, run targeted searches, "confirm with exact-case searches that the paper never mentions Smart-seq2, TPM, biopsies, or patients". | The assistant works in tool steps over the paper. |
| 28 | `查看 Hafemeister_Satija_2019_sctransform.jsonl` | It reads a parsed block file of the PDF. |
| 29 | `搜索内容 Smart\|TPM\|transcripts\|biops\|patient\|Donor\|donor\|full-length\|full length，共 1 处` | Searches are regular expressions; the panel shows pattern and count. |
| 31 | "Only one match: \"Healthy Donor\" (singular). No Smart-seq2, no TPM, no biopsy, no patient." | Absence statements come from this lexical search. |
| 32–33 | "The instruction says: \"Cite parsed PDF evidence as ⟦source:RESOURCE_ID⟧ using the exact non-empty resourceId from a supporting block you read.\"" | Every citation must point to a block the model read. |
| 34–77 | Draft notes listing the quotes, most with a block `resourceId` (`pdf-block-…`), line and page. | Quotes are copied from anchored blocks. |
| 99 | Draft: "doesn't address patient/sample independence or replication design". | "Replication" enters here; the visible pattern does not contain it. |
| 119–128 | "正在分析... 29.8s"; 请求批准, "上下文已使用 14%", 推理强度 (disabled while generating). | Context use is shown. |
| 133, 143–146 | Page field "/ 15"; 全文翻译 off, **阅读助手 on**, 论文速览 off, 图表速览 off. | Only the reading assistant was used. |

After completion the panel collapsed behind "已处理（用时 1m 6s）" (node 22 of
[app-followup-complete-ax.txt](app-followup-complete-ax.txt)). The earlier search steps (nodes 24, 26) are
summaries without patterns; they name Smart-seq2, TPM, non-UMI, biopsy and patient, not replicate or read-level.
By the App's own statement ("197 blocks, pages 1–14", node 23 of the complete export), page 15 (references 22–39,
publisher's note) was outside the parsed range.

## D2. All 11 absence and uniqueness claims

Counting rule (our judgement, applied the same way to both answers): every sentence saying a term or topic does
not occur in the paper, or that a passage or set of hits is the only/all of a kind. Statements that the paper is
*silent on a question* (e.g. "The paper is silent on whether TPM … could be coerced into the model") are not
counted. Round 1: nodes of [app-followup-complete-ax.txt](app-followup-complete-ax.txt); T1-R: nodes of
[t1r-test/final-answer-excerpt.txt](t1r-test/final-answer-excerpt.txt). Term hits: [replay-absence-search-output.json](replay-absence-search-output.json) [M].

| Claim | Node | App wording | Term hits in the PDF | Our check |
|---|---|---|---|---|
| A1 | 27 | "The words "Smart-seq2" and "TPM" never appear anywhere in the paper." | none | holds |
| A2 | 32 | "Nothing about biopsies, patients, or replicate design — those terms do not occur." | `replicat` p. 5 | contradicted: "the data from each droplet represents a technical replicate of a bulk RNA sample" (p. 5) |
| A3 | 27 | "The only reference to non-UMI data is about a different tool, not sctransform: … SCnorm" (p. 3) | `non-UMI` p. 3; `read-level` p. 2; `read count` pp. 11, 15 | contradicted: "read-level (instead of UMI-level) data" (p. 2); "DESeq [23] uses the negative binomial distribution for read count data" (p. 11); voom reference (p. 15) |
| A4 | 32 | "The only remotely relevant statement is an assumption about heterogeneity" (p. 10 cited) | not scriptable | arguable: p. 5 technical replicate; p. 9 cell-type RNA content |
| A5 | 29 | "there is no empirical demonstration for full-length/non-UMI data" | none for full-length, Smart-seq, TPM | holds (D3) |
| B1 | 51, 54, 91 | "The paper never mentions Smart-seq2 or TPM (search terms above: no h…" (node 91 clipped) | none | holds |
| B2 | 97, 100 | "Nothing about biopsies, patients, or tumours … the tumour/biopsy/patient concepts never appear" | none | holds |
| B3 | 57 | "hits on pages 2, 3, 11, 15 (5 hits; these are the only non-UMI / read-level / plate-based mentions)" | `plate[- ]?based` none; `plate` pp. 2, 8 | contradicted: "generated with both plate- and droplet-based protocols" (p. 2); "including both plate- and droplet-based protocols" (p. 8) |
| B4 | 113 | "the paper never uses the word "comparable" (search above: no literal hit)" | none | holds |
| B5 | 92 | "The paper never evaluates sctransform on TPM, read counts, or full-length/non-UMI input" | none for full-length, Smart-seq, TPM | holds (D3) |
| B6 | 78 | "9 hits; all are "across genes"/"between genes" in the sense of pooling information" | pp. 1, 2, 3, 4, 5, 10, 11 (all contexts printed) | contradicted: "Relationship between gene variance and cell sequencing depth" (p. 3, Fig. 1); "substantial variation across genes" (p. 5) |

In B3 the answer itself says the paper's plate-based datasets are UMI datasets, so its scientific conclusion is
unaffected; the "only" wording is not. Two T1-R page lists also omit p. 3 (answer nodes 72 and 78) although
replaying their patterns finds p. 3 lines inside the App's own counts: counts come from the tool, page lists
and "all are…" summaries are the model's restatement [I].

## D3. Audit rule: the two evaluation claims

A5 and B5 are about what the paper *evaluates*, not only about words. The shipped replay lists only full-length,
Smart-seq and TPM for them (no hits). Listing their own words as well, non-UMI (p. 3), read-level (p. 2) and read
count (pp. 11, 15) hit, so the rule flags both; reading the hits clears them: they concern other methods (SCnorm,
earlier read-level models, DESeq, voom), not an sctransform evaluation. The cost of the rule on correct claims is
therefore one reading, not a false verdict.

## D4. Round 1 vs T1-R, measured with the same scripts

| Measure | Round 1 (T1) | T1-R probe |
|---|---|---|
| Absence/uniqueness claims; contradicted | 5; 2 + 1 arguable | 6; 2 (B3, B6) |
| Word-absence claims backed by a pattern shown in the answer | 0 | 5 of 5 (B5 is about evaluation, not lexical) |
| "Replicate design does not occur" | stated | not stated; "technical replicate" listed among its `replicat` hits |
| read-level / read count reached without a hint | no | yes, at page level (pp. 2, 11); no quote of them in the visible, partly clipped text |
| App "共 N 处" vs our replay | 1 vs 1 (p. 14, "Donor") | 20 of 20 equal matching **lines**; 14 of 20 equal matches |
| Quotes on the claimed page | 13/13 | 10/11: the abstract sentence quoted with a full stop where the paper continues "dataset and is freely available" |

Round 1 used the paper reader (parsed blocks, pp. 1–14); T1-R a new task with the PDF attached (`pdftotext`, all
15 pages). The first T1-R attempt (multi-line entry) is not counted: delivery of the rule was not established
([INTERFACE_EVENT.md](t1r-test/INTERFACE_EVENT.md)). The plan written before the run: [t1r-test/PLAN.md](t1r-test/PLAN.md).

## D5. Two App routes side by side

| | Route A: paper reader + 阅读助手 (rounds 1–2) | Route B: 新任务 + PDF attachment (T1-R) |
|---|---|---|
| Start | 文献阅读 → 本地导入 → open paper → switch on 阅读助手 | 新任务 → attach the PDF in the input box (chip "PDF·5.13MB") → type → 发送; the bar showed 选择运行位置：本地 and 请求批准 |
| What the model reads | Parsed block file `<paper>.jsonl`; "197 blocks, pages 1–14" | Its own tool steps: page count → "Extract PDF text with layout" → "Split … into per-page files"; all 15 pages |
| Citation anchor | `pdf-block-…` resource IDs and pages | File + page (the article footer reads "Page N of 15") |
| Search | Regex; panel shows pattern and "共 N 处" | Same; 20 patterns visible |
| After completion | Collapsed behind "已处理（用时 1m 6s）" | Collapsed behind "已处理（用时 2m 10s）", expandable |
| Quote check | 13/13 on page | 10/11 (one added full stop) |
| Context meter | 14% mid-answer (16% after round 2) | 16% at the end |

## D6. Source-check record and environment

This section replaces verification.md (v1.0–v1.4); its findings are unchanged.

**Round-1 conclusions** (record: [source-answer-review.tsv](source-answer-review.tsv), with AX nodes):
1. UMI counts are within the paper's stated input scope (pp. 1, 11); the Smart-seq2 TPM transfer is a
   constructed scenario the paper does not validate.
2. Six biopsies do not establish six independent patients: reasoning about missing target metadata; the
   healthy-donor dataset (p. 14) cannot supply the mapping.
3. Residuals have a common standardized scale (p. 5), defined by a gene-specific expectation and standard
   deviation (p. 11), not absolute expression units; PCA additionally centres and scales genes (p. 13).

**Qualifications the answer dropped**: the Fig. 4 density peak near 1 (p. 7) concerns genes with little
biological variation and is a distribution, not proof that every variance above 1 is biology; the p. 5
depth-independence quote has a p. 9 qualification (cell types differ in RNA content). The round-2 sentence "No
wording in this section needed revision" is the App's statement, not an accuracy certificate.

**Quote matching.** Poppler 26.08.0 text, NFKC, line-end hyphens joined, whitespace removed, each page searched;
pypdf 6.10.0 gave an independent extraction; pages 5 and 11 were inspected visually. "Replicate" has one lexical
occurrence in this PDF; no Smart-seq2, TPM, biopsy or patient match. These bound claims to this supplied PDF,
not to supplements or related papers. Matching validates location only, not interpretation.

**Exports.** The raw AX exports are the record of what the App displayed; they were not edited. Round 1 and round
2 are both in app-followup-complete-ax.txt (round 1 first exported 2026-10-29T18:28:04.716Z, round-2 UI time
02:47 AM UTC+8; [followup-export-provenance.json](followup-export-provenance.json)). The Markdown renderings of
both answers shipped up to v1.4 are dropped; they repeated this text. T1-R excerpts are privacy-selected
with original node IDs; AX clips some nodes near 512 characters ([t1r-test/PROVENANCE.json](t1r-test/PROVENANCE.json)).

**App version** [I]: the installed App's bundle metadata read 0.10.14 with a modification time before the
sessions (checked locally, not shipped), so they most likely ran 0.10.14; an update prompt to 0.10.15 was
dismissed before T1-R ([PLAN.md](t1r-test/PLAN.md)). The UI showed no model, version or token count.

**Expected script outputs** (identical to the shipped files): quote check
`"on_claimed_page": {"quote-page-check.json": "13/13", "followup-quote-page-check.json": "4/4", "t1r-test/quote-page-check.json": "10/11"}`;
replay `"app_count_equals_matching_lines": 20`, `"app_count_equals_matches": 14`, one round-1 match (p. 14),
A2 `replicat` → `[5]`, B3 `plate[- ]?based` → `[]` but `plate` → `[2, 8]`; `--claims claims-example.json`
reproduces [claims-example-output.json](claims-example-output.json) (`"claims_with_hits": ["A2", "B3"]`,
`comparab` → `[]`). Another Poppler version may change line breaks and so line counts, not pages.
