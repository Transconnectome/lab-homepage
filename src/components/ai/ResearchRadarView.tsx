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
  badge?: string;
}

interface Props {
  trends: TrendItem[];
}

export default function ResearchRadarView({ trends }: Props) {
  const [selectedTopic, setSelectedTopic] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const topics = ['All', 'Brain Foundation Models', 'fMRI/EEG Dynamics', 'Genomics & Connectomics', 'Quantum ML', 'Brain-LLM Alignment'];

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
      {/* Search & Topic Selector Bar */}
      <div className="p-6 rounded-3xl glass-panel border border-slate-700/60 shadow-xl space-y-5">
        <div className="flex flex-col md:flex-row gap-4 justify-between items-center">
          {/* Search Input */}
          <div className="relative w-full md:w-96">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search SOTA papers, modalities, topics..."
              className="w-full bg-slate-900/80 border border-slate-700 rounded-2xl pl-11 pr-4 py-2.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-400 transition"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400 hover:text-white px-1.5 py-0.5 rounded bg-slate-800"
              >
                ✕
              </button>
            )}
          </div>

          {/* Sync status indicator */}
          <div className="flex items-center gap-2 text-xs text-slate-400 font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span>LLM Research Radar Active</span>
          </div>
        </div>

        {/* Topic Pills */}
        <div className="flex flex-wrap gap-2 pt-2 border-t border-slate-800">
          {topics.map((topic) => (
            <button
              key={topic}
              onClick={() => setSelectedTopic(topic)}
              className={`px-4 py-2 rounded-xl text-xs font-medium transition-all duration-200 ${
                selectedTopic === topic
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-lg shadow-cyan-500/25 scale-105'
                  : 'bg-slate-900/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-800'
              }`}
            >
              {topic}
            </button>
          ))}
        </div>
      </div>

      {/* SOTA Radar Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {filteredTrends.map((trend, idx) => (
          <div
            key={idx}
            className="rounded-3xl glass-panel glass-panel-hover p-6 border border-slate-800 flex flex-col justify-between group"
          >
            <div>
              {/* Header tags */}
              <div className="flex items-center justify-between gap-2 mb-3">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-[11px] font-semibold px-2.5 py-1 rounded-full bg-cyan-950/80 text-cyan-300 border border-cyan-800/60">
                    {trend.topic}
                  </span>
                  {trend.badge && (
                    <span className="text-[11px] font-semibold px-2.5 py-1 rounded-full bg-indigo-950/80 text-indigo-300 border border-indigo-700/60 flex items-center gap-1">
                      <Sparkles className="w-3 h-3 text-indigo-400" />
                      {trend.badge}
                    </span>
                  )}
                </div>
                <span className="text-xs font-mono text-slate-500">{trend.publishedDate}</span>
              </div>

              {/* Title */}
              <h3 className="text-lg font-bold text-white group-hover:text-cyan-300 transition duration-200 leading-snug mb-2">
                <a href={trend.url} target="_blank" rel="noreferrer" className="hover:underline flex items-start gap-1.5">
                  <span>{trend.title}</span>
                  <ExternalLink className="w-4 h-4 text-slate-500 group-hover:text-cyan-400 shrink-0 mt-1" />
                </a>
              </h3>

              {/* Source & Authors */}
              <div className="text-xs text-slate-400 mb-4 font-mono">
                <span>{trend.source}</span> • <span className="text-slate-300">{trend.authors.join(', ')}</span>
              </div>

              {/* AI 3-Bullet Summary Points */}
              <div className="mb-4 p-3.5 rounded-2xl bg-slate-950/60 border border-slate-800/80">
                <div className="text-[11px] font-semibold uppercase tracking-wider text-cyan-400 mb-2 flex items-center gap-1.5">
                  <Brain className="w-3.5 h-3.5" />
                  <span>AI Executive Summary</span>
                </div>
                <ul className="space-y-1.5">
                  {trend.summaryPoints.map((point, pIdx) => (
                    <li key={pIdx} className="text-xs text-slate-300 flex items-start gap-2 leading-relaxed">
                      <span className="text-cyan-400 font-bold mt-0.5">•</span>
                      <span>{point}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Significance Box */}
              <div className="text-xs text-slate-300 mb-3 leading-relaxed">
                <strong className="text-slate-200">Significance: </strong>
                {trend.significance}
              </div>

              {/* Lab Relevance Box */}
              <div className="p-3 rounded-xl bg-blue-950/30 border border-blue-900/40 text-xs text-blue-200 leading-relaxed mb-4">
                <strong className="text-cyan-300">Connectome Lab Context: </strong>
                {trend.labRelevance}
              </div>
            </div>

            {/* Footer Modality Badges */}
            <div className="flex flex-wrap items-center gap-1.5 pt-3 border-t border-slate-800/80">
              {trend.modality.map((m, mIdx) => (
                <span
                  key={mIdx}
                  className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-slate-800/90 text-slate-300 border border-slate-700"
                >
                  #{m}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>

      {filteredTrends.length === 0 && (
        <div className="text-center py-16 rounded-3xl glass-panel border border-slate-800">
          <Brain className="w-12 h-12 text-slate-600 mx-auto mb-3 animate-pulse" />
          <h3 className="text-lg font-semibold text-white mb-1">No matching research radar entries</h3>
          <p className="text-sm text-slate-400">Try changing your search keywords or topic filters.</p>
        </div>
      )}
    </div>
  );
}
