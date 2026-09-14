export interface EditorialCorrection {
  date: string;
  note: string;
  noteKo: string;
}

export default function EditorialNote({ correction, lang }: {
  correction?: EditorialCorrection;
  lang: 'en' | 'ko';
}) {
  if (!correction) return null;
  return (
    <p className="text-xs text-ink-soft leading-relaxed" data-editorial-note>
      {lang === 'ko' ? '내용 교정' : 'Content correction'} · <time dateTime={correction.date}>{correction.date}</time>
      {' — '}{lang === 'ko' ? correction.noteKo : correction.note}
    </p>
  );
}
