---
title: "The Neuro-X Project: Brain Foundation Models"
titleKo: "Neuro-X 프로젝트: 뇌 파운데이션 모델"
tagline: "We build models around fMRI patterns across space and time and EEG channel configurations, examining how they learn information related to cognition, emotion and behavior."
category: "foundation-models"
question: "How can AI trained on brain data help us understand and predict cognition, emotion, and behavior?"
featured: true
order: 1
keyHighlights:
  - "[SwiFT](https://doi.org/10.52202/075280-1820) and [SwiFUN](https://doi.org/10.1162/imag_a_00440): learning fMRI patterns across space and time, and predicting task activation"
  - "[MBBN](https://doi.org/10.1038/s42003-026-10011-7): frequency-resolved brain dynamics (Communications Biology, 2026)"
  - "[NeuroMamba](https://neurips.cc/virtual/2025/132664): state-space modeling for fMRI (NeurIPS 2025 Brain & Body workshop, Spotlight)"
  - "[DIVER-0](https://arxiv.org/abs/2507.14141): EEG modeling across channel configurations (ICML 2025 GenBio workshop, Spotlight). [DIVER-1](https://doi.org/10.48550/arxiv.2512.19097) extends the work to intracranial EEG"
---

Neuro-X studies AI that can help us understand and predict human cognition, emotion, behavior, and their changes through brain activity. Our goal is to apply patterns learned from diverse brain data to new people and tasks. We develop a range of foundation models suited to different brain signals and research goals.

Brain activity varies across space and time, and fMRI and EEG record different aspects of it. Models designed around these differences predict cognitive states and mental-health measures; we also analyze what the patterns used for prediction reveal about relationships between brain and behavior. Choices about signal summaries, frequency bands, and electrode configurations serve this goal. Evaluation with new people and recording settings tests where the models can be used.

### Learning spatial and temporal patterns in fMRI

[SwiFT](https://doi.org/10.52202/075280-1820) learns spatial and temporal patterns from fMRI without first reducing it to averages over predefined brain regions. Its successor, [SwiFUN](https://doi.org/10.1162/imag_a_00440), predicts task-evoked brain activity from resting-state fMRI.

In adult UK Biobank and child ABCD data, SwiFUN achieved higher overall similarity between predicted and measured maps than the connectivity-based comparison model, ConnTask. ConnTask performed better at identifying individuals. Predicting shared response patterns and preserving individual specificity therefore require separate evaluation.

[MBBN](https://doi.org/10.1038/s42003-026-10011-7) learns from separate frequency bands in fMRI to analyze brain-activity patterns relevant to cognitive and mental-health prediction. It examines how distinguishing different timescales changes the information used for prediction. [NeuroMamba](https://neurips.cc/virtual/2025/132664) uses state-space modeling and removal of non-brain background tokens to reduce the computational cost of fMRI learning. The public study evaluates sex classification; extending it to cognition and mental health remains a goal for further testing.

### Learning from EEG across recording settings

[DIVER-0](https://arxiv.org/abs/2507.14141) addresses differences in EEG channel configurations. It is designed so that outputs follow changes in channel order, and was evaluated on emotion recognition and motor-imagery classification. [DIVER-1](https://doi.org/10.48550/arxiv.2512.19097) extends this work to intracranial EEG for cognitive tasks and seizure detection.

Building on these models, we study how brain-signal analysis can adapt to new recording settings and limited training data. Combining information from different kinds of brain recordings is another direction within the program.
