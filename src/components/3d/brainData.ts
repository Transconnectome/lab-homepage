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
    id: 'neuro-x',
    name: 'Neuro-X: Large Brain Models',
    nameKo: 'Neuro-X: 대규모 뇌 모델 (LBM)',
    axis: 'Neuro-X · LBM',
    axisKo: 'Neuro-X · LBM',
    position: [0, 0.9, 0.1],
    color: '#38bdf8',
    description:
      'A unified AI system pre-trained on massive multi-modal brain data — the lab’s moonshot toward a Large Brain Model that decodes the neural syntax of the mind.',
    descriptionKo:
      '대규모 멀티모달 뇌 데이터로 사전학습하는 통합 AI 시스템 — 마음의 신경 구문(neural syntax)을 해독하는 대규모 뇌 모델(LBM)을 향한 연구실의 문샷입니다.',
    brainFocus:
      'Whole-brain dynamics: time-varying functional connectomics across fMRI, EEG and diffusion MRI, framed by Buzsáki’s “inside-out” view of the brain as a prediction engine.',
    brainFocusKo:
      '전뇌 동역학 — fMRI·EEG·확산 MRI를 아우르는 시변 기능 커넥토믹스. 뇌를 예측 기계로 보는 Buzsáki의 inside-out 관점이 이론적 틀입니다.',
    highlights: [
      {
        label: 'Mind the Gap: nonlinear brain–LLM representation alignment',
        labelKo: 'Mind the Gap: 뇌-LLM 표상의 비선형 정렬',
      },
      {
        label: 'Dynamic functional connectomics beyond static correlation matrices',
        labelKo: '정적 상관 행렬을 넘어서는 동적 기능 커넥토믹스',
      },
    ],
  },
  {
    id: 'fmri-eeg-foundation-models',
    name: 'fMRI & EEG Foundation Models',
    nameKo: 'fMRI·EEG 파운데이션 모델',
    axis: 'Foundation Models',
    axisKo: '파운데이션 모델',
    position: [1.3, 0.7, -0.5],
    color: '#818cf8',
    description:
      'New deep-learning architectures designed from neuroscience first principles for 4D brain signals — state-space models and channel-equivariant networks.',
    descriptionKo:
      '신경과학 제1원리에서 출발해 4D 뇌 신호에 맞게 새로 설계한 딥러닝 아키텍처 — 상태공간 모델과 채널 등변 네트워크입니다.',
    brainFocus:
      'Resting-state and task fMRI volumes, and EEG rhythms sampled at millisecond resolution across arbitrary electrode montages.',
    brainFocusKo:
      '휴지기·과제 fMRI 볼륨, 그리고 임의의 전극 배치에서 밀리초 해상도로 기록되는 EEG 리듬.',
    highlights: [
      {
        label: 'NeuroMamba: state-space foundation model for 4D fMRI (NeurIPS 2025 Spotlight)',
        labelKo: 'NeuroMamba: 4D fMRI 상태공간 파운데이션 모델 (NeurIPS 2025 Spotlight)',
      },
      {
        label: 'DIVER-0: channel-equivariant EEG foundation model (ICML 2025 GenBio Spotlight)',
        labelKo: 'DIVER-0: 채널 등변 EEG 파운데이션 모델 (ICML 2025 GenBio Spotlight)',
      },
      {
        label: 'SwiFT: 4D Swin Transformers for fMRI (NeurIPS 2023)',
        labelKo: 'SwiFT: fMRI를 위한 4D Swin Transformer (NeurIPS 2023)',
      },
    ],
  },
  {
    id: 'computational-genetics-psychiatry',
    name: 'Computational Psychiatry & Multi-Modal Genetics',
    nameKo: '계산정신의학·다중오믹스 유전체',
    axis: 'Genetics & Psychiatry',
    axisKo: '유전체·정신의학',
    position: [-1.3, 0.6, 0.2],
    color: '#f43f5e',
    description:
      'Bridging polygenic risk, white-matter tractography and environmental adversity to predict mental-health trajectories in youth.',
    descriptionKo:
      '다유전자 위험과 백질 신경로, 환경적 역경을 연결해 청소년 정신건강 궤적을 예측합니다.',
    brainFocus:
      'Developing brains in large cohorts (ABCD): white-matter integrity, subcortical structure, and their genetic architecture across generations.',
    brainFocusKo:
      '대규모 코호트(ABCD)의 발달 중인 뇌 — 백질 완결성, 피질하 구조, 그리고 세대를 잇는 유전적 구조.',
    highlights: [
      {
        label: 'Polygenic architecture of the developing brain (Nat Comms 2025)',
        labelKo: '발달하는 뇌의 다유전자 구조 (Nat Comms 2025)',
      },
      {
        label: 'Multigenerational transmission of psychiatric vulnerability (Mol Psychiatry 2025)',
        labelKo: '정신질환 취약성의 다세대 전달 (Mol Psychiatry 2025)',
      },
      {
        label: 'Adolescent depression & suicide risk prediction',
        labelKo: '청소년 우울·자살 위험 예측',
      },
    ],
  },
  {
    id: 'quantum-machine-learning',
    name: 'Quantum Machine Learning for Brain Data',
    nameKo: '뇌데이터를 위한 양자 머신러닝',
    axis: 'Quantum ML',
    axisKo: '양자 ML',
    position: [0.8, -0.5, 0.7],
    color: '#fbbf24',
    description:
      'Parameterized quantum circuits and quantum kernels for connectome graphs whose dimensionality overwhelms classical computation.',
    descriptionKo:
      '고전 컴퓨팅을 압도하는 초고차원 커넥톰 그래프를 위한 매개변수화 양자 회로와 양자 커널 연구입니다.',
    brainFocus:
      'The connectome as a graph: 86 billion neurons and ~100 trillion connections — high-order network interactions beyond classical reach.',
    brainFocusKo:
      '그래프로서의 커넥톰 — 860억 뉴런과 약 100조 연결. 고전적 접근을 넘어서는 고차 네트워크 상호작용을 다룹니다.',
    highlights: [
      {
        label: 'Quantum graph neural networks for anatomical & functional brain graphs',
        labelKo: '해부학적·기능적 뇌 그래프를 위한 양자 그래프 신경망(QGNN)',
      },
      {
        label: 'Quantum kernel estimation with polynomial speedup',
        labelKo: '다항 가속을 노리는 양자 커널 추정',
      },
      {
        label: 'Active research internship program (Quantum Computing & AI)',
        labelKo: '양자컴퓨팅·AI 연구 인턴십 프로그램 운영',
      },
    ],
  },
  {
    id: 'art-and-neuroscience',
    name: 'Art & Neuroscience',
    nameKo: '예술 × 뇌과학',
    axis: 'Art × Science',
    axisKo: '예술 × 과학',
    position: [-0.9, -0.6, -1.1],
    color: '#c084fc',
    description:
      'EEG-based memory reconstruction and interactive media — treating brain science as a cultural and humanistic inquiry, in Da Vinci’s spirit.',
    descriptionKo:
      'EEG 기반 기억 재구성과 인터랙티브 미디어 — 다빈치의 정신을 따라 뇌과학을 문화적·인문학적 탐구로 확장합니다.',
    brainFocus:
      'Real-time affective EEG signals, decoded live to drive generative audio-visual systems.',
    brainFocusKo:
      '실시간으로 해독되어 생성형 시청각 시스템을 구동하는 정서 EEG 신호.',
    highlights: [
      {
        label: 'OB/Scene Focus Exhibition 2025: “Connectome: Reconstruction of Memory”',
        labelKo: 'OB/Scene 포커스 전시 2025: 〈커넥톰: 기억의 재구성〉',
      },
      {
        label: 'Art & technology commissions bridging consciousness and aesthetics',
        labelKo: '의식과 미학을 잇는 예술·기술 협업 커미션',
      },
    ],
  },
];

