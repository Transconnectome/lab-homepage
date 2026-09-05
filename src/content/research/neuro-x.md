---
title: "The Neuro-X Project: Brain Foundation Models"
titleKo: "Neuro-X 프로젝트: 뇌 파운데이션 모델"
tagline: "fMRI and EEG models built from the properties of the signal, pretrained at scale, and converging on one Large Brain Model."
category: "foundation-models"
featured: true
order: 1
keyHighlights:
  - "[NeuroMamba](https://jubilant-choi.notion.site/neuromamba-neurips2025): state-space foundation model that learns directly from whole-brain 4D fMRI (NeurIPS 2025 Brain & Body workshop, Spotlight)"
  - "[DIVER-0](https://arxiv.org/abs/2507.14141): channel-equivariant EEG foundation model that works across electrode layouts (ICML 2025 GenBio workshop, Spotlight). Its successor [DIVER-1](https://doi.org/10.48550/arxiv.2512.19097) extends the idea to intracranial EEG"
  - "[SwiFT](https://doi.org/10.52202/075280-1820): Swin Transformer trained directly on raw 4D fMRI (NeurIPS 2023). Its successor [SwiFUN](https://doi.org/10.1162/imag_a_00440) predicts task activation from resting-state fMRI (Imaging Neuroscience 2025)"
  - "[MBBN](https://doi.org/10.1038/s42003-026-10011-7): frequency-band attention over fMRI dynamics that improves prediction of depression, ADHD and autism and finds band-specific signatures of ADHD and autism (Communications Biology 2026)"
  - "Next: a multimodal Large Brain Model that learns fMRI, EEG, diffusion MRI and polygenic scores in one latent space"
---

## The goal

Neuro-X is the lab's brain foundation model program. Its premise is borrowed from large language models: if an LLM can learn the structure of language from a large body of text, a model pretrained on large brain datasets (fMRI, EEG, diffusion MRI) should be able to learn the structure of brain activity. We call the endpoint a Large Brain Model (LBM).

The theoretical starting point is György Buzsáki's inside-out view of the brain. The brain does not transcribe stimuli handed to it from outside; it generates its own action plans and learns from their consequences, which makes it a prediction machine. On that view, the structure of brain activity lives in the signal itself rather than in labels people assign to it, so we favor pretraining that learns the signal's spatiotemporal structure over training that only fits labels.

Reading the structure of brain activity as completely as a grammar is still far off, and the work here is narrower. We design architectures that fit brain signals, pretrain them on large datasets, and judge the learned representations by how well they predict cognitive states and psychiatric risk.

## Why brain signals need their own architectures

An fMRI scan is a 4D signal, three spatial dimensions plus time: tens of thousands of voxels (3D pixels) changing over hundreds to thousands of frames. EEG is recorded at millisecond resolution, which gives it fine timing, but the number and placement of electrodes differ from one dataset to the next. Both signals combine the brain's spatial layout with a signal that is continuous in time, and that structure has to be built into the architecture. This is why architectures from computer vision and natural language processing do not transfer unchanged.

## Models so far

### fMRI: from transformers to state-space models

[SwiFT](https://doi.org/10.52202/075280-1820) (Peter Kim, Junbeom Kwon et al., NeurIPS 2023) is a Swin Transformer that takes raw 4D fMRI volumes as input, with no preprocessing step that first summarizes the brain into regions. With it we showed that representations can be learned directly from the raw volumes.

Its successor [SwiFUN](https://doi.org/10.1162/imag_a_00440) (Junbeom Kwon, Jungwoo Seo, Heehwan Wang et al., Imaging Neuroscience 2025) predicts maps of task-evoked brain activity from resting-state fMRI, the scans taken while a person lies in the scanner doing nothing in particular. The question behind it is how much of the task response is already present in the resting signal.

[MBBN](https://doi.org/10.1038/s42003-026-10011-7) (Multi-Band Brain Net; Sangyoon Bae, Junbeom Kwon et al., Communications Biology 2026) splits the fMRI signal into frequency bands and gives each band its own attention, so the model can learn dynamics that differ from one band to the next. Trained on 49,673 people from UK Biobank, ABCD and ABIDE, it improved prediction of depression, ADHD and autism, and for ADHD and autism it showed which connections in which bands change.

[NeuroMamba](https://jubilant-choi.notion.site/neuromamba-neurips2025) (Jubin Choi, David Keetae Park, Junbeom Kwon et al., Spotlight at the NeurIPS 2025 workshop on Foundation Models for the Brain and Body) replaces the transformer's attention with a selective state-space model (Mamba). Attention's cost grows with the square of the input length; Mamba's grows only in proportion to it, and discarding the non-brain background tokens before training cuts the cost almost in half again. That made pretraining on whole-brain fMRI from more than 50,000 people in UK Biobank, ABCD and HCP tractable, and after fine-tuning, a 3.1M-parameter model scored higher on HCP sex classification than SwiFT's published 4.6M-parameter result, though on a different train/test split. Cognitive scores and clinical diagnoses are the next targets.

### EEG: models that do not depend on the electrode layout

[DIVER-0](https://arxiv.org/abs/2507.14141) (Dong Yeop Han, Ahhyun Lee, Taeyang Lee et al., Spotlight at the ICML 2025 GenBio workshop) builds equivariance to channel permutation and to shifts in time into the architecture: reorder the channels or slide the window and the output follows. That lets it adapt to electrode layouts it never saw in pretraining, so the differing layouts of clinics and labs can be handled by one model, and it reached competitive performance with only a tenth of the pretraining data.

[DIVER-1](https://doi.org/10.48550/arxiv.2512.19097) (Dong Yeop Han et al., 2025) carries the same principle to intracranial EEG. A model that assumes no fixed electrode layout was pretrained on 5,310 hours of ECoG and SEEG recordings and outperformed earlier intracranial EEG foundation models on cognitive decoding and seizure detection benchmarks. A scaling study up to 1.8 billion parameters found that collecting more recordings and training long enough raised performance more reliably than adding parameters.

## What comes next

Three directions remain open. The first is dynamic functional connectomics. Instead of fixing the relations between brain regions in a single correlation matrix, we want time-varying attention patterns that read out short-lived cognitive states, emotional transitions, and subtle neuropathological shifts.

The second is a multimodal model that combines fMRI for its spatial resolution, EEG for its temporal resolution, diffusion MRI for the structural scaffold, and polygenic scores in one latent space. [Mind the Gap](https://doi.org/10.48550/arXiv.2502.12771) (Dong Yeop Han et al., 2025) predicted brain responses to speech from the representations of pretrained language and audio models and found that a nonlinear model combining the two predicts them better than a linear mapping from either alone. We take that result as a reason to expect the same when brain signals are combined with each other.

The third is representations that adapt to new tasks from little data. Cognitive state decoding, psychiatric risk stratification, and generative simulation of brain activity are the tests.
