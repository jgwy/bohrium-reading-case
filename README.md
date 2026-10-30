# Correct quotations, overbroad claims: a two-round paper-reading case

A real Bohrium Science Space desktop session answered three questions about the 2019 sctransform paper. Thirteen selected quotations were found on the stated PDF pages, yet two surrounding scope statements were too broad. An independent source check identified them; an explicit follow-up supplied the counterpassages; the App acknowledged and revised both statements.

The three main conclusions remained: UMI counts fall within the paper's scope, whereas Smart-seq2 TPM transfer is unsupported by it; six biopsies do not establish six independent patients; Pearson residuals share a standardized scale, not absolute expression units.

This repository contains the complete evidence for this one case. Publishing it is not an official score or an independent validation.

## Start with the actual record

| Item | Local evidence |
|---|---|
| Original paper | [Publisher PDF](materials/Hafemeister_Satija_2019_sctransform.pdf), 15 pages, CC BY 4.0 |
| First request and answer | [Exact prompt](prompt.txt), [faithful visible transcript](app-answer.md) |
| Source check | [Review table](source-answer-review.tsv), [explanation](verification.md), [13 quotation/page checks](quote-page-check.json) |
| Corrective follow-up | [Exact prompt](followup-prompt.txt), [faithful revised answer](app-followup-answer.md) |
| What changed | [Original claim / external feedback / actual revision](revision-comparison.tsv), [4 follow-up quotation checks](followup-quote-page-check.json) |
| Raw visible record | [First-round complete AX export](app-answer-complete-ax.txt), [complete two-round AX export](app-followup-complete-ax.txt) |
| Capture provenance | [First export](export-provenance.json), [follow-up export](followup-export-provenance.json) |

AX means accessibility text exported from the actual App window. These are visible conversation exports, not native model telemetry. The Markdown versions remove UI wrappers and duplicate headings; equation glyphs are joined into ordinary notation. Original wording and errors are retained. The initial answer was not overwritten by the revision.

## The reading problem

The question uses a **constructed scenario**: six tumour biopsies represented by 10x UMI counts, plus a separate Smart-seq2 TPM matrix. It asks whether the paper supports both inputs, whether the biopsy count establishes independent patients, and what residual values mean across genes.

This is a method-reading decision, not a dataset analysis. No scientific computation, installation or compute job was requested. The record does not claim real patient observations or a user study.

The answer's useful distinction is between an input-type claim and a validated use under particular conditions. The paper defines a count-based model on p. 11 and states its UMI scope on p. 1. Rejecting direct substitution of a TPM matrix follows from that input contract; it is not an empirical TPM experiment reported by the authors. Likewise, the patient-count conclusion comes from the scenario's missing mapping, not from a number supplied by the paper.

## Why checking quotations was not enough

| First-round statement | Source check | Actual follow-up revision |
|---|---|---|
| SCnorm is the only reference to non-UMI data. | p. 3 discusses SCnorm, but p. 2 also describes read-level models; p. 11 discusses bulk read-count methods. | The App explicitly retracts “only,” identifies those passages and keeps sctransform's own UMI scope separate. |
| Nothing about biopsies, patients or replicate design; those terms do not occur. | The searched PDF contains no biopsy/patient match, but p. 5 explicitly discusses a technical replicate of a bulk RNA sample. | The App distinguishes technical replication from independent patients and leaves the biopsy-to-patient mapping unknown. |

A quotation can be exact while the sentence around it overgeneralizes. “Only” is a claim about the whole source, not just the quoted passage. A lexical search can support “this word was not found in this supplied file”; it cannot establish that a concept is absent from all related material.

The follow-up also cites DESeq's read-count model on p. 11. That quotation, the p. 2 read-level passage, the p. 3 SCnorm passage and the p. 5 technical-replicate passage all match their stated pages. This is assisted revision after specific external feedback, not spontaneous self-correction. The source-check work and corrective prompt are part of the method and effort.

## Repeat the observed App workflow

