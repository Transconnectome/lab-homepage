import { useEffect, useRef, useState, type KeyboardEvent } from 'react';
import { researchConnections } from '../../data/researchMap';
import type { Lang } from '../../i18n/ui';

export interface MapArea {
  id: string;
  label: string;
  question: string;
  summary: string;
  approach: string;
  href: string;
  example: { label: string; href: string } | null;
}

const copy = {
  ko: {
    areas: '연구 질문 선택', approach: '질문에 접근하는 방법', example: '연구 사례',
    read: '이 연구 자세히 읽기', connections: '질문이 만나는 지점',
    kinds: { implemented: '연구에서의 결합', shared: '공유하는 관심', open: '열린 질문' },
    brainAlt: '왼쪽 앞 위에서 본 양쪽 대뇌피질의 굴곡과 전체 윤곽',
    brainCaption: '대뇌피질의 구조', brainSource: 'FreeSurfer fsaverage5 · 표면 자료를 렌더링한 그림',
    source: '자료 출처', license: '이용 조건', note: '아래 연결은 연구 질문 사이의 관계를 나타냅니다.',
  },
  en: {
    areas: 'Choose a research question', approach: 'How we approach the question', example: 'Research example',
    read: 'Read about this research', connections: 'Where the questions meet',
    kinds: { implemented: 'Combined in research', shared: 'Shared interest', open: 'Open question' },
    brainAlt: 'Full outline and folds of both cerebral cortical surfaces, seen from above and the left front',
    brainCaption: 'The structure of the cerebral cortex', brainSource: 'FreeSurfer fsaverage5 · rendered surface reference',
    source: 'Data source', license: 'Terms', note: 'The connections below describe relationships between research questions.',
  },
};

