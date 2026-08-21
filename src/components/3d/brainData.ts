export interface LabProjectLink {
  label: string;
  labelKo: string;
  /** Locale-neutral path ('/research#slug' or '/publications'); BrainViewer prefixes /ko for Korean pages. */
  href: string;
}

export interface BrainNode {
  id: string;
  name: string;
  nameKo: string;
  /** Short label for the legend chips. */
  network: string;
  networkKo: string;
  position: [number, number, number];
  color: string;
  /** What this network does. */
  description: string;
  descriptionKo: string;
  /** Why the lab studies it — ties the network to concrete lab projects. */
  whyWeStudy: string;
  whyWeStudyKo: string;
  projects: LabProjectLink[];
}

export const BRAIN_HUBS: BrainNode[] = [
  {
    id: 'dmn',
    name: 'Default Mode Network (DMN)',
    nameKo: '디폴트 모드 네트워크 (DMN)',
    network: 'Default Mode',
    networkKo: '디폴트 모드',
    position: [0, 1.2, -1.0],
    color: '#38bdf8',
    description:
      'Active when the mind is at rest — self-referential thought, autobiographical memory, and imagining the future.',
    descriptionKo:
      '마음이 쉬고 있을 때 활성화되는 네트워크로, 자기참조적 사고와 자전적 기억, 미래 상상을 담당합니다.',
    whyWeStudy:
      'Resting-state fMRI, dominated by DMN dynamics, is the training ground for our brain foundation models — and our genetics work traces how polygenic risk shapes this network across adolescent development.',
    whyWeStudyKo:
      'DMN 동역학이 지배하는 휴지기 fMRI는 연구실 뇌 파운데이션 모델의 학습 무대입니다. 유전체 연구는 다유전자 위험이 청소년 발달 과정에서 이 네트워크를 어떻게 형성하는지 추적합니다.',
    projects: [
      {
        label: 'NeuroMamba: state-space foundation model for 4D fMRI (NeurIPS 2025 Spotlight)',
        labelKo: 'NeuroMamba: 4D fMRI 상태공간 파운데이션 모델 (NeurIPS 2025 Spotlight)',
        href: '/research#fmri-eeg-foundation-models',
      },
      {
        label: 'Polygenic architecture of the developing brain (Nat Comms 2025)',
        labelKo: '발달하는 뇌의 다유전자 구조 (Nat Comms 2025)',
        href: '/research#computational-genetics-psychiatry',
      },
    ],
  },
  {
    id: 'ecn',
    name: 'Executive Control Network (ECN / FPN)',
    nameKo: '집행 제어 네트워크 (전두두정망)',
    network: 'Executive Control',
    networkKo: '집행 제어',
    position: [1.3, 1.0, 0.8],
    color: '#818cf8',
    description:
      'Top-down cognitive control, working memory, and flexible switching between tasks.',
    descriptionKo:
      '하향식 인지 제어와 작업 기억, 과제 사이의 유연한 전환을 담당하는 전두두정 네트워크입니다.',
    whyWeStudy:
      'Task-evoked control states are where our 4D transformers prove themselves: SwiFT decodes cognition from raw fMRI volumes, and Neuro-X models the time-varying connectivity that frontoparietal control relies on.',
    whyWeStudyKo:
      '과제 수행 중의 제어 상태는 연구실 4D 트랜스포머가 실력을 입증하는 무대입니다. SwiFT는 원시 fMRI 볼륨에서 인지 상태를 해독하고, Neuro-X는 전두두정 제어가 의존하는 시변 연결성을 모델링합니다.',
    projects: [
      {
        label: 'SwiFT: 4D Swin Transformers for fMRI (NeurIPS 2023)',
        labelKo: 'SwiFT: fMRI를 위한 4D Swin Transformer (NeurIPS 2023)',
        href: '/research#fmri-eeg-foundation-models',
      },
      {
        label: 'Neuro-X: dynamic functional connectomics',
        labelKo: 'Neuro-X: 동적 기능 커넥토믹스',
        href: '/research#neuro-x',
      },
    ],
  },
  {
    id: 'salience',
    name: 'Salience Network (Insula / dACC)',
    nameKo: '돌출 네트워크 (섬엽·전대상피질)',
    network: 'Salience',
    networkKo: '돌출 네트워크',
    position: [-1.2, 0.4, 0.4],
    color: '#f43f5e',
    description:
      'Flags emotionally and biologically important events, switching the brain between rest and focused control.',
    descriptionKo:
      '정서적·생물학적으로 중요한 자극을 포착해, 뇌를 휴식 모드와 집중 제어 모드 사이에서 전환시킵니다.',
    whyWeStudy:
      'Salience dysfunction is central to adolescent depression and suicide risk — a core target of our computational psychiatry work — and its affective signals drive our EEG art-decoding installations.',
    whyWeStudyKo:
      '돌출 네트워크의 기능 이상은 청소년 우울과 자살 위험의 핵심으로, 연구실 계산정신의학 연구의 주요 표적입니다. 이 네트워크의 정서 신호는 EEG 예술 디코딩 설치 작품의 원천이기도 합니다.',
    projects: [
      {
        label: 'Adolescent depression & suicide risk prediction',
        labelKo: '청소년 우울·자살 위험 예측',
        href: '/research#computational-genetics-psychiatry',
      },
      {
        label: 'OB/Scene “Connectome: Reconstruction of Memory” EEG installation (2025)',
        labelKo: 'OB/Scene 〈커넥톰: 기억의 재구성〉 EEG 설치 (2025)',
        href: '/research#art-and-neuroscience',
      },
    ],
  },
  {
    id: 'sensory',
    name: 'Visual & Sensory Cortex (V1/V2)',
    nameKo: '시각 및 감각 피질 (V1/V2)',
    network: 'Visual & Sensory',
    networkKo: '시각·감각',
    position: [0.9, -0.6, -1.6],
    color: '#34d399',
    description:
      'Hierarchical visual representations — from edges to objects to scenes — and reconstruction of sensory states.',
    descriptionKo:
      '선분에서 사물, 장면으로 이어지는 위계적 시각 표상과 감각 상태의 재구성을 담당합니다.',
    whyWeStudy:
      'Visual cortex is where brains and AI models meet: we align its representations with large language and vision models, and generate synthetic fMRI to test what these networks truly encode.',
    whyWeStudyKo:
      '시각 피질은 뇌와 AI 모델이 만나는 접점입니다. 연구실은 시각 표상을 대규모 언어·비전 모델과 정렬하고, 합성 fMRI를 생성해 이 네트워크가 실제로 무엇을 부호화하는지 검증합니다.',
    projects: [
      {
        label: 'Mind the Gap: nonlinear brain–LLM alignment',
        labelKo: 'Mind the Gap: 뇌-LLM 비선형 정렬',
        href: '/research#neuro-x',
      },
      {
        label: 'Generative fMRI simulation',
        labelKo: '생성형 fMRI 시뮬레이션',
        href: '/research#neuro-x',
      },
    ],
  },
  {
    id: 'subcortical',
    name: 'Subcortical & Hippocampal Complex',
    nameKo: '피질하 및 해마 복합체',
    network: 'Subcortical',
    networkKo: '피질하·해마',
    position: [-0.6, -0.5, -0.2],
    color: '#fbbf24',
    description:
      'Deep-brain structures for memory consolidation, emotion, and reward — key nodes of psychiatric vulnerability.',
    descriptionKo:
      '기억 공고화와 정서, 보상을 담당하는 심부 뇌 구조로, 정신질환 취약성의 핵심 노드입니다.',
    whyWeStudy:
      'Subcortical circuits carry psychiatric risk across generations: we model how polygenic scores shape these structures, and their dense graph topology motivates our quantum machine-learning kernels.',
    whyWeStudyKo:
      '피질하 회로는 정신질환 위험이 세대를 넘어 전달되는 경로입니다. 연구실은 다유전자 점수가 이 구조를 어떻게 형성하는지 모델링하며, 조밀한 그래프 위상은 양자 머신러닝 커널 연구의 동기가 됩니다.',
    projects: [
      {
        label: 'Multigenerational transmission of psychiatric vulnerability (Mol Psychiatry 2025)',
        labelKo: '정신질환 취약성의 다세대 전달 (Mol Psychiatry 2025)',
        href: '/research#computational-genetics-psychiatry',
      },
      {
        label: 'Quantum ML kernels for connectome graphs',
        labelKo: '커넥톰 그래프를 위한 양자 ML 커널',
        href: '/research#quantum-machine-learning',
      },
    ],
  },
  {
    id: 'eeg-mesh',
    name: 'EEG Sensor Mesh (DIVER-0)',
    nameKo: 'EEG 센서 메쉬 (DIVER-0)',
    network: 'EEG Sensors',
    networkKo: 'EEG 센서',
    position: [-1.4, 1.2, 0.0],
    color: '#c084fc',
    description:
      'Not a brain network but the measurement layer: scalp electrodes sampling neural rhythms at millisecond resolution.',
    descriptionKo:
      '뇌 네트워크가 아닌 측정 계층입니다. 두피 전극이 밀리초 해상도로 신경 리듬을 기록합니다.',
    whyWeStudy:
      'Every EEG cap has a different electrode montage. DIVER-0, our channel-equivariant foundation model, is built to read them all — one model across clinical and research datasets.',
    whyWeStudyKo:
      'EEG 장비마다 전극 배치가 다릅니다. 연구실의 채널 등변 파운데이션 모델 DIVER-0는 임상·연구 데이터셋을 가리지 않고 하나의 모델로 읽어내도록 설계되었습니다.',
    projects: [
      {
        label: 'DIVER-0: channel-equivariant EEG foundation model (ICML 2025 GenBio Spotlight)',
        labelKo: 'DIVER-0: 채널 등변 EEG 파운데이션 모델 (ICML 2025 GenBio Spotlight)',
        href: '/research#fmri-eeg-foundation-models',
      },
      {
        label: 'All lab publications',
        labelKo: '연구실 전체 논문',
        href: '/publications',
      },
    ],
  },
];
