// 2026 동계 학부 연구 인턴 모집 공고.
// 정본: Transconnectome/intern-2026-winter `ops/ANNOUNCEMENT_DRAFT.md` 버전 1 (11/9 일정 +7일 반영).
// 공고 문구를 바꿀 때는 정본과 이 파일을 함께 고친다.

export interface Link {
  label: string;
  href: string;
}

export interface Project {
  id: string;
  code: string;
  modality: string;
  title: string;
  stack: string;
  overview: string;
  note?: string;
  question: string;
  deliverables: string;
  refsLabel: string;
  refs: Link[];
  refsNote?: string;
}

export interface Step {
  date: string;
  datetime: string;
  stage: string;
  title: string;
  body: string;
  detail?: string[];
}

export const swiftPaper: Link = {
  label: 'SwiFT 논문 (NeurIPS 2023, arXiv:2307.05916)',
  href: 'https://arxiv.org/abs/2307.05916',
};
export const swiftCode: Link = {
  label: 'SwiFT 공개 GitHub 저장소',
  href: 'https://github.com/Transconnectome/SwiFT',
};

export const keyFacts = [
  { label: '모집 인원', value: '3명' },
  { label: '인턴 기간', value: '2027. 1. 4.–2. 26.', sub: '8주' },
  { label: '서류 마감', value: '2026. 11. 20. (금) 18:00', sub: '한국 시간' },
  { label: '학업장려금', value: '월 60만 원', sub: '세전' },
];

export const overview = [
  { term: '모집 인원', desc: ['3명'] },
  {
    term: '모집 대상',
    desc: ['국내외 4년제 대학 학부 재학생·휴학생 (전공 제한 없음)', '2027년 또는 2028년 대학원 진학 계획자 우대'],
  },
  {
    term: '인턴 기간',
    desc: [
      '2027년 1월 4일(월) ~ 2월 26일(금), 8주',
      '8주 수료 후 희망자는 협의를 거쳐 2027년 학기 중 연구를 지속합니다.',
    ],
  },
  {
    term: '근무 형태',
    desc: [
      '대면·원격 하이브리드 운영',
      '주 1회 연구실 랩미팅과 멘토 연구 미팅은 대면 참석을 권장합니다. 지방·타 대학 학생은 사전 협의 시 온라인 화상 참여가 가능합니다.',
    ],
  },
  {
    term: '필요 역량',
    desc: [
      '선형대수·미적분·확률통계 기초, Python 데이터 분석 경험',
      '모델 구현 과제는 PyTorch 경험을 권장합니다.',
    ],
  },
];

export const midterm = {
  date: '1월 29일(금)',
  checks: [
    '프로젝트 기준선(baseline) 재현 또는 파일럿 완료',
    '주간 보고 4회 중 3회 이상 제출',
    '2개월차 연구 계획서(1쪽)',
    '연구 보안 레드라인 준수',
  ],
  after:
    '4주차에 위 네 가지를 점검해 2개월차(5~8주차 본 실험) 진행 여부를 정합니다. 1개월 평가에서 과정을 마치는 경우에도 4주 과정 수료증과 첫 달 학업장려금(600,000원)은 불이익 없이 지급합니다.',
};

export const readiness = [
  '뇌과학·뉴로이미징(fMRI·EEG) 사전 지식은 필수가 아닙니다. 1단계 학습 과제와 2단계 연구 챌린지는 뇌 신호를 처음 접하는 타 전공 학부생도 안내 문서와 AI 도구(2단계에서는 연구실이 제공하는 OpenRouter API 키 포함)의 도움을 받아 스스로 공부하며 해결할 수 있도록 설계했습니다.',
  '수강 과목·학점 정량 컷오프는 두지 않습니다. 1단계(서류 심사)에서는 이력서의 프로그래밍·프로젝트 경험과 학습·설명 과제를 실제로 시도했는지로 최소한의 기초 준비도만 확인합니다. 실제 분석·구현 역량은 2단계(연구 챌린지)와 3단계(대면 면접 구술·코드 검증)에서 평가합니다.',
];

