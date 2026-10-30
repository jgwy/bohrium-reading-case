# Independent source check and assisted revision

Date: 30 October 2026 (UTC+8). This check concerns one actual Bohrium Science Space App case and the included 15-page publisher PDF. It is not a scientific rerun or an official grade.

## What the evidence shows

The first answer's three core judgments are supported with qualifications:

1. UMI counts are within the paper's stated input scope (pp. 1, 11). The Smart-seq2 TPM question is a constructed application scenario; the paper does not validate that transfer.
2. Six biopsies do not establish six independent patients. This is reasoning about missing target metadata; the paper's healthy-donor dataset (p. 14) cannot supply the target mapping.
3. Residuals have a common standardized scale (p. 5), defined by a gene-specific expectation and standard deviation (p. 11), not absolute expression units. PCA additionally centers/scales genes (p. 13).

The source-to-answer table is [source-answer-review.tsv](source-answer-review.tsv). Thirteen selected quotation spans were located on their claimed pages, recorded in [quote-page-check.json](quote-page-check.json). This is not a semantic-accuracy percentage.

## Two scope problems were explicitly corrected

The first answer calls SCnorm the only non-UMI discussion. Page 2 also discusses read-level models; p. 11 cites DESeq's negative-binomial read-count method. Its other statement broadly excludes replicate-related discussion, although p. 5 says each droplet is a technical replicate of a bulk RNA sample.

The source check identified these passages, and [the exact follow-up](followup-prompt.txt) supplied them to the App. The App explicitly acknowledged and revised both statements in [the second answer](app-followup-answer.md). [revision-comparison.tsv](revision-comparison.tsv) preserves original wording, external feedback and actual revision. No initial error was overwritten.

Four selected follow-up quotation spans match pp. 2, 3, 5 and 11; see [followup-quote-page-check.json](followup-quote-page-check.json). “Replicate” has one lexical occurrence in normalized text from this supplied PDF. No Smart-seq2, TPM, biopsy or patient match was found there. Those observations do not extend to unavailable supplements or every discussion of the same concepts.

The independent check was performed within this task and then supplied as explicit feedback. This is assisted revision, not spontaneous model self-correction or a claim of human-expert approval.

## Remaining qualifications

- The Fig.4 density peak near variance 1 concerns the null/low-biological-variation setting and an observed gene distribution. It does not make every variance above 1 proven biology.
- The p. 5 independence quotation has a later p. 9 qualification: complete biological/technical independence is not expected because cell types differ in RNA content.
- The second answer keeps the useful standardized-versus-absolute distinction. Its “no wording needed revision” sentence is a product statement, not an independent accuracy certificate.
- The App says it read 197 parsed blocks on pages 1–14; the complete PDF has 15 pages. The independent text search covered all 15. No supplementary full text was available.

## Provenance and effort

The complete raw accessibility exports preserve the actual visible conversation. Older node-truncated snapshots were excluded. Derived Markdown removes only UI wrappers/duplicate labels and reconstructs equation notation. Each screenshot shows a partial view; the raw two-round AX export supplies the full visible wording.

The App badges show 1m 6s and 33s separately. Source reading, correction and interaction effort are not included by summing them. No total wall-time, token cost or actual billing was obtained. Model/version are unavailable in the captured view.

The historical matching used Poppler 26.08.0 text extraction, NFKC normalization, whitespace removal and line-hyphen joining; pypdf 6.10.0 supplied an independent text extraction. Relevant pages 5 and 11 were visually inspected. The reproduction helper implements that matching method without calling a model or modifying evidence.

The case demonstrates real product use and a useful correction process. It does not establish a controlled comparison against other tools, general model superiority or scientific reproduction.
