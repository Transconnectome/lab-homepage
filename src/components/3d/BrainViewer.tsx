import React, { useEffect, useRef, useState } from 'react';
import BrainCanvas from './BrainCanvas';
import { BRAIN_HUBS, type BrainNode } from './brainData';

type Lang = 'en' | 'ko';

interface Props {
  lang?: Lang;
}

const LABELS: Record<Lang, Record<string, string>> = {
  en: {
    badge: 'CONNECTOME SKETCH · ILLUSTRATIVE',
    hint: 'Tap a node or a chip to explore each network',
    canvasAria: 'Interactive illustration of brain networks studied by the lab',
    legendLabel: 'Brain networks',
    emptyTitle: 'Pick a brain network',
    emptyBody:
      'Each glowing node is a brain system our lab studies. Select one to see what it does and which lab projects investigate it.',
    what: 'What it does',
    why: 'Why we study it',
    related: 'Related lab research',
    explore: 'Explore research',
    pubs: 'All publications',
    close: 'Clear selection',
  },
  ko: {
    badge: '커넥톰 스케치 · 일러스트',
    hint: '노드나 칩을 눌러 각 네트워크를 살펴보세요',
    canvasAria: '연구실이 탐구하는 뇌 네트워크의 인터랙티브 일러스트',
    legendLabel: '뇌 네트워크',
    emptyTitle: '뇌 네트워크를 선택하세요',
    emptyBody:
      '빛나는 각 노드는 연구실이 탐구하는 뇌 시스템입니다. 하나를 선택하면 그 기능과 관련 연구 프로젝트를 볼 수 있습니다.',
    what: '무엇을 하는가',
    why: '왜 연구하는가',
    related: '관련 연구',
    explore: '연구 살펴보기',
    pubs: '전체 논문',
    close: '선택 해제',
  },
};

const withLang = (lang: Lang, path: string) => (lang === 'ko' ? `/ko${path}` : path);