export const support = [
  {
    title: '연구 과제 중 1개 모듈 전담',
    body: '아래 후보 과제(F1~F5) 중 하나에 배정되어 맡은 모듈을 구현·검증합니다. 가설이 기각되더라도 기준선 재현과 원인 분석이 엄밀히 입증된 음성 결과(negative result)는 성공한 결과와 동등하게 평가합니다.',
    link: { label: '연구 과제 보기', href: '#projects' },
  },
  {
    title: '전용 연산 인프라 (NVIDIA DGX Spark)',
    body: '1주차 에이전틱 코딩 온보딩을 마친 뒤 2주차부터 연구실 NVIDIA DGX Spark GPU 워크스테이션 개인 계정을 부여합니다.',
  },
  {
    title: '연구용 AI API 무제한 지원',
    body: '인턴 기간(8주) 동안 Claude Code, Codex, Cursor 등 AI 코딩·연구 도구에 연결해 쓰는 AI API(OpenRouter 등) 사용료를 사용량 제한 없이 연구실이 부담합니다(연구 목적, 사용 내역 확인).',
  },
  {
    title: '학업장려금 월 600,000원',
    body: '세전 월 600,000원, 8주 최대 1,200,000원을 지급합니다. 지급 경로·지급일과 타 대학 학생 지급 절차는 확정되는 대로 이 페이지에 안내합니다.',
  },
  {
    title: '밀착 멘토링',
    body: '담당 멘토와 주 1회 연구 미팅(30~60분)을 하고, 연구실 랩미팅과 주간 코드 리뷰(PR 기반)에 참여합니다.',
  },
];

export const supportNote =
  '인턴 참여는 커넥톰 연구실을 포함한 어느 대학원의 입학이나 연구실 배정도 보장하지 않습니다. 공저자 자격은 인턴 수료 후에도 연구에 지속 참여해 ICMJE 국제 저자 기준을 충족한 경우 심의를 거쳐 부여합니다.';

