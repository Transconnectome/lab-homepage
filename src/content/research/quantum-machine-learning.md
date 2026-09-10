---
title: "Quantum Machine Learning for Neuroimaging and Time-Series"
titleKo: "뉴로이미징과 시계열을 위한 양자 머신러닝(QML)"
tagline: "We study hybrid quantum–classical models for brain signals and methods for reliable computation on noisy quantum devices."
category: "qml"
featured: true
order: 3
keyHighlights:
  - "[Quantum Time-series Transformer](https://doi.org/10.1109/QCE65121.2025.00256): fMRI time-series analysis (IEEE QCE 2025)"
  - "[Q-DIVER](https://arxiv.org/abs/2603.28122): combining pretrained EEG models with quantum circuits"
  - "[Multi-chip ensembles](https://arxiv.org/abs/2505.08782): learning with combinations of smaller quantum circuits"
  - "[IBM quantum device study](https://arxiv.org/abs/2607.17705): image classification on real hardware"
---

Quantum machine learning uses quantum circuits to learn from data. We design models for complex time series such as fMRI and EEG, and examine how circuit structure and device noise affect learning.

### Brain time-series analysis

The [Quantum Time-series Transformer](https://doi.org/10.1109/QCE65121.2025.00256) represents relationships across time using quantum operations and applies them to fMRI analysis. [Q-DIVER](https://arxiv.org/abs/2603.28122) combines a pretrained EEG model with quantum circuits and searches for circuit designs suited to motor-imagery classification. Both studies evaluated model design and performance in simulation.

### Circuit training and hardware

Our [multi-chip ensemble study](https://arxiv.org/abs/2505.08782) proposes dividing computation among smaller circuits and combining their outputs. It evaluates training stability under simulated noise. A separate [IBM quantum device study](https://arxiv.org/abs/2607.17705) runs a handwritten-digit classifier on real quantum hardware.

We evaluate quantum circuits against conventional neural networks. A quantum advantage on brain data has not yet been established.
