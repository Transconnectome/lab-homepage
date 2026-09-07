---
title: "Computational Psychiatry & Multi-Modal Genetics"
titleKo: "계산정신의학 및 다중오믹스-뇌연결성 유전체 연구"
tagline: "Across complementary studies, we test what polygenic scores add to maps of the developing brain, family history, and youth mental-health prediction—and where the evidence remains non-causal or clinically limited."
category: "genetics"
featured: true
order: 2
keyHighlights:
  - "Covariance map—not diagnosis: 33 polygenic scores, seven imaging modalities, and 266 phenotypes; primary N=6,555 and exploratory N=8,620 ([Nature Communications, 2025](https://doi.org/10.1038/s41467-025-63312-6))"
  - "Statistical mediation—not a causal pathway: depression PGS was estimated to mediate 1.39–5.87% of the observed family-history association; in one model, explained variance changed from 2.41% to 2.59% ([Molecular Psychiatry, 2025](https://doi.org/10.1038/s41380-025-03221-8))"
  - "Initial transfer test—not clinical validation: a PGS-supervised white-matter model reported AUROC 0.61–0.66 in separate ABCD subsets and 0.67 in an independent Korean sample of 108 youths ([Communications Medicine, 2026](https://doi.org/10.1038/s43856-026-01828-8))"
---

## The question: what can genetics add without mistaking association for explanation?

These studies ask three related but distinct questions in children and adolescents. Where do distributed genetic differences covary with brain and behavioral measures? How much does a child's polygenic score add to a reported family history? Can genetic information used during model training improve brain-imaging prediction in a separate sample?

Each question requires a different standard of evidence. A multivariate association maps variables that change together. A mediation model partitions an observed association under assumptions. A held-out or external cohort tests prediction. None of these designs, by itself, identifies a causal developmental pathway or establishes a clinically useful test.

## Why connect genes, brain, and context?

A polygenic score (PGS) aggregates small estimated effects across many common genetic variants. It ranks relative genetic liability within a population; it is not a diagnosis. MRI supplies measured brain features that may correlate with genetic and behavioral differences. Family history and environmental measures may add familial and contextual information not captured by a child's current PGS.

The method therefore follows the question: sparse multivariate models for mapping many correlated measures, mediation analysis for estimating how much of an observed family-history association is statistically consistent with a measured PGS, and PGS-supervised representation learning for testing whether a white-matter pattern predicts outcomes in separate samples.

## Three studies, three levels of evidence

### 1. Mapping what varies together

In [*Nature Communications* (2025)](https://doi.org/10.1038/s41467-025-63312-6), the researchers analyzed ABCD baseline data using 33 PGS, seven neuroimaging modalities, and 266 cognitive and psychological phenotypes. After imaging and genetic quality control, the primary analysis included 6,555 children of European ancestry; an exploratory multi-ancestry analysis included 8,620 children.

Sparse generalized canonical correlation analysis identified multivariate covariance patterns. Cognitive-related PGS tended to load in the same direction as structural MRI, diffusion MRI, and some task-fMRI measures, whereas PGS related to depression, ADHD, neuroticism, and other health risks often loaded in the opposite direction. Functional measures showed associations with a wider range of family and socioeconomic variables than structural measures in this dataset.

These are cross-sectional, mainly linear associations—not temporal or causal mechanisms. In simpler bivariate analyses, PGS for ADHD, depression, and PTSD explained no more than about 3% of their corresponding trait variance. The primary analysis was restricted to European-ancestry children, and PGS do not measure transcriptomic, epigenomic, or proteomic variation. Despite the current research-axis name, this study is therefore not evidence of a completed multi-omics analysis.

### 2. Estimating what PGS adds to family history

In [*Molecular Psychiatry* (online 2025)](https://doi.org/10.1038/s41380-025-03221-8), 8,111 nine- to ten-year-olds had complete genotype, caregiver-reported multigenerational family-history, and diagnostic data. Of 30 PGS, the depression score was the only one associated with both a multigenerational history of depression and offspring psychopathology.

Across the tested outcomes, mediation models estimated that the depression PGS accounted for 1.39–5.87% of the observed family-history association. The absolute increment was small: in one reported diagnostic model, family history alone explained 2.41% of variance, compared with 2.59% for family history plus PGS.

Statistical mediation in cross-sectional data is not evidence that the PGS causes intergenerational transmission. Parent and grandparent genotypes were unavailable, so direct inheritance could not be separated from indirect genetic effects such as genetic nurture. Family history was also reported retrospectively by caregivers, and discovery GWAS were weighted toward European-ancestry samples.

### 3. Testing a genetically supervised imaging predictor

In [*Communications Medicine* (2026)](https://doi.org/10.1038/s43856-026-01828-8), depression-related PGS were used as supervision to pretrain a 3D convolutional model on track-weighted white-matter fractional anisotropy from 4,741 ABCD participants. The learned imaging representation was then fine-tuned in separate cross-sectional and two-year follow-up subsets to predict depression and suicidality.

The authors report higher AUROC than genetics-only, imaging-only, and non-pretrained comparison models. AUROC was 0.61–0.66 in the separate ABCD prediction tasks and 0.67 in one independent Korean sample of 108 youths. This is initial transfer evidence from one small external cohort, not an independent replication or a clinical validation.

The discrimination remains limited, the external sample is small, and the model omits environmental measures. Diffusion MRI also has difficulty resolving crossing fibers and carries acquisition costs. The reported model is neither a diagnostic test nor a screening tool.

## What the sequence contributes

Read together, the studies move from a population-level covariance map, to a small statistical mediation estimate, to a PGS-supervised imaging prediction test outside its training sample. The progression matters because the claims do not collapse into one another: association is not mediation, mediation is not causation, and better performance than a comparison model is not clinical readiness.

Stronger evidence would require longitudinal designs that establish temporal order, ancestry-diverse discovery data and family genotypes, models that measure environmental exposures alongside biology, and prospective evaluation of calibration and decision benefit before clinical use.

## Why the connectome matters here

The connectome is not assumed to be a causal bridge between genes and symptoms. It is a measured brain phenotype—and, in the prediction study, a learned imaging representation—whose added value must be tested against simpler genetic, familial, and environmental information. That constraint is what turns an appealing gene-to-brain story into a falsifiable research program.
