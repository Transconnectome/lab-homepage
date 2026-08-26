import { defineCollection, z } from 'astro:content';

const membersCollection = defineCollection({
  type: 'data',
  schema: z.object({
    name: z.string(),
    nameKo: z.string(),
    role: z.string(),
    roleKo: z.string(),
    category: z.enum(['pi', 'phd', 'ms', 'undergrad', 'staff', 'alumni']),
    email: z.string().nullable().optional(),
    avatar: z.string().nullable().optional(),
    affiliations: z.array(z.string()).default([]),
    education: z.array(z.string()).default([]),
    researchInterests: z.array(z.string()).default([]),
    passions: z.array(z.string()).default([]),
    links: z.object({
      scholar: z.string().nullable().optional(),
      github: z.string().nullable().optional(),
      linkedin: z.string().nullable().optional(),
      website: z.string().nullable().optional(),
    }).nullable().optional(),
    order: z.number().default(99),
  }),
});

const researchCollection = defineCollection({
  type: 'content',
  schema: z.object({
    lang: z.enum(['en', 'ko']).default('en'),
    baseSlug: z.string().nullable().optional(),
    title: z.string(),
    titleKo: z.string(),
    tagline: z.string(),
    category: z.enum(['foundation-models', 'connectomics', 'genetics', 'qml', 'art-science']),
    heroImage: z.string().nullable().optional(),
    featured: z.boolean().default(false),
    order: z.number().default(99),
    keyHighlights: z.array(z.string()).default([]),
  }),
});

const newsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    lang: z.enum(['en', 'ko']).default('en'),
    baseSlug: z.string().nullable().optional(),
    title: z.string(),
    titleKo: z.string().nullable().optional(),
    date: z.string(),
    category: z.enum(['award', 'paper', 'conference', 'event', 'exhibition', 'general']),
    featured: z.boolean().default(false),
    link: z.string().nullable().optional(),
    image: z.string().nullable().optional(),
  }),
});

// Publication filter taxonomy — one shared level of granularity (research domain).
// Modalities (fMRI, EEG), architectures (Mamba, geometric DL) and sub-fields (MDD,
// polygenic risk) are folded into the domain they belong to, so no filter chip ends up
// matching a single paper. Keep in sync with derive_tags() in scripts/sync_scholar.py.
export const PUBLICATION_TAGS = [
  'AI & Foundation Models',
  'Genetics',
  'Neuroimaging',
  'Neuroscience',
  'Psychiatry',
  'Quantum ML',
] as const;

const publicationsCollection = defineCollection({
  type: 'data',
  schema: z.object({
    title: z.string(),
    authors: z.array(z.string()),
    venue: z.string(),
    year: z.number(),
    month: z.string().nullable().optional(),
    doi: z.string().nullable().optional(),
    url: z.string().nullable().optional(),
    pdfUrl: z.string().nullable().optional(),
    codeUrl: z.string().nullable().optional(),
    tags: z.array(z.enum(PUBLICATION_TAGS)).default([]),
    featured: z.boolean().default(false),
    spotlight: z.string().nullable().optional(),
    abstract: z.string().nullable().optional(),
    labMembers: z.array(z.string()).default([]),
    kind: z.enum(['journal', 'conference', 'workshop', 'preprint']).default('journal'),
  }),
});

const trendsCollection = defineCollection({
  type: 'data',
  schema: z.object({
    title: z.string(),
    authors: z.array(z.string()),
    publishedDate: z.string(),
    source: z.string(),
    topic: z.enum(['Brain Foundation Models', 'fMRI/EEG Dynamics', 'Genomics & Connectomics', 'Quantum ML', 'Brain-LLM Alignment']),
    url: z.string(),
    summaryPoints: z.array(z.string()),
    significance: z.string(),
    labRelevance: z.string(),
    modality: z.array(z.string()).default([]),
    badge: z.string().nullable().optional(),
    generatedBy: z.string().nullable().optional(),
  }),
});

const historyCollection = defineCollection({
  type: 'content',
  schema: z.object({
    lang: z.enum(['en', 'ko']).default('en'),
    baseSlug: z.string().nullable().optional(),
    period: z.string(),
    year: z.number(),
    title: z.string(),
    category: z.enum(['internship', 'hackathon', 'workshop', 'graduation', 'general']),
    order: z.number().default(99),
  }),
});

const ideasCollection = defineCollection({
  type: 'data',
  schema: z.object({
    title: z.string(),
    titleKo: z.string().nullable().optional(),
    date: z.string(),
    // Same taxonomy as the research collection's pillars, so ideas can be
    // browsed by the same categories visitors already see on /research.
    category: z.enum(['foundation-models', 'connectomics', 'genetics', 'qml', 'art-science']),
    hypothesis: z.string(),
    hypothesisKo: z.string().nullable().optional(),
    rationale: z.string(),
    rationaleKo: z.string().nullable().optional(),
    labThreads: z.array(z.string()).default([]),
    externalInspiration: z.array(z.string()).default([]),
    firstExperiment: z.string(),
    firstExperimentKo: z.string().nullable().optional(),
    risks: z.string(),
    risksKo: z.string().nullable().optional(),
    generatedBy: z.string(),
    image: z.string().nullable().optional(), // /assets/ideas/<slug>.png, rendered by scripts/generate_idea_infographics.py
    imageGeneratedBy: z.string().nullable().optional(),
  }),
});

const projectsCollection = defineCollection({
  type: 'data',
  schema: z.object({
    // Curated fields — hand-maintained; scripts/sync_project_metadata.py never writes these.
    name: z.string(),
    repo: z.string(), // "owner/name" — the sync key; the set of files on disk IS the allowlist
    blurb: z.string(),
    blurbKo: z.string().nullable().optional(),
    // Hub ids of the research-map networks (mirrors the BrainViewer hub ids).
    network: z.enum(['dmn', 'ecn', 'salience', 'sensory', 'subcortical', 'eeg-mesh']),
    publicationSlug: z.string().nullable().optional(), // publications entry id (filename minus .json)
    highlight: z.string().nullable().optional(), // e.g. "NeurIPS 2023"
    featured: z.boolean().default(false),
    order: z.number().default(99),
    generatedBy: z.string().nullable().optional(), // provenance when the blurb is LLM-drafted
    // Synced fields — machine-owned, refreshed weekly from the GitHub API.
    repoUrl: z.string(),
    stars: z.number().nullable().optional(),
    primaryLanguage: z.string().nullable().optional(),
    lastPush: z.string().nullable().optional(),
    archived: z.boolean().default(false),
  }),
});

export const collections = {
  members: membersCollection,
  research: researchCollection,
  news: newsCollection,
  publications: publicationsCollection,
  trends: trendsCollection,
  history: historyCollection,
  ideas: ideasCollection,
  projects: projectsCollection,
};
