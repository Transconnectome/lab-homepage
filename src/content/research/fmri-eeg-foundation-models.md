---
title: "fMRI & EEG Foundation Models"
titleKo: "fMRI 및 EEG 파운데이션 모델 (NeuroMamba, SwiFT, DIVER-0)"
tagline: "Pioneering state-space models and channel-equivariant architectures for 4D neural dynamics."
category: "foundation-models"
featured: true
order: 2
keyHighlights:
  - "[NeuroMamba](https://jubilant-choi.notion.site/neuromamba-neurips2025): First State-Space Foundation Model for 4D functional MRI (NeurIPS 2025 Brain & Body Workshop, Spotlight)"
  - "[DIVER-0](https://arxiv.org/abs/2507.14141): Fully Channel-Equivariant EEG Foundation Model (ICML 2025 GenBio Workshop, Spotlight)"
  - "[SwiFT](https://doi.org/10.52202/075280-1820) & SwiFT IO: Scalable 4D Swin Transformer architecture for resting-state and task fMRI"
  - "[Frequency-Specific Multi-Band Attention](https://doi.org/10.48550/arXiv.2503.23394) for long-range spatial brain dynamics"
---

## Groundbreaking Architectures for 4D Brain Signals

Biological neural signals possess unique spatial symmetries, continuous temporal flows, and non-Euclidean geometries that challenge conventional computer vision and NLP architectures. Connectome Lab pioneers customized deep learning paradigms designed from first neuroscientific principles:

### 1. [NeuroMamba](https://jubilant-choi.notion.site/neuromamba-neurips2025): State-Space Foundation Model for fMRI
- **Authors**: Jubin Choi et al. (NeurIPS 2025 Foundation Models for Brain and Body - **Spotlight**)
- **Core Innovation**: Overcomes the quadratic computational complexity of Transformers in handling long continuous 4D fMRI scans by integrating selective State-Space Models (Mamba). Enables efficient linear-time context modeling across tens of thousands of volumetric brain voxels over thousands of time frames.

### 2. [DIVER-0](https://arxiv.org/abs/2507.14141): Fully Channel-Equivariant EEG Foundation Model
- **Authors**: Dongyeop Han, Ahhyun Lee, Taeyang Lee, Sebin Lee et al. (ICML 2025 GenBio - **Spotlight**)
- **Core Innovation**: Solves the notorious electrode montage mismatch problem across clinical and research EEG datasets by ensuring strict spatial equivariance over arbitrary channel layouts.

### 3. Spatiotemporal Multi-Band Dynamics
- **Authors**: Sangyoon Bae et al. ([arXiv:2503.23394](https://doi.org/10.48550/arXiv.2503.23394))
- **Core Innovation**: Novel frequency-specific multi-band attention mechanisms that disentangle canonical neural oscillation bands within low-frequency hemodynamic fluctuations in fMRI.
