# Bohrium reading assistant — follow-up derived transcript

This is a faithful rendering of the second visible answer in app-followup-complete-ax.txt. The raw full AX state contains both rounds. UI wrappers and duplicate headings/list containers were removed; equation glyphs were joined into ordinary notation. No answer correction was applied in this file. The first answer remains unchanged in app-answer.md.

The follow-up explicitly supplied the two corrections identified by an independent source check in this task. This is assisted revision after external feedback, not unprompted self-correction. The App displayed 33s for this response; no end-to-end duration or summed 99-second cost is inferred. Model/version, token use and billed cost are not visible.

## Exact follow-up request

Please recheck two scope statements in your answer against this PDF. Page 5 discusses a “technical replicate”; clarify that this is different from independent patients, rather than saying nothing about replicates occurs. Page 2 also discusses read-level models, so clarify whether SCnorm is really the only relevant discussion of non-UMI/read-level data. Keep the three main conclusions only where supported, give exact page/section evidence, and explicitly identify any wording you revise. Do not use outside sources or run data analysis.

## Visible assistant answer

I rechecked both passages against the PDF. Both points are valid, and I've made two corrections to my earlier wording. Here are the three conclusions with the corrected evidence.

### Corrections to my earlier wording

Revision 1 (Question 1). I previously wrote: "The only reference to non-UMI data is about a different tool … SCnorm." That was too narrow. I revise it to: SCnorm is one of several non-UMI/read-level mentions, not the only one. The paper also discusses (a) historical read-level single-cell strategies on p. 2 and (b) bulk read-count methods (DESeq/edgeR) on p. 11. None of these is a claim that sctransform applies to read-level or TPM data.

Revision 2 (Question 2). I previously wrote: "Nothing about biopsies, patients, or replicate design — those terms do not occur." That was imprecise. I revise it to: the words "biopsy" and "patient" do not occur, but the paper does use the word "replicate" once, in the specific sense of a technical replicate (p. 5). I now distinguish that concept from independent patients.

### 1. Does the paper support applying sctransform to both inputs?

Conclusion (unchanged, supported): The paper supports sctransform for the 10x UMI input, but not for the Smart-seq2 TPM input.

Evidence. The method is scoped to UMI counts: "Our approach can be applied to any UMI-based scRNA-seq dataset" (p. 1, Abstract); "our procedure can apply widely to any UMI-based scRNA-seq experiment" (p. 8, Results); "We explicitly model the UMI counts for a given gene using a generalized linear model" (p. 11, Methods). "Smart-seq2" and "TPM" never appear in the paper.

Revised scope note. Non-UMI/read-level data is discussed in three places, all referring to other methods or historical context, never to sctransform's own applicability:

- p. 2, Introduction: "initial strategies focused on read-level (instead of UMI-level) data and modeled the measurement of each cell as a mixture of two components" — a description of earlier approaches, contrasted with the UMI-based NB strategies the paper builds on.

- p. 3, Results: "the authors of SCnorm [6] reached similar conclusions in the normalization of non-UMI-based single-cell RNA-seq data" — about SCnorm, not sctransform.

- p. 11, Methods: "DESeq [23] uses the negative binomial distribution for read count data" — bulk RNA-seq methods cited as inspiration.

So the paper contains more than one read-level/non-UMI discussion, but none extends sctransform's own scope beyond UMI counts.

What remains unknown: whether TPM or raw Smart-seq2 read counts could validly be coerced into the model; the paper does not address this.

### 2. Does "six biopsies" establish six independent patients?

Conclusion (unchanged, supported): No. The number of biopsies does not by itself establish the number of independent patients.

Revised evidence. The words "biopsy" and "patient" do not occur in the paper. The main dataset is from a single individual: "33k PBMCs from a Healthy Donor, v1 Chemistry" (p. 14, Availability of data and materials).

The word "replicate" appears once, on p. 5, and it means a technical replicate, not a patient: "the data from each droplet represents a technical replicate of a bulk RNA sample. There is no biological variation in this sample" (p. 5, Results). Here "technical replicate" refers to multiple droplets profiled from one bulk RNA sample — repeated measurements of the same biological material. This is a different concept from independent patients (biological replicates/subjects), and the paper does not use the term in the latter sense or discuss patient-level independence.

What follows from the scenario: six biopsies are six specimens; they could come from one patient, six patients, or a mix, so independence is not established by the count alone.

What remains unknown: the biopsy-to-patient mapping and whether the specimens are biologically independent. The paper offers no basis for resolving this.

### 3. Can Pearson residuals be interpreted as comparable expression levels across genes?

Conclusion (unchanged, supported): Only as variance-stabilized, standardized deviations on a common scale — not as absolute expression levels.

Evidence. "We utilize the Pearson residuals … effectively representing a variance-stabilizing transformation (VST), where both lowly and highly expressed genes are transformed onto a common scale" (p. 5, Results); residuals are "effectively standardized expression values" (p. 6, Results); non-variable genes have residual variance "peaks at 1" (p. 7, Fig. 4). The residual is a gene-specific standardized deviation, 


```text
z_ij = (x_ij − μ_ij) / σ_ij
```


(p. 11, Methods), i.e., "how many gene-specific SDs above/below expectation," not "same number of transcripts." For PCA the paper re-standardizes anyway: "We centered and scaled all 16K genes" (p. 13, Methods).

No wording in this section needed revision.
