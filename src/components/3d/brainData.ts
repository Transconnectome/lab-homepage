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
    // One research program can include multiple signal- and task-specific models.
    id: 'neuro-x',
    name: 'Neuro-X: Brain Foundation Models',
    nameKo: '뇌 파운데이션 모델 (Neuro-X)',
    axis: 'Brain Foundation Models',
    axisKo: '뇌 파운데이션 모델',
    position: [0, 0.8, 0.0],
    color: '#38bdf8',
    description:
      'We develop a range of brain foundation models suited to different signals and research goals, including fMRI models such as SwiFT and NeuroMamba, and EEG models such as DIVER.',
    descriptionKo:
      'SwiFT·NeuroMamba 같은 fMRI 모델과 DIVER 같은 EEG 모델을 비롯해, 신호의 특성과 연구 목적에 맞는 다양한 뇌 파운데이션 모델을 개발합니다.',
    brainFocus:
      'Spatial and temporal patterns in fMRI, and EEG from different recording settings.',
    brainFocusKo:
      'fMRI의 공간·시간 패턴과, 서로 다른 기록 환경에서 얻은 EEG를 다룹니다.',
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
      'We study individual differences in development and mental health through genetic information, brain imaging, and family history.',
    descriptionKo:
      '유전 정보, 뇌영상, 가족력을 함께 살펴 발달과 정신건강의 개인차를 연구합니다.',
    brainFocus:
      'Brain structure and function, polygenic scores, and cognitive and mental-health measures in children and adolescents.',
    brainFocusKo:
      '아동·청소년의 뇌 구조와 기능, 다유전자 점수, 인지·정신건강 지표를 분석합니다.',
    highlights: [
      {
        label: 'Polygenic architecture of the developing brain (Nat Comms 2025)',
        labelKo: '발달하는 뇌의 다유전자 구조 (Nat Comms 2025)',
      },
      {
        label: 'Depression family history and offspring genetic liability (Molecular Psychiatry)',
        labelKo: '우울증 가족력과 자녀의 유전적 소인 (Molecular Psychiatry)',
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
      'We study hybrid quantum–classical models for brain signals, circuit training, and computation on noisy quantum devices.',
    descriptionKo:
      '뇌 신호를 분석하는 양자·고전 결합 모델, 회로 학습, 잡음이 있는 양자 장치에서의 계산을 연구합니다.',
    brainFocus:
      'fMRI and EEG time series, alongside benchmarks for circuit training and hardware execution.',
    brainFocusKo:
      'fMRI·EEG 시계열과, 회로 학습 및 하드웨어 실행을 평가하는 벤치마크를 다룹니다.',
    highlights: [
      {
        label: 'Quantum Time-series Transformer on ABCD and UK Biobank resting-state fMRI (IEEE QCE 2025)',
        labelKo: 'ABCD·UK Biobank 휴지기 fMRI에 적용한 양자 시계열 트랜스포머 (IEEE QCE 2025)',
      },
      {
        label: 'Multi-chip ensembles evaluated under simulated noise (arXiv:2505.08782)',
        labelKo: '모사된 잡음 환경에서 평가한 멀티칩 앙상블 (arXiv:2505.08782)',
      },
      {
        label: 'Handwritten-image classification on IBM quantum hardware (arXiv:2607.17705)',
        labelKo: 'IBM 양자 하드웨어에서의 손글씨 이미지 분류 (arXiv:2607.17705)',
      },
      {
        label: 'Q-DIVER: pretrained EEG models combined with quantum circuits (arXiv:2603.28122)',
        labelKo: 'Q-DIVER: 사전학습 EEG 모델과 양자 회로의 결합 (arXiv:2603.28122)',
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
      'We study complex emotions during awe and autobiographical recall, alongside models of visual and musical expression.',
    descriptionKo:
      '경외와 회상에서 경험하는 복합적인 정서, 이미지와 음악의 표현 방식을 연구합니다.',
    brainFocus:
      'EEG and experience reports during VR viewing and autobiographical recall.',
    brainFocusKo:
      'VR 영상을 보거나 개인적인 기억을 떠올리는 동안의 EEG와 경험 보고를 분석합니다.',
    highlights: [
      {
        label:
          'Awe and mixed feelings studied with VR and EEG (Communications Psychology, 2025)',
        labelKo:
          'VR과 EEG로 살펴본 경외와 복합 정서 (Communications Psychology, 2025)',
      },
      {
        label: 'Exploratory audiovisual generation from participant-provided memories and EEG-derived emotion',
        labelKo: '참여자가 제공한 기억 자료와 EEG 기반 정서 정보를 활용한 음악·영상 생성 탐색',
      },
      {
        label: 'Generative models of aesthetic style: AesFA (AAAI 2024), music style transfer (ICIP 2026)',
        labelKo: '미적 스타일의 생성 모형: AesFA (AAAI 2024), 음악 스타일 전이 (ICIP 2026)',
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
    reason: 'EEG modeling and affective neuroscience both study how brain signals relate to emotions that change over time.',
    reasonKo: 'EEG 모델 연구와 정서 신경과학은 시간에 따라 달라지는 정서와 뇌 신호의 관계를 함께 다룹니다.',
  },
];
