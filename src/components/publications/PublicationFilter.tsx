import React, { useState, useMemo, useEffect, useRef } from 'react';
import { isCsAiConference } from '../../utils/publications';

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
  csAiVenue?: boolean | null;
}

/** Venue-type view; mirrored in the ?type= query param so views are linkable. */
type VenueType = 'all' | 'journal' | 'cs-ai';

interface Props {
  publications: PublicationItem[];
  lang?: 'en' | 'ko';
}

const MAX_VISIBLE_AUTHORS = 12;

const LABELS: Record<'en' | 'ko', Record<string, string>> = {
  en: {
    searchLabel: 'Search publications',
    search: 'Title, author, venue or abstract',
    year: 'Year',
    allYears: 'All years',
    topic: 'Topic',
    allTopics: 'All topics',
    includePreprints: 'Include preprints',
    paper: 'Paper',
    code: 'Code',
    abstract: 'Abstract',
    copyBibtex: 'Copy BibTeX',
    copied: 'Copied',
    copyFailed: 'Could not copy. Check clipboard access and try again.',
    noMatch: 'No publications matched',
    noMatchDesc: 'Clear the filters or try a different search term.',
    etAl: 'authors',
    showAuthors: 'All authors',
    results: 'publications',
    kindJournal: 'Journal',
    kindConference: 'Conference',
    kindWorkshop: 'Workshop',
    kindPreprint: 'Preprint',
    venueType: 'Publication type',
    typeAll: 'All types',
    typeJournal: 'Journals',
    typeCsAi: 'CS/AI conferences',
    preprintsNA: 'Preprints are available under “All types”.',
    csAiNote:
      'Conference and workshop papers at computing venues, including NeurIPS, ICML, AAAI, ICASSP, ICIP, MICCAI and IEEE quantum computing.',
  },
  ko: {
    searchLabel: '논문 검색',
    search: '제목, 저자, 게재지 또는 초록',
    year: '연도',
    allYears: '전체 연도',
    topic: '주제',
    allTopics: '전체 주제',
    includePreprints: '프리프린트 포함',
    paper: '논문',
    code: '코드',
    abstract: '초록',
    copyBibtex: 'BibTeX 복사',
    copied: '복사됨',
    copyFailed: '복사하지 못했습니다. 클립보드 접근을 확인한 뒤 다시 시도해 주세요.',
    noMatch: '조건에 맞는 논문이 없습니다',
    noMatchDesc: '필터를 해제하거나 다른 검색어를 시도해 보세요.',
    etAl: '명의 저자',
    showAuthors: '전체 저자',
    results: '편',
    kindJournal: '저널',
    kindConference: '학회',
    kindWorkshop: '워크숍',
    kindPreprint: '프리프린트',
    venueType: '게재 유형',
    typeAll: '전체 유형',
    typeJournal: '저널 논문',
    typeCsAi: 'CS/AI 학회 논문',
    preprintsNA: '프리프린트는 ‘전체 유형’에서 볼 수 있습니다.',
    csAiNote:
      'NeurIPS, ICML, AAAI, ICASSP, ICIP, MICCAI, IEEE 양자컴퓨팅 등 컴퓨터·AI 분야 학회와 워크숍에 게재된 논문입니다.',
  },
};

function bibtexKey(pub: PublicationItem): string {
  const first = pub.authors[0] || 'connectomelab';
  const family = first.trim().split(/\s+/).pop() || 'connectomelab';
  const word = (pub.title.match(/[A-Za-z]{4,}/) || ['paper'])[0].toLowerCase();
  return `${family.toLowerCase().replace(/[^a-z]/g, '')}${pub.year}${word}`;
}

function bibtexEntry(pub: PublicationItem): string {
  const kind = pub.kind ?? 'journal';
  const conference = kind === 'conference' || kind === 'workshop';
  const entryType = conference ? 'inproceedings' : kind === 'preprint' ? 'unpublished' : 'article';
  const fields = [
    `title={${pub.title}}`,
    `author={${pub.authors.join(' and ')}}`,
    kind === 'preprint' ? 'note={Preprint}' : `${conference ? 'booktitle' : 'journal'}={${pub.venue}}`,
    `year={${pub.year}}`,
    ...(pub.doi ? [`doi={${pub.doi}}`] : []),
    ...(pub.url ? [`url={${pub.url}}`] : []),
  ];
  return `@${entryType}{${bibtexKey(pub)},\n  ${fields.join(',\n  ')}\n}`;
}

