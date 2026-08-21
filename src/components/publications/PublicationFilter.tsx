import React, { useState, useMemo } from 'react';
import { Search, Code, ExternalLink, Copy, Check, Sparkles, BookOpen } from 'lucide-react';
import confetti from 'canvas-confetti';

interface PublicationItem {
  title: string;
  authors: string[];
  venue: string;
  year: number;
  month?: string;
  doi?: string;
  url?: string;
  pdfUrl?: string;
  codeUrl?: string;
  tags: string[];
  featured?: boolean;
  spotlight?: string;
  abstract?: string;
  labMembers: string[];
}

interface Props {
  publications: PublicationItem[];
}

export default function PublicationFilter({ publications }: Props) {
  const [selectedTag, setSelectedTag] = useState<string>('All');
  const [selectedYear, setSelectedYear] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const allTags = useMemo(() => {
    const set = new Set<string>();
    publications.forEach((p) => p.tags.forEach((t) => set.add(t)));
    return ['All', ...Array.from(set)];
  }, [publications]);

  const allYears = useMemo(() => {
    const years = Array.from(new Set(publications.map((p) => p.year.toString()))).sort(
      (a, b) => Number(b) - Number(a)
    );
    return ['All', ...years];
  }, [publications]);

  const filteredPublications = useMemo(() => {
    return publications.filter((pub) => {
      const matchTag = selectedTag === 'All' || pub.tags.includes(selectedTag);
      const matchYear = selectedYear === 'All' || pub.year.toString() === selectedYear;
      const query = searchQuery.toLowerCase();
      const matchSearch =
        pub.title.toLowerCase().includes(query) ||
        pub.venue.toLowerCase().includes(query) ||
        pub.authors.some((a) => a.toLowerCase().includes(query)) ||
        (pub.abstract && pub.abstract.toLowerCase().includes(query));

      return matchTag && matchYear && matchSearch;
    });
  }, [publications, selectedTag, selectedYear, searchQuery]);

  const copyBibtex = (pub: PublicationItem, e: React.MouseEvent) => {
    const key = (pub.authors[0]?.split(' ')[1] || 'cha') + pub.year;
    const bibtex = `@article{${key.toLowerCase()},\n  title={${pub.title}},\n  author={${pub.authors.join(' and ')}},\n  journal={${pub.venue}},\n  year={${pub.year}},\n  ${pub.doi ? `doi={${pub.doi}},` : ''}\n  url={${pub.url || ''}}\n}`;

    navigator.clipboard.writeText(bibtex);
    setCopiedId(pub.title);

    // Trigger subtle celebratory confetti
    confetti({
      particleCount: 30,
      spread: 60,
      origin: { y: 0.8 },
      colors: ['#38bdf8', '#818cf8', '#00e5ff'],
    });

    setTimeout(() => setCopiedId(null), 2500);
  };

  return (
    <div className="space-y-8">
      {/* Control Panel: Search & Filters */}
      <div className="p-6 rounded-3xl glass-panel border border-slate-700/60 shadow-xl space-y-4">
        <div className="flex flex-col md:flex-row gap-4 justify-between items-center">
          {/* Search bar */}
          <div className="relative w-full md:w-96">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by title, author, keyword, or venue..."
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

          {/* Year selector */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400 font-mono">Year:</span>
            <div className="flex gap-1.5 bg-slate-900/80 p-1 rounded-xl border border-slate-800">
              {allYears.map((year) => (
                <button
                  key={year}
                  onClick={() => setSelectedYear(year)}
                  className={`px-3 py-1 rounded-lg text-xs font-mono transition ${
                    selectedYear === year
                      ? 'bg-cyan-500 text-slate-950 font-bold'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {year}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Tag pills */}
        <div className="flex flex-wrap gap-2 pt-2 border-t border-slate-800">
          {allTags.map((tag) => (
            <button
              key={tag}
              onClick={() => setSelectedTag(tag)}
              className={`px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
                selectedTag === tag
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md'
                  : 'bg-slate-900/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-800'
              }`}
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      {/* Publications List */}
      <div className="space-y-4">
        {filteredPublications.map((pub, idx) => (
          <div
            key={idx}
            className="p-6 rounded-3xl glass-panel glass-panel-hover border border-slate-800 flex flex-col md:flex-row gap-6 justify-between items-start group"
          >
            <div className="space-y-2.5 flex-1">
              {/* Badges / Spotlight */}
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs font-mono font-bold text-cyan-400 bg-cyan-950/60 border border-cyan-800/60 px-2.5 py-0.5 rounded-full">
                  {pub.year}
                </span>
                {pub.spotlight && (
                  <span className="text-xs font-medium px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/30 flex items-center gap-1">
                    <Sparkles className="w-3 h-3 text-amber-400" />
                    {pub.spotlight}
                  </span>
                )}
                {pub.tags.map((tag, tIdx) => (
                  <span
                    key={tIdx}
                    className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-slate-900 text-slate-400 border border-slate-800"
                  >
                    #{tag}
                  </span>
                ))}
              </div>

              {/* Title */}
              <h3 className="text-lg font-bold text-white group-hover:text-cyan-300 transition leading-snug">
                {pub.url ? (
                  <a href={pub.url} target="_blank" rel="noreferrer" className="hover:underline flex items-start gap-1.5">
                    <span>{pub.title}</span>
                    <ExternalLink className="w-4 h-4 text-slate-500 group-hover:text-cyan-400 shrink-0 mt-1" />
                  </a>
                ) : (
                  pub.title
                )}
              </h3>

              {/* Authors */}
              <p className="text-xs text-slate-300 leading-relaxed">
                {pub.authors.map((author, aIdx) => {
                  const isLabMember = pub.labMembers.some((m) => author.includes(m) || m.includes(author));
                  return (
                    <span key={aIdx}>
                      <span className={isLabMember ? 'font-semibold text-cyan-300' : 'text-slate-400'}>
                        {author}
                      </span>
                      {aIdx < pub.authors.length - 1 ? ', ' : ''}
                    </span>
                  );
                })}
              </p>

              {/* Venue */}
              <p className="text-xs font-mono text-slate-400 italic">{pub.venue}</p>

              {/* Abstract */}
              {pub.abstract && (
                <p className="text-xs text-slate-400 leading-relaxed pt-1 line-clamp-2 group-hover:line-clamp-none transition-all">
                  {pub.abstract}
                </p>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex flex-row md:flex-col gap-2 shrink-0 w-full md:w-auto justify-end pt-2 md:pt-0 border-t md:border-t-0 border-slate-800">
              {pub.url && (
                <a
                  href={pub.url}
                  target="_blank"
                  rel="noreferrer"
                  className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs flex items-center justify-center gap-1.5 border border-slate-700 transition"
                >
                  <BookOpen className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Paper</span>
                </a>
              )}
              {pub.codeUrl && (
                <a
                  href={pub.codeUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs flex items-center justify-center gap-1.5 border border-slate-700 transition"
                >
                  <Code className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Code</span>
                </a>
              )}
              <button
                onClick={(e) => copyBibtex(pub, e)}
                className="px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs flex items-center justify-center gap-1.5 border border-slate-700 transition"
              >
                {copiedId === pub.title ? (
                  <>
                    <Check className="w-3.5 h-3.5 text-emerald-400" />
                    <span className="text-emerald-300 font-semibold">Copied!</span>
                  </>
                ) : (
                  <>
                    <Copy className="w-3.5 h-3.5 text-slate-400" />
                    <span>BibTeX</span>
                  </>
                )}
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredPublications.length === 0 && (
        <div className="text-center py-16 rounded-3xl glass-panel border border-slate-800">
          <BookOpen className="w-12 h-12 text-slate-600 mx-auto mb-3 animate-pulse" />
          <h3 className="text-lg font-semibold text-white mb-1">No publications matched</h3>
          <p className="text-sm text-slate-400">Try clearing filters or changing your search terms.</p>
        </div>
      )}
    </div>
  );
}