function InfoPanel({
  hub,
  lang,
  onClose,
}: {
  hub: BrainNode;
  lang: Lang;
  onClose: () => void;
}) {
  const L = LABELS[lang];
  const name = lang === 'ko' ? hub.nameKo : hub.name;
  const altName = lang === 'ko' ? hub.name : hub.nameKo;
  return (
    <div className="h-full p-5 rounded-xl bg-slate-900/80 border border-cyan-500/40 text-slate-200 shadow-xl animate-in fade-in slide-in-from-bottom-2 duration-300">
      <div className="flex items-start justify-between gap-3 mb-1">
        <div className="flex items-center gap-2 min-w-0">
          <span
            className="w-3.5 h-3.5 rounded-full ring-2 ring-cyan-400/40 shrink-0"
            style={{ backgroundColor: hub.color }}
          />
          <h3 className="font-bold text-white text-base leading-snug">{name}</h3>
        </div>
        <button
          onClick={onClose}
          className="text-slate-400 hover:text-white text-xs px-2 py-1 rounded bg-slate-800 border border-slate-700 shrink-0"
          aria-label={L.close}
        >
          ✕
        </button>
      </div>
      <p className="text-xs text-cyan-300/90 font-medium mb-3">{altName}</p>

      <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
        {L.what}
      </div>
      <p className="text-sm text-slate-300 leading-relaxed mb-3">
        {lang === 'ko' ? hub.descriptionKo : hub.description}
      </p>

      <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
        {L.why}
      </div>
      <p className="text-sm text-slate-300 leading-relaxed mb-3">
        {lang === 'ko' ? hub.whyWeStudyKo : hub.whyWeStudy}
      </p>

      <div className="border-t border-slate-800 pt-3">
        <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
          {L.related}
        </div>
        <ul className="space-y-1.5">
          {hub.projects.map((proj) => (
            <li key={proj.href + proj.label} className="text-sm flex items-start gap-1.5">
              <span className="text-cyan-400 mt-0.5">▹</span>
              <a
                href={withLang(lang, proj.href)}
                className="text-slate-200 underline decoration-cyan-500/40 underline-offset-2 hover:text-cyan-300 transition-colors"
              >
                {lang === 'ko' ? proj.labelKo : proj.label}
              </a>
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-4 flex gap-2">
        <a
          href={withLang(lang, '/research')}
          className="flex-1 text-center py-2 px-3 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-sm transition"
        >
          {L.explore}
        </a>
        <a
          href={withLang(lang, '/publications')}
          className="py-2 px-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm transition"
        >
          {L.pubs}
        </a>
      </div>
    </div>
  );
}

export default function BrainViewer({ lang = 'en' }: Props) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const L = LABELS[lang];

  const selected = BRAIN_HUBS.find((h) => h.id === selectedId) ?? null;
  const hovered = BRAIN_HUBS.find((h) => h.id === hoveredId) ?? null;

  // On small screens the panel sits below the canvas — bring it into view
  // after a node/chip selection so the tap visibly does something.
  useEffect(() => {
    if (!selectedId) return;
    if (window.matchMedia('(min-width: 1024px)').matches) return;
    panelRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }, [selectedId]);

  return (
    <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_22rem]">
      <div className="relative h-[420px] sm:h-[500px] md:h-[560px] overflow-hidden rounded-2xl bg-deep border border-deep-line shadow-2xl">
        <BrainCanvas
          selectedId={selectedId}
          hoveredId={hoveredId}
          onSelect={setSelectedId}
          onHover={setHoveredId}
          ariaLabel={L.canvasAria}
        />

        {/* Honest caption: this is an illustration, not anatomical data */}
        <div className="absolute top-5 left-5 px-3 py-1.5 rounded-full bg-slate-900/80 backdrop-blur-md border border-cyan-500/30 text-xs font-mono text-cyan-300 pointer-events-none">
          {L.badge}
        </div>
        <div className="absolute top-5 right-5 hidden sm:flex px-3 py-1.5 rounded-lg bg-slate-900/70 border border-slate-700 text-xs text-slate-400 pointer-events-none">
          {L.hint}
        </div>

        {hovered && hovered.id !== selectedId && (
          <div className="absolute bottom-5 left-5 max-w-sm p-4 rounded-xl bg-slate-900/90 backdrop-blur-xl border border-cyan-500/40 text-slate-200 shadow-xl pointer-events-none">
            <div className="flex items-center gap-2 mb-1">
              <span className="w-3 h-3 rounded-full" style={{ backgroundColor: hovered.color }} />
              <h4 className="font-semibold text-white text-sm">
                {lang === 'ko' ? hovered.nameKo : hovered.name}
              </h4>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              {lang === 'ko' ? hovered.descriptionKo : hovered.description}
            </p>
          </div>
        )}
      </div>

      <div className="flex flex-col gap-3 min-w-0">
        <div role="group" aria-label={L.legendLabel} className="flex flex-wrap lg:grid lg:grid-cols-2 gap-2">
          {BRAIN_HUBS.map((hub) => {
            const isSelected = selectedId === hub.id;
            return (
              <button
                key={hub.id}
                type="button"
                aria-pressed={isSelected}
                onClick={() => setSelectedId((prev) => (prev === hub.id ? null : hub.id))}
                onMouseEnter={() => setHoveredId(hub.id)}
                onMouseLeave={() => setHoveredId((prev) => (prev === hub.id ? null : prev))}
                onFocus={() => setHoveredId(hub.id)}
                onBlur={() => setHoveredId((prev) => (prev === hub.id ? null : prev))}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg border text-left text-xs font-medium transition-colors ${
                  isSelected
                    ? 'border-cyan-400/70 bg-cyan-500/10 text-white'
                    : 'border-slate-700 bg-slate-900/70 text-slate-300 hover:border-slate-500 hover:text-white'
                }`}
              >
                <span
                  className="w-2.5 h-2.5 rounded-full shrink-0"
                  style={{ backgroundColor: hub.color }}
                />
                <span className="truncate">{lang === 'ko' ? hub.networkKo : hub.network}</span>
              </button>
            );
          })}
        </div>

        <div ref={panelRef} className="flex-1 min-h-0" aria-live="polite">
          {selected ? (
            <InfoPanel hub={selected} lang={lang} onClose={() => setSelectedId(null)} />
          ) : (
            <div className="h-full min-h-[16rem] p-5 rounded-xl border border-dashed border-slate-700 bg-slate-900/40 text-slate-400 flex flex-col items-start justify-center gap-2">
              <div className="flex gap-1.5 mb-1">
                {BRAIN_HUBS.map((hub) => (
                  <span
                    key={hub.id}
                    className="w-2 h-2 rounded-full opacity-70"
                    style={{ backgroundColor: hub.color }}
                  />
                ))}
              </div>
              <h3 className="font-semibold text-slate-200 text-sm">{L.emptyTitle}</h3>
              <p className="text-sm leading-relaxed">{L.emptyBody}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