export const AXIS_LINKS: AxisLink[] = [
  {
    a: 'neuro-x',
    b: 'fmri-eeg-foundation-models',
    reason: 'SwiFT, NeuroMamba and DIVER-0 are the building blocks of the Large Brain Model.',
    reasonKo: 'SwiFT·NeuroMamba·DIVER-0가 대규모 뇌 모델(LBM)의 구성 블록입니다.',
  },
  {
    a: 'neuro-x',
    b: 'computational-genetics-psychiatry',
    reason: 'Polygenic scores join imaging in the LBM’s joint multi-modal latent space.',
    reasonKo: '다유전자 점수가 뇌영상과 함께 LBM의 멀티모달 잠재공간에 통합됩니다.',
  },
  {
    a: 'fmri-eeg-foundation-models',
    b: 'computational-genetics-psychiatry',
    reason: 'Shared large cohorts (e.g., ABCD): foundation-model features feed psychiatric risk prediction.',
    reasonKo: '대규모 코호트(ABCD 등)를 공유 — 파운데이션 모델의 특징이 정신질환 위험 예측에 투입됩니다.',
  },
  {
    a: 'computational-genetics-psychiatry',
    b: 'quantum-machine-learning',
    reason: 'Quantum kernels tackle the high-dimensional gene–connectome graphs.',
    reasonKo: '양자 커널로 초고차원 유전자-커넥톰 그래프를 다룹니다.',
  },
  {
    a: 'fmri-eeg-foundation-models',
    b: 'art-and-neuroscience',
    reason: 'Real-time EEG decoding powers the interactive installations.',
    reasonKo: '실시간 EEG 디코딩이 인터랙티브 설치 작품을 구동합니다.',
  },
];
