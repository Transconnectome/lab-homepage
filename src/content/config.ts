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
    title: z.string(),
    titleKo: z.string().nullable().optional(),
    date: z.string(),
    category: z.enum(['award', 'paper', 'conference', 'event', 'exhibition', 'general']),
    featured: z.boolean().default(false),
    link: z.string().nullable().optional(),
    image: z.string().nullable().optional(),
  }),
});

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
    tags: z.array(z.string()).default([]),
    featured: z.boolean().default(false),
    spotlight: z.string().nullable().optional(),
    abstract: z.string().nullable().optional(),
    labMembers: z.array(z.string()).default([]),
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
    hypothesis: z.string(),
    rationale: z.string(),
    labThreads: z.array(z.string()).default([]),
    externalInspiration: z.array(z.string()).default([]),
    firstExperiment: z.string(),
    risks: z.string(),
    generatedBy: z.string(),
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
};
