---
title: "Affective Neuroscience: Awe, Memory, and Aesthetic Experience"
titleKo: "정서 신경과학: 경외, 기억, 그리고 미적 경험"
tagline: "The feelings that are hardest to put into words — awe, being moved, remembering — measured, modeled, and occasionally staged."
category: "affective-neuro"
featured: false
order: 4
keyHighlights:
  - "Awe is an ambivalent affect, not a purely positive one — in behavior and in cortex (Communications Psychology, 2025)"
  - "Nine-participant proof of concept: an EEG-derived three-state valence trajectory guided audiovisual generation from participant-provided essays, sketches, and melodies (ACM Multimedia workshop, 2025)"
  - "Generative models of aesthetic style: AesFA (AAAI 2024) and training-free music style transfer on mel-spectrograms (IEEE ICIP 2026)"
  - "Naturalistic stimuli — film, music, VR — as the experimental setting for real affective dynamics"
  - "OB/Scene Focus (2025): an interactive brain-art installation and live EEG affect-decoding demonstration exploring AI-generated music and video"
---

## The hard end of affect

Most affective neuroscience runs on stimuli chosen for experimental control:
static images, isolated faces, single adjectives on a valence scale. The feelings
people actually care about do not arrive that way. Awe, being moved by a piece of
music, the particular colour a memory takes on when you revisit it — these are
mixed, temporally extended, and bound to context.

This axis studies affect at that harder end, with three moves: measure the
feelings that resist a single scale, model the media that evoke them, and
sometimes put the whole apparatus in a room with an audience.

### 1. Awe is ambivalent

- **Authors**: Jinwoo Yi, Dong Yeop Han, Seung-Yeop Oh, Jiook Cha —
  [*Communications Psychology* (2025)](https://doi.org/10.1038/s44271-025-00299-2)
- Awe is usually filed under positive emotion. Across behavior and cortical
  responses, this work finds it is better described as **ambivalent** — carrying
  positive and negative affect at once, rather than sitting at one end of a
  valence axis.
- That matters beyond awe: it is a concrete case where the standard
  one-dimensional valence model loses information that the brain evidently keeps.

### 2. Reconstructing a remembered feeling

- **Revisiting Your Memory: Reconstruction of Affect-Contextualized Memory via
  EEG-guided Audiovisual Generation** — Joonwoo Kwon, Heehwan Wang, Jinwoo Yi,
  Sooyoung Kim, Shinjae Yoo, Yuewei Lin, Jiook Cha
  ([ACM Multimedia workshop, 2025](https://doi.org/10.1145/3746277.3760413)).
- In a nine-participant proof of concept, participants first provided a memory
  essay, sketch, and guiding melody. EEG recorded during recall was used to decode
  a three-state valence trajectory (positive, neutral, or negative); that
  trajectory guided audiovisual generation from the participant-provided
  material. EEG supplied an affect trajectory, not the episodic content.
- Leave-one-participant-out affect decoding reported a weighted F1 of 0.90. In a
  later preference test, however, only five of nine participants preferred the
  correctly ordered affect trajectory to a permuted one. The homogeneous sample
  of right-handed Korean adults aged 22–28 limits generalization, so the study is
  evidence of feasibility rather than validated memory reconstruction.

### 3. Modeling aesthetic style

- **AesFA: An Aesthetic Feature-Aware Arbitrary Neural Style Transfer** —
  Joonwoo Kwon, Soo Young Kim, Yuewei Lin, Shinjae Yoo, Jiook Cha
  ([AAAI 2024](https://doi.org/10.1609/aaai.v38i12.29232)). Style transfer that
  separates aesthetic features by frequency rather than leaning on a heavy
  pretrained encoder.
- **Repurposing Image Diffusion Models for Training-Free Music Style Transfer on
  Mel-Spectrograms** — Heehwan Wang, Joonwoo Kwon, Sooyoung Kim, Jungwoo Seo,
  Shinjae Yoo, Yuewei Lin, Jiook Cha
  ([IEEE ICIP 2026](https://doi.org/10.1109/icip61757.2026.11630156)). An image
  diffusion model, pointed at a mel-spectrogram, transfers musical style with no
  training at all.
- These are not side projects. A generative model of style is a working
  hypothesis about what a stimulus does to a listener or a viewer — which is
  exactly what an affect experiment needs to manipulate.

### 4. Naturalistic settings

Film, music, and virtual reality are how this axis gets ecological validity. The
lab's earlier work on **anticipation of high-arousal film clips**
(*Social Cognitive and Affective Neuroscience*, 2014) established the approach,
and it now runs through VR protocols for anxiety and panic disorder shared with
the computational-psychiatry axis.

### And then, sometimes, a gallery

> *"Study the science of art. Study the art of science. Develop your senses — especially learn how to see. Realize that everything connects to everything else."*
> — **Leonardo da Vinci**

In November 2025, **Seokjin Moon, Heehwan Wang, and Kyungjin Oh** presented
*「Connectome: Reconstruction of Memory」* at [**OB/Scene Focus**](https://obscenefocus.com/artandtech_conecotm).
The public program and the [lab's event record](https://www.connectomelab.com/en/news/)
describe an interactive brain-art installation and live EEG affect-decoding
demonstration exploring AI-generated music and video. They do not document the
exact headset, electrode density, or visitor-to-output pipeline, so those details
are not asserted here.

The exhibition translates a research idea into a public setting; it does not
validate the decoder. Audience interaction can reveal usability and conceptual
questions, but it cannot replace controlled evaluation of accuracy,
generalization, or subjective agreement.
