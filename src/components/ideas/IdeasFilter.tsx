import React, { useState, useMemo } from 'react';

export interface IdeaItem {
  slug: string;
  title: string;
  titleKo?: string | null;
  date: string;
  category: 'foundation-models' | 'connectomics' | 'genetics' | 'qml' | 'art-science'
    | 'agentic-ai' | 'affective-development';
  hypothesis: string;
  hypothesisKo?: string | null;
  rationale: string;
  rationaleKo?: string | null;
  labThreads: string[];
  externalInspiration: string[];
  firstExperiment: string;
  firstExperimentKo?: string | null;
  risks: string;
  risksKo?: string | null;
  generatedBy: string;
  image?: string | null;
  imageGeneratedBy?: string | null;
}

interface Props {
  ideas: IdeaItem[];
  lang?: 'en' | 'ko';
}

const CATEGORY_ORDER: IdeaItem['category'][] = [
  'foundation-models', 'connectomics', 'genetics', 'affective-development',
  'agentic-ai', 'qml', 'art-science',
];

const CATEGORY_LABELS: Record<'en' | 'ko', Record<IdeaItem['category'], string>> = {
  en: {
    'foundation-models': 'Foundation Models',
    connectomics: 'Connectomics',
    genetics: 'Genetics & Psychiatry',
    qml: 'Quantum ML',
    'art-science': 'Art & Neuroscience',
    'agentic-ai': 'Agentic AI',
    'affective-development': 'Affective & Developmental',
  },
  ko: {
    'foundation-models': '파운데이션 모델',
    connectomics: '커넥토믹스',
    genetics: '유전체·정신의학',
    qml: '양자 머신러닝',
    'art-science': '예술과 신경과학',
    'agentic-ai': '에이전틱 AI',
    'affective-development': '정서·발달 신경과학',
  },
};

const LABELS = {
  en: {
    allCategories: 'All topics',
    archiveNote: 'Every idea generated stays archived here — nothing is ever removed, only added to.',
    hypothesis: 'Hypothesis',
    whyNow: 'Why now',
    buildsOn: 'Builds on',
    inspiration: 'Inspired by',
    firstExperiment: 'First experiment',
    howFails: 'How it could fail',
    noMatch: 'No ideas in this topic yet',
    noMatchDesc: 'Try a different topic — new ideas are added weekly.',
  },
  ko: {
    allCategories: '전체 주제',
    archiveNote: '생성된 아이디어는 모두 이곳에 그대로 보관됩니다 — 지워지지 않고 매주 쌓입니다.',
    hypothesis: '가설',
    whyNow: '왜 지금인가',
    buildsOn: '연구실 기반',
    inspiration: '외부 영감',
    firstExperiment: '첫 실험',
    howFails: '실패 가능성',
    noMatch: '이 주제의 아이디어는 아직 없습니다',
    noMatchDesc: '다른 주제를 선택해 보세요 — 매주 새 아이디어가 추가됩니다.',
  },
};