export const projects: Project[] = [
  {
    id: 'f1',
    code: 'F1',
    modality: 'fMRI',
    title: 'SwiFT 확장',
    stack: 'PyTorch',
    overview:
      '4차원 뇌 영상(4D fMRI)을 트랜스포머에 넣을 때 정보량이 적은 배경·비활성 토큰을 동적으로 가지치기(token pruning)해 메모리를 줄이고, 적은 데이터(N=20~50)로도 사전학습 표상의 전이 성능이 유지되는지 실험합니다.',
    question:
      '토큰 가지치기로 긴 4D fMRI 스캔의 어텐션 메모리를 줄이면서 정보 손실을 얼마나 막을 수 있는가? 휴지기 fMRI로 사전학습한 표상이 소표본(N=20~50) 인지·임상 과제로 효과적으로 전이되는가?',
    deliverables:
      '시공간 토큰 가지치기 어텐션 모듈 구현, 소표본 미세조정 벤치마크 파이프라인 구축, 5개 시드 반복 실험 및 절제 실험 결과표 작성.',
    refsLabel: '참고 논문 및 공개 코드',
    refs: [
      { label: 'SwiFT: Swin 4D fMRI Transformer (NeurIPS 2023)', href: 'https://arxiv.org/abs/2307.05916' },
      { label: 'GitHub: Transconnectome/SwiFT', href: 'https://github.com/Transconnectome/SwiFT' },
      { label: 'GitHub: Transconnectome/NeuroMamba (후속 4D fMRI 상태공간 모델)', href: 'https://github.com/Transconnectome/NeuroMamba' },
    ],
  },
  {
    id: 'f2',
    code: 'F2',
    modality: 'EEG',
    title: 'DIVER 전극 불변성 확장',
    stack: 'PyTorch',
    overview:
      '두피 뇌파(scalp EEG) 모델 DIVER-0에서 다룬 전극 불변(electrode-invariant) 표상 학습을 확장합니다. 병원용 19채널 이상 뇌파로 배운 모델이 웨어러블처럼 채널이 극소수이거나(예: 이마 2채널) 실환경 잡음이 많은 환경에서도 견고하게 작동하는지 평가·보강합니다.',
    question:
      '19채널 이상 임상 뇌파로 학습한 DIVER-0 표상이 극소수 채널(2~4채널)이나 이종 장비 몽타주로 옮겨 갈 때 성능이 어디까지 유지되는가? 실환경 잡음(전원선 잡음, 접촉 불량, 부분 채널 탈락)에 표상이 얼마나 흔들리며 어떻게 보강할 수 있는가?',
    deliverables:
      'DIVER-0 기반 극단적 채널 축소·전극 마스킹·잡음 주입 절제 파이프라인 구현, 이종 공개 EEG 데이터셋 간 제로샷/소표본 견고성 평가, 채널 수·잡음 강도별 부트스트랩 신뢰구간 산출.',
    refsLabel: '참고 논문',
    refs: [{ label: 'DIVER: Brain Electrophysiology Foundation Model (arXiv:2512.19097)', href: 'https://arxiv.org/abs/2512.19097' }],
    refsNote:
      'DIVER 코드 저장소는 연구실 내부 저장소로, 선발 후 온보딩을 마치면 권한을 드립니다. 논문은 두개내 뇌파(iEEG) 기반 DIVER-1 참고 문헌이며, F2 과제는 두피 뇌파 모델 DIVER-0를 극소수 채널·잡음 환경으로 확장합니다.',
  },
  {
    id: 'f3',
    code: 'F3',
    modality: 'AI4Science',
    title: 'NeuroX 가설 근거 합성',
    stack: 'Python · LLM API',
    overview:
      '연구 가설마다 지지·반대 논문 근거를 학술 문헌에서 찾아 구조화하는 합성 에이전트와, 인용의 실존·맥락 정합성을 독립 점검하는 비평 에이전트가 서로 검증하는 파이프라인을 구축합니다.',
    note: '뇌영상·딥러닝 직접 구현 경험이 적은 학생도 지원할 수 있습니다.',
    question:
      'NeuroX 핵심 가설마다 지지 근거와 반대(반증) 근거를 문헌에서 균형 있게 찾아, AI 합성 에이전트와 비평 에이전트가 서로 검증하며 인간 연구자 평가와 높은 일치도를 달성할 수 있는가?',
    deliverables:
      '가설 지지·반대 근거 합성-비평 멀티에이전트 파이프라인 구축, DOI/초록 기반 인용 검증 자동화 모듈 구현, 공개 문헌·기발표 학술 가설 대상 인간 평가자와의 일치도 측정 보고서 작성.',
    refsLabel: '참고 공개 코드',
    refs: [
      { label: 'GitHub: Transconnectome/AI-CoScientist', href: 'https://github.com/Transconnectome/AI-CoScientist' },
      { label: 'GitHub: Transconnectome/sci-method', href: 'https://github.com/Transconnectome/sci-method' },
    ],
  },
  {
    id: 'f4',
    code: 'F4',
    modality: 'FM + 에이전트',
    title: 'NeuroX-Reason 도구 통합',
    stack: 'Python · LLM API · 테스트 코드',
    overview:
      '추론형 언어 모델 에이전트(LLM Agent)가 뇌영상·뇌파 파운데이션 모델(SwiFT, DIVER 등)을 분석 도구로 호출해 복합 추론을 수행하도록 연결합니다. 모달리티 불일치나 잘못된 입력은 추측하지 않고 명확히 거부(abstention)하도록 입출력 계약과 테스트를 구현합니다.',
    note: '뇌영상·딥러닝 직접 구현 경험이 적은 학생도 지원할 수 있습니다.',
    question:
      '뇌 신호 파운데이션 모델을 언어 모델 에이전트가 호출하는 도구로 붙일 때, 모달리티 불일치나 규격 외 입력을 받으면 환각으로 추측하지 않고 신뢰성 있게 거부하게 만들 수 있는가?',
    deliverables:
      '뇌영상·뇌파 파운데이션 모델 1~2개의 에이전트 도구 래퍼(tool wrapper) 및 입출력 계약 스키마 구현, 단위·통합 테스트 스위트 구축, 합성 오류 입력 벤치마크 제작 및 거부율(abstention rate) 정량 평가 보고서 작성.',
    refsLabel: '연동 대상 모델',
    refs: [
      { label: 'SwiFT (GitHub)', href: 'https://github.com/Transconnectome/SwiFT' },
      { label: 'DIVER (arXiv:2512.19097)', href: 'https://arxiv.org/abs/2512.19097' },
    ],
  },
  {
    id: 'f5',
    code: 'F5',
    modality: 'EEG · 해외 공동연구',
    title: 'EEG GINR',
    stack: 'PyTorch',
    overview:
      '여러 사람의 뇌파를 연속 좌표 함수 신경망(Generalized Implicit Neural Representation, GINR) 하나로 표현하고, 새로운 피험자에게는 작은 잠재 벡터만 맞춰 신호가 정밀하게 재구성되는지 공개 데이터(BCI Competition IV-2a)로 해외 공동연구진과 함께 검증합니다.',
    question:
      '피험자 공통 좌표 신경망과 개인별 저차원 잠재 벡터를 분리해 학습하면, 처음 보는 피험자에게 작은 잠재 벡터만 맞춰서 단순 전이학습이나 보간법보다 뇌파 재구성 성능이 나아지는가?',
    deliverables:
      '공개 데이터셋(BCI Competition IV-2a) 전처리 및 좌표 질의 로더 구축, 소형 프로토타입을 다피험자 규모로 키우는 PyTorch 학습 파이프라인 구현, 미관측 피험자 간 재구성 성능 비교 결과표 작성.',
    refsLabel: '공개 데이터 및 연습 챌린지',
    refs: [{ label: 'GitHub: Transconnectome/connectome-challenges-public', href: 'https://github.com/Transconnectome/connectome-challenges-public' }],
    refsNote: '공개 데이터: BCI Competition IV-2a',
  },
];

