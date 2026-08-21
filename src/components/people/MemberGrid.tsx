import React, { useState } from 'react';
import { Mail, Sparkles, ExternalLink, Heart, Github, BookOpen } from 'lucide-react';

interface Member {
  name: string;
  nameKo: string;
  role: string;
  roleKo: string;
  category: 'pi' | 'phd' | 'ms' | 'undergrad' | 'alumni';
  email?: string;
  avatar?: string;
  affiliations: string[];
  education: string[];
  researchInterests: string[];
  passions: string[];
  links?: {
    scholar?: string;
    github?: string;
    linkedin?: string;
    website?: string;
  };
  order: number;
}

interface Props {
  members: Member[];
}

export default function MemberGrid({ members }: Props) {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const categories = [
    { id: 'all', label: 'All Members' },
    { id: 'pi', label: 'Principal Investigator' },
    { id: 'phd', label: 'Graduate Researchers' },
    { id: 'alumni', label: 'Alumni' },
  ];

  const filteredMembers = members.filter((m) => {
    if (selectedCategory === 'all') return true;
    if (selectedCategory === 'phd') return m.category === 'phd' || m.category === 'ms';
    return m.category === selectedCategory;
  });

  return (
    <div className="space-y-8">
      {/* Category Tabs */}
      <div className="flex flex-wrap justify-center gap-2">
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setSelectedCategory(cat.id)}
            className={`px-5 py-2.5 rounded-2xl text-xs font-semibold transition-all ${
              selectedCategory === cat.id
                ? 'bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-600 text-white shadow-lg shadow-cyan-500/25 scale-105'
                : 'bg-slate-900/80 text-slate-400 hover:text-slate-200 hover:bg-slate-800 border border-slate-800'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredMembers.map((member, idx) => (
          <div
            key={idx}
            className="rounded-3xl glass-panel glass-panel-hover p-6 border border-slate-800/80 flex flex-col justify-between group relative overflow-hidden"
          >
            {/* Ambient Background Gradient for PI & Spotlight Members */}
            {member.category === 'pi' && (
              <div className="absolute -top-24 -right-24 w-48 h-48 bg-cyan-500/15 rounded-full blur-3xl pointer-events-none" />
            )}

            <div>
              {/* Header: Avatar & Name */}
              <div className="flex items-start gap-4 mb-4">
                <div className="relative">
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-slate-800 to-slate-700 border border-slate-600 flex items-center justify-center text-cyan-300 font-bold text-xl overflow-hidden shadow-md">
                    {member.avatar ? (
                      <img src={member.avatar} alt={member.name} className="w-full h-full object-cover" />
                    ) : (
                      <span>{member.name.split(' ').map((n) => n[0]).join('')}</span>
                    )}
                  </div>
                  {member.category === 'pi' && (
                    <span className="absolute -bottom-1 -right-1 p-1 rounded-full bg-cyan-500 text-slate-950 text-[10px]" title="Lab PI">
                      <Sparkles className="w-3 h-3" />
                    </span>
                  )}
                </div>

                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-bold text-white group-hover:text-cyan-300 transition leading-tight">
                      {member.name}
                    </h3>
                    <span className="text-xs text-slate-400 font-medium">{member.nameKo}</span>
                  </div>
                  <p className="text-xs font-semibold text-cyan-400 mt-0.5">{member.role}</p>
                  <p className="text-[11px] text-slate-400 font-mono mt-0.5">{member.roleKo}</p>
                </div>
              </div>

              {/* Affiliations & Education */}
              <div className="space-y-1.5 mb-4 text-xs text-slate-300">
                {member.affiliations.map((aff, aIdx) => (
                  <div key={aIdx} className="flex items-center gap-1.5 text-slate-400">
                    <span className="text-cyan-400 text-xs">▹</span>
                    <span>{aff}</span>
                  </div>
                ))}
              </div>

              {/* Research Interests */}
              {member.researchInterests.length > 0 && (
                <div className="mb-4 p-3 rounded-2xl bg-slate-950/60 border border-slate-800/80">
                  <div className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                    Research Focus:
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {member.researchInterests.map((interest, iIdx) => (
                      <span
                        key={iIdx}
                        className="text-[10px] px-2 py-0.5 rounded-md bg-slate-900 text-slate-300 border border-slate-800"
                      >
                        {interest}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Passion & Lab Culture Badges */}
              {member.passions.length > 0 && (
                <div className="mb-4">
                  <div className="text-[10px] font-semibold uppercase tracking-wider text-slate-500 mb-1.5 flex items-center gap-1">
                    <Heart className="w-3 h-3 text-rose-400" />
                    <span>Passionate for:</span>
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {member.passions.map((passion, pIdx) => (
                      <span
                        key={pIdx}
                        className="text-[10px] px-2 py-0.5 rounded-full bg-slate-900/90 text-slate-300 border border-slate-800/80 italic"
                      >
                        {passion}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Footer Contact & Links */}
            <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              {member.email ? (
                <a
                  href={`mailto:${member.email}`}
                  className="flex items-center gap-1.5 text-slate-400 hover:text-cyan-300 font-mono text-[11px] transition"
                >
                  <Mail className="w-3.5 h-3.5 text-cyan-400" />
                  <span>{member.email}</span>
                </a>
              ) : (
                <span className="text-slate-600 text-[11px] font-mono">Connectome Lab</span>
              )}

              {/* External Profile Links */}
              <div className="flex items-center gap-2">
                {member.links?.scholar && (
                  <a
                    href={member.links.scholar}
                    target="_blank"
                    rel="noreferrer"
                    className="p-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition"
                    title="Google Scholar"
                  >
                    <BookOpen className="w-3.5 h-3.5" />
                  </a>
                )}
                {member.links?.github && (
                  <a
                    href={member.links.github}
                    target="_blank"
                    rel="noreferrer"
                    className="p-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition"
                    title="GitHub"
                  >
                    <Github className="w-3.5 h-3.5" />
                  </a>
                )}
                {member.links?.website && (
                  <a
                    href={member.links.website}
                    target="_blank"
                    rel="noreferrer"
                    className="p-1.5 rounded-lg bg-slate-900 text-slate-400 hover:text-white border border-slate-800 transition"
                    title="Website / Notion"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