export default function IdeasFilter({ ideas, lang = 'en' }: Props) {
  const L = LABELS[lang];
  const CL = CATEGORY_LABELS[lang];
  const [selectedCategory, setSelectedCategory] = useState<string>('All');

  const pick = (en: string, ko?: string | null) => (lang === 'ko' && ko ? ko : en);

  const presentCategories = useMemo(
    () => CATEGORY_ORDER.filter((c) => ideas.some((i) => i.category === c)),
    [ideas]
  );

  const counts = useMemo(() => {
    const m = new Map<string, number>();
    ideas.forEach((i) => m.set(i.category, (m.get(i.category) ?? 0) + 1));
    return m;
  }, [ideas]);

  const filtered = useMemo(
    () => (selectedCategory === 'All' ? ideas : ideas.filter((i) => i.category === selectedCategory)),
    [ideas, selectedCategory]
  );

  return (
    <div className="space-y-8">
      <div className="space-y-3">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedCategory('All')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              selectedCategory === 'All'
                ? 'bg-lab-700 text-white'
                : 'bg-paper text-ink-soft hover:text-ink border border-line'
            }`}
          >
            {L.allCategories} <span className="opacity-70">({ideas.length})</span>
          </button>
          {presentCategories.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                selectedCategory === cat
                  ? 'bg-lab-700 text-white'
                  : 'bg-paper text-ink-soft hover:text-ink border border-line'
              }`}
            >
              {CL[cat]} <span className="opacity-70">({counts.get(cat)})</span>
            </button>
          ))}
        </div>
        <p className="font-mono text-xs text-ink-faint">{L.archiveNote}</p>
      </div>

      <div className="space-y-6">
        {filtered.map((idea) => (
          <article key={idea.slug} className="card p-7 sm:p-9 space-y-5">
            <header className="space-y-2">
              <div className="flex flex-wrap items-center gap-2">
                <span className="chip-accent">{idea.date}</span>
                <span className="chip">{CL[idea.category]}</span>
                <span className="chip">🤖 {idea.generatedBy.replace('llm:', '')}</span>
              </div>
              <h2 className="font-display text-xl sm:text-2xl font-semibold text-ink leading-snug">
                {lang === 'ko' && idea.titleKo ? idea.titleKo : idea.title}
              </h2>
              {lang === 'ko'
                ? <p className="text-sm text-ink-faint">{idea.title}</p>
                : idea.titleKo && <p className="text-sm text-ink-faint">{idea.titleKo}</p>}
            </header>

            {idea.image && (
              <figure className="space-y-1.5">
                <img
                  src={idea.image}
                  alt={idea.titleKo ?? idea.title}
                  className="rounded-xl border border-line w-full"
                  loading="lazy"
                />
                {idea.imageGeneratedBy && (
                  <figcaption className="font-mono text-xs text-ink-faint">
                    🤖 {idea.imageGeneratedBy}
                  </figcaption>
                )}
              </figure>
            )}

            <div className="p-4 rounded-xl bg-paper border border-line">
              <div className="eyebrow mb-1.5">{L.hypothesis}</div>
              <p className="text-base text-ink leading-relaxed measure">{pick(idea.hypothesis, idea.hypothesisKo)}</p>
            </div>

            <div className="space-y-1.5">
              <div className="eyebrow">{L.whyNow}</div>
              <p className="text-base text-ink-soft leading-relaxed measure">{pick(idea.rationale, idea.rationaleKo)}</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div className="space-y-1.5">
                <div className="eyebrow">{L.buildsOn}</div>
                <ul className="space-y-1">
                  {idea.labThreads.map((th) => (
                    <li key={th} className="text-sm text-ink-soft flex items-start gap-2">
                      <span className="text-lab-700 mt-0.5">·</span>
                      <span>{th}</span>
                    </li>
                  ))}
                </ul>
              </div>
              <div className="space-y-1.5">
                <div className="eyebrow">{L.inspiration}</div>
                <ul className="space-y-1">
                  {idea.externalInspiration.map((th) => (
                    <li key={th} className="text-sm text-ink-soft flex items-start gap-2">
                      <span className="text-lab-700 mt-0.5">·</span>
                      <span>{th}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="space-y-1.5">
              <div className="eyebrow">{L.firstExperiment}</div>
              <p className="text-base text-ink-soft leading-relaxed measure">
                {pick(idea.firstExperiment, idea.firstExperimentKo)}
              </p>
            </div>

            <div className="pt-4 border-t border-line space-y-1.5">
              <div className="eyebrow">{L.howFails}</div>
              <p className="text-sm text-ink-faint leading-relaxed measure">{pick(idea.risks, idea.risksKo)}</p>
            </div>
          </article>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-16 card">
          <h3 className="text-lg font-semibold text-ink mb-1">{L.noMatch}</h3>
          <p className="text-sm text-ink-soft">{L.noMatchDesc}</p>
        </div>
      )}
    </div>
  );
}
