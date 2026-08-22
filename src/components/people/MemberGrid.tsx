import React, { useState } from 'react';
import { Mail, ExternalLink, Heart, Github, BookOpen, GraduationCap } from 'lucide-react';

interface Member {
  name: string;
  nameKo: string;
  role: string;
  roleKo: string;
  category: 'pi' | 'phd' | 'ms' | 'undergrad' | 'staff' | 'alumni';
  email?: string | null;
  avatar?: string | null;
  affiliations: string[];
  education: string[];
  researchInterests: string[];
  passions: string[];
  links?: {
    scholar?: string | null;
    github?: string | null;
    linkedin?: string | null;
    website?: string | null;
  } | null;
  order: number;
}

interface Props {
  members: Member[];
  lang?: 'en' | 'ko';
}

const TAB_LABELS: Record<'en' | 'ko', Record<string, string>> = {
  en: { all: 'Everyone', pi: 'Principal Investigator', grad: 'Graduate Students', undergrad: 'Interns', staff: 'Staff', alumni: 'Alumni' },
  ko: { all: '전체', pi: '지도교수', grad: '대학원생', undergrad: '학부 인턴', staff: '스태프', alumni: '동문' },
};

const CATEGORY_TABS: { id: string; match: (c: Member['category']) => boolean }[] = [
  { id: 'all', match: () => true },
  { id: 'pi', match: (c) => c === 'pi' },
  { id: 'grad', match: (c) => c === 'phd' || c === 'ms' },
  { id: 'undergrad', match: (c) => c === 'undergrad' },
  { id: 'staff', match: (c) => c === 'staff' },
  { id: 'alumni', match: (c) => c === 'alumni' },
];

export default function MemberGrid({ members, lang = 'en' }: Props) {
  const [selected, setSelected] = useState('all');

  // Only show tabs that actually have members
  const tabs = CATEGORY_TABS.filter(
    (tab) => tab.id === 'all' || members.some((m) => tab.match(m.category))
  );
  const activeTab = tabs.find((t) => t.id === selected) || tabs[0];
  const filtered = members.filter((m) => activeTab.match(m.category));

  return (
    <div className="space-y-8">
      {/* Category tabs */}
      <div className="flex flex-wrap gap-2" role="tablist" aria-label="Member categories">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            aria-selected={selected === tab.id}
            onClick={() => setSelected(tab.id)}
            className={`px-4 py-2 rounded-lg text-sm font-semibold transition-colors ${
              selected === tab.id
                ? 'bg-lab-700 text-white'
                : 'bg-white text-ink-soft hover:text-ink border border-line hover:border-lab-600/40'
            }`}
          >
            {TAB_LABELS[lang][tab.id]}
          </button>
        ))}
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {filtered.map((member) => (
          <article
            key={member.name}
            className="card card-hover overflow-hidden flex flex-col"
          >
            {/* Photo */}
            {member.avatar ? (
              <div className="aspect-[4/3] w-full overflow-hidden bg-paper">
                <img
                  src={member.avatar}
                  alt={`${member.name} (${member.nameKo})`}
                  loading="lazy"
                  className="w-full h-full object-cover object-[center_30%]"
                />
              </div>
            ) : (
              <div className="aspect-[4/3] w-full bg-paper flex items-center justify-center">
                <span className="font-display text-4xl text-line select-none" aria-hidden="true">
                  {member.name.split(' ').map((n) => n[0]).join('')}
                </span>
              </div>
            )}

            <div className="p-5 flex-1 flex flex-col gap-3.5">
              {/* Name & role */}
              <div>
                <div className="flex items-baseline gap-2 flex-wrap">
                  <h3
                    className="font-display text-lg font-semibold text-ink leading-tight"
                    lang={lang === 'ko' && member.nameKo ? 'ko' : 'en'}
                  >
                    {lang === 'ko' && member.nameKo ? member.nameKo : member.name}
                  </h3>
                  {/* The counterpart name is the other script, so it needs its own
                      lang — both for the Korean type rules and for screen readers. */}
                  <span className="text-sm text-ink-faint" lang={lang === 'ko' ? 'en' : 'ko'}>
                    {lang === 'ko' ? member.name : member.nameKo}
                  </span>
                </div>
                <p className="text-sm font-semibold text-lab-700 mt-0.5">
                  {lang === 'ko' && member.roleKo ? member.roleKo : member.role}
                </p>
                {member.affiliations.length > 0 && (
                  <p className="text-sm text-ink-faint mt-0.5">{member.affiliations[0]}</p>
                )}
              </div>

              {/* Education */}
              {member.education.length > 0 && (
                <div className="flex items-start gap-2 text-sm text-ink-soft">
                  <GraduationCap className="w-4 h-4 text-lab-700 shrink-0 mt-0.5" aria-hidden="true" />
                  <div className="space-y-0.5">
                    {member.education.map((edu, i) => (
                      <p key={i} className="leading-snug">{edu}</p>
                    ))}
                  </div>
                </div>
              )}

              {/* Research interests */}
              {member.researchInterests.length > 0 && (
                <div className="flex flex-wrap gap-1.5">
                  {member.researchInterests.map((interest, i) => (
                    <span key={i} className="chip">{interest}</span>
                  ))}
                </div>
              )}

              {/* Passions — the human side */}
              {member.passions.length > 0 && (
                <div className="flex items-start gap-2 text-sm text-ink-faint">
                  <Heart className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" aria-hidden="true" />
                  <p className="italic leading-snug">{member.passions.join(' · ')}</p>
                </div>
              )}

              {/* Contact & links */}
              <div className="pt-3 mt-auto border-t border-line flex items-center justify-between gap-2 text-sm">
                {member.email ? (
                  <a
                    href={`mailto:${member.email}`}
                    className="flex items-center gap-1.5 text-ink-soft hover:text-lab-700 transition-colors font-mono text-xs truncate"
                  >
                    <Mail className="w-3.5 h-3.5 text-lab-700 shrink-0" aria-hidden="true" />
                    <span className="truncate">{member.email}</span>
                  </a>
                ) : (
                  <span aria-hidden="true" />
                )}

                <div className="flex items-center gap-1.5 shrink-0">
                  {member.links?.scholar && (
                    <a
                      href={member.links.scholar}
                      target="_blank"
                      rel="noreferrer"
                      className="p-1.5 rounded-lg text-ink-faint hover:text-lab-700 hover:bg-paper transition-colors"
                      title="Google Scholar"
                    >
                      <BookOpen className="w-4 h-4" />
                    </a>
                  )}
                  {member.links?.github && (
                    <a
                      href={member.links.github}
                      target="_blank"
                      rel="noreferrer"
                      className="p-1.5 rounded-lg text-ink-faint hover:text-lab-700 hover:bg-paper transition-colors"
                      title="GitHub"
                    >
                      <Github className="w-4 h-4" />
                    </a>
                  )}
                  {member.links?.website && (
                    <a
                      href={member.links.website}
                      target="_blank"
                      rel="noreferrer"
                      className="p-1.5 rounded-lg text-ink-faint hover:text-lab-700 hover:bg-paper transition-colors"
                      title="Website"
                    >
                      <ExternalLink className="w-4 h-4" />
                    </a>
                  )}
                </div>
              </div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
