import type { Lang } from '../i18n/ui';

export interface DailyEditorialTheme {
  id: string;
  axisIndex: string;
  tabLabel: Record<Lang, string>;
  eyebrow: Record<Lang, string>;
  headline: {
    ko: { lead: string; emphasis: string; tail: string };
    en: { lead: string; emphasis: string; tail: string };
  };
  heroSub: Record<Lang, string>;
  premiseCol1: {
    title: Record<Lang, string>;
    p1: Record<Lang, string>;
    p2: Record<Lang, string>;
    pullquote: Record<Lang, string>;
  };
  premiseCol2: {
    title: Record<Lang, string>;
    p1: Record<Lang, string>;
    p2: Record<Lang, string>;
    p3: Record<Lang, string>;
  };
}

export const dailyThemes: DailyEditorialTheme[] = [
  // 0: 4D Brain Foundation Models & Spatiotemporal Dynamics
  {
    id: 'foundation',
    axisIndex: 'AXIS 01',
    tabLabel: {
      ko: '01 · 4D 파운데이션 & 동역학',
      en: '01 · 4D Foundation & Dynamics',
    },
    eyebrow: {
      ko: 'Laboratory Prospectus · 2026 / 4차원 시공간 뇌 동역학 & 인사이드-아웃',
      en: 'Laboratory Prospectus · 2026 / 4D Brain Dynamics & Predictive Processing',
    },
    headline: {
      ko: {
        lead: '뇌는 카메라가 아니라,',
        emphasis: '프로젝터',
        tail: '다. 어둠 속에 가설을 쏘아 올린다.',
      },
      en: {
        lead: 'The brain is not a camera. It is a',
        emphasis: 'projector',
        tail: ', casting preformed conjectures into the dark.',
      },
    },
    heroSub: {
      ko: '우리는 100조 개의 시냅스 연결망과 4차원 신경 시계열을 통해 인간 마음의 숨은 기하학을 탐구합니다. 인간을 기계 부품으로 환원하기 위함이 아닙니다. 어둠 속에서 가설을 던지고, 그 가설이 현실과 어긋나 산산조각 나는 순간(예측 오차)에서 어떻게 배움과 지능, 그리고 고유한 자아의 연속성이 피어나는가를 묻습니다.',
      en: 'We explore the hidden geometry of mind through 100 trillion synaptic connections and 4D neural time series. Not to reduce human beings to mechanical components, but to ask how learning, intelligence, and the continuity of the self emerge from the very moment preformed conjectures collide with reality and shatter into prediction errors.',
    },
    premiseCol1: {
      title: {
        ko: '인사이드-아웃: 뇌는 수동적 수광판이 아니다',
        en: 'Inside-Out: The Brain Is Not a Passive Receptor',
      },
      p1: {
        ko: '전통적인 신경과학의 외부-내부(Outside-In) 관점은 뇌를 감각 입력을 수동적으로 받아들여 처리하는 카메라로 바라보았습니다. 그러나 실제 뇌는 자극이 주어지기 전부터 내부에서 스스로 발화 궤적을 만들어내는 사전 재생(Preplay)의 동역학을 갖추고 있습니다.',
        en: 'Traditional neuroscience often adopted an outside-in stance, viewing the brain as an exposure camera passively recording sensory inputs. Yet the biological brain exhibits preplay dynamics, continually projecting endogenous firing trajectories prior to sensory impingement.',
      },
      p2: {
        ko: '피아노 건반의 수가 88개로 유한하더라도 천문학적인 선율을 낳듯이, 뇌는 태어날 때부터 유한한 시냅스 기저 위에서 무수한 가설의 멜로디를 연주합니다. 우리가 경험하는 현실은 뇌가 칠흑 같은 두개골 속에서 직조하는 통제된 환각(Controlled Hallucination)입니다.',
        en: 'Just as eighty-eight keys yield astronomical melodies, the brain plays preconfigured conjectures upon a finite synaptic substrate. Conscious reality is a controlled hallucination woven within the pitch-black vault of the cranium.',
      },
      pullquote: {
        ko: '“배움의 유일한 화폐는 예측 오차(Prediction Error)다. 가설이 현실과 부딪혀 박살 나는 순간에서만 뇌는 세계의 지도를 다시 그린다.”',
        en: '“The sole currency of learning is prediction error. Only when a conjecture collides with reality and shatters does the brain redraw its map of the world.”',
      },
    },
    premiseCol2: {
      title: {
        ko: '기계론적 환원을 넘어: 고통과 경외의 생물학적 기저',
        en: 'Beyond Mechanical Reductionism: The Biology of Suffering and Awe',
      },
      p1: {
        ko: '도스토옙스키는 《지하생활자의 수기》에서 자연 법칙과 수학으로 인간을 완전히 계산할 수 있다면 인간은 단지 ‘피아노 건반’이나 기계 부품에 불과하지 않은가라고 절규했습니다. 우리는 이 실존적 긴장을 결코 외면하지 않습니다.',
        en: 'In Notes from Underground, Dostoevsky cried out: if man can be fully formulated by natural laws and mathematics, is he not merely an organ stop or a piano key? We do not look away from this existential tension.',
      },
      p2: {
        ko: '우리가 최첨단 4차원 인공지능과 유전체 코호트로 뇌의 생물학적 건반을 해독하는 이유는, 인간을 한낱 기계로 격하하기 위함이 아닙니다. 오히려 왜 인간은 우울과 고통에 빠지는가, 왜 불합리하게 타인의 슬픔에 공감하는가, 그리고 왜 예술과 광활한 자연 앞에서 자아를 잊고 전율(Awe)하는가라는 가장 깊은 물음에 과학의 언어로 정직하게 답하기 위함입니다.',
        en: 'Our pursuit of 4D foundation models and longitudinal cohorts is not to diminish man to a cog, but to provide an honest, scientific answer to the most enduring questions: Why do we descend into depression and anguish? Why do we empathize with another’s pain? And why do we feel transcendent awe before sublime art and the cosmos?',
      },
      p3: {
        ko: '우리는 계산신경과학의 엄밀성과 인문학적 성찰이 교차하는 지점에서, 인간 마음의 존엄을 밝히고자 합니다.',
        en: 'At the intersection of computational rigor and humanist reflection, we seek to illuminate the biological dignity of the human mind.',
      },
    },
  },

  // 1: Developmental Genomics & Longitudinal Causal Inference
  {
    id: 'genetics',
    axisIndex: 'AXIS 02',
    tabLabel: {
      ko: '02 · 발달 유전체 & 10년 코호트',
      en: '02 · Genomics & Longitudinal Cohort',
    },
    eyebrow: {
      ko: 'Laboratory Prospectus · 2026 / 발달 유전체학과 11,875명 종단 코호트 인과 추론',
      en: 'Laboratory Prospectus · 2026 / Developmental Genomics & Longitudinal Causal Inference',
    },
    headline: {
      ko: {
        lead: '유전이라는 선천적 악보와 환경의 마찰 속에서,',
        emphasis: '10년의 궤적',
        tail: '을 묻는다.',
      },
      en: {
        lead: 'Between the innate score of genetics and the friction of the world, we trace the',
        emphasis: 'ten-year trajectory',
        tail: 'inscribed upon the mind.',
      },
    },
    heroSub: {
      ko: '인간의 정신건강은 단일 유전자나 결함의 꼬리표로 단정할 수 없습니다. 우리는 NIH ABCD 연구의 청소년 11,875명을 10년간 종단 추적하며, 타고난 다유전자 점수(PRS)와 가정·학교 환경의 마찰이 대뇌피질 연결망을 거쳐 어떻게 우울과 불안, 그리고 놀라운 회복탄력성(Resilience)으로 갈라지는가를 다층적 생물학 그래프로 해독합니다.',
      en: 'Mental health cannot be defined by isolated genetic defects. Tracking 11,875 adolescents over a decade in the NIH ABCD Study, we decode through multi-scale biological graphs how innate polygenic risk scores (PRS) and environmental friction diverge across cortical networks into vulnerability or extraordinary resilience.',
    },
    premiseCol1: {
      title: {
        ko: '다층적 생물학 네트워크: 단일 유전자 환원주의의 종언',
        en: 'Multi-scale Biological Networks: Beyond Single-Gene Reductionism',
      },
      p1: {
        ko: '단일 유전자 결함이나 뇌의 한 국소 영역만으로 인간의 심리적 고통과 발달을 설명하려는 시도는 실패해 왔습니다. 유전체(PRS), 세포 유전자 발현, 대규모 신경 연결망은 고립된 원인이 아니라 서로를 제약하고 증폭하는 다층적 시스템입니다.',
        en: 'Attempts to explain psychological suffering or developmental trajectories through single genes or isolated brain regions have consistently fallen short. Polygenic risk scores, cell-type gene expression, and macroscale neural connectomes form a deeply intertwined, multi-scale system.',
      },
      p2: {
        ko: '우리는 유전체 분자 수준부터 거시적 뇌 영상까지를 하나의 수학적 그래프로 결합합니다. 환경적 스트레스가 어떻게 생물학적 다층 네트워크를 타고 흘러 신경망의 발달 궤적을 굴절시키는지를 최초로 모델링했습니다.',
        en: 'By coupling molecular genomic variation with macroscopic connectomics into a unified mathematical graph, we demonstrate for the first time how socio-environmental stress propagates across biological layers to bend neurodevelopmental trajectories.',
      },
      pullquote: {
        ko: '“생명은 고정된 단일 코드가 아니라, 유전과 환경이 10년에 걸쳐 서로를 침식하고 북돋우는 다층적 대위법(Counterpoint)이다.”',
        en: '“Life is not an unbending single code, but a multi-scale counterpoint where genetics and environment continually reshape one another across time.”',
      },
    },
    premiseCol2: {
      title: {
        ko: '청소년기 마음의 취약성과 회복의 기하학',
        en: 'Adolescent Vulnerability and the Geometry of Resilience',
      },
      p1: {
        ko: '청소년기는 뇌의 전두엽-변연계 연결망이 급격히 재배치되는 생애 최고의 변곡점입니다. 이 시기의 마찰은 깊은 상처를 남기기도 하지만, 동시에 환경적 지지를 통해 극적인 회복을 이루어내는 가소성의 황금기입니다.',
        en: 'Adolescence represents a critical developmental inflection point during which prefrontal-limbic circuits undergo massive rewiring. While vulnerable to enduring scars from environmental friction, this period also offers extraordinary plasticity for dramatic resilience and recovery.',
      },
      p2: {
        ko: '우리는 단지 질환을 예측하는 데 그치지 않고, 동일한 유전적 위험 속에서도 어떤 보호 요인과 신경망 지표가 청소년을 회복으로 이끄는가를 인과 추론합니다. 데이터의 엄밀함으로 한 인간의 고통을 미리 경감할 수 있는 과학적 개입의 근거를 마련합니다.',
        en: 'Beyond mere disease classification, we apply rigorous causal inference to uncover what protective neurobiological and environmental factors guide adolescents toward resilience under identical genetic risk, establishing empirical foundations for early preventive intervention.',
      },
      p3: {
        ko: '1만 2천 명의 삶이 증언하는 종단 데이터 속에서, 우리는 생물학적 운명론을 넘어선 회복의 가능성을 읽어냅니다.',
        en: 'Across the longitudinal trajectories of 12,000 young lives, we uncover genuine possibilities for recovery that transcend biological fatalism.',
      },
    },
  },

  // 2: Hidden Cortical Topology & Quantum Manifolds
  {
    id: 'topology',
    axisIndex: 'AXIS 03',
    tabLabel: {
      ko: '03 · 피질 위상 기하학 & 양자 ML',
      en: '03 · Cortical Topology & Quantum ML',
    },
    eyebrow: {
      ko: 'Laboratory Prospectus · 2026 / 대뇌피질 360 영역의 숨겨진 위상 기하학과 양자 매니폴드',
      en: 'Laboratory Prospectus · 2026 / Cortical Topology & Quantum State Manifolds',
    },
    headline: {
      ko: {
        lead: '100조 개 시냅스가 빚어낸 대뇌피질의 주름 속,',
        emphasis: '위상 다양체',
        tail: '를 측량한다.',
      },
      en: {
        lead: 'Within the cortical folds sculpted by 100 trillion synapses, we measure the invisible',
        emphasis: 'topological manifold',
        tail: 'of thought.',
      },
    },
    heroSub: {
      ko: '고전 통계학의 단순한 선형 상관관계로는 뇌의 복잡한 3차원 기하학적 주름을 포착할 수 없습니다. 우리는 Glasser 360 영역의 초고해상도 피질 형태측량 데이터에 위상 데이터 분석(TDA)과 양자 상태 커널(Quantum State Kernels)을 결합하여, 유클리드 공간을 뛰어넘는 고차원 뇌 구조의 숨은 대칭성과 불변량을 탐색합니다.',
      en: 'Classical linear correlations cannot capture the intricate three-dimensional curvature of the brain. Fusing Glasser 360 morphometry with topological data analysis (TDA) and quantum state kernels, we discover hidden symmetries and topological invariants that transcend Euclidean space.',
    },
    premiseCol1: {
      title: {
        ko: '형태측량과 다양체: 뇌 주름에 새겨진 수학적 불변량',
        en: 'Morphometry and Manifolds: Invariants in Cortical Folds',
      },
      p1: {
        ko: '인간 대뇌피질의 복잡한 회(Gyrus)와 구(Sulcus)는 무작위로 구겨진 종이가 아닙니다. 100조 개 축삭과 시냅스가 최적의 배선 비용과 정보 전달 속도를 달성하기 위해 물리적·위상학적으로 응축된 고차원 매니폴드입니다.',
        en: 'The intricate gyri and sulci of the human cortex are not random folds. They form a high-dimensional physical manifold condensed by 100 trillion axons and synapses to optimize computational wiring and signaling latency.',
      },
      p2: {
        ko: 'Glasser 360개 다중 양식 파셀레이션을 바탕으로 피질 두께와 표면적의 국소적 공변화 네트워크를 측정하고, 지속 호몰로지(Persistent Homology)를 통해 뇌 발달과 인지 저하의 기하학적 랜드마크를 추출합니다.',
        en: 'Leveraging the Glasser 360 multi-modal parcellation, we survey local covariance networks of cortical thickness and area, applying persistent homology to isolate geometric landmarks of neurodevelopment and cognitive shift.',
      },
      pullquote: {
        ko: '“기하학은 뇌가 세계를 지각하기 위해 발명한 형식이자, 뇌 스스로의 구조를 지탱하는 가장 깊은 물리 법칙이다.”',
        en: '“Geometry is both the form invented by the brain to perceive the world, and the deepest physical law sustaining its own architecture.”',
      },
    },
    premiseCol2: {
      title: {
        ko: '양자 기계학습과 계산신경과학의 새로운 지평',
        en: 'Quantum Machine Learning and Horizons of Neuroscience',
      },
      p1: {
        ko: '신경망의 고차원 위상 구조는 전통적인 선형 벡터 공간에서는 계산량이 지수적으로 폭발하는 복잡성을 지닙니다. 우리는 양자 상태 커널을 도입하여 뇌 연결망의 비유클리드적 유사도를 효율적으로 계산하는 이론적 프레임워크를 개척합니다.',
        en: 'The high-dimensional topological structure of brain networks exhibits exponential complexity within traditional linear vector spaces. We develop theoretical frameworks employing quantum state kernels to map non-Euclidean similarities across brain networks.',
      },
      p2: {
        ko: '이는 단순한 연산 가속에 머물지 않습니다. 뇌가 정보를 압축하고 표상하는 방식과 양자 시스템의 상태 공간 사이에 존재하는 수학적 유사성을 탐색하여, 인공지능과 뇌과학 모두에 새로운 개념적 도구를 제공합니다.',
        en: 'This goes beyond mere computational acceleration. By exploring mathematical parallels between quantum state spaces and biological neural representations, we supply new conceptual tools to both cognitive neuroscience and artificial intelligence.',
      },
      p3: {
        ko: '순수 수학의 엄밀성과 생물학적 구조의 만남을 통해, 우리는 마음의 물질적 형태를 가장 순수한 기하학의 언어로 기록합니다.',
        en: 'Through the union of pure mathematical rigor and biological architecture, we chronicle the physical form of mind in the language of geometry.',
      },
    },
  },

  // 3: Naturalistic Cognitive Neuroscience & The Neuroaesthetics of Awe
  {
    id: 'awe',
    axisIndex: 'AXIS 04',
    tabLabel: {
      ko: '04 · 경외감 & 자연주의 신경미학',
      en: '04 · Awe & Naturalistic Neuroaesthetics',
    },
    eyebrow: {
      ko: 'Laboratory Prospectus · 2026 / 자연주의 인지신경학과 경외감(Awe)의 신경미학',
      en: 'Laboratory Prospectus · 2026 / Naturalistic Cognitive Neuroscience & The Neuroaesthetics of Awe',
    },
    headline: {
      ko: {
        lead: '인간은 왜 웅장한 예술과 타인의 슬픔 앞에서',
        emphasis: '전율(Awe)',
        tail: '하며 자아를 잊는가.',
      },
      en: {
        lead: 'Why does the self dissolve in transcendent',
        emphasis: 'awe',
        tail: 'before sublime art and another’s sorrow?',
      },
    },
    heroSub: {
      ko: '인위적인 실험실 버튼 누르기 과제에서 벗어나, 인간이 영화와 문학, 장엄한 음악에 깊이 몰입할 때 일어나는 뇌의 생생한 반응을 추적합니다. 자아의 경계를 표상하는 기본모드신경망(DMN)이 순간적으로 해체되고 세계와 연결되는 ‘경외(Awe)’의 신경 메커니즘을 밝혀, 예술적 경험이 어떻게 상처 입은 영혼을 치유하는지를 탐구합니다.',
      en: 'Moving beyond artificial laboratory button-pressing tasks to investigate brain dynamics during profound immersion in cinema, literature, and music. We explore how the Default Mode Network (DMN) temporarily deconstructs during aesthetic awe, discovering how art and transcendent connection heal wounded minds.',
    },
    premiseCol1: {
      title: {
        ko: '자아의 해체와 경외: 기본모드신경망(DMN)의 동역학',
        en: 'Deconstruction of Self: The Dynamics of the Default Mode Network',
      },
      p1: {
        ko: '인간의 자아의식과 반추(Rumination)는 대뇌피질의 기본모드신경망(DMN)에 깊이 정박되어 있습니다. 우울증과 불안 장애 환자들은 이 자아 중심의 신경망 회로에 갇혀 끝없는 고통의 되새김질에 시달립니다.',
        en: 'Human self-consciousness and depressive rumination are deeply anchored in the Default Mode Network (DMN). In clinical depression and anxiety, individuals frequently become trapped within hyperactive egoic loops of perpetual cognitive rumination.',
      },
      p2: {
        ko: '그러나 인간이 압도적인 자연, 숭고한 건축, 심금을 울리는 음악과 마주할 때, DMN의 견고한 연결성은 일시적으로 붕괴합니다. 자아의 경계가 희미해지고 관찰자와 세계가 하나로 이어지는 신경미학적 전율(Awe)이 일어납니다.',
        en: 'Yet when confronted with sublime nature, monumental architecture, or transcendent music, this rigid connectivity temporarily yields. The boundaries of the ego dissolve, sparking a neuroaesthetic state of awe that unites the observer with the world.',
      },
      pullquote: {
        ko: '“경외(Awe)란 자아의 작은 성벽이 무너지고, 세계라는 광활한 전체와 다시 연결되는 신경생물학적 치유의 사건이다.”',
        en: '“Awe is a neurobiological event wherein the fragile fortress of the ego dissolves, reconnecting the individual to the vast continuum of reality.”',
      },
    },
    premiseCol2: {
      title: {
        ko: '도스토옙스키의 질문: 왜 인간은 불합리하게 예술과 타인을 갈망하는가',
        en: 'Dostoevsky’s Question: Why We Yearn for the Sublime',
      },
      p1: {
        ko: '도스토옙스키는 《지하생활자의 수기》에서 인간을 단지 이익과 효용만 계산하는 존재로 규정하는 당대의 합리주의를 통렬히 비판했습니다. 인간은 때로 손해를 감수하면서도 고결한 예술에 눈물 흘리고, 전혀 상관없는 타인의 슬픔에 가슴 아파합니다.',
        en: 'In Notes from Underground, Dostoevsky delivered a scathing critique of rational utilitarianism that sought to define man merely through self-interest and calculated advantage. Human beings will suffer great costs to weep before great art, and ache in empathy for a stranger’s sorrow.',
      },
      p2: {
        ko: '우리는 자연주의적 fMRI와 뇌파(EEG)를 통해, 인간이 예술적 내러티브에 몰입할 때 일어나는 동역학적 뇌 상태 전이를 추적합니다. 이 비합리적 공감과 숭고미의 경험이야말로 인간을 기계와 구별 짓는 본질임을 과학적으로 증명하고자 합니다.',
        en: 'Utilizing naturalistic fMRI and high-density EEG, we trace dynamical brain state transitions as individuals immerse themselves in aesthetic narratives. We aim to scientifically demonstrate that this non-utilitarian empathy and capacity for awe define the essence of human dignity.',
      },
      p3: {
        ko: '계산신경과학의 기술적 칼끝을 인간에 대한 깊은 경외와 연민으로 벼릴 때, 비로소 마음의 과학은 진정한 치유가 됩니다.',
        en: 'When computational rigor is sharpened with profound awe and compassion for human existence, the science of mind becomes a pathway to healing.',
      },
    },
  },
];

export function getTodayThemeIndex(): number {
  // Epoch day in KST (UTC + 9 hours)
  const now = new Date();
  const kstOffsetMs = 9 * 60 * 60 * 1000;
  const kstTime = new Date(now.getTime() + kstOffsetMs);
  const epochDays = Math.floor(kstTime.getTime() / (1000 * 60 * 60 * 24));
  return Math.abs(epochDays) % dailyThemes.length;
}
