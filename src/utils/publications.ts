/**
 * CS/AI venue classification for the publications list.
 *
 * The lab publishes into two very different worlds: clinical and neuroscience
 * journals, and computer-science conferences where the proceedings paper *is*
 * the archival publication. Visitors coming from the CS/AI side want that
 * second set on its own, so /publications offers a "CS/AI conference" view.
 *
 * A record counts as a CS/AI conference paper when it is a conference or
 * workshop publication AND its venue (or, failing that, its topic tags) points
 * at a computing venue. Records are written by scripts/sync_scholar.py, which
 * knows nothing about this split, so the classification is derived here rather
 * than stored — with `csAiVenue` in the JSON record as a manual override for
 * the cases the heuristics get wrong.
 */

export interface VenueClassifiable {
  venue: string;
  tags?: string[];
  kind?: 'journal' | 'conference' | 'workshop' | 'preprint';
  csAiVenue?: boolean | null;
}

/** Venue-name fragments that mark a proceedings volume as a computing venue. */
const CS_AI_VENUE_PATTERNS: RegExp[] = [
  // Machine learning / AI flagships, by acronym and by spelled-out name.
  /\bneurips\b|neural information processing systems/,
  /\bicml\b|international conference on machine learning/,
  /\biclr\b|learning representations/,
  /\baaai\b|\bijcai\b|\baistats\b|\buai\b|\bcolt\b/,
  /machine learning|artificial intelligence|computational intelligence|deep learning/,
  // Vision, speech, language, signal processing.
  /\bcvpr\b|\biccv\b|\beccv\b|\bwacv\b|computer vision|pattern recognition/,
  /\bicassp\b|\bicip\b|\binterspeech\b|acoustics, speech|signal processing|image processing/,
  /\bacl\b|\bemnlp\b|\bnaacl\b|\bcoling\b|computational linguistics|language processing/,
  // Medical imaging / health informatics proceedings (MICCAI, IPMI, ISBI, SPIE).
  /\bmiccai\b|\bipmi\b|\bisbi\b|medical image computing|biomedical imaging|medical imaging/,
  /informatics|knowledge discovery|\bkdd\b|\bsigir\b|\bwww\b/,
  // Quantum computing venues (QCE, QAI, QCNC) and their spelled-out names.
  /\bqce\b|\bqai\b|\bqcnc\b|quantum computing|quantum artificial intelligence|quantum communications/,
  // Human-computer interaction, multimedia, robotics, graphics.
  /\bchi\b|\bicmi\b|\bicra\b|\biros\b|siggraph|multimedia|human-computer|robotics/,
  // Catch-alls: Springer's CS series and anything that names itself computing.
  /lecture notes in computer science|computer science|\bcomputing\b|computational|\bcomputer\b|data summit/,
];

/** Topic tags that stand in for the venue name when the venue is opaque. */
const CS_AI_TAGS = new Set([
  'AI & Foundation Models',
  'Quantum ML',
  'Foundation Model',
  'Machine Learning',
  'Deep Learning',
  'Geometric Deep Learning',
  'Equivariance',
  'State-Space Models',
  'Mamba',
  'NLP',
  'Brain-LLM Alignment',
]);

/** True for peer-reviewed conference and workshop papers at computing venues. */
export function isCsAiConference(pub: VenueClassifiable): boolean {
  if (typeof pub.csAiVenue === 'boolean') return pub.csAiVenue;
  const kind = pub.kind ?? 'journal';
  if (kind !== 'conference' && kind !== 'workshop') return false;
  const venue = (pub.venue || '').toLowerCase();
  if (CS_AI_VENUE_PATTERNS.some((re) => re.test(venue))) return true;
  return (pub.tags ?? []).some((tag) => CS_AI_TAGS.has(tag));
}
