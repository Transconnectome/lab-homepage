---
title: "The Neuro-X Project: Brain Foundation Models"
titleKo: "Neuro-X 프로젝트: 뇌 파운데이션 모델"
tagline: "We develop a range of brain foundation models suited to fMRI and EEG, learning from brain activity for use with new datasets and tasks."
category: "foundation-models"
featured: true
order: 1
keyHighlights:
  - "[SwiFT](https://doi.org/10.52202/075280-1820) and [SwiFUN](https://doi.org/10.1162/imag_a_00440): learning fMRI patterns across space and time, and predicting task activation"
  - "[MBBN](https://doi.org/10.1038/s42003-026-10011-7): frequency-resolved brain dynamics (Communications Biology, 2026)"
  - "[NeuroMamba](https://neurips.cc/virtual/2025/132664): state-space modeling for fMRI (NeurIPS 2025 Brain & Body workshop, Spotlight)"
  - "[DIVER-0](https://arxiv.org/abs/2507.14141): EEG modeling across channel configurations (ICML 2025 GenBio workshop, Spotlight). [DIVER-1](https://doi.org/10.48550/arxiv.2512.19097) extends the work to intracranial EEG"
---

Neuro-X is a research program developing a range of foundation models suited to different brain signals and research goals. We aim to learn features from large brain datasets that can support tasks such as cognitive-state analysis and mental-health research.

fMRI captures spatial patterns across the brain and their changes over time. EEG records rapid neural activity, but electrode configurations vary across datasets. We design models around these differences and evaluate whether what they learn transfers to new people and data.

### Learning spatial and temporal patterns in fMRI

[SwiFT](https://doi.org/10.52202/075280-1820) learns spatial and temporal patterns from fMRI without first reducing it to averages over predefined brain regions. Its successor, [SwiFUN](https://doi.org/10.1162/imag_a_00440), predicts task-evoked brain activity from resting-state fMRI.

[MBBN](https://doi.org/10.1038/s42003-026-10011-7) learns from separate frequency bands in fMRI to analyze brain-activity patterns relevant to cognitive and mental-health prediction. [NeuroMamba](https://neurips.cc/virtual/2025/132664) uses state-space modeling to process long spatiotemporal recordings efficiently.

### Learning from EEG across recording settings

[DIVER-0](https://arxiv.org/abs/2507.14141) addresses differences in EEG channel configurations. It is designed so that outputs follow changes in channel order, and was evaluated on emotion recognition and motor-imagery classification. [DIVER-1](https://doi.org/10.48550/arxiv.2512.19097) extends this work to intracranial EEG for cognitive tasks and seizure detection.

Building on these models, we study how brain-signal analysis can adapt to new recording settings and limited training data. Combining information from different kinds of brain recordings is another direction within the program.
