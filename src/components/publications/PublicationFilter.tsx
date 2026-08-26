import React, { useState, useMemo } from 'react';
import { Search, Code, ExternalLink, Copy, Check, BookOpen } from 'lucide-react';
import confetti from 'canvas-confetti';

interface PublicationItem {
  title: string;
  authors: string[];
  venue: string;
  year: number;
  month?: string | null;
  doi?: string | null;
  url?: string | null;
  pdfUrl?: string | null;
  codeUrl?: string | null;
  tags: string[];
  featured?: boolean;
  spotlight?: string | null;
  abstract?: string | null;
  labMembers: string[];
  kind?: 'journal' | 'conference' | 'workshop' | 'preprint';
}

interface Props {
  publications: PublicationItem[];
  lang?: 'en' | 'ko';
}

const MAX_VISIBLE_AUTHORS = 12;

const LABELS: Record<'en' | 'ko', Record<string, string>> = {
  en: {
    search: 'Search title, author, venue...',
    year: 'Year',
    allYears: 'All years',
    includePreprints: 'Include preprints',
    paper: 'Paper',
    code: 'Code',
    copied: 'Copied',
    noMatch: 'No publications matched',
    noMatchDesc: 'Clear the filters or try a different search term.',
    etAl: 'authors',
    kindJournal: 'Journal',
    kindConference: 'Conference',
    kindWorkshop: 'Workshop',
    kindPreprint: 'Preprint',
  },
  ko: {
    search: '제목·저자·게재지 검색...',
    year: '연도',
    allYears: '전체 연도',
    includePreprints: '프리프린트 포함',
    paper: '논문',
    code: '코드',
    copied: '복사됨',
    noMatch: '조건에 맞는 논문이 없습니다',
    noMatchDesc: '필터를 해제하거나 다른 검색어를 시도해 보세요.',
    etAl: '명의 저자',
    kindJournal: '저널',
    kindConference: '학회',
    kindWorkshop: '워크숍',
    kindPreprint: '프리프린트',
  },
};

function bibtexKey(pub: PublicationItem): string {
  const first = pub.authors[0] || 'connectomelab';
  const family = first.trim().split(/\s+/).pop() || 'connectomelab';
  const word = (pub.title.match(/[A-Za-z]{4,}/) || ['paper'])[0].toLowerCase();
  return `${family.toLowerCase().replace(/[^a-z]/g, '')}${pub.year}${word}`;
}