export const steps: Step[] = [
  {
    date: '~ 11. 20. (금) 18:00',
    datetime: '2026-11-20T18:00:00+09:00',
    stage: '1단계',
    title: '서류 접수',
    body: '이력서, 지원서, 학습·설명 과제(A4 2쪽), 온라인 사전 설문을 제출합니다.',
  },
  {
    date: '11. 25. (수)',
    datetime: '2026-11-25',
    stage: '결과',
    title: '서류 결과 · 챌린지 안내',
    body: '서류 심사에서 기본 준비가 확인된 지원자 전원에게 개인용 OpenRouter AI API 키와 2단계 연구 챌린지 과제를 보냅니다.',
  },
  {
    date: '11. 25. (수) ~ 12. 7. (월) 23:59',
    datetime: '2026-12-07T23:59:00+09:00',
    stage: '2단계',
    title: '연구 챌린지',
    body: '연구실이 제공한 AI API 키로 공개 뇌 신호(EEG/fMRI) 챌린지를 풀고, 본인만의 확장 질문 1개를 실험·검증합니다. 확장 질문의 사전 예측 기준은 12월 1일(화)까지 제출합니다.',
  },
  {
    date: '12. 11. (금)',
    datetime: '2026-12-11',
    stage: '결과',
    title: '면접 대상 발표',
    body: '필수 항목을 충족하고 60점 이상인 기준 통과자 중 최종 정원(3명)의 약 2~3배수(약 6~9명 내외)를 대면 면접 대상으로 안내합니다. 기준 통과자가 2~3배수 이하이면 통과자 전원이 면접을 봅니다.',
  },
  {
    date: '12. 14. (월) ~ 12. 18. (금)',
    datetime: '2026-12-14',
    stage: '3단계',
    title: '대면 면접 · 1인 30분',
    body: '서울대학교에서 진행하며 본인 노트북을 지참합니다. 지도교수와 각 연구 프로젝트 담당 대학원생 멘토가 함께 참여합니다.',
    detail: [
      '챌린지 새 seed 즉석 재실행·코드 확인, 학습·설명 과제 3분 무메모 설명 (~10분)',
      '연구 딜레마 상황 대화, 사전 설문·챌린지 수행 과정 질의 (~12분)',
      '관심 과제·진학 계획 확인, 함께 연구할 대학원생 멘토·지도교수와의 질의응답 (~8분, 지원자 역질문은 채점하지 않음)',
    ],
  },
  {
    date: '12. 22. (화)',
    datetime: '2026-12-22',
    stage: '발표',
    title: '최종 합격자 발표',
    body: '최종 3명을 선발합니다. 12월 중 사전 온보딩·계정 설정을 거쳐 2027년 1월 4일(월)에 시작합니다.',
  },
];

export const stepsNote = [
  '1단계는 순위를 매기지 않습니다. 필수 서류·설문 제출, 학습 과제 시도, 연구 윤리 관련 기본 요건만 확인하고, 통과자 전원에게 챌린지와 개인 AI API 키를 드립니다.',
  '설문은 이 확인 외에는 점수에 넣지 않고, 면접 대화와 선발 후 멘토 배정 참고 자료로 씁니다.',
];

export const apply = {
  deadline: '2026년 11월 20일(금) 18:00 (한국 시간)',
  email: 'connectome@snu.ac.kr',
  subject: '[2026동계인턴지원] 이름_학교_진학희망연도',
  subjectExample: '[2026동계인턴지원] 홍길동_서울대_2028',
  consent: '개인정보 수집·이용에 동의합니다',
};

