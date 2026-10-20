import type { Lang } from '../i18n/ui';

/** Human-reviewed summaries; evidence and boundaries: docs/homepage-editorial-review-2026-10-20.md.
 * Keep each comparator and qualification together when updating either language. */
export const researchStories = [
  {
    id: 'swifun', area: 'neuro-x', source: 'https://doi.org/10.1162/imag_a_00440',
    citation: 'Kwon et al. · Imaging Neuroscience · 2025',
    title: {
      ko: '쉬고 있는 뇌에서 과제 중 반응을 예측할 수 있을까?',
      en: 'Can the resting brain tell us how it will respond to a task?',
    },
    body: {
      ko: 'SwiFUN은 휴지기 fMRI로 과제를 수행할 때의 뇌 활성 지도를 예측합니다. 성인과 아동 자료에서 예측 지도와 실제 지도의 전체 유사도는 비교 모델 ConnTask보다 높았지만, 누구의 지도인지 구별하는 성능은 ConnTask가 더 좋았습니다. 공통된 반응을 잘 예측하는 것에서 한 사람의 고유한 반응을 이해하는 것으로, 질문이 이어집니다.',
      en: 'SwiFUN predicts task-evoked brain activity from resting-state fMRI. In adult and child datasets, its predicted maps were more similar overall to measured maps than those from ConnTask, while ConnTask identified individuals more accurately. This opens a further question: how can prediction capture the responses that distinguish one person from another?',
    },
    context: { ko: '뇌 모델 연구', en: 'Brain models' },
  },
  {
    id: 'development', area: 'computational-genetics-psychiatry',
    source: 'https://doi.org/10.1038/s41467-025-63312-6',
    citation: 'Joo et al. · Nature Communications · 2025',
    title: {
      ko: '한 아이의 발달을 여러 관측에서 함께 읽는다면?',
      en: "What can different observations reveal about a child's development?",
    },
    body: {
      ko: '아동의 유전적 차이와 뇌영상에 인지·행동·환경 지표를 함께 놓고, 어떤 특징들이 같이 달라지는지 분석했습니다. 학교와 이웃의 조건도 이 관측에 포함됩니다. 예를 들어, 이 아동 표본에서는 인지 능력 관련 유전 변이들의 효과를 합산한 점수와 뇌 부피·표면적이 함께 높은 패턴이 관찰됐습니다. 이렇게 발견한 관계는 발달을 설명할 단서를 주지만, 무엇이 무엇을 일으켰는지는 별도의 검증이 필요합니다.',
      en: 'We analyzed genetic differences and brain imaging alongside cognitive, behavioral and environmental measures to find patterns that vary together. School and neighborhood conditions were part of those observations. For example, one pattern in this child sample linked higher scores combining the effects of cognition-related genetic variants with larger brain volumes and surface areas. These relationships offer clues about development; establishing what causes what requires further evidence.',
    },
    context: { ko: '유전·뇌·환경 연구', en: 'Genes, brain and environment' },
  },
  {
    id: 'awe', area: 'art-and-neuroscience',
    source: 'https://doi.org/10.1038/s44271-025-00299-2',
    citation: 'Lee et al. · Communications Psychology · 2025',
    title: {
      ko: '경외는 즐거움과 불편함이 함께하는 감정일까?',
      en: 'Can awe feel pleasant and unpleasant at the same time?',
    },
    body: {
      ko: 'VR 영상을 보는 동안의 경험 보고와 EEG를 함께 기록했습니다. 긍정과 부정이 섞인 감정의 지속 시간과 강도는 보고된 경외의 강도와 관련됐습니다. 하나의 좋음–싫음 척도에 담기 어려운 경험을 어떻게 측정할지 묻는 연구입니다.',
      en: 'We recorded experience reports and EEG while participants watched VR videos. The duration and intensity of mixed positive and negative feelings were related to reported awe. The study asks how to measure experiences that a single pleasant–unpleasant scale can miss.',
    },
    context: { ko: '정서와 경험 연구', en: 'Emotion and experience' },
  },
] satisfies Array<{
  id: string; area: string; source: string; citation: string;
  title: Record<Lang, string>; body: Record<Lang, string>; context: Record<Lang, string>;
}>;
