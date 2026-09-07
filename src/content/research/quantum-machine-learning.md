---
title: "Quantum Machine Learning for Neuroimaging and Time-Series"
titleKo: "뉴로이미징과 시계열을 위한 양자 머신러닝(QML)"
tagline: "Circuits that actually train, fit real brain signals, and run on today's noisy hardware."
category: "qml"
featured: true
order: 3
keyHighlights:
  - "[Quantum Time-series Transformer](https://doi.org/10.1109/QCE65121.2025.00256): polylogarithmic-complexity attention applied to resting-state fMRI from ABCD and UK Biobank (IEEE QCE 2025)"
  - "[Multi-chip ensemble circuits](https://arxiv.org/abs/2505.08782) that mitigate barren plateaus and reduce quantum error bias and variance at the same time"
  - "[Q-DIVER](https://arxiv.org/abs/2603.28122): on one EEG benchmark, the authors report comparable F1 with a task head of 2.10M versus 105.02M parameters (~50×); total trainable parameters drop by a factor of ~2.9 and most head parameters remain classical"
  - "[IBM Eagle feasibility study](https://arxiv.org/abs/2607.17705): a 12-qubit classifier was deployed on a 127-qubit device; four-way inference used 48 qubits, hardware fine-tuning gave no measurable gain, and a matched classical model performed better"
---

## Why quantum, and what actually blocks it

Quantum machine learning is usually sold on asymptotics. The wall we actually hit
is more prosaic: variational circuits on current hardware are noisy, small, and
hard to train. Several of the cited projects include coauthors from **Brookhaven
National Laboratory**. The work runs at that wall along three threads — make
circuits trainable at scale, fit them to real brain signals, and test them on
real devices.

### 1. Trainable at scale

[**Multi-chip ensembles**](https://doi.org/10.48550/arxiv.2505.08782) (Junghoon
Justin Park et al.) partition a high-dimensional computation across smaller,
independently operating quantum chips. This mitigates barren plateaus and —
unusually — reduces quantum error bias and variance at the same time, with no
separate error-mitigation pass. The same ensemble idea carries into quantum
reinforcement learning (IEEE QAI 2025, IEEE QCE 2024).

The evidence combines theory with benchmark experiments under calibrated,
simulated NISQ noise. The paper analyzes compatibility with current and emerging
hardware; it does not report a multi-device hardware deployment.

### 2. Fitting real brain signals

[The **Quantum Time-series Transformer**](https://doi.org/10.1109/QCE65121.2025.00256) (Park, Jungwoo Seo, Sangyoon Bae et al.,
IEEE QCE 2025) builds attention with polylogarithmic complexity and holds up on
smaller parameter and sample budgets, evaluated on resting-state fMRI from
**ABCD** and the **UK Biobank**. [**Q-DIVER**](https://arxiv.org/abs/2603.28122)
(IEEE QCNC 2026) uses differentiable quantum architecture search on a pretrained
EEG encoder. On one four-class PhysioNet motor-imagery benchmark (109
participants, 64 channels), the paper reports a test F1 of 63.49% and performance
comparable to a classical MLP head. The comparison is not tabulated in the
results table, so it should not be read as an independently established
advantage.

The parameter claim also needs its denominator. The task head falls from
105.02M to 2.10M parameters (about **50×**), but the full trainable model falls
from 156.38M to 53.46M (about **2.9×**). Of the 2.10M-parameter hybrid head,
2.097M parameters belong to a classical projection and 43 to the quantum
circuit. No quantum hardware was used in this study. [**HQTCN**](https://doi.org/10.1109/QCNC69040.2026.00149) (IEEE QCNC 2026)
samples dilated temporal windows into shared circuits, so parameters do not grow
with sequence length.

### 3. Running on real devices

[A ten-class MNIST feasibility study](https://doi.org/10.48550/arxiv.2607.17705)
trained a **12-qubit** classifier primarily on a simulator and deployed it on the
127-qubit `ibm_yonsei` Eagle-r3 processor. Four-way quantum multi-programming
placed four separate 12-qubit circuits on 48 physical qubits. Two hardware
fine-tuning epochs produced no measurable accuracy gain. The best hardware cell
reported 76.89% accuracy, while a parameter-matched classical MLP reported
82.22% on the same 75-image test split. The small split and three-seed design
make this a workflow demonstration, not a broad performance result. [**QPATE**](https://doi.org/10.1109/ICASSP48485.2024.10447786)
(ICASSP 2024) carries differential-privacy guarantees into quantum classifiers.

None of these results establishes a quantum advantage on brain data today. The
supported claim is narrower: the studies test trainability, signal fit, parameter
accounting, and hardware feasibility—and disclose where current quantum models
remain behind matched classical baselines.