export default function ResearchMap({ areas, lang }: { areas: MapArea[]; lang: Lang }) {
  const [selected, setSelected] = useState(0);
  const [enhanced, setEnhanced] = useState(false);
  const tabs = useRef<(HTMLAnchorElement | null)[]>([]);
  const L = copy[lang];
  useEffect(() => setEnhanced(true), []);

  function onKeyDown(event: KeyboardEvent<HTMLAnchorElement>, index: number) {
    let next: number;
    switch (event.key) {
      case 'ArrowDown': next = (index + 1) % areas.length; break;
      case 'ArrowUp': next = (index + areas.length - 1) % areas.length; break;
      case 'Home': next = 0; break;
      case 'End': next = areas.length - 1; break;
      case ' ': event.preventDefault(); setSelected(index); return;
      default: return;
    }
    event.preventDefault();
    setSelected(next);
    tabs.current[next]?.focus({ preventScroll: true });
  }

  return (
    <div>
      <div className="grid lg:grid-cols-[minmax(0,1fr)_minmax(0,1.15fr)] gap-x-12 xl:gap-x-16 gap-y-8">
        <nav role={enhanced ? 'tablist' : undefined} aria-label={L.areas} aria-orientation={enhanced ? 'vertical' : undefined}
          className="border-t border-ink self-start">
          {areas.map((area, index) => (
            <a key={area.id} id={`map-tab-${area.id}`} href={`#${area.id}`}
              role={enhanced ? 'tab' : undefined} aria-selected={enhanced ? selected === index : undefined}
              aria-controls={enhanced ? `map-panel-${area.id}` : undefined}
              tabIndex={!enhanced || selected === index ? 0 : -1}
              ref={(element) => { tabs.current[index] = element; }}
              onClick={(event) => { event.preventDefault(); setSelected(index); }}
              onKeyDown={(event) => onKeyDown(event, index)}
              className={`group grid grid-cols-[1.5rem_minmax(0,1fr)_1rem] gap-3 sm:gap-4 py-3 lg:py-6 border-b border-line text-left focus-visible:outline focus-visible:outline-2 focus-visible:outline-lab-800 focus-visible:outline-offset-4 ${selected === index ? 'text-lab-900' : 'text-ink-soft hover:text-lab-800'}`}>
              <span className="text-xs tabular-nums pt-0.5" aria-hidden="true">{String(index + 1).padStart(2, '0')}</span>
              <span className="space-y-2 min-w-0">
                <span className="block text-sm lg:text-xs tracking-wide font-medium">{area.label}</span>
                <span className={`sr-only lg:not-sr-only lg:block font-display text-xl leading-relaxed ${selected === index ? 'font-semibold' : ''}`}>{area.question}</span>
              </span>
              <span aria-hidden="true" className={`lg:pt-5 text-lg leading-none ${selected === index ? 'opacity-100' : 'opacity-0'}`}>→</span>
            </a>
          ))}
        </nav>

        <div className="min-w-0 flex flex-col">
          <div className="lg:min-h-[20rem]">
            {areas.map((area, index) => (
              <div key={area.id} id={`map-panel-${area.id}`} role={enhanced ? 'tabpanel' : 'region'}
                aria-labelledby={`map-tab-${area.id}`} tabIndex={0} hidden={selected !== index}
                className="focus-visible:outline focus-visible:outline-2 focus-visible:outline-lab-800 focus-visible:outline-offset-4">
                <p className="text-xs font-medium tracking-wide text-lab-800 mb-4">{L.approach}</p>
                <h3 className="font-display text-2xl sm:text-3xl leading-snug font-semibold text-ink">{area.question}</h3>
                <p className="mt-5 text-base leading-relaxed text-ink-soft">{area.approach || area.summary}</p>
                <div className="mt-6 flex flex-wrap items-baseline gap-x-6 gap-y-3 text-sm">
                  {area.example && (
                    <div role="group" aria-label={L.example} className="flex flex-wrap gap-x-2 gap-y-1">
                      <span className="text-ink-faint">{L.example}</span>
                      <a href={area.example.href} className="text-lab-800 underline underline-offset-4 decoration-lab-800/30 hover:decoration-lab-800">{area.example.label}</a>
                    </div>
                  )}
                  <a href={area.href} className="text-lab-800 font-medium underline underline-offset-4 decoration-lab-800/30 hover:decoration-lab-800">{L.read} <span aria-hidden="true">↗</span></a>
                </div>
              </div>
            ))}
          </div>

          <figure className="mt-6 lg:mt-auto flex items-center gap-4 border-t border-line pt-4">
            <img src="/assets/research/cortical-surface.png" width="1600" height="1120"
              alt={L.brainAlt} className="w-2/5 max-w-[13rem] h-auto object-contain shrink-0" loading="lazy" decoding="async" />
            <figcaption className="text-xs leading-relaxed text-ink-faint min-w-0">
              <span className="block text-ink font-medium mb-1">{L.brainCaption}</span>
              <span className="block">{L.brainSource}</span>
              <span className="mt-2 flex flex-wrap gap-x-3 gap-y-1">
                <a href="https://nilearn.github.io/dev/modules/description/fsaverage5.html" className="underline underline-offset-4">{L.source}</a>
                <a href="/assets/research/FreeSurfer-LICENSE.txt" className="underline underline-offset-4">{L.license}</a>
              </span>
            </figcaption>
          </figure>
        </div>
      </div>

      <div className="mt-10 sm:mt-12 pt-6 border-t border-ink">
        <div className="flex flex-wrap items-baseline gap-x-6 gap-y-2 mb-6">
          <h3 className="font-display text-xl font-semibold">{L.connections}</h3>
          <p className="text-xs text-ink-faint">{L.note}</p>
        </div>
        <ul className="grid md:grid-cols-3 gap-x-8 gap-y-6">
          {researchConnections.map((connection) => (
            <li key={`${connection.a}-${connection.b}`} className="border-t border-line pt-4">
              <p className="text-xs text-ink-faint mb-2">{L.kinds[connection.kind]}</p>
              <p className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-lab-800 mb-3">
                {[connection.a, connection.b].map((id, index) => {
                  const areaIndex = areas.findIndex((area) => area.id === id);
                  const area = areas[areaIndex];
                  if (!area) return null;
                  return <span key={id} className="inline-flex gap-2 items-center min-w-0">
                    {index > 0 && <span aria-hidden="true">—</span>}
                    <a href={`#${id}`} title={area.label} className="underline underline-offset-4"
                      aria-label={`${String(areaIndex + 1).padStart(2, '0')} ${area.label}`}>
                      {String(areaIndex + 1).padStart(2, '0')} {area.label}
                    </a>
                  </span>;
                })}
              </p>
              <h4 className="text-sm font-semibold text-ink mb-2">{connection.title[lang]}</h4>
              <p className="text-sm leading-relaxed text-ink-soft">{connection.description[lang]}</p>
              {'source' in connection && (
                <a href={connection.source} className="inline-block mt-3 text-xs text-lab-800 underline underline-offset-4">
                  {typeof connection.sourceLabel === 'string' ? connection.sourceLabel : connection.sourceLabel[lang]} <span aria-hidden="true">↗</span>
                </a>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
