import React, { useState } from 'react';
import { affiliationLabel } from '../../i18n/ui';

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
  researchExperience: string[];
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

const CATEGORY_LABELS: Record<'en' | 'ko', Record<string, string>> = {
  en: { all: 'Everyone', pi: 'Principal Investigator', grad: 'Graduate Students', undergrad: 'Interns', staff: 'Staff', alumni: 'Alumni' },
  ko: { all: '전체', pi: '지도교수', grad: '대학원생', undergrad: '학부 인턴', staff: '스태프', alumni: '동문' },
};

const LABELS = {
  en: { category: 'Browse people', education: 'Education', research: 'Research interests', passions: 'Outside the lab', website: 'Website', email: 'Email', people: 'people' },
  ko: { category: '구성원 구분', education: '학력', research: '연구 관심사', passions: '관심과 취미', website: '웹사이트', email: '이메일', people: '명' },
};

const CATEGORIES: { id: string; match: (category: Member['category']) => boolean }[] = [
  { id: 'all', match: () => true },
  { id: 'pi', match: (category) => category === 'pi' },
  { id: 'grad', match: (category) => category === 'phd' || category === 'ms' },
  { id: 'undergrad', match: (category) => category === 'undergrad' },
  { id: 'staff', match: (category) => category === 'staff' },
  { id: 'alumni', match: (category) => category === 'alumni' },
];

// Shared by the profile article and links from the homepage's photo strip.
export const memberAnchor = (name: string) => `member-${name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')}`;
const textLang = (text: string) => /[\uac00-\ud7a3]/.test(text) ? 'ko' : 'en';

export default function MemberGrid({ members, lang = 'en' }: Props) {
  const [selected, setSelected] = useState('all');
  const L = LABELS[lang];
  const categories = CATEGORIES.filter((category) => category.id === 'all' || members.some((member) => category.match(member.category)));
  const activeCategory = categories.find((category) => category.id === selected) ?? categories[0];
  const filtered = members.filter((member) => activeCategory.match(member.category));

  return (
    <div className="space-y-10">
      <div className="border-y border-line py-5 flex flex-wrap items-end justify-between gap-4">
        <div className="space-y-2 w-full sm:w-auto">
          <label htmlFor="member-category" className="block text-sm font-medium text-ink">{L.category}</label>
          <select
            id="member-category"
            value={selected}
            onChange={(event) => setSelected(event.target.value)}
            className="form-field sm:w-64 py-2.5 focus:border-lab-700"
          >
            {categories.map((category) => <option key={category.id} value={category.id}>{CATEGORY_LABELS[lang][category.id]}</option>)}
          </select>
        </div>
        <p role="status" className="text-sm text-ink-faint">{filtered.length} {L.people}</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12">
        {filtered.map((member) => {
          const anchor = memberAnchor(member.name);
          return (
            <article key={member.name} id={anchor} aria-labelledby={`${anchor}-name`} className="min-w-0 border-t border-line pt-5 scroll-mt-24 flex flex-col gap-5">
              {member.avatar && (
                <div className="aspect-[4/3] w-full overflow-hidden">
                  <img
                    src={member.avatar}
                    alt={member.nameKo ? `${member.name} (${member.nameKo})` : member.name}
                    loading="lazy"
                    className="w-full h-full object-cover object-[center_30%]"
                  />
                </div>
              )}

              <div className="space-y-1.5">
                <h2 id={`${anchor}-name`} className="font-display text-xl font-semibold text-ink leading-snug" lang={lang === 'ko' && member.nameKo ? 'ko' : 'en'}>
                  {lang === 'ko' && member.nameKo ? member.nameKo : member.name}
                </h2>
                {member.nameKo && (
                  <p className="text-sm text-ink-faint" lang={lang === 'ko' ? 'en' : 'ko'}>
                    {lang === 'ko' ? member.name : member.nameKo}
                  </p>
                )}
                <p className="text-sm font-medium text-ink-soft">{lang === 'ko' && member.roleKo ? member.roleKo : member.role}</p>
                {member.affiliations.length > 0 && (
                  <p className="text-sm text-ink-soft leading-relaxed">{member.affiliations.map((affiliation) => affiliationLabel(lang, affiliation)).join(' · ')}</p>
                )}
              </div>

              {(member.education.length > 0 || member.researchExperience.length > 0 || member.researchInterests.length > 0 || member.passions.length > 0) && (
                <dl className="space-y-4 text-sm text-ink-soft">
                  {member.education.length > 0 && (
                    <div className="space-y-1">
                      <dt className="text-xs font-medium text-ink-faint">{L.education}</dt>
                      <dd className="space-y-1">
                        {member.education.map((education, index) => <p key={index} className="leading-relaxed" lang={textLang(education)}>{education}</p>)}
                      </dd>
                    </div>
                  )}
                  {member.researchInterests.length > 0 && (
                    <div className="space-y-1">
                      <dt className="text-xs font-medium text-ink-faint">{L.research}</dt>
                      <dd className="leading-relaxed">
                        {member.researchInterests.map((interest, index) => (
                          <React.Fragment key={index}>
                            <span lang={textLang(interest)}>{interest}</span>{index < member.researchInterests.length - 1 ? ' · ' : ''}
                          </React.Fragment>
                        ))}
                      </dd>
                    </div>
                  )}
                  {member.researchExperience.length > 0 && (
                    <div className="space-y-1">
                      <dt className="text-xs font-medium text-ink-faint">{lang === 'ko' ? '연구 활동과 경력' : 'Research experience and activities'}</dt>
                      <dd className="space-y-1">
                        {member.researchExperience.map((experience, index) => <p key={index} className="leading-relaxed" lang={textLang(experience)}>{experience}</p>)}
                      </dd>
                    </div>
                  )}
                  {member.passions.length > 0 && (
                    <div className="space-y-1">
                      <dt className="text-xs font-medium text-ink-faint">{L.passions}</dt>
                      <dd className="leading-relaxed">
                        {member.passions.map((passion, index) => (
                          <React.Fragment key={index}>
                            <span lang={textLang(passion)}>{passion}</span>{index < member.passions.length - 1 ? ' · ' : ''}
                          </React.Fragment>
                        ))}
                      </dd>
                    </div>
                  )}
                </dl>
              )}

              {(member.email || member.links?.scholar || member.links?.github || member.links?.linkedin || member.links?.website) && (
                <div className="mt-auto pt-1 space-y-3 text-sm">
                  {member.email && (
                    <a href={`mailto:${member.email}`} className="text-link break-all" aria-label={`${L.email}: ${member.name}`}>
                      {member.email}
                    </a>
                  )}
                  <div className="flex flex-wrap gap-x-4 gap-y-2">
                    {member.links?.scholar && <a href={member.links.scholar} target="_blank" rel="noreferrer" className="text-link">Google Scholar</a>}
                    {member.links?.github && <a href={member.links.github} target="_blank" rel="noreferrer" className="text-link">GitHub</a>}
                    {member.links?.linkedin && <a href={member.links.linkedin} target="_blank" rel="noreferrer" className="text-link">LinkedIn</a>}
                    {member.links?.website && <a href={member.links.website} target="_blank" rel="noreferrer" className="text-link">{L.website}</a>}
                  </div>
                </div>
              )}
            </article>
          );
        })}
      </div>
    </div>
  );
}