export const materials = [
  {
    file: '이력서_이름.pdf',
    tag: '필수 · A4 1~2쪽',
    body: '인적사항, 주요 수강 과목, 프로그래밍·프로젝트·연구 경험',
  },
  {
    file: '지원서_이름.pdf',
    tag: '필수 · A4 1쪽',
    body: '희망 연구 프로젝트(F1~F5 중 1·2순위와 이유), 대학원 진학 계획(희망 시기·과정·분야), 8주 후 학기 중 가용 시간, 8주 기간 중 중복 일정 유무',
  },
  {
    file: '과제_이름.pdf',
    tag: '필수 · A4 2쪽 이내',
    body: '학습·설명 과제. 아래 과제 안내를 참고하세요.',
    link: { label: '학습·설명 과제 안내', href: '#task' },
  },
  {
    file: '온라인 사전 설문',
    tag: '필수 · 약 25~30분',
    body: '정답이 있는 시험이 아니라, 연구 상황에서 선호하는 문제 해결 호흡·협업 스타일·연구 윤리 기준을 묻는 설문입니다. 점수화해 순위를 매기지 않으며, 면접 대화와 선발 후 멘토 배정 참고 자료로 씁니다. PDF 서류와 같은 마감까지 응답해 주세요. 설문 링크는 접수를 시작할 때 이 페이지에 게시합니다.',
  },
  {
    file: '선택자료_이름.pdf',
    tag: '선택',
    body: 'GitHub 링크, 기존 보고서·포스터, 공개 챌린지 사전 풀이 등',
  },
];

export const task = {
  topic: '뇌 영상을 트랜스포머에 넣으면 왜 메모리가 모자라고, 어떻게 줄이는가',
  intro:
    '사전 지식을 평가하는 시험이 아닙니다. fMRI 한 회기를 4차원 데이터(예: 96×96×96 복셀 × 20 시점)로 트랜스포머 모델에 넣으려 할 때, 왜 메모리가 부족하고 어떻게 줄이는지를 AI 도구와 문헌으로 스스로 공부해 자기 말로 설명하는 A4 2쪽 탐구 과제입니다. 다음 다섯 가지를 씁니다.',
  items: [
    '셀프 어텐션(self-attention)이 무엇을 계산하는지 수식 하나와 자기 말로 설명합니다.',
    '이 데이터를 토큰으로 어떻게 나눌지 정하고, 어텐션 계산에 필요한 메모리를 직접 계산합니다. 가정과 계산 과정을 모두 적습니다.',
    '메모리를 줄이는 방법을 둘 이상 찾아 같은 기준으로 비교하고, 하나를 고른 이유를 씁니다. 그중 하나는 반드시 Swin Transformer의 윈도 어텐션(window attention)이어야 합니다.',
    '아직 이해하지 못한 것 하나와, 그것을 알아내려면 무엇을 하겠는지 씁니다.',
    '어떻게 공부했는지 씁니다: 읽은 자료, 쓴 AI 도구, 걸린 시간, 가장 막혔던 곳과 거기서 한 일.',
  ],
  notes: [
    '메모리는 어텐션 점수 행렬(한 층·한 헤드)부터 계산해도 되며, 패치 크기·정밀도(FP16/FP32) 등 가정은 자유롭게 정해 적으면 됩니다.',
    '예상 소요 시간은 배경지식에 따라 약 3~6시간(AI 도구·문헌 학습 포함)입니다.',
    '계산을 짧은 코드로 확인했다면 GitHub 링크를 붙입니다(선택).',
    'AI 도구로 공부해도 됩니다. 대신 면접에서 이 주제를 메모 없이 3분 안에 다시 설명하고 질문에 답합니다.',
    '정답을 맞혔는지보다 어려운 부분을 피하지 않고 끝까지 파고들었는지를 봅니다. 계산이 틀려도 과정이 보이면 괜찮습니다.',
  ],
};

export const privacy =
  '제출 메일 본문에 "개인정보 수집·이용에 동의합니다" 문구를 반드시 적어 주세요. 제출 서류와 설문 응답은 이번 인턴 선발 심사와 선발 후 행정 처리에만 씁니다. 선발되지 않은 지원자의 서류와 설문 원본은 선발 종료 후 지체 없이 파기하는 원칙이며, 구체적인 보유·파기 기준은 접수를 시작할 때 이 페이지에 안내합니다.';
