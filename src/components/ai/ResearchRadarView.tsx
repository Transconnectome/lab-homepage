import React, { useState, useMemo } from 'react';
import { useTranslations } from '../../i18n/ui';

interface TrendItem {
  title: string;
  authors: string[];
  publishedDate: string;
  source: string;
  topic: string;
  url: string;
  summaryPoints: string[];
  significance: string;
  labRelevance: string;
  modality: string[];
  badge?: string | null;
  generatedBy?: string | null;
}

interface Props {
  trends: TrendItem[];
  lang?: 'en' | 'ko';
}

const TOPICS = [
  'All',
  'Brain Foundation Models (fMRI)',
  'Brain Foundation Models (EEG)',
  'Gene & Brain',
  'Affective & Developmental',
  'Agentic AI',
  'Quantum ML',
  'Brain-LLM Alignment',
];

const TOPIC_LABELS: Record<'en' | 'ko', Record<string, string>> = {
  en: {
    All: 'All',
    'Brain Foundation Models (fMRI)': 'fMRI Foundation Models',
    'Brain Foundation Models (EEG)': 'EEG Foundation Models',
    'Gene & Brain': 'Gene & Brain',
    'Affective & Developmental': 'Affective & Developmental',
    'Agentic AI': 'Agentic AI',
    'Quantum ML': 'Quantum ML',
    'Brain-LLM Alignment': 'Brain-LLM Alignment',
  },
  ko: {
    All: '전체',
    'Brain Foundation Models (fMRI)': 'fMRI 파운데이션 모델',
    'Brain Foundation Models (EEG)': 'EEG 파운데이션 모델',
    'Gene & Brain': '유전자와 뇌',
    'Affective & Developmental': '정서·발달 신경과학',
    'Agentic AI': '에이전틱 AI',
    'Quantum ML': '양자 머신러닝',
    'Brain-LLM Alignment': '뇌-언어모델 정렬',
  },
};

const HANGUL = /[\uac00-\ud7a3]/;
const itemLang = (text: string) => (HANGUL.test(text) ? 'ko' : 'en');

export default function ResearchRadarView({ trends, lang = 'en' }: Props) {
  const t = useTranslations(lang);
  const [selectedTopic, setSelectedTopic] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const filteredTrends = useMemo(() => trends.filter((item) => {
    const matchTopic = selectedTopic === 'All' || item.topic === selectedTopic;
    const query = searchQuery.trim().toLowerCase();
    const matchSearch = [item.title, item.significance, item.labRelevance, item.topic,
      TOPIC_LABELS[lang][item.topic] ?? '', ...item.modality, ...item.authors]
      .some((value) => value.toLowerCase().includes(query));
    return matchTopic && matchSearch;
  }), [trends, selectedTopic, searchQuery, lang]);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-[minmax(0,1.4fr)_minmax(0,1fr)] gap-5">
        <div className="space-y-2">
          <label htmlFor="radar-search" className="block text-sm font-semibold text-ink">{t('radar.searchLabel')}</label>
          <input id="radar-search" type="search" className="form-field" value={searchQuery} onChange={(event) => setSearchQuery(event.target.value)} placeholder={t('radar.searchPlaceholder')} />
        </div>
        <div className="space-y-2">
          <label htmlFor="radar-topic" className="block text-sm font-semibold text-ink">{t('filters.topic')}</label>
          <select id="radar-topic" className="form-field" value={selectedTopic} onChange={(event) => setSelectedTopic(event.target.value)}>
            {TOPICS.map((topic) => <option key={topic} value={topic}>{topic === 'All' ? t('filters.allTopics') : TOPIC_LABELS[lang][topic] ?? topic}</option>)}
          </select>
        </div>
      </div>
      <div className="flex flex-wrap items-center justify-between gap-3 text-sm">
        <p role="status" aria-live="polite" className="text-ink-soft">{t('filters.results')}: {filteredTrends.length}</p>
        {searchQuery && <button type="button" className="text-link" onClick={() => setSearchQuery('')}>{t('radar.clearSearch')}</button>}
      </div>

      <div>
        {filteredTrends.map((trend) => (
          <article key={trend.url} className="border-t border-line py-7 sm:py-8 space-y-4">
            <header className="space-y-3">
              <div className="flex flex-wrap items-baseline gap-x-4 gap-y-1 text-xs text-ink-faint">
                <time dateTime={trend.publishedDate} className="font-mono" lang="en">{trend.publishedDate}</time>
                <span>{TOPIC_LABELS[lang][trend.topic] ?? trend.topic}</span>
                {trend.badge && <span lang={itemLang(trend.badge)}>{trend.badge}</span>}
              </div>
              <h2 className="font-display text-xl sm:text-2xl font-semibold text-ink leading-snug">
                <a href={trend.url} target="_blank" rel="noreferrer" className="hover:underline underline-offset-4 hover:text-lab-800" lang={itemLang(trend.title)}>{trend.title}</a>
              </h2>
              <p className="text-sm text-ink-soft leading-relaxed" lang={itemLang(trend.authors.join(', '))}>{trend.source} · {trend.authors.join(', ')}</p>
            </header>

            <details className="group">
              <summary className="cursor-pointer py-3 text-sm font-semibold text-lab-800">
                <span className="group-open:hidden">{t('radar.showDetails')}</span>
                <span className="hidden group-open:inline">{t('radar.hideDetails')}</span>
              </summary>
              <div className="space-y-5 pt-2 pb-4 max-w-3xl">
                <section className="space-y-2">
                  <h3 className="text-sm font-semibold text-ink">
                    {trend.generatedBy?.startsWith('llm') ? t('radar.llmSummary') : trend.generatedBy === 'extractive-fallback' ? t('radar.excerpt') : t('radar.summary')}
                  </h3>
                  <ul className="list-disc pl-5 space-y-2 text-sm text-ink-soft leading-relaxed">
                    {trend.summaryPoints.map((point, index) => <li key={index} lang={itemLang(point)}>{point}</li>)}
                  </ul>
                </section>
                <section className="space-y-2">
                  <h3 className="text-sm font-semibold text-ink">{t('radar.significance')}</h3>
                  <p className="text-sm text-ink-soft leading-relaxed" lang={itemLang(trend.significance)}>{trend.significance}</p>
                </section>
                <section className="space-y-2">
                  <h3 className="text-sm font-semibold text-ink">{t('radar.labRelevance')}</h3>
                  <p className="text-sm text-ink-soft leading-relaxed" lang={itemLang(trend.labRelevance)}>{trend.labRelevance}</p>
                </section>
              </div>
            </details>
            <footer className="space-y-2 text-xs text-ink-faint">
              <p lang="en">{trend.modality.join(' · ')}</p>
              <p className="break-words">{t('radar.provenance')}: <span lang={trend.generatedBy ? 'en' : lang}>{trend.generatedBy || t('radar.unknownSource')}</span></p>
            </footer>
          </article>
        ))}
      </div>
      {filteredTrends.length === 0 && (
        <div className="border-t border-line py-10 space-y-2">
          <h2 className="text-lg font-semibold text-ink">{t('radar.noMatch')}</h2>
          <p className="text-sm text-ink-soft">{t('radar.noMatchDesc')}</p>
        </div>
      )}
    </div>
  );
}
