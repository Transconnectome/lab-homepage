import React, { useState, useMemo } from 'react';
import { Search, Sparkles, ExternalLink, Brain } from 'lucide-react';

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

const LABELS: Record<'en' | 'ko', Record<string, string>> = {
  en: {
    search: 'Search papers, modalities, topics...',
    entries: 'entries · updated weekly from arXiv',
    llmSummary: 'LLM summary',
    excerpt: 'Abstract excerpt',
    summary: 'Summary',
    significance: 'Significance: ',
    whyUs: 'Why it matters to us: ',
    noMatch: 'No matching radar entries',
    noMatchDesc: 'Try a different keyword or topic filter.',
  },
  ko: {
    search: '논문·모달리티·주제 검색...',
    entries: '건 · arXiv에서 매주 갱신',
    llmSummary: 'LLM 요약',
    excerpt: '초록 발췌',
    summary: '요약',
    significance: '의의: ',
    whyUs: '우리 연구실과의 연결: ',
    noMatch: '조건에 맞는 항목이 없습니다',
    noMatchDesc: '다른 검색어나 주제 필터를 시도해 보세요.',
  },
};

const TOPICS = [
  'All',
  'Brain Foundation Models',
  'fMRI/EEG Dynamics',
  'Genomics & Connectomics',
  'Quantum ML',
  'Brain-LLM Alignment',
];

export default function ResearchRadarView({ trends, lang = 'en' }: Props) {
  const L = LABELS[lang];
  const [selectedTopic, setSelectedTopic] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const filteredTrends = useMemo(() => {
    return trends.filter((item) => {
      const matchTopic = selectedTopic === 'All' || item.topic === selectedTopic;
      const query = searchQuery.toLowerCase();
      const matchSearch =
        item.title.toLowerCase().includes(query) ||
        item.significance.toLowerCase().includes(query) ||
        item.labRelevance.toLowerCase().includes(query) ||
        item.modality.some((m) => m.toLowerCase().includes(query)) ||
        item.authors.some((a) => a.toLowerCase().includes(query));
      return matchTopic && matchSearch;
    });
  }, [trends, selectedTopic, searchQuery]);

  return (
    <div className="space-y-8">
      {/* Controls */}
      <div className="card p-5 sm:p-6 space-y-4">
        <div className="flex flex-col md:flex-row gap-4 justify-between md:items-center">
          <div className="relative w-full md:w-96">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-faint" aria-hidden="true" />
            <label htmlFor="radar-search" className="sr-only">Search radar entries</label>
            <input
              id="radar-search"
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder={L.search}
              className="w-full bg-paper border border-line rounded-lg pl-10 pr-9 py-2.5 text-sm text-ink placeholder-ink-faint focus:border-lab-600 transition-colors"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-xs text-ink-faint hover:text-ink px-1.5 py-0.5 rounded bg-white border border-line"
                aria-label="Clear search"
              >
                ✕
              </button>
            )}
          </div>
          <span className="font-mono text-xs text-ink-faint shrink-0">
            {filteredTrends.length}{lang === 'ko' ? '' : ' '}{L.entries}
          </span>
        </div>

        <div className="flex flex-wrap gap-2 pt-3 border-t border-line">
          {TOPICS.map((topic) => (
            <button
              key={topic}
              onClick={() => setSelectedTopic(topic)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                selectedTopic === topic
                  ? 'bg-lab-700 text-white'
                  : 'bg-paper text-ink-soft hover:text-ink border border-line'
              }`}
            >
              {topic}
            </button>
          ))}
        </div>
      </div>

      {/* Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {filteredTrends.map((trend, idx) => (
          <article key={idx} className="card card-hover p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between gap-2 mb-3">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="chip-accent">{trend.topic}</span>
                  {trend.badge && (
                    <span className="chip">
                      <Sparkles className="w-3 h-3 mr-1 text-lab-700" aria-hidden="true" />
                      {trend.badge}
                    </span>
                  )}
                </div>
                <span className="font-mono text-xs text-ink-faint shrink-0">{trend.publishedDate}</span>
              </div>

              <h3 className="text-base sm:text-lg font-semibold text-ink leading-snug mb-2">
                <a
                  href={trend.url}
                  target="_blank"
                  rel="noreferrer"
                  className="hover:text-lab-700 transition-colors inline-flex items-start gap-1.5"
                >
                  <span>{trend.title}</span>
                  <ExternalLink className="w-4 h-4 text-ink-faint shrink-0 mt-1" aria-hidden="true" />
                </a>
              </h3>

              <p className="font-mono text-xs text-ink-faint mb-4">
                {trend.source} · {trend.authors.join(', ')}
              </p>

              {/* Summary — honestly labeled by how it was produced */}
              <div className="mb-4 p-3.5 rounded-xl bg-paper border border-line">
                <div className="text-xs font-semibold uppercase tracking-wider text-lab-700 mb-2 flex items-center gap-1.5">
                  <Brain className="w-3.5 h-3.5" aria-hidden="true" />
                  <span>
                    {trend.generatedBy && trend.generatedBy.startsWith('llm')
                      ? L.llmSummary
                      : trend.generatedBy === 'extractive-fallback'
                        ? L.excerpt
                        : L.summary}
                  </span>
                </div>
                <ul className="space-y-1.5">
                  {trend.summaryPoints.map((point, pIdx) => (
                    <li key={pIdx} className="text-sm text-ink-soft flex items-start gap-2 leading-relaxed">
                      <span className="text-lab-700 font-bold mt-0.5">•</span>
                      <span>{point}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <p className="text-sm text-ink-soft mb-3 leading-relaxed">
                <strong className="text-ink">{L.significance}</strong>
                {trend.significance}
              </p>

              <div className="p-3 rounded-xl bg-lab-50 border border-lab-600/20 text-sm text-lab-900 leading-relaxed mb-4">
                <strong>{L.whyUs}</strong>
                {trend.labRelevance}
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-1.5 pt-3 border-t border-line">
              {trend.modality.map((m, mIdx) => (
                <span key={mIdx} className="chip">#{m}</span>
              ))}
            </div>
          </article>
        ))}
      </div>

      {filteredTrends.length === 0 && (
        <div className="text-center py-16 card">
          <Brain className="w-10 h-10 text-ink-faint mx-auto mb-3" aria-hidden="true" />
          <h3 className="text-lg font-semibold text-ink mb-1">{L.noMatch}</h3>
          <p className="text-sm text-ink-soft">{L.noMatchDesc}</p>
        </div>
      )}
    </div>
  );
}