const publicationId = (pub: PublicationItem) => pub.doi || pub.url || `${pub.year}:${pub.title}`;
const CONTROL_CLASS = 'form-field min-w-0 py-2.5 focus:border-lab-700';

export default function PublicationFilter({ publications, lang = 'en' }: Props) {
  const L = LABELS[lang];
  const [selectedTag, setSelectedTag] = useState('All');
  const [selectedYear, setSelectedYear] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [copyFeedback, setCopyFeedback] = useState<{ id: string; status: 'copied' | 'error' } | null>(null);
  const [includePreprints, setIncludePreprints] = useState(false);
  const [venueType, setVenueType] = useState<VenueType>('all');
  const copyTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const copyAttempt = useRef(0);

  // Read after mount so the initial hydrated markup matches the static page.
  // A direct ?type= link is not rewritten while that initial state is loading.
  useEffect(() => {
    const readVenueType = () => {
      const param = new URLSearchParams(window.location.search).get('type');
      setVenueType(param === 'cs-ai' || param === 'journal' ? param : 'all');
      setSelectedTag('All');
      setSelectedYear('All');
    };
    readVenueType();
    window.addEventListener('popstate', readVenueType);
    return () => window.removeEventListener('popstate', readVenueType);
  }, []);

  useEffect(() => () => {
    if (copyTimer.current) clearTimeout(copyTimer.current);
    copyAttempt.current += 1;
  }, []);

  const selectVenueType = (next: VenueType) => {
    setVenueType(next);
    setSelectedTag('All');
    setSelectedYear('All');
    const url = new URL(window.location.href);
    if (next === 'all') url.searchParams.delete('type');
    else url.searchParams.set('type', next);
    window.history.replaceState({}, '', url);
  };

  // Preprints remain opt-in, and are never included in either published view.
  const basePublications = useMemo(
    () => publications.filter((p) => {
      if (venueType === 'cs-ai') return isCsAiConference(p);
      if (venueType === 'journal') return (p.kind ?? 'journal') === 'journal';
      return includePreprints || (p.kind ?? 'journal') !== 'preprint';
    }),
    [publications, includePreprints, venueType]
  );

  const allTags = useMemo(
    () => ['All', ...Array.from(new Set(basePublications.flatMap((p) => p.tags))).sort()],
    [basePublications]
  );
  const allYears = useMemo(
    () => ['All', ...Array.from(new Set(basePublications.map((p) => String(p.year))))
      .sort((a, b) => Number(b) - Number(a))],
    [basePublications]
  );

  // Removing preprints can also remove the selected topic or year.
  useEffect(() => {
    if (!allTags.includes(selectedTag)) setSelectedTag('All');
    if (!allYears.includes(selectedYear)) setSelectedYear('All');
  }, [allTags, allYears, selectedTag, selectedYear]);

  const filteredPublications = useMemo(() => {
    const query = searchQuery.trim().toLowerCase();
    return basePublications.filter((pub) => {
      const matchTag = selectedTag === 'All' || pub.tags.includes(selectedTag);
      const matchYear = selectedYear === 'All' || String(pub.year) === selectedYear;
      const matchSearch = !query || [pub.title, pub.venue, ...pub.authors, pub.abstract ?? '']
        .some((text) => text.toLowerCase().includes(query));
      return matchTag && matchYear && matchSearch;
    });
  }, [basePublications, selectedTag, selectedYear, searchQuery]);

  const publicationsByYear = useMemo(() => {
    const groups = new Map<number, PublicationItem[]>();
    filteredPublications.forEach((pub) => {
      const entries = groups.get(pub.year) ?? [];
      entries.push(pub);
      groups.set(pub.year, entries);
    });
    return Array.from(groups.entries()).sort(([a], [b]) => b - a);
  }, [filteredPublications]);

  const kindLabel = (kind?: string) => kind === 'conference' ? L.kindConference
    : kind === 'workshop' ? L.kindWorkshop : kind === 'preprint' ? L.kindPreprint : L.kindJournal;

  const copyBibtex = async (pub: PublicationItem) => {
    const attempt = ++copyAttempt.current;
    if (copyTimer.current) clearTimeout(copyTimer.current);
    setCopyFeedback(null);
    try {
      if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(bibtexEntry(pub));
      if (attempt !== copyAttempt.current) return;
      setCopyFeedback({ id: publicationId(pub), status: 'copied' });
      copyTimer.current = setTimeout(() => setCopyFeedback(null), 2500);
    } catch {
      if (attempt === copyAttempt.current) setCopyFeedback({ id: publicationId(pub), status: 'error' });
    }
  };

  const authorNames = (pub: PublicationItem, authors: string[]) => authors.map((author, index) => (
    <React.Fragment key={`${author}-${index}`}>
      <span className={pub.labMembers.includes(author) ? 'font-medium text-ink' : undefined}>{author}</span>
      {index < authors.length - 1 ? ', ' : ''}
    </React.Fragment>
  ));

  return (
    <div className="space-y-12">
      <div className="border-y border-line py-6 space-y-4">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-[minmax(0,1.5fr)_minmax(0,1fr)_minmax(0,0.7fr)_minmax(0,1.1fr)]">
          <div className="min-w-0 space-y-2">
            <label htmlFor="pub-search" className="block text-sm font-medium text-ink">{L.searchLabel}</label>
            <input
              id="pub-search"
              type="search"
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
              placeholder={L.search}
              className={CONTROL_CLASS}
            />
          </div>
          <div className="min-w-0 space-y-2">
            <label htmlFor="pub-type" className="block text-sm font-medium text-ink">{L.venueType}</label>
            <select id="pub-type" value={venueType} onChange={(event) => selectVenueType(event.target.value as VenueType)} className={CONTROL_CLASS}>
              <option value="all">{L.typeAll}</option>
              <option value="journal">{L.typeJournal}</option>
              <option value="cs-ai">{L.typeCsAi}</option>
            </select>
          </div>
          <div className="min-w-0 space-y-2">
            <label htmlFor="pub-year" className="block text-sm font-medium text-ink">{L.year}</label>
            <select id="pub-year" value={selectedYear} onChange={(event) => setSelectedYear(event.target.value)} className={CONTROL_CLASS}>
              {allYears.map((year) => <option key={year} value={year}>{year === 'All' ? L.allYears : year}</option>)}
            </select>
          </div>
          <div className="min-w-0 space-y-2">
            <label htmlFor="pub-topic" className="block text-sm font-medium text-ink">{L.topic}</label>
            <select id="pub-topic" value={selectedTag} onChange={(event) => setSelectedTag(event.target.value)} className={CONTROL_CLASS}>
              {allTags.map((tag) => <option key={tag} value={tag}>{tag === 'All' ? L.allTopics : tag}</option>)}
            </select>
          </div>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-x-6 gap-y-3 text-sm">
          <div className="flex flex-wrap items-center gap-x-4 gap-y-2">
            <label htmlFor="pub-preprints" className={`inline-flex items-center gap-2 ${venueType === 'all' ? 'text-ink-soft cursor-pointer' : 'text-ink-faint'}`}>
              <input
                id="pub-preprints"
                type="checkbox"
                checked={includePreprints && venueType === 'all'}
                disabled={venueType !== 'all'}
                aria-describedby={venueType === 'all' ? undefined : 'pub-preprint-note'}
                onChange={(event) => setIncludePreprints(event.target.checked)}
                className="border-line accent-[#0E7490] disabled:opacity-50"
              />
              {L.includePreprints}
            </label>
            {venueType !== 'all' && <p id="pub-preprint-note" className="text-xs text-ink-faint">{L.preprintsNA}</p>}
          </div>
          <p className="text-ink-faint" role="status">{filteredPublications.length} {L.results}</p>
        </div>
        {venueType === 'cs-ai' && <p className="text-sm text-ink-soft leading-relaxed">{L.csAiNote}</p>}
      </div>

      <div className="space-y-14">
        {publicationsByYear.map(([year, entries]) => (
          <section key={year} aria-labelledby={`publications-year-${year}`} className="grid gap-5 sm:grid-cols-[5rem_minmax(0,1fr)] sm:gap-8">
            <h2 id={`publications-year-${year}`} className="font-display text-2xl font-semibold text-ink scroll-mt-24">{year}</h2>
            <ol className="min-w-0 border-t border-line divide-y divide-line">
              {entries.map((pub) => {
                const id = publicationId(pub);
                const visibleAuthors = pub.authors.slice(0, MAX_VISIBLE_AUTHORS);
                const doiUrl = pub.doi ? (/^https?:\/\//i.test(pub.doi) ? pub.doi : `https://doi.org/${pub.doi}`) : null;
                const feedback = copyFeedback?.id === id ? copyFeedback.status : null;
                return (
                  <li key={id} className="py-6">
                    <article className="space-y-2.5" data-publication-kind={pub.kind ?? 'journal'}>
                      <p className="text-sm text-ink-soft leading-relaxed" lang="en">
                        {authorNames(pub, visibleAuthors)}
                        {pub.authors.length > MAX_VISIBLE_AUTHORS && <span> … et al.</span>}
                      </p>
                      <h3 className="text-base sm:text-lg font-semibold text-ink leading-snug" lang="en">
                        {pub.url ? <a href={pub.url} target="_blank" rel="noreferrer" className="hover:underline underline-offset-4">{pub.title}</a> : pub.title}
                      </h3>
                      <p className="text-sm text-ink-soft leading-relaxed">
                        <cite className="italic" lang="en">{pub.venue}</cite>. <span lang="en">{pub.year}</span>
                        <span className="text-ink-faint"> · {kindLabel(pub.kind)}</span>
                        {pub.spotlight && <span className="text-ink-faint" lang="en"> · {pub.spotlight}</span>}
                      </p>
                      <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-sm pt-1">
                        {doiUrl && <a href={doiUrl} target="_blank" rel="noreferrer" className="text-link">DOI</a>}
                        {pub.url && <a href={pub.url} target="_blank" rel="noreferrer" className="text-link">{L.paper}</a>}
                        {pub.pdfUrl && <a href={pub.pdfUrl} target="_blank" rel="noreferrer" className="text-link">PDF</a>}
                        {pub.codeUrl && <a href={pub.codeUrl} target="_blank" rel="noreferrer" className="text-link">{L.code}</a>}
                        <button type="button" onClick={() => void copyBibtex(pub)} className="text-link" aria-label={`${L.copyBibtex}: ${pub.title}`} data-bibtex-copy>
                          BibTeX
                        </button>
                        <span role="status" className="text-xs text-ink-soft">
                          {feedback === 'copied' ? L.copied : feedback === 'error' ? L.copyFailed : ''}
                        </span>
                      </div>
                      {pub.authors.length > MAX_VISIBLE_AUTHORS && (
                        <details className="text-sm text-ink-soft pt-1">
                          <summary className="cursor-pointer text-link">{L.showAuthors} ({pub.authors.length} {L.etAl})</summary>
                          <p className="pt-3 leading-relaxed" lang="en">{authorNames(pub, pub.authors)}</p>
                        </details>
                      )}
                      {pub.abstract && (
                        <details className="text-sm text-ink-soft pt-1" data-publication-abstract>
                          <summary className="cursor-pointer text-link">{L.abstract}</summary>
                          <p className="pt-3 leading-relaxed" lang="en">{pub.abstract}</p>
                        </details>
                      )}
                    </article>
                  </li>
                );
              })}
            </ol>
          </section>
        ))}
      </div>

      {filteredPublications.length === 0 && (
        <div className="border-t border-line py-8">
          <h2 className="text-lg font-semibold text-ink mb-2">{L.noMatch}</h2>
          <p className="text-sm text-ink-soft">{L.noMatchDesc}</p>
        </div>
      )}
    </div>
  );
}
