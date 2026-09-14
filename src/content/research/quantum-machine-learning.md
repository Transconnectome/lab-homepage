---
title: "Quantum Machine Learning for Neuroimaging and Time-Series"
titleKo: "뉴로이미징과 시계열을 위한 양자 머신러닝(QML)"
tagline: "We combine quantum and classical computation to explore new ways of representing and learning relationships in brain signals."
category: "qml"
question: "What possibilities does quantum computation open for representing and learning complex brain signals?"
featured: true
order: 3
keyHighlights:
  - "[Quantum Time-series Transformer](https://doi.org/10.1109/QCE65121.2025.00256): fMRI time-series analysis (IEEE QCE 2025)"
  - "[Q-DIVER](https://arxiv.org/abs/2603.28122): combining pretrained EEG models with quantum circuits"
  - "[Multi-chip ensembles](https://arxiv.org/abs/2505.08782): learning with combinations of smaller quantum circuits"
  - "[IBM quantum device study](https://arxiv.org/abs/2607.17705): image classification on real hardware"
---

What kinds of computation can learn the complex relationships within brain signals? We combine quantum circuits with classical models to explore new ways of representing and learning from those signals. Applying quantum operations to relationships across time and to learned brain representations lets us ask what different computational structures can contribute to learning.

We test these possibilities by varying circuit size, connectivity, and combinations with classical models. Alongside predictive performance, we examine the number of trainable parameters, constraints on scaling circuits, and training stability under noise. Simulations with brain data and real-hardware experiments on separate tasks test computational methods under different conditions.

### Brain time-series analysis

The [Quantum Time-series Transformer](https://doi.org/10.1109/QCE65121.2025.00256) represents relationships across time using quantum operations and applies them to fMRI analysis. [Q-DIVER](https://arxiv.org/abs/2603.28122) combines a pretrained EEG model with quantum circuits and searches for circuit designs suited to motor-imagery classification. Both studies evaluated model design and performance in simulation.

Q-DIVER connects quantum circuits to the readout of an already learned EEG representation. It turns the question of which part of a model to assign to quantum computation into a concrete design problem.

### Circuit training and hardware

Our [multi-chip ensemble study](https://arxiv.org/abs/2505.08782) proposes dividing computation among smaller circuits and combining their outputs. It evaluates training stability under simulated noise. Comparing compression into a single circuit with distributing inputs across smaller circuits lets us examine the relationship between representing information and being able to learn from it.

A separate [IBM quantum device study](https://arxiv.org/abs/2607.17705) runs a handwritten-digit classifier on real quantum hardware.

We evaluate quantum circuits against conventional neural networks. A quantum advantage on brain data has not yet been established.