1. In the installed Bohrium Science Space desktop App, open **文献阅读 → 本地导入** and select the included publisher PDF.
2. Open the imported paper and enable **阅读助手**. The recorded PDF viewer displays 15 pages.
3. Send [prompt.txt](prompt.txt) unchanged. Save the complete visible answer before modifying anything.
4. Open the cited original passages, especially pp.2,3,5 and11. Compare the scope of the statement with the scope of its evidence.
5. Send [followup-prompt.txt](followup-prompt.txt), which supplies the two specific corrections. Preserve the new answer separately.
6. Record whether the answer acknowledges the original wording, supplies supporting passages and retains only conclusions those passages justify.

The genuine screenshots show selected views, not the full conversation:

- [02 — original request and completed response](02-reading-request.jpg)
- [03 — Methods page 11 beside the reading session](03-method-page.jpg)
- [04 — second response beside original page 5](04-followup.jpg)

![Actual second response beside the source paper](04-followup.jpg)

## Repeat the quotation/page matching

The independent check extracted PDF text with Poppler, joined line-break hyphenation, applied Unicode NFKC normalization and removed whitespace for matching. It searched each selected quote within each physical PDF page. Pages5 and11 were also visually inspected. The accompanying [small script](reproduce_quote_pages.py) packages that already-used matching procedure:

```sh
python3 reproduce_quote_pages.py
```

It requires Python 3.10+ and Poppler's `pdftotext` on PATH. The recorded environment used Poppler 26.08.0; pypdf 6.10.0 was used for independent extraction and the one-time text-size calculation. [requirements.txt](requirements.txt) records that Python dependency.

The script reads the included PDF and both quote-check records, then prints newly observed page matches. It does not run a model, call the network, alter the historical results or decide whether an interpretation is scientifically sound. Word-boundary normalization makes extracted-text matching practical, but it does not validate figures, equations or surrounding claims by itself.

## Measured facts and unknowns

- The first App badge displayed **1m 6s**; the follow-up displayed **33s**. These are separate UI observations. They are not added into a 99-second end-to-end time: source inspection, verification and interaction also took effort.
- Thirteen selected first-round quotation spans and four selected follow-up spans matched their claimed pages. These are selected evidence checks, not an answer-accuracy percentage.
- The product reported reading 197 parsed blocks on pages 1–14. The included publisher PDF has15 pages. The independent search covered extractable text on all 15 pages; supplements were not supplied.
- Model/version, token usage and billed cost were not visible. They are **unavailable**, not zero.
- No controlled baseline, model comparison, scientific reproduction, independent human-expert approval or official ecosystem score is claimed.

Some source caveats remain important after the revision. A density peak at residual variance 1 is not a requirement that every gene have exactly unit variance. The p. 5 depth-independence quotation must be read with p. 9's explicit caveat about incomplete biological/technical independence. The [review](verification.md) retains these qualifications.

## Sources and contribution

The paper is Hafemeister C, Satija R. *Normalization and variance stabilization of single-cell RNA-seq data using regularized negative binomial regression*. Genome Biology 20, 296 (2019), DOI[10.1186/s13059-019-1874-1](https://doi.org/10.1186/s13059-019-1874-1). Its copyright, CC BY 4.0 permission and extraction changes are recorded in [SOURCE.md](SOURCE.md).

Our contribution is the focused reading scenario, exact prompts, actual visible App record, source/page checks, scope corrections and reproducible matching procedure. The App's original answer and revision remain separately attributable in the record; no human-expert review is invented.

[TEXT_BUDGET.json](TEXT_BUDGET.json) records the text-size calculation, including PDF-extracted text. [提交说明.md](提交说明.md) is the competition submission note for this release.

## License

The original text, prompts, check records and script written for this case are licensed under [CC BY-NC-ND 4.0](LICENSE) (Attribution-NonCommercial-NoDerivatives 4.0 International). The included paper PDF is not covered by that license: it remains © The Author(s) 2019 under its own CC BY 4.0 license, as recorded in [SOURCE.md](SOURCE.md). Quoted App output and product screenshots are reproduced as observations of the Bohrium Science Space App; no ownership of the product interface is claimed.
