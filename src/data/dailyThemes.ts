/** Select a reviewed research entry by KST calendar day. Copy lives in the research collection. */
export function getTodayThemeIndex(count: number, now: Date = new Date()): number {
  if (!Number.isInteger(count) || count < 1) return 0;
  const day = Math.floor((now.getTime() + 9 * 60 * 60 * 1000) / 86400000);
  return ((day % count) + count) % count;
}
