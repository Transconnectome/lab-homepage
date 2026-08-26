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
  - "Undergraduate research internships — no prior quantum background required"
---

## Why quantum, and what actually blocks it

Quantum machine learning is usually sold on asymptotics. The wall we actually hit
is more prosaic: variational circuits on current hardware are noisy, small, and
hard to train. Barren plateaus flatten gradients as circuits widen, device noise
biases every expectation value, and the parameter-shift rule makes on-hardware
training cost climb with every parameter added.

Our work, much of it with **Brookhaven National Laboratory**, runs at that wall along
three threads: make circuits trainable at scale, make them fit real brain signals,
and get them onto real devices.

### 1. Trainable at scale — multi-chip ensembles

- **Authors**: Junghoon Justin Park, Jiook Cha, Samuel Yen-Chi Chen, Huan-Hsin Tseng, Shinjae Yoo — [arXiv:2505.08782](https://doi.org/10.48550/arxiv.2505.08782)
- **Idea**: partition a high-dimensional computation across an ensemble of smaller,
  independently operating quantum chips, entangling only at controlled inter-chip
  boundaries.
- **Result**: mitigates barren plateaus, improves generalization, and — unusually —
  reduces quantum error *bias and variance simultaneously*, with no separate
  error-mitigation pass. Validated on MNIST, FashionMNIST, CIFAR-10, and a
  real-world PhysioNet EEG dataset.
- The same ensemble idea carries into reinforcement learning in
  **It's-A-Me, Quantum Mario** (IEEE QAI 2025), which follows
  **Over the Quantum Rainbow** (IEEE QCE 2024), where variational circuits were
  paired with a Rainbow DQN agent and then explained rather than left as a black box.

### 2. Fitting real brain signals

- **Quantum Time-series Transformer** — Junghoon Justin Park, Jungwoo Seo, Sangyoon Bae,
  Samuel Yen-Chi Chen, Huan-Hsin Tseng, Jiook Cha, Shinjae Yoo (IEEE QCE 2025).
  Classical self-attention costs quadratic time and a parameter budget that
  neuroimaging cohorts cannot always feed. Building attention out of a Linear
  Combination of Unitaries and Quantum Singular Value Transformation brings that
  to polylogarithmic complexity, and holds up with fewer parameters and smaller
  samples. Evaluated on resting-state fMRI from **ABCD** and the **UK Biobank**.
- **Q-DIVER** — Junghoon Justin Park, YeongHyeon Park, Jiook Cha (IEEE QCNC 2026).
  A differentiable quantum classifier sits on top of the lab's pretrained
  **DIVER-1** EEG encoder, and Differentiable Quantum Architecture Search discovers
  the circuit topology during end-to-end fine-tuning rather than fixing an ansatz
  by hand. On PhysioNet Motor Imagery it matches a classical MLP head
  (test F1 63.49%) using roughly **50× fewer task-specific parameters**
  (2.10M vs 105.02M) — a budget a portable BCI could actually carry.
- **HQTCN** — Junghoon Justin Park, Maria Pak, Sebin Lee, Samuel Yen-Chi Chen,
  Shinjae Yoo, Huan-Hsin Tseng, Jiook Cha (IEEE QCNC 2026).
  A hybrid quantum temporal convolutional network: dilated temporal windows are
  sampled into shared quantum circuits, so one circuit reads several time scales
  without a parameter count that grows with the sequence.

### 3. Running on real devices

- **Image Classification on IBM Quantum Computers** — Junghoon Justin Park, Jiook Cha,
  Jun-gyeong Park, Hwidong Yoo, Kwangmin Yu — [arXiv:2607.17705](https://doi.org/10.48550/arxiv.2607.17705).
  Ten-class MNIST, trained and served end-to-end on a **127-qubit IBM Eagle**
  processor. A two-phase protocol separates gradient-based classical optimization
  of the encoder and readout from gradient-free optimization of the quantum
  parameters, removing the parameter-shift cost that makes on-hardware training
  impractical. It is also the first use of Quantum Multi-Programming on a *trained*
  classifier: several copies of the circuit are packed onto one device for parallel
  inference at no cost in mean accuracy.
- **QPATE** (ICASSP 2024) — with William H. Watkins, Heehwan Wang, and Sangyoon Bae —
  carries differential-privacy guarantees into quantum classifiers through private
  aggregation of teacher ensembles.

### Where this is going

Brain data is where the scaling pressure is real. A 4D fMRI scan or a long EEG
montage is exactly the high-dimensional, long-sequence regime in which classical
attention gets expensive and quantum encodings start to look interesting.

None of the results above claims a quantum advantage on brain data today. The claim
is narrower and more useful: circuits that train, that fit the signal, and that run.

We recruit **undergraduate research interns** on this line year-round. Prior
knowledge of quantum mechanics is not required.
