# Bohrium Science Space reading assistant — derived visible transcript

This is a faithful Markdown rendering of the complete accessibility export, not native model telemetry. Source: the round-1 nodes of app-followup-complete-ax.txt (identical text; v1.0-v1.2 also shipped a separate round-1 export, removed in v1.3 as a duplicate); export-provenance.json records the round-1 capture time. UI wrappers and duplicate heading nodes were removed; the displayed equation was reconstructed from its AX glyph nodes as z_ij = (x_ij − μ_ij) / σ_ij. The answer wording, qualifications and errors are otherwise retained. Corrections belong to verification.md, not to this transcript.

Observed UI: processed in 1m 6s; prompt timestamp 02:24 AM and answer timestamp 02:25 AM on 2026-10-30 (UTC+8). The model/version, token use and billed cost are not shown in the captured view. This is a single real App session, not a controlled comparison.

## Exact request

Use only this PDF for a source-grounded reading check. Constructed scenario: I have six tumour biopsies measured with 10x UMI counts, plus a separate Smart-seq2 TPM matrix. Does the paper support applying sctransform to both inputs? Does “six biopsies” establish six independent patients? Can Pearson residuals be interpreted as comparable expression levels across genes? For each answer, distinguish what the paper states, what follows from the scenario, and what remains unknown. Give the original page/section and one short exact quotation where possible. Do not run data analysis, install software, launch compute, or read unrelated local files.

## Visible assistant answer

I've read only the provided parsed PDF (197 blocks, pages 1–14). Below are the three grounded answers. I quote the paper's exact wording and mark where each claim comes from.

### 1. Does the paper support applying sctransform to both inputs (10x UMI counts and a Smart-seq2 TPM matrix)?

What the paper states. The method is explicitly scoped to UMI count data, not to any continuous or read-level matrix. The Abstract says, "Our approach can be applied to any UMI-based scRNA-seq dataset" (p. 1, Abstract). The Results restate the same boundary: "our procedure can apply widely to any UMI-based scRNA-seq experiment" (p. 8, Results). The model itself is built on integer molecule counts with a negative-binomial GLM: "We explicitly model the UMI counts for a given gene using a generalized linear model" (p. 11, Methods), using per-cell sequencing depth (sum of molecules) as the covariate. The Discussion likewise frames it as "normalization and variance stabilization of single-cell UMI datasets" (p. 10, Discussion).

The paper's five validation datasets are described as "five UMI datasets from diverse tissues, generated with both plate- and droplet-based protocols" (p. 2, Results) — so "plate-based" here still means plate-based UMI protocols, not full-length non-UMI libraries. The words "Smart-seq2" and "TPM" never appear anywhere in the paper. The only reference to non-UMI data is about a different tool, not sctransform: "SCnorm [6] reached similar conclusions in the normalization of non-UMI-based single-cell RNA-seq data" (p. 3, Results).

What follows from the scenario. A 10x UMI count matrix is UMI-based, so it falls within the paper's stated scope. A Smart-seq2 TPM matrix is not: TPM is a continuous, length-normalized value, not integer UMI counts, and Smart-seq2 is a full-length (non-UMI) protocol. The negative-binomial GLM in the Methods assumes count observations and a per-cell total-molecule depth covariate, which a TPM matrix does not provide.

What remains unknown. The paper is silent on whether TPM (or raw Smart-seq2 read counts) could be coerced into the model and still be valid; there is no empirical demonstration for full-length/non-UMI data. So the paper supports sctransform for the 10x UMI input, but it does not support applying it to the Smart-seq2 TPM input.

### 2. Does "six biopsies" establish six independent patients?

What the paper states. Nothing about biopsies, patients, or replicate design — those terms do not occur. The paper's main dataset is from a single individual: "33k PBMCs from a Healthy Donor, v1 Chemistry" (p. 14, Availability of data and materials). Its unit of analysis throughout is cells and genes, not specimens or subjects. The only remotely relevant statement is an assumption about heterogeneity: "we make an implicit assumption that the majority of genes in the dataset do not exhibit significant biological variation … may be overly simplistic when performing scRNA-seq on a highly heterogeneous sample" (p. 10, Discussion).

What follows from the scenario. "Six biopsies" means six physical specimens. That alone does not establish six independent patients: six biopsies could come from one patient, one each from six patients, or some other combination. The count of specimens is not the same as the count of independent biological replicates.

What remains unknown. The biopsy-to-patient mapping and whether the specimens are biologically independent. The paper provides no criterion for this and makes no claim that its conclusions transfer to a multi-patient or multi-biopsy design; with six specimens and no stated independence structure, the patient-level sample size cannot be determined from the scenario.

### 3. Can Pearson residuals be interpreted as comparable expression levels across genes?

What the paper states. Yes, in the specific sense of a variance-stabilized, standardized scale — not as absolute abundance. The Results say: "We utilize the Pearson residuals (response residuals divided by the expected standard deviation), effectively representing a variance-stabilizing transformation (VST), where both lowly and highly expressed genes are transformed onto a common scale" (p. 5, Results). They are described as "effectively standardized expression values" (p. 6, Results), and the figure caption states that non-variable genes have residual variance "peaks at 1" (p. 7, Fig. 4). They are also stated to be usable downstream: "Pearson residuals are independent of sequencing depth and can be used for variable gene selection, dimensional reduction, clustering, visualization, and differential expression" (p. 5, Results).

Crucially, the residual is a gene-specific standardized deviation,


```text
z_ij = (x_ij − μ_ij) / σ_ij
```


(p. 11, Methods). So "comparable across genes" means "how many gene-specific standard deviations above or below its expected value," not "same number of transcripts." The paper claims unit variance for the majority of (non-variable) genes and treats variance greater than 1 as biological signal.

What follows from the scenario. "Comparable expression levels across genes" is supported only if read as "standardized/relative expression on a common scale." It is not supported as "absolute expression magnitudes in the same units across genes"; the paper does not claim residuals recover absolute transcript abundance.

What remains unknown. Whether residual magnitudes can be treated as directly comparable across genes in an absolute sense is not addressed. Notably, for DE the paper uses residuals directly, but for PCA it re-standardizes: "We centered and scaled all 16K genes" before PCA (p. 13, Methods, Dimensionality reduction), so the paper itself applies an additional per-gene scaling for at least one downstream use.
