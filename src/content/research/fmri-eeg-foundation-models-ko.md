---
title: "fMRI·EEG 파운데이션 모델 (NeuroMamba, SwiFT, DIVER-0)"
titleKo: "fMRI & EEG Foundation Models"
tagline: "4D 신경 동역학을 위한 상태공간 모델과 채널 등변(channel-equivariant) 아키텍처를 개척한다."
category: "foundation-models"
featured: true
order: 2
keyHighlights:
  - "[NeuroMamba](https://jubilant-choi.notion.site/neuromamba-neurips2025): 4D 기능적 MRI를 위한 최초의 상태공간 파운데이션 모델 (NeurIPS 2025 Brain & Body 워크숍 Spotlight)"
  - "[DIVER-0](https://arxiv.org/abs/2507.14141): 완전 채널 등변 EEG 파운데이션 모델 (ICML 2025 GenBio 워크숍 Spotlight)"
  - "[SwiFT](https://doi.org/10.52202/075280-1820) & SwiFT IO: 휴지기 및 과제 fMRI를 위한 확장 가능한 4D Swin Transformer 아키텍처"
  - "[주파수 특이적 다중 대역 어텐션](https://doi.org/10.48550/arXiv.2503.23394) — 장거리 공간 뇌 동역학을 위한 설계"
lang: "ko"
baseSlug: "fmri-eeg-foundation-models"
---

## 4D 뇌 신호를 위한 새로운 아키텍처

생물학적 신경 신호는 고유한 공간적 대칭성과 연속적인 시간 흐름, 비유클리드 기하 구조를 지닌다. 컴퓨터 비전이나 NLP에서 쓰이는 기존 아키텍처를 그대로 가져다 쓰기 어려운 이유다. Connectome Lab은 신경과학의 제1원리에서 출발해 이러한 신호에 맞는 딥러닝 아키텍처를 새로 설계한다.

### 1. [NeuroMamba](https://jubilant-choi.notion.site/neuromamba-neurips2025): fMRI를 위한 상태공간 파운데이션 모델
- **저자**: 최주빈 외 (NeurIPS 2025 Foundation Models for Brain and Body - **Spotlight**)
- **핵심 혁신**: 선택적 상태공간 모델(Mamba)을 도입해, 길고 연속적인 4D fMRI 스캔을 처리할 때 트랜스포머가 부딪히는 이차(quadratic) 계산 복잡도의 한계를 넘어섰다. 수만 개의 뇌 복셀과 수천 개의 시간 프레임에 걸친 문맥을 선형 시간으로 모델링한다.

### 2. [DIVER-0](https://arxiv.org/abs/2507.14141): 완전 채널 등변 EEG 파운데이션 모델
- **저자**: 한동엽, 이아현, 이태양, 이세빈 외 (ICML 2025 GenBio - **Spotlight**)
- **핵심 혁신**: 어떤 채널 배치에서도 공간 등변성(spatial equivariance)이 엄밀하게 성립하도록 설계해, 임상용과 연구용 EEG 데이터셋 사이의 고질적인 전극 몽타주 불일치를 해소했다.

### 3. 시공간 다중 대역 동역학
- **저자**: 배상윤 외 ([arXiv:2503.23394](https://doi.org/10.48550/arXiv.2503.23394))
- **핵심 혁신**: fMRI의 저주파 혈류역학적 변동 속에 얽혀 있는 정준(canonical) 신경 진동 대역들을 분리해 내는 주파수 특이적 다중 대역 어텐션 메커니즘을 제안했다.
