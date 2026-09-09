export interface AxisHighlight {
  label: string;
  labelKo: string;
}

export interface ResearchAxis {
  /** Matches the research collection anchor: /research#<id> works in both locales. */
  id: string;
  name: string;
  nameKo: string;
  /** Short label for the legend chips. */
  axis: string;
  axisKo: string;
  position: [number, number, number];
  color: string;
  /** What this research axis studies. */
  description: string;
  descriptionKo: string;
  /** Which brain systems / signals it works with — keeps the neuroscience flavor. */
  brainFocus: string;
  brainFocusKo: string;
  highlights: AxisHighlight[];
}

/** A real methodological/data connection between two axes — not decoration. */
export interface AxisLink {
  a: string;
  b: string;
  reason: string;
  reasonKo: string;
}

export const RESEARCH_AXES: ResearchAxis[] = [
  {
    // Neuro-X is one research program: SwiFT/NeuroMamba/DIVER-0 are the models
    // built so far, and the Large Brain Model is where the program is heading.
    // The research page carries it as a single entry for the same reason.
    id: 'neuro-x',
    name: 'Neuro-X: Brain Foundation Models (LBM)',
    nameKo: '뇌 파운데이션 모델 (Neuro-X · LBM)',
    axis: 'Brain Foundation Models',
    axisKo: '뇌 파운데이션 모델',
    position: [0, 0.8, 0.0],
    color: '#38bdf8',
    description:
      'Deep-learning models built for 4D fMRI (SwiFT, NeuroMamba) and channel-order-robust EEG (DIVER-0), pretrained on large cohorts. The Neuro-X project aims to develop a scalable, multimodal Large Brain Model.',
    descriptionKo:
      '4D fMRI 모델(SwiFT·NeuroMamba)과 채널 순서에 강건하도록 설계한 EEG 모델(DIVER-0)을 대규모 코호트로 사전학습해 왔습니다. Neuro-X의 목표는 확장 가능한 멀티모달 대규모 뇌 모델(LBM)입니다.',
    brainFocus:
      'Whole-brain 4D dynamics — resting-state and task fMRI, millisecond-resolution EEG recorded with heterogeneous electrode configurations, and proposed extensions to other modalities — framed by Buzsáki’s “inside-out” view of the brain as a prediction engine.',
    brainFocusKo:
      '전뇌 4D 동역학 — 휴지기·과제 fMRI, 서로 다른 전극 구성으로 기록한 밀리초 해상도 EEG, 그리고 다른 모달리티로의 제안된 확장. 뇌를 예측 기계로 보는 Buzsáki의 inside-out 관점이 이론적 틀입니다.',
    highlights: [
      {
        label: 'NeuroMamba: state-space foundation model for 4D fMRI (NeurIPS 2025 Brain & Body workshop, Spotlight)',
        labelKo: 'NeuroMamba: 4D fMRI 상태공간 파운데이션 모델 (NeurIPS 2025 Brain & Body 워크숍, Spotlight)',
      },
      {
        label: 'DIVER-0: channel-equivariant EEG foundation model (ICML 2025 GenBio workshop, Spotlight)',
        labelKo: 'DIVER-0: 채널 등변 EEG 파운데이션 모델 (ICML 2025 GenBio 워크숍, Spotlight)',
      },
      {
        label: 'SwiFT: 4D Swin Transformers for fMRI (NeurIPS 2023)',
        labelKo: 'SwiFT: fMRI를 위한 4D Swin Transformer (NeurIPS 2023)',
      },
      {
        label: 'Mind the Gap: nonlinear brain–LLM representation alignment',
        labelKo: 'Mind the Gap: 뇌-LLM 표상의 비선형 정렬',
      },
    ],
  },
  {
    id: 'computational-genetics-psychiatry',
    name: 'Computational Psychiatry & Multi-Modal Genetics',
    nameKo: '계산정신의학·다중오믹스 유전체',
    axis: 'Genetics & Psychiatry',
    axisKo: '유전체·정신의학',
    position: [-1.3, 0.4, 0.2],
    color: '#f43f5e',
    description:
      'Across complementary studies, testing what polygenic scores add to brain-imaging maps, family history, and limited youth mental-health prediction.',
    descriptionKo:
      '서로 다른 연구에서 다유전자 점수가 뇌영상 관계 지도, 가족력, 제한적인 청소년 정신건강 예측에 무엇을 더하는지 시험합니다.',
    brainFocus:
      'Children and adolescents in large cohorts (ABCD): multimodal brain measures, family history, polygenic scores, and prediction tested at distinct levels of evidence.',
    brainFocusKo:
      '대규모 코호트(ABCD)의 아동·청소년 — 다중 뇌영상 지표, 가족력, 다유전자 점수, 그리고 서로 다른 증거 수준에서 시험한 예측.',
    highlights: [
      {
        label: 'Polygenic architecture of the developing brain (Nat Comms 2025)',
        labelKo: '발달하는 뇌의 다유전자 구조 (Nat Comms 2025)',
      },
      {
        label: 'Statistical mediation of a family-history association (Mol Psychiatry 2025)',
        labelKo: '가족력 연관에 대한 통계적 매개 추정 (Mol Psychiatry 2025)',
      },
      {
        label: 'Initial youth depression and suicidality prediction tests',
        labelKo: '청소년 우울·자살성 예측의 초기 시험',
      },
    ],
  },
  {
    id: 'quantum-machine-learning',
    name: 'Quantum Machine Learning for Neuroimaging and Time-Series',
    nameKo: '뉴로이미징과 시계열을 위한 양자 머신러닝',
    axis: 'Quantum ML',
    axisKo: '양자 ML',
    position: [1.2, -0.1, -0.4],
    color: '#fbbf24',
    description:
      'Quantum circuits tested for trainability, parameter efficiency, fMRI and EEG fit, and noisy-hardware feasibility. Several cited studies include Brookhaven National Laboratory coauthors.',
    descriptionKo:
      '학습 가능성, 파라미터 효율, fMRI·EEG 적합성, 노이즈 하드웨어 실행 가능성을 시험합니다. 인용된 여러 연구에는 브룩헤이븐 국립연구소 소속 공동저자가 참여했습니다.',
    brainFocus:
      'Long 4D fMRI runs and long EEG montages — the high-dimensional, long-sequence regime where classical attention gets expensive.',
    brainFocusKo:
      '긴 4D fMRI 스캔과 긴 EEG 몽타주 — 고전적 어텐션이 비싸지는 고차원·장시퀀스 영역입니다.',
    highlights: [
      {
        label: 'Quantum Time-series Transformer on ABCD and UK Biobank resting-state fMRI (IEEE QCE 2025)',
        labelKo: 'ABCD·UK Biobank 휴지기 fMRI에 적용한 양자 시계열 트랜스포머 (IEEE QCE 2025)',
      },
      {
        label: 'Multi-chip ensemble circuits that mitigate barren plateaus (arXiv:2505.08782)',
        labelKo: '배런 플래토를 완화하는 멀티칩 앙상블 회로 (arXiv:2505.08782)',
      },
      {
        label: 'A 12-qubit MNIST classifier deployed on a 127-qubit IBM Eagle device (arXiv:2607.17705)',
        labelKo: '12큐비트 MNIST 분류기를 127큐비트 IBM Eagle 장치에 배포 (arXiv:2607.17705)',
      },
      {
        label: 'Q-DIVER: ~50× smaller task head, but ~2.9× fewer total trainable parameters (arXiv:2603.28122)',
        labelKo: 'Q-DIVER: 과제 헤드는 약 50배, 전체 학습 파라미터는 약 2.9배 감소 (arXiv:2603.28122)',
      },
    ],
  },
  {
    id: 'art-and-neuroscience',
    name: 'Affective Neuroscience',
    nameKo: '정서 신경과학',
    axis: 'Affective Neuroscience',
    axisKo: '정서 신경과학',
    position: [-0.6, -0.7, -1.2],
    color: '#c084fc',
    description:
      'Awe, being moved, and remembered feeling — the mixed, temporally extended affects that a single valence scale loses.',
    descriptionKo:
      '경외, 뭉클함, 되살아나는 감정 — 정서가 척도 하나로는 놓쳐 버리는, 뒤섞이고 시간에 걸쳐 펼쳐지는 정서들을 다룹니다.',
    brainFocus:
      'Cortical and EEG responses to naturalistic stimuli — film, music, and live interaction rather than isolated images.',
    brainFocusKo:
      '자연주의적 자극에 대한 피질·EEG 반응 — 고립된 이미지가 아니라 영화, 음악, 실시간 상호작용입니다.',
    highlights: [
      {
        label:
          'Awe is an ambivalent affect in human behavior and cortex — Jinwoo Yi et al., Communications Psychology (2025)',
        labelKo:
          '경외(awe)가 행동과 대뇌 피질 모두에서 양가적 정서임을 규명 — 이진우 외, Communications Psychology (2025)',
      },
      {
        label: 'Affect-contextualized memory reconstructed via EEG-guided audiovisual generation',
        labelKo: 'EEG로 유도한 오디오·비주얼 생성으로 재구성한 정서 맥락의 기억',
      },
      {
        label: 'Generative models of aesthetic style: AesFA (AAAI 2024), music style transfer (ICIP 2026)',
        labelKo: '미적 스타일의 생성 모형: AesFA (AAAI 2024), 음악 스타일 전이 (ICIP 2026)',
      },
      {
        label: 'OB/Scene Focus 2025: “Connectome: Reconstruction of Memory”',
        labelKo: 'OB/Scene 포커스 2025: 〈커넥톰: 기억의 재구성〉',
      },
    ],
  },
];

