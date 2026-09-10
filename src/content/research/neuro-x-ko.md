---
title: "Neuro-X 프로젝트: 뇌 파운데이션 모델"
titleKo: "The Neuro-X Project: Brain Foundation Models"
tagline: "fMRI와 EEG의 특성에 맞는 다양한 뇌 파운데이션 모델을 개발해, 뇌 활동을 학습하고 새로운 데이터와 과제에 활용합니다."
category: "foundation-models"
featured: true
order: 1
keyHighlights:
  - "[SwiFT](https://doi.org/10.52202/075280-1820)·[SwiFUN](https://doi.org/10.1162/imag_a_00440): fMRI의 시공간 패턴 학습과 과제 활성 예측"
  - "[MBBN](https://doi.org/10.1038/s42003-026-10011-7): 주파수 대역별 뇌 활동 분석 (Communications Biology, 2026)"
  - "[NeuroMamba](https://neurips.cc/virtual/2025/132664): 상태공간 모델을 활용한 fMRI 학습 (NeurIPS 2025 Brain & Body 워크숍, Spotlight)"
  - "[DIVER-0](https://arxiv.org/abs/2507.14141): 채널 구성을 고려한 EEG 모델 (ICML 2025 GenBio 워크숍, Spotlight). [DIVER-1](https://doi.org/10.48550/arxiv.2512.19097)은 두개내 EEG로 확장"
lang: "ko"
baseSlug: "neuro-x"
---

Neuro-X는 뇌 신호의 특성과 연구 목적에 맞는 다양한 파운데이션 모델을 개발하는 연구 프로그램입니다. 대규모 뇌 데이터에서 먼저 학습한 특징을 인지 상태 분석이나 정신건강 연구 등 여러 과제에 활용하는 것을 목표로 합니다.

fMRI는 뇌 전체의 공간적 패턴과 시간에 따른 변화를 담고, EEG는 빠른 신경 활동을 기록하지만 전극 구성이 자료마다 다릅니다. 연구실은 이러한 차이를 고려해 모델을 설계하고, 학습한 특징이 새로운 사람과 데이터에서도 유효한지 평가합니다.

### fMRI의 공간·시간 패턴 학습

[SwiFT](https://doi.org/10.52202/075280-1820)는 fMRI를 미리 정한 뇌 영역별 평균으로 축약하지 않고, 공간과 시간의 변화를 함께 학습합니다. 후속 모델인 [SwiFUN](https://doi.org/10.1162/imag_a_00440)은 휴지기 fMRI로 과제 수행 중의 뇌 활성 패턴을 예측합니다.

[MBBN](https://doi.org/10.1038/s42003-026-10011-7)은 fMRI를 주파수 대역별로 나누어 학습하며, 인지·정신건강 지표 예측에 관련된 뇌 활동 패턴을 분석합니다. [NeuroMamba](https://neurips.cc/virtual/2025/132664)는 긴 시공간 기록을 효율적으로 처리하도록 상태공간 모델을 활용합니다.

### 다양한 기록 환경의 EEG 학습

[DIVER-0](https://arxiv.org/abs/2507.14141)는 기록마다 다른 EEG 채널 구성을 고려한 모델입니다. 채널 순서가 바뀌면 출력도 그 순서에 맞게 바뀌도록 설계하고, 정서 인식과 운동심상 분류에서 평가했습니다. [DIVER-1](https://doi.org/10.48550/arxiv.2512.19097)은 두개내 EEG로 연구를 확장해 인지 과제와 발작 검출을 다룹니다.

이 모델들을 바탕으로 새로운 기록 환경과 적은 학습 자료에서도 활용할 수 있는 뇌 신호 분석 방법을 연구합니다. 여러 종류의 뇌 데이터를 함께 활용하는 방법도 이 프로그램의 연구 방향입니다.
