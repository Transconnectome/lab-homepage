import React, { useState, useMemo } from 'react';
import { useTranslations } from '../../i18n/ui';
import EditorialNote, { type EditorialCorrection } from '../common/EditorialNote';

export interface IdeaItem {
  slug: string;
  title: string;
  titleKo?: string | null;
  date: string;
  category: 'foundation-models' | 'connectomics' | 'genetics' | 'qml' | 'affective-neuro'
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
  editorialNote?: EditorialCorrection;
  image?: string | null;
  imageGeneratedBy?: string | null;
  imageHidden?: boolean;
}

interface Props {
  ideas: IdeaItem[];
  lang?: 'en' | 'ko';
}

const CATEGORY_ORDER: IdeaItem['category'][] = [
  'foundation-models', 'connectomics', 'genetics', 'affective-development',
  'agentic-ai', 'qml', 'affective-neuro',
];

const CATEGORY_LABELS: Record<'en' | 'ko', Record<IdeaItem['category'], string>> = {
  en: {
    'foundation-models': 'Foundation Models',
    connectomics: 'Connectomics',
    genetics: 'Genetics & Psychiatry',
    qml: 'Quantum ML',
    'affective-neuro': 'Affective Neuroscience',
    'agentic-ai': 'Agentic AI',
    'affective-development': 'Affective & Developmental',
  },
  ko: {
    'foundation-models': '파운데이션 모델',
    connectomics: '커넥토믹스',
    genetics: '유전체·정신의학',
    qml: '양자 머신러닝',
    'affective-neuro': '정서 신경과학',
    'agentic-ai': '에이전틱 AI',
    'affective-development': '정서·발달 신경과학',
  },
};

// Generated free text can use either language on either page.
const HANGUL = /[\uac00-\ud7a3]/;
const itemLang = (text: string) => (HANGUL.test(text) ? 'ko' : 'en');

export default function IdeasFilter({ ideas, lang = 'en' }: Props) {
  const t = useTranslations(lang);
  const CL = CATEGORY_LABELS[lang];
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const pick = (en: string, ko?: string | null) => (lang === 'ko' && ko ? ko : en);

  const presentCategories = useMemo(
    () => CATEGORY_ORDER.filter((category) => ideas.some((idea) => idea.category === category)),
    [ideas]
  );
  const counts = useMemo(() => {
    const result = new Map<string, number>();
    ideas.forEach((idea) => result.set(idea.category, (result.get(idea.category) ?? 0) + 1));
    return result;
  }, [ideas]);
  const filtered = useMemo(
    () => selectedCategory === 'All' ? ideas : ideas.filter((idea) => idea.category === selectedCategory),
    [ideas, selectedCategory]
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-end gap-4 sm:gap-8">
        <div className="w-full sm:max-w-sm space-y-2">
          <label htmlFor="ideas-topic" className="block text-sm font-semibold text-ink">{t('filters.topic')}</label>
          <select id="ideas-topic" className="form-field" value={selectedCategory} onChange={(event) => setSelectedCategory(event.target.value)}>
            <option value="All">{t('filters.allTopics')} ({ideas.length})</option>
            {presentCategories.map((category) => (
              <option key={category} value={category}>{CL[category]} ({counts.get(category)})</option>
            ))}
          </select>
        </div>
        <p role="status" aria-live="polite" className="text-sm text-ink-soft sm:pb-2">
          {t('filters.results')}: {filtered.length}
        </p>
      </div>

      <div>
        {filtered.map((idea) => (
          <article id={`idea-${idea.slug}`} key={idea.slug} className="border-t border-line py-8 sm:py-10 space-y-6">
            <header className="space-y-3">
              <div className="flex flex-wrap items-baseline gap-x-4 gap-y-1 text-xs text-ink-faint">
                <time dateTime={idea.date} className="font-mono" lang="en">{idea.date}</time>
                <span>{CL[idea.category]}</span>
              </div>
              <h2 className="font-display text-xl sm:text-2xl font-semibold text-ink leading-snug" lang={itemLang(pick(idea.title, idea.titleKo))}>
                {pick(idea.title, idea.titleKo)}
              </h2>
              {lang === 'ko'
                ? idea.titleKo && <p className="text-sm text-ink-faint" lang="en">{idea.title}</p>
                : idea.titleKo && <p className="text-sm text-ink-faint" lang="ko">{idea.titleKo}</p>}
            </header>

            {idea.image && !idea.imageHidden && (
              <figure className="space-y-2">
                <img src={idea.image} alt={pick(idea.title, idea.titleKo)} className="w-full" loading="lazy" />
                {idea.imageGeneratedBy && (
                  <figcaption className="text-xs text-ink-faint">
                    {t('ideas.generatedImage')}: <span lang="en">{idea.imageGeneratedBy}</span>
                  </figcaption>
                )}
              </figure>
            )}

            <section className="space-y-2">
              <h3 className="text-sm font-semibold text-ink">{t('ideas.hypothesis')}</h3>
              <p className="text-base text-ink leading-relaxed measure" lang={itemLang(pick(idea.hypothesis, idea.hypothesisKo))}>{pick(idea.hypothesis, idea.hypothesisKo)}</p>
            </section>
            <section className="space-y-2">
              <h3 className="text-sm font-semibold text-ink">{t('ideas.whyNow')}</h3>
              <p className="text-base text-ink-soft leading-relaxed measure" lang={itemLang(pick(idea.rationale, idea.rationaleKo))}>{pick(idea.rationale, idea.rationaleKo)}</p>
            </section>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <section className="space-y-2">
                <h3 className="text-sm font-semibold text-ink">{t('ideas.buildsOn')}</h3>
                <ul className="list-disc pl-5 space-y-2 text-sm text-ink-soft leading-relaxed">
                  {idea.labThreads.map((thread, index) => <li key={index} lang={itemLang(thread)}>{thread}</li>)}
                </ul>
              </section>
              <section className="space-y-2">
                <h3 className="text-sm font-semibold text-ink">{t('ideas.inspiration')}</h3>
                <ul className="list-disc pl-5 space-y-2 text-sm text-ink-soft leading-relaxed">
                  {idea.externalInspiration.map((thread, index) => <li key={index} lang={itemLang(thread)}>{thread}</li>)}
                </ul>
              </section>
            </div>
            <section className="space-y-2">
              <h3 className="text-sm font-semibold text-ink">{t('ideas.firstExperiment')}</h3>
              <p className="text-base text-ink-soft leading-relaxed measure" lang={itemLang(pick(idea.firstExperiment, idea.firstExperimentKo))}>{pick(idea.firstExperiment, idea.firstExperimentKo)}</p>
            </section>
            <section className="space-y-2">
              <h3 className="text-sm font-semibold text-ink">{t('ideas.howFails')}</h3>
              <p className="text-sm text-ink-soft leading-relaxed measure" lang={itemLang(pick(idea.risks, idea.risksKo))}>{pick(idea.risks, idea.risksKo)}</p>
            </section>
            <footer className="space-y-2 text-xs text-ink-faint break-words">
              <p>{t('ideas.generatedSummary')}: <span lang="en">{idea.generatedBy.replace('llm:', '')}</span></p>
              <EditorialNote correction={idea.editorialNote} lang={lang} />
            </footer>
          </article>
        ))}
      </div>
      {filtered.length === 0 && (
        <div className="border-t border-line py-10 space-y-2">
          <h2 className="text-lg font-semibold text-ink">{t('ideas.noMatch')}</h2>
          <p className="text-sm text-ink-soft">{t('ideas.noMatchDesc')}</p>
        </div>
      )}
    </div>
  );
}
