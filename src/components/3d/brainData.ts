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
      'Deep-learning models built for 4D fMRI (SwiFT, NeuroMamba) and for EEG recorded with any electrode layout (DIVER-0), pretrained on large cohorts. Where the program is heading: a single Large Brain Model that learns several modalities together.',
    descriptionKo:
      '4D fMRI 모델(SwiFT·NeuroMamba)과 전극 배치에 묶이지 않는 EEG 모델(DIVER-0)을 대규모 코호트로 사전학습해 왔습니다. 이 프로그램의 도달점은 여러 모달리티를 함께 학습하는 하나의 대규모 뇌 모델(LBM)입니다.',
    brainFocus:
      'Whole-brain 4D dynamics — resting-state and task fMRI, EEG rhythms at millisecond resolution across arbitrary electrode montages, and diffusion MRI — framed by Buzsáki’s “inside-out” view of the brain as a prediction engine.',
    brainFocusKo:
      '전뇌 4D 동역학 — 휴지기·과제 fMRI, 임의 전극 배치의 밀리초 해상도 EEG 리듬, 확산 MRI. 뇌를 예측 기계로 보는 Buzsáki의 inside-out 관점이 이론적 틀입니다.',
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
    name: 'Quantum Machine Learning for Neuroimaging and Time-Series',
    nameKo: '뉴로이미징과 시계열을 위한 양자 머신러닝',
    axis: 'Quantum ML',
    axisKo: '양자 ML',
    position: [1.2, -0.1, -0.4],
    color: '#fbbf24',
    description:
      'Quantum circuits that train at scale, fit real fMRI and EEG, and run on today’s noisy hardware — much of it with Brookhaven National Laboratory.',
    descriptionKo:
      '규모에서 학습되고 실제 fMRI·EEG에 맞으며 오늘의 노이즈 있는 하드웨어에서 도는 양자 회로 — 상당수는 브룩헤이븐 국립연구소와 함께 합니다.',
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
        label: 'Ten-class MNIST end-to-end on a 127-qubit IBM Eagle processor (arXiv:2607.17705)',
        labelKo: '127큐비트 IBM Eagle에서 엔드투엔드로 실행한 10클래스 MNIST (arXiv:2607.17705)',
      },
      {
        label: 'Active research internship program (Quantum Computing & AI)',
        labelKo: '양자컴퓨팅·AI 연구 인턴십 프로그램 운영',
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
      'Shared large cohorts (e.g., ABCD): foundation-model features and polygenic scores meet in a joint multi-modal latent space for psychiatric risk prediction.',
    reasonKo:
      '대규모 코호트(ABCD 등)를 공유 — 파운데이션 모델의 특징과 다유전자 점수가 멀티모달 잠재공간에서 만나 정신질환 위험 예측에 쓰입니다.',
  },
  {
    a: 'computational-genetics-psychiatry',
    b: 'quantum-machine-learning',
    reason: 'Quantum kernels tackle the high-dimensional gene–connectome graphs.',
    reasonKo: '양자 커널로 초고차원 유전자-커넥톰 그래프를 다룹니다.',
  },
  {
    a: 'neuro-x',
    b: 'art-and-neuroscience',
    reason: 'Real-time EEG decoding powers the interactive installations.',
    reasonKo: '실시간 EEG 디코딩이 인터랙티브 설치 작품을 구동합니다.',
  },
];
