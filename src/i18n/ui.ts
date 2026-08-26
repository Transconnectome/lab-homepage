export type Lang = 'en' | 'ko';

export const ui = {
  en: {
    // Navbar
    'nav.research': 'Research',
    'nav.publications': 'Publications',
    'nav.people': 'People',
    'nav.news': 'News',
    'nav.history': 'History',
    'nav.radar': 'Radar',
    'nav.ideas': 'Ideas',
    'nav.join': 'Join us',
    'nav.langToggle': '한국어',

    // Footer
    'footer.navigate': 'Navigate',
    'footer.contact': 'Contact',
    'footer.ideaLab': 'AI Idea Lab',
    'footer.researchRadar': 'Research Radar',
    'footer.affiliations':
      'Department of Psychology · Interdisciplinary Program in AI (IPAI) · Department of Brain & Cognitive Sciences',
    'footer.address': 'Office M512, Building 16<br />Seoul National University<br />1 Gwanak-ro, Gwanak-gu, Seoul',
    'footer.backToTop': '↑ Back to top',

    // Home
    'home.eyebrow': 'Seoul National University · Connectome Laboratory',
    'home.mottoCredit': '— Leonardo da Vinci, the lab’s founding conviction',
    'home.heroDesc':
      'We study how the brain’s connections give rise to mind — cognition, emotion, development, and psychiatric resilience. Our instruments are brain foundation models, multimodal genetics, and quantum machine learning; our conviction is that seeing well is a scientific skill.',
    'home.exploreCta': 'Explore our research',
    'home.peopleCta': 'Meet the people',
    'home.mapEyebrow': 'The research map',
    'home.mapTitle': 'Four research axes, one brain',
    'home.mapDesc': 'An illustrative sketch of how our research programs connect — select a node to see what each axis studies and how the axes link together.',
    'home.newsEyebrow': 'From the lab',
    'home.newsTitle': 'Latest news',
    'home.allNews': 'All news →',
    'home.researchEyebrow': 'Research',
    'home.researchTitle': 'From foundation models to art exhibitions',
    'home.researchDesc': 'Different instruments, one question: how do neural connections become a mind?',
    'home.readMore': 'Read more →',
    'home.pubsEyebrow': 'Selected work',
    'home.pubsTitle': 'Featured publications',
    'home.allPubs': 'All publications →',
    'home.alumniEyebrow': 'Alumni',
    'home.alumniTitle': 'Where our people go',
    'home.alumniCta': 'Meet current members and alumni →',
    'home.joinTitle': 'Curious about brains, models, or both?',
    'home.joinDesc':
      'We welcome graduate students, postdocs, and undergraduate interns from psychology, AI, neuroscience, physics, and beyond. Tell us what you want to figure out.',
    'home.joinCta': 'How to apply',
    'home.emailPi': 'Email the PI',
    'home.projectsEyebrow': 'Open source',
    'home.projectsTitle': 'Featured projects',
    'home.allProjects': 'All code on GitHub →',
    'home.projectPaper': 'Paper',

    // Research page
    'research.eyebrow': 'Research',
    'research.title': 'How do neural connections become a mind?',
    'research.desc':
      'We combine representation learning, population genetics, high-performance computing — and occasionally an art gallery — to study the functional anatomy of human connectomes.',
    'research.keyDirections': 'Key directions',

    // People page
    'people.eyebrow': 'People',
    'people.title': 'The people behind the models',
    'people.desc':
      'Psychologists, engineers, physicists, economists, and one art historian — a team at Seoul National University that believes good science needs many ways of seeing.',
    'people.labLifeEyebrow': 'Lab life',
    'people.labLifeTitle': 'Work hard, dream boldly, enjoy life',
    'people.retreatTitle': 'Hongcheon retreats & hackathons',
    'people.retreatDesc':
      'Multi-day deep-dive hackathons in the hills of Gangwon-do: building EEG foundation models by day, cooking and debating ideas by night.',
    'people.fellowshipTitle': 'Global fellowships',
    'people.fellowshipDesc':
      'Students regularly spend funded research terms at MILA (Montreal) and Brookhaven National Laboratory (New York) — and come back with new collaborations.',
    'people.artTitle': 'Art, opera, coffee & cocktails',
    'people.artDesc':
      "From interactive EEG art at the OB/Scene festival to the PI's handmade cocktails and makgeolli appreciation — creativity thrives on life's finer pleasures.",

    // Publications page
    'pubs.eyebrow': 'Publications',
    'pubs.desc':
      "The lab's peer-reviewed record — from Nature Communications and Molecular Psychiatry to NeurIPS and IEEE proceedings — synced from OpenAlex and curated by hand. Lab members are highlighted in each author list.",
    'pubs.alsoOn': 'Also on',

    // News page
    'news.eyebrow': 'News',
    'news.title': "What's new in the lab",
    'news.desc': 'Papers accepted, awards won, exhibitions opened — and the people who made them happen.',

    // History page
    'history.eyebrow': 'History',
    'history.title': 'Milestones and memories',
    'history.desc':
      "Graduations, hackathons, fellowships abroad, and the occasional art exhibition — the lab's story, year by year.",

    // Radar page
    'radar.eyebrow': 'Research radar',
    'radar.title': "What we're reading this week",
    'radar.desc':
      'A weekly scan of new arXiv papers in brain foundation models, fMRI/EEG dynamics, genomics & connectomics, and quantum machine learning. Summaries are generated by an LLM pipeline and labeled by how they were produced; selected lab papers appear alongside.',
    'radar.ideasHint': 'Wondering what these papers could mean for us? Visit the',
    'radar.ideasLink': 'AI Idea Lab',
    'radar.ideasHint2': '— weekly machine-proposed hypotheses built on this radar.',

    // Ideas page
    'ideas.eyebrow': 'AI Idea Lab',
    'ideas.title': 'What would an AI have us try next?',
    'ideas.desc':
      'Every week, a language model reads our research areas, recent publications, and the newest papers on the Research Radar — then proposes hypotheses connecting the two. We publish them unedited, as conversation starters for lab meetings and prospective students.',
    'ideas.honestyTitle': 'Honesty note:',
    'ideas.honestyBody':
      'everything below is machine-generated and not lab-endorsed. Ideas may be wrong, infeasible, or already done — judging that is half the fun. Each card names the model that wrote it.',
    'ideas.hypothesis': 'Hypothesis',
    'ideas.whyNow': 'Why now, why us',
    'ideas.buildsOn': 'Builds on lab work',
    'ideas.inspiration': 'External inspiration',
    'ideas.firstExperiment': 'A first experiment',
    'ideas.howFails': 'How this fails',
    'ideas.ctaDesc':
      'Interested in one of these ideas, or want to explore it with us? Get in touch — we welcome inquiries from prospective graduate students, postdocs, and undergraduate interns.',
    'ideas.cta': 'Get in touch',
    'ideas.empty': 'No ideas yet',
    'ideas.emptyDesc': "The weekly generator hasn't produced its first batch.",

    // Join page
    'join.eyebrow': 'Join us',
    'join.title': 'Tell us what you want to figure out',
    'join.desc':
      'We welcome graduate students (PhD / MS-PhD / MS), postdoctoral fellows, and undergraduate research interns on a rolling basis. Applications are reviewed year-round; formal admission follows each SNU graduate admissions cycle.',
    'join.tracksEyebrow': 'Degree programs',
    'join.tracksTitle': 'Three ways into the lab',
    'join.gsai': 'Interdisciplinary Program in AI (IPAI)',
    'join.gsaiDesc':
      'Foundation models (NeuroMamba, DIVER-0), 4D spatiotemporal representation learning, geometric deep learning, and large-scale multimodal brain AI.',
    'join.bcs': 'Dept. of Brain & Cognitive Sciences (BCS)',
    'join.bcsDesc':
      'Generative fMRI modeling, decoding cognitive dynamics, EEG/ECoG signal processing, and multimodal brain-behavior connectivity.',
    'join.psych': 'Department of Psychology',
    'join.psychDesc':
      'Computational psychiatry, multi-omics genetics (PRS) and brain connectivity, and developmental prediction of child & adolescent mental health.',
    'join.internEyebrow': 'Undergraduate internships',
    'join.internTitle': 'Research internships',
    'join.internDesc':
      'We recruit undergraduate research interns on a rolling basis. Recent interns have worked on quantum machine learning (QML), EEG foundation models, and imaging-genetics projects. Prior knowledge of quantum mechanics or neuroscience is not required — we value motivation to learn fast and critical thinking. Openings are announced on department boards and in lab news.',
    'join.applyEyebrow': 'How to apply',
    'join.applyTitle': 'How to apply',
    'join.materialsTitle': 'What to send',
    'join.material1': 'Curriculum Vitae — education, research experience, projects, technical skills',
    'join.material2': 'Transcripts',
    'join.material3':
      'A short statement of interest — one or two paragraphs on which lab topic draws you (brain foundation models, QML, genetics, fMRI/EEG…) and why',
    'join.sendTitle': 'Where to send it',
    'join.sendDesc':
      'Email the materials below and we will follow up with an interview. International applicants are always welcome — feel free to apply in English.',
  },

  ko: {
    // Navbar
    'nav.research': '연구',
    'nav.publications': '논문',
    'nav.people': '구성원',
    'nav.news': '소식',
    'nav.history': '연혁',
    'nav.radar': '레이더',
    'nav.ideas': '아이디어',
    'nav.join': '함께하기',
    'nav.langToggle': 'English',

    // Footer
    'footer.navigate': '바로가기',
    'footer.contact': '연락처',
    'footer.ideaLab': 'AI 아이디어 랩',
    'footer.researchRadar': '리서치 레이더',
    'footer.affiliations': '심리학과 · 협동과정 인공지능전공(IPAI) · 뇌인지과학과',
    'footer.address': '서울특별시 관악구 관악로 1<br />서울대학교 16동 M512호',
    'footer.backToTop': '↑ 맨 위로',

    // Home
    'home.eyebrow': '서울대학교 · 커넥톰 연구실',
    'home.mottoCredit': '— 레오나르도 다빈치. 모든 것은 서로 연결되어 있다.',
    'home.heroDesc':
      '뇌의 연결이 어떻게 마음을 만들어내는지 연구합니다. 인지와 정서, 발달, 그리고 정신건강의 회복탄력성까지가 그 대상입니다. 뇌 파운데이션 모델과 멀티모달 유전체학, 양자 머신러닝이 우리의 도구이며, ‘잘 보는 것’이야말로 과학적 능력이라 믿습니다.',
    'home.exploreCta': '연구 살펴보기',
    'home.peopleCta': '구성원 만나기',
    'home.mapEyebrow': '연구 지도',
    'home.mapTitle': '네 개의 연구 축, 하나의 뇌',
    'home.mapDesc': '연구 프로그램들이 연결되는 방식의 일러스트 스케치 — 노드를 선택하면 각 축이 무엇을 연구하고 서로 어떻게 이어지는지 볼 수 있습니다.',
    'home.newsEyebrow': '연구실 소식',
    'home.newsTitle': '최근 소식',
    'home.allNews': '전체 소식 →',
    'home.researchEyebrow': '연구',
    'home.researchTitle': '파운데이션 모델부터 예술 전시까지',
    'home.researchDesc': '갈래는 달라도 질문은 하나: 신경 연결은 어떻게 마음이 되는가?',
    'home.readMore': '자세히 보기 →',
    'home.pubsEyebrow': '대표 성과',
    'home.pubsTitle': '주요 논문',
    'home.allPubs': '전체 논문 →',
    'home.alumniEyebrow': '동문',
    'home.alumniTitle': '연구실 사람들이 나아간 곳',
    'home.alumniCta': '현재 구성원과 동문 보기 →',
    'home.joinTitle': '뇌가 궁금한가요, 모델이 궁금한가요 — 아니면 둘 다인가요?',
    'home.joinDesc':
      '심리학, 인공지능, 신경과학, 물리학 등 다양한 배경의 대학원생, 박사후연구원, 학부 인턴을 환영합니다. 무엇을 밝혀내고 싶은지 들려주세요.',
    'home.joinCta': '지원 방법',
    'home.emailPi': '교수님께 이메일',
    'home.projectsEyebrow': '오픈 소스',
    'home.projectsTitle': '주요 프로젝트',
    'home.allProjects': 'GitHub에서 전체 코드 →',
    'home.projectPaper': '논문',

    // Research page
    'research.eyebrow': '연구',
    'research.title': '신경 연결은 어떻게 마음이 되는가?',
    'research.desc':
      '표현 학습과 집단 유전학, 고성능 컴퓨팅을 결합해 인간 커넥톰의 기능적 해부학을 연구합니다. 때로는 미술관도 실험실이 됩니다.',
    'research.keyDirections': '핵심 방향',

    // People page
    'people.eyebrow': '구성원',
    'people.title': '모델 뒤에 있는 사람들',
    'people.desc':
      '심리학자와 엔지니어, 물리학자, 경제학도, 그리고 미술사학도까지. 좋은 과학에는 여러 개의 시선이 필요하다고 믿는 서울대학교 연구팀입니다.',
    'people.labLifeEyebrow': '연구실 생활',
    'people.labLifeTitle': '연구는 치열하게, 꿈은 대담하게, 삶은 즐겁게',
    'people.retreatTitle': '홍천 리트릿과 해커톤',
    'people.retreatDesc':
      '강원도의 산자락에서 며칠간 몰입하는 해커톤 — 낮에는 EEG 파운데이션 모델을 만들고, 밤에는 함께 요리하며 아이디어를 토론합니다.',
    'people.fellowshipTitle': '글로벌 펠로우십',
    'people.fellowshipDesc':
      '학생들이 MILA(몬트리올)와 브룩헤이븐 국립연구소(뉴욕)에서 수개월간 연구 펠로우십을 수행하고, 새로운 공동연구와 함께 돌아옵니다.',
    'people.artTitle': '예술, 오페라, 커피, 그리고 칵테일',
    'people.artDesc':
      '옵/신 페스티벌의 인터랙티브 EEG 아트부터 교수님의 수제 칵테일과 막걸리 감상까지 — 창의성은 삶의 즐거움에서 자란다고 믿습니다.',

    // Publications page
    'pubs.eyebrow': '논문',
    'pubs.desc':
      'Nature Communications와 Molecular Psychiatry부터 NeurIPS와 IEEE 프로시딩까지 — OpenAlex에서 자동으로 모으고 직접 다듬은 연구실의 피어리뷰 논문 목록입니다. 저자 목록에는 연구실 구성원이 강조되어 있습니다.',
    'pubs.alsoOn': '외부 프로필:',

    // News page
    'news.eyebrow': '소식',
    'news.title': '연구실의 새로운 소식',
    'news.desc': '게재된 논문, 수상, 전시 — 그리고 그것을 만들어낸 사람들의 이야기.',

    // History page
    'history.eyebrow': '연혁',
    'history.title': '이정표와 기억들',
    'history.desc': '졸업, 해커톤, 해외 연수, 그리고 가끔의 예술 전시까지 — 연구실의 이야기를 해마다 기록합니다.',

    // Radar page
    'radar.eyebrow': '리서치 레이더',
    'radar.title': '이번 주 우리가 읽고 있는 것',
    'radar.desc':
      '뇌 파운데이션 모델, fMRI/EEG 역학, 유전체학과 커넥토믹스, 양자 머신러닝 분야의 새 arXiv 논문을 매주 스캔합니다. 요약은 LLM 파이프라인이 생성하며 생성 방식이 함께 표기됩니다. 연구실 논문도 선별 수록됩니다.',
    'radar.ideasHint': '이 논문들이 우리에게 어떤 의미일지 궁금하다면,',
    'radar.ideasLink': 'AI 아이디어 랩',
    'radar.ideasHint2': '을 방문해 보세요 — 이 레이더를 바탕으로 매주 기계가 제안하는 가설들입니다.',

    // Ideas page
    'ideas.eyebrow': 'AI 아이디어 랩',
    'ideas.title': 'AI라면 다음에 무엇을 시도해 보자고 할까?',
    'ideas.desc':
      '매주 언어모델이 연구실의 연구 분야, 최근 논문, 리서치 레이더의 최신 논문을 읽고 이 둘을 연결하는 가설을 제안합니다. 랩미팅과 지원자들을 위한 대화의 출발점으로, 편집 없이 그대로 공개합니다.',
    'ideas.honestyTitle': '정직성 안내:',
    'ideas.honestyBody':
      '아래 내용은 전부 기계가 생성한 것이며 연구실의 공식 입장이 아닙니다. 틀렸거나, 실현 불가능하거나, 이미 있는 아이디어일 수 있습니다 — 그것을 가려내는 것이 재미의 절반입니다. 각 카드에 작성한 모델이 표기됩니다.',
    'ideas.hypothesis': '가설',
    'ideas.whyNow': '왜 지금, 왜 우리인가',
    'ideas.buildsOn': '연결되는 연구실 연구',
    'ideas.inspiration': '외부 영감',
    'ideas.firstExperiment': '첫 실험 제안',
    'ideas.howFails': '실패 시나리오',
    'ideas.ctaDesc':
      '이 아이디어들에 관심이 있거나 함께 발전시켜 보고 싶다면 연락 주세요. 대학원생, 박사후연구원, 학부 인턴 지원 문의를 언제든 환영합니다.',
    'ideas.cta': '문의하기',
    'ideas.empty': '아직 아이디어가 없습니다',
    'ideas.emptyDesc': '주간 생성기가 아직 첫 결과를 만들지 않았습니다.',

    // Join page
    'join.eyebrow': '함께하기',
    'join.title': '무엇을 밝혀내고 싶은지 들려주세요',
    'join.desc':
      '대학원생(박사/석박통합/석사), 박사후연구원, 학부 연구 인턴을 상시 모집합니다. 지원서는 연중 검토하며, 정식 입학은 서울대학교 대학원 입시 일정을 따릅니다.',
    'join.tracksEyebrow': '학위 과정',
    'join.tracksTitle': '연구실로 오는 세 가지 길',
    'join.gsai': '협동과정 인공지능전공 (IPAI)',
    'join.gsaiDesc':
      '파운데이션 모델(NeuroMamba, DIVER-0), 4D 시공간 표현학습, 기하학적 딥러닝, 대규모 멀티모달 뇌 AI 연구.',
    'join.bcs': '뇌인지과학과 (BCS)',
    'join.bcsDesc': 'fMRI 생성 모델링, 인지 역동성 해독, EEG/ECoG 신호 처리, 다중모달 뇌-행동 연결성 연구.',
    'join.psych': '심리학과',
    'join.psychDesc': '계산정신의학, 다중오믹스 유전체(PRS)와 뇌연결성, 아동·청소년 정신건강의 발달적 예측 연구.',
    'join.internEyebrow': '학부 인턴십',
    'join.internTitle': '연구 인턴십',
    'join.internDesc':
      '학부 연구 인턴은 수시로 모집합니다. 최근에는 양자 머신러닝(QML), EEG 파운데이션 모델, 뇌영상-유전체 융합 프로젝트에서 인턴들이 활동해 왔습니다. 양자역학이나 신경과학 사전 지식은 필수가 아닙니다 — 빠르게 배우려는 동기와 비판적 사고를 더 중요하게 봅니다. 모집 공고는 학과 게시판과 연구실 소식으로 안내됩니다.',
    'join.applyEyebrow': '지원 방법',
    'join.applyTitle': '지원 방법',
    'join.materialsTitle': '준비 서류',
    'join.material1': 'Curriculum Vitae — 학력, 연구 경험, 프로젝트, 기술 스택',
    'join.material2': '성적증명서',
    'join.material3':
      '관심 연구 소개 — 커넥톰랩의 어떤 주제(뇌 파운데이션 모델, QML, 유전체, fMRI/EEG 등)에 왜 끌리는지 1-2단락',
    'join.sendTitle': '보내실 곳',
    'join.sendDesc':
      '아래 이메일로 서류를 보내주시면 검토 후 인터뷰 일정을 안내해 드립니다. 국제 지원자도 언제나 환영합니다 — 영어로 지원하셔도 됩니다.',
  },
} as const;

export type UIKey = keyof (typeof ui)['en'];

export function useTranslations(lang: Lang) {
  return function t(key: UIKey): string {
    return (ui[lang] as Record<UIKey, string>)[key] ?? ui.en[key];
  };
}

/**
 * Map a pathname to its counterpart in the other language.
 * Korean is the default locale and sits at the root; English is under /en/.
 */
export function altLangPath(pathname: string, lang: Lang): string {
  if (lang === 'ko') {
    return pathname === '/' ? '/en/' : `/en${pathname}`;
  }
  const stripped = pathname.replace(/^\/en/, '');
  return stripped === '' || stripped === '/' ? '/' : stripped;
}

export function localePath(lang: Lang, path: string): string {
  return lang === 'en' ? `/en${path === '/' ? '/' : path}` : path;
}