export default function PublicationFilter({ publications, lang = 'en' }: Props) {
  const L = LABELS[lang];
  const [selectedTag, setSelectedTag] = useState<string>('All');
  const [selectedYear, setSelectedYear] = useState<string>('All');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [includePreprints, setIncludePreprints] = useState<boolean>(false);

  // Peer-reviewed by default; preprints shown only when explicitly toggled on.
  const basePublications = useMemo(
    () => publications.filter((p) => includePreprints || (p.kind ?? 'journal') !== 'preprint'),
    [publications, includePreprints]
  );

  const allTags = useMemo(() => {
    const set = new Set<string>();
    basePublications.forEach((p) => p.tags.forEach((t) => set.add(t)));
    return ['All', ...Array.from(set).sort()];
  }, [basePublications]);

  const allYears = useMemo(() => {
    const years = Array.from(new Set(basePublications.map((p) => p.year.toString()))).sort(
      (a, b) => Number(b) - Number(a)
    );
    return ['All', ...years];
  }, [basePublications]);

  const filteredPublications = useMemo(() => {
    return basePublications.filter((pub) => {
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
  }, [basePublications, selectedTag, selectedYear, searchQuery]);

  const kindLabel = (k?: string) =>
    k === 'conference' ? L.kindConference : k === 'workshop' ? L.kindWorkshop : k === 'preprint' ? L.kindPreprint : L.kindJournal;

  const copyBibtex = (pub: PublicationItem) => {
    const bibtex = `@article{${bibtexKey(pub)},\n  title={${pub.title}},\n  author={${pub.authors.join(' and ')}},\n  journal={${pub.venue}},\n  year={${pub.year}},${pub.doi ? `\n  doi={${pub.doi}},` : ''}\n  url={${pub.url || ''}}\n}`;
    navigator.clipboard.writeText(bibtex);
    setCopiedId(pub.title);
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      confetti({ particleCount: 24, spread: 55, origin: { y: 0.85 }, colors: ['#0E7490', '#0891B2', '#164E63'] });
    }
    setTimeout(() => setCopiedId(null), 2500);
  };

  return (
    <div className="space-y-8">
      {/* Controls */}
      <div className="card p-5 sm:p-6 space-y-4">
        <div className="flex flex-col md:flex-row gap-4 justify-between md:items-center">
          <div className="relative w-full md:w-96">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-ink-faint" aria-hidden="true" />
            <label htmlFor="pub-search" className="sr-only">Search publications</label>
            <input
              id="pub-search"
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

          <div className="flex items-center gap-3 flex-wrap">
            <label htmlFor="pub-year" className="font-mono text-xs text-ink-faint">{L.year}</label>
            <select
              id="pub-year"
              value={selectedYear}
              onChange={(e) => setSelectedYear(e.target.value)}
              className="bg-paper border border-line rounded-lg px-3 py-2 text-sm text-ink focus:border-lab-600"
            >
              {allYears.map((year) => (
                <option key={year} value={year}>{year === 'All' ? L.allYears : year}</option>
              ))}
            </select>
            <label className="flex items-center gap-1.5 text-xs text-ink-soft cursor-pointer select-none">
              <input
                type="checkbox"
                checked={includePreprints}
                onChange={(e) => setIncludePreprints(e.target.checked)}
                className="rounded border-line accent-[#0E7490]"
              />
              {L.includePreprints}
            </label>
            <span className="font-mono text-xs text-ink-faint">
              {filteredPublications.length} / {basePublications.length}
            </span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 pt-3 border-t border-line">
          {allTags.map((tag) => (
            <button
              key={tag}
              onClick={() => setSelectedTag(tag)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                selectedTag === tag
                  ? 'bg-lab-700 text-white'
                  : 'bg-paper text-ink-soft hover:text-ink border border-line'
              }`}
            >
              {tag}
            </button>
          ))}
        </div>
      </div>

      {/* List */}
      <div className="space-y-4">
        {filteredPublications.map((pub, idx) => {
          const visibleAuthors = pub.authors.slice(0, MAX_VISIBLE_AUTHORS);
          const hiddenCount = pub.authors.length - visibleAuthors.length;
          return (
            <article
              key={`${pub.title}-${idx}`}
              className="card card-hover p-6 flex flex-col md:flex-row gap-5 justify-between items-start"
            >
              <div className="space-y-2.5 flex-1 min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="chip-accent" lang="en">{pub.year}</span>
                  <span className="chip">{kindLabel(pub.kind)}</span>
                  {pub.spotlight && <span className="chip" lang="en">✨ {pub.spotlight}</span>}
                  {pub.tags.map((tag) => (
                    <span key={tag} className="chip" lang="en">#{tag}</span>
                  ))}
                </div>

                <h3 className="text-base sm:text-lg font-semibold text-ink leading-snug">
                  {pub.url ? (
                    <a href={pub.url} target="_blank" rel="noreferrer" className="hover:text-lab-700 transition-colors">
                      {pub.title}
                    </a>
                  ) : (
                    pub.title
                  )}
                </h3>

                <p className="text-sm text-ink-soft leading-relaxed">
                  {visibleAuthors.map((author, aIdx) => {
                    const isLabMember = pub.labMembers.includes(author);
                    return (
                      <span key={aIdx}>
                        <span className={isLabMember ? 'font-semibold text-lab-800' : ''}>{author}</span>
                        {aIdx < visibleAuthors.length - 1 ? ', ' : ''}
                      </span>
                    );
                  })}
                  {hiddenCount > 0 && (
                    <span className="text-ink-faint"> … et al. ({pub.authors.length} {L.etAl})</span>
                  )}
                </p>

                <p className="font-mono text-xs text-ink-faint italic">{pub.venue}</p>

                {pub.abstract && (
                  <p className="text-sm text-ink-soft leading-relaxed pt-1">{pub.abstract}</p>
                )}
              </div>

              {/* Actions */}
              <div className="flex flex-row md:flex-col gap-2 shrink-0 w-full md:w-auto justify-end">
                {pub.url && (
                  <a
                    href={pub.url}
                    target="_blank"
                    rel="noreferrer"
                    className="px-3.5 py-2 rounded-lg bg-paper hover:bg-lab-50 text-ink-soft hover:text-lab-800 text-sm flex items-center justify-center gap-1.5 border border-line transition-colors"
                  >
                    <BookOpen className="w-4 h-4 text-lab-700" aria-hidden="true" />
                    <span>{L.paper}</span>
                  </a>
                )}
                {pub.codeUrl && (
                  <a
                    href={pub.codeUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="px-3.5 py-2 rounded-lg bg-paper hover:bg-lab-50 text-ink-soft hover:text-lab-800 text-sm flex items-center justify-center gap-1.5 border border-line transition-colors"
                  >
                    <Code className="w-4 h-4 text-lab-700" aria-hidden="true" />
                    <span>{L.code}</span>
                  </a>
                )}
                <button
                  onClick={() => copyBibtex(pub)}
                  className="px-3.5 py-2 rounded-lg bg-paper hover:bg-lab-50 text-ink-soft hover:text-lab-800 text-sm flex items-center justify-center gap-1.5 border border-line transition-colors"
                >
                  {copiedId === pub.title ? (
                    <>
                      <Check className="w-4 h-4 text-emerald-600" aria-hidden="true" />
                      <span className="text-emerald-700 font-semibold">{L.copied}</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4" aria-hidden="true" />
                      <span>BibTeX</span>
                    </>
                  )}
                </button>
              </div>
            </article>
          );
        })}
      </div>

      {filteredPublications.length === 0 && (
        <div className="text-center py-16 card">
          <BookOpen className="w-10 h-10 text-ink-faint mx-auto mb-3" aria-hidden="true" />
          <h3 className="text-lg font-semibold text-ink mb-1">{L.noMatch}</h3>
          <p className="text-sm text-ink-soft">{L.noMatchDesc}</p>
        </div>
      )}
    </div>
  );
}
