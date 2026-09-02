---
title: "Quantum Machine Learning for Neuroimaging and Time-Series"
titleKo: "뉴로이미징과 시계열을 위한 양자 머신러닝(QML)"
tagline: "Circuits that actually train, fit real brain signals, and run on today's noisy hardware."
category: "qml"
featured: true
order: 4
keyHighlights:
  - "Quantum Time-series Transformer: polylogarithmic-complexity attention applied to resting-state fMRI from ABCD and UK Biobank (IEEE QCE 2025)"
  - "Multi-chip ensemble circuits that mitigate barren plateaus and reduce quantum error bias and variance at the same time (arXiv:2505.08782)"
  - "Q-DIVER: quantum architecture search on a pretrained EEG encoder — classical-MLP F1 with ~50× fewer task-head parameters (IEEE QCNC 2026)"
  - "Ten-class MNIST trained and served end-to-end on a 127-qubit IBM Eagle processor (arXiv:2607.17705)"
---

## Why quantum, and what actually blocks it

Quantum machine learning is usually sold on asymptotics. The wall we actually hit
is more prosaic: variational circuits on current hardware are noisy, small, and
hard to train. Our work, much of it with **Brookhaven National Laboratory**, runs
at that wall along three threads — make circuits trainable at scale, fit them to
real brain signals, and run them on real devices.

### 1. Trainable at scale

[**Multi-chip ensembles**](https://doi.org/10.48550/arxiv.2505.08782) (Junghoon
Justin Park et al.) partition a high-dimensional computation across smaller,
independently operating quantum chips. This mitigates barren plateaus and —
unusually — reduces quantum error bias and variance at the same time, with no
separate error-mitigation pass. The same ensemble idea carries into quantum
reinforcement learning (IEEE QAI 2025, IEEE QCE 2024).

### 2. Fitting real brain signals

The **Quantum Time-series Transformer** (Park, Jungwoo Seo, Sangyoon Bae et al.,
IEEE QCE 2025) builds attention with polylogarithmic complexity and holds up on
smaller parameter and sample budgets, evaluated on resting-state fMRI from
**ABCD** and the **UK Biobank**. **Q-DIVER** (IEEE QCNC 2026) lets differentiable
quantum architecture search find a circuit on top of the lab's pretrained DIVER
EEG encoder, matching a classical MLP head's F1 with roughly **50× fewer
task-specific parameters**. **HQTCN** (IEEE QCNC 2026) samples dilated temporal
windows into shared circuits, so parameters do not grow with sequence length.

### 3. Running on real devices

Ten-class MNIST was [trained and served end-to-end on a **127-qubit IBM Eagle**
processor](https://doi.org/10.48550/arxiv.2607.17705), with a two-phase protocol
that removes the parameter-shift cost of on-hardware training, plus the first use
of quantum multi-programming on a trained classifier. **QPATE** (ICASSP 2024)
carries differential-privacy guarantees into quantum classifiers.

None of these results claims a quantum advantage on brain data today. The claim
is narrower and more useful: circuits that train, that fit the signal, and that
run. We recruit **undergraduate research interns** on this line year-round — no
prior quantum background required.
