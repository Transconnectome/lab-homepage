/**
 * Inline markdown links for content fields that are plain strings.
 *
 * `keyHighlights` on the research collection is a `string[]`, not a markdown
 * body, so Astro prints it as text — a `[label](url)` written there would show
 * up verbatim. The research page wants the paper behind each key direction to
 * be clickable the same way the papers in the prose body are, so those bullets
 * go through here instead: the string is HTML-escaped first, then the one
 * markdown construct the field needs, the inline link, is turned back into an
 * anchor.
 *
 * Escaping runs before any anchor is emitted, so nothing an author writes in a
 * content file can inject markup through the `set:html` on the other side.
 */

const HTML_ESCAPES: Record<string, string> = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
};

const escapeHtml = (value: string): string => value.replace(/[&<>"']/g, (c) => HTML_ESCAPES[c]);

/** `[label](target)` — absolute http(s) URLs and site-relative paths only. */
const INLINE_LINK = /\[([^\]]+)\]\((https?:\/\/[^\s)]+|\/[^\s)]*)\)/g;

/** Anchors are outside `prose`, so they carry their own link styling. */
const LINK_CLASS = 'text-lab-700 underline underline-offset-2 decoration-line hover:text-lab-900';

export function renderInlineLinks(text: string): string {
  return escapeHtml(text).replace(
    INLINE_LINK,
    (_match, label: string, href: string) => `<a href="${href}" class="${LINK_CLASS}">${label}</a>`
  );
}
