/** Editorial relationships between research questions, never anatomical tracts.
 * Sources and scope are reviewed in docs/research-content-review.md.
 */
export const researchConnections = [
  {
    a: 'neuro-x', b: 'quantum-machine-learning',
    kind: 'implemented',
    title: { ko: 'EEG 모델과 양자 회로', en: 'EEG models and quantum circuits' },
    description: {
      ko: 'Q-DIVER는 DIVER-1 EEG 모델에 양자 분류 모듈을 결합하고, 운동심상 분류를 시뮬레이션에서 평가합니다.',
      en: 'Q-DIVER combines the DIVER-1 EEG model with a quantum classification module, evaluated on motor-imagery classification in simulation.',
    },
    source: 'https://arxiv.org/html/2603.28122v1',
    sourceLabel: 'Q-DIVER',
  },
  {
    a: 'neuro-x', b: 'art-and-neuroscience',
    kind: 'shared',
    title: { ko: '뇌신호와 정서의 변화', en: 'Brain signals and changing emotions' },
    description: {
      ko: '경외 연구는 경험 보고와 EEG를 함께 살펴 복합 정서를 연구합니다. EEG에서 정서를 분류하는 모델과 만나는 질문은, 사람이 보고한 느낌과 신경 신호의 관계를 어떻게 이해할 것인가입니다.',
      en: 'The awe study brings experience reports and EEG together to study complex feelings. It shares a question with models that classify emotion from EEG: how can we understand the relationship between reported feelings and neural signals?',
    },
    source: 'https://doi.org/10.1038/s44271-025-00299-2',
    sourceLabel: { ko: '경외 연구', en: 'Awe study' },
  },
  {
    a: 'neuro-x', b: 'computational-genetics-psychiatry',
    kind: 'open',
    title: { ko: '발달을 여러 수준에서 이해하기', en: 'Understanding development across levels' },
    description: {
      ko: '유전·뇌·행동·환경의 자료와 뇌 모델이 학습한 표현을 연결하면, 발달과 정신건강의 개인차를 어떻게 이해할 수 있을까요? 두 접근의 접점에서 탐구할 질문입니다.',
      en: 'How could connecting genetic, brain, behavioral, and environmental data with learned brain representations help us understand differences in development and mental health? This is a question to explore where the two approaches meet.',
    },
  },
] as const;

export const mapLabels: Record<string, { ko: string; en: string }> = {
  'neuro-x': { ko: '뇌 활동과 인지·행동', en: 'Brain activity, cognition & behavior' },
  'computational-genetics-psychiatry': { ko: '유전·뇌·행동·환경', en: 'Genes, brain, behavior & environment' },
  'quantum-machine-learning': { ko: '뇌신호를 위한 양자 학습', en: 'Quantum learning for brain signals' },
  'art-and-neuroscience': { ko: '감정·기억과 뇌 활동', en: 'Feelings, memory & brain activity' },
};