export const AXIS_LINKS: AxisLink[] = [
  {
    a: 'neuro-x',
    b: 'computational-genetics-psychiatry',
    reason:
      'Open question: can brain foundation-model representations add predictive information beyond polygenic scores in shared cohorts such as ABCD?',
    reasonKo:
      '열린 질문: ABCD 같은 공통 코호트에서 뇌 파운데이션 모델의 표상이 다유전자 점수에 더해 예측 정보를 제공할 수 있을까요?',
  },
  {
    a: 'computational-genetics-psychiatry',
    b: 'quantum-machine-learning',
    reason: 'Possible connection, not a demonstrated result: testing quantum models on high-dimensional genetic and brain features would require matched classical baselines.',
    reasonKo: '아직 입증되지 않은 연결 가능성입니다. 고차원 유전·뇌 특징에 양자 모형을 적용하려면 동등한 고전 모형과의 비교가 필요합니다.',
  },
  {
    a: 'neuro-x',
    b: 'art-and-neuroscience',
    reason: 'EEG research and the art program share questions about representing emotion over time. The public presentation is not a validation of a foundation-model decoder.',
    reasonKo: 'EEG 연구와 예술 프로그램은 시간에 따라 변하는 정서를 어떻게 표현할지 묻습니다. 공개 발표가 파운데이션 모델 디코더의 타당성을 검증한 것은 아닙니다.',
  },
];
