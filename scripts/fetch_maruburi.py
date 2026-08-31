#!/usr/bin/env python3
"""Fetch Naver MaruBuri SemiBold (unmodified) plus licence evidence, and write
font + LICENSE.txt + PROVENANCE.txt into public/fonts/maruburi/ (HANDOFF 5.3).

Runs on the Actions runner (the dev container has no egress).

Why unmodified: the TTF's name table carries the copyright notice but no
licence text, and no authoritative standalone licence file was found on the
official CDN. Rather than subset under licence uncertainty, we redistribute
Naver's official woff2 byte-for-byte — permitted with attribution under every
candidate licence (Naver font licence and OFL alike; OFL's Reserved Font Name
clause applies only to modified fonts). The Hangul-only scoping happens in
our CSS @font-face unicode-range, which does not modify the font.

Licence determination, best evidence first:
  1. Google Fonts hosting (css2 returns 200 for the family) → proves OFL 1.1,
     in which case the canonical OFL text is included in LICENSE.txt.
  2. Mirror metadata (fonts-archive package.json licence field, READMEs).
  3. Official hangeul.naver.com pages.
All evidence and hashes land in PROVENANCE.txt.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

OUT = 'public/fonts/maruburi'
UA = {'User-Agent': 'Mozilla/5.0 (lab-homepage font tooling; contact: repo Transconnectome/lab-homepage)'}


def get(url, timeout=40, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def try_get(url, headers=None):
    try:
        b = get(url, headers=headers)
        print(f'OK  {url} ({len(b)} bytes)', flush=True)
        return b
    except Exception as e:
        print(f'--  {url}: {e}', flush=True)
        return None


evidence = []

# --- font: official woff2, byte-for-byte ---
font = None
font_src = None
for url in (
    'https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-SemiBold.woff2',
    'https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-SemiBold.woff',
):
    font = try_get(url)
    if font:
        font_src = url
        break
if font is None:
    sys.exit('FATAL: official MaruBuri SemiBold webfont not reachable.')
font_sha = hashlib.sha256(font).hexdigest()
print(f'font: {font_src} ({len(font)} bytes, sha256 {font_sha})', flush=True)

# copyright notice from the TTF's name table (the woff2 name table works too,
# but the TTF is already known to carry ID 0)
copyright_notice = '© NAVER Corp. © NAVER Cultural Foundation Corp.'
ttf = try_get('https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-SemiBold.ttf')
if ttf:
    with open('/tmp/maruburi.ttf', 'wb') as f:
        f.write(ttf)
    try:
        from fontTools.ttLib import TTFont
        tt = TTFont('/tmp/maruburi.ttf', lazy=True)
        for rec in tt['name'].names:
            if rec.nameID == 0:
                copyright_notice = rec.toUnicode()
                break
    except Exception as e:
        print(f'name table read failed, using known notice: {e}', flush=True)
print(f'copyright: {copyright_notice}', flush=True)

# --- licence evidence ---
ofl_confirmed = False

# 1) Google Fonts only hosts OFL faces; a 200 for the family proves OFL.
gf = try_get('https://fonts.googleapis.com/css2?family=MaruBuri:wght@600&display=swap')
if gf and b'@font-face' in gf:
    ofl_confirmed = True
    evidence.append('Google Fonts serves family "MaruBuri" (css2 HTTP 200 with @font-face) — Google Fonts hosts OFL-licensed faces only.')

# 2) fonts-archive mirror metadata (their packages state the licence).
for meta_url in (
    'https://raw.githubusercontent.com/fonts-archive/MaruBuri/main/package.json',
    'https://raw.githubusercontent.com/fonts-archive/MaruBuri/master/package.json',
):
    b = try_get(meta_url)
    if b:
        try:
            pkg = json.loads(b)
            lic = pkg.get('license') or pkg.get('licence')
            if lic:
                evidence.append(f'fonts-archive/MaruBuri package.json license field: {lic!r}')
                if 'ofl' in str(lic).lower() or 'open font license' in str(lic).lower():
                    ofl_confirmed = True
        except Exception:
            pass
        break
for readme_url in (
    'https://raw.githubusercontent.com/fonts-archive/MaruBuri/main/README.md',
    'https://raw.githubusercontent.com/wefonts/maruBuri/main/README.md',
):
    b = try_get(readme_url)
    if b:
        text = b.decode('utf-8', 'replace')
        for line in text.splitlines():
            if re.search(r'ofl|open font license|라이선스|license', line, re.I):
                evidence.append(f'{readme_url.split("/")[3]}/{readme_url.split("/")[4]} README: {line.strip()[:200]}')
                if re.search(r'\bofl\b|open font license', line, re.I):
                    ofl_confirmed = True
        if len(evidence) > 12:
            evidence = evidence[:12]

# 3) Official pages (may be JS-rendered; grep whatever HTML we get).
for page in ('https://hangeul.naver.com/maru', 'https://hangeul.naver.com/font'):
    b = try_get(page)
    if b:
        text = b.decode('utf-8', 'replace')
        hits = [m.strip()[:200] for m in re.findall(r'[^\n<>]*(?:OFL|Open Font License|폰트 라이선스)[^\n<>]*', text)][:3]
        for h in hits:
            evidence.append(f'{page}: {h}')
            if re.search(r'\bofl\b|open font license', h, re.I):
                ofl_confirmed = True

print('licence evidence:', flush=True)
for e in evidence:
    print(f'  - {e}', flush=True)
print(f'OFL confirmed: {ofl_confirmed}', flush=True)

ofl_text = None
if ofl_confirmed:
    for u in (
        'https://openfontlicense.org/documents/OFL.txt',
        'https://raw.githubusercontent.com/googlefonts/opensource/main/OFL.txt',
    ):
        b = try_get(u)
        if b and b'SIL OPEN FONT LICENSE' in b.upper():
            ofl_text = b.decode('utf-8', 'replace')
            break

if not evidence:
    sys.exit('FATAL: no licence evidence gathered; refusing to self-host blind.')

# --- write outputs ---
os.makedirs(OUT, exist_ok=True)
with open(f'{OUT}/MaruBuri-SemiBold.woff2', 'wb') as f:
    f.write(font)

lines = [
    'MaruBuri (마루 부리) SemiBold — redistributed unmodified with attribution.',
    '',
    f'Copyright notice (from the font\'s own name table): {copyright_notice}',
    '',
    'Source: Naver 한글한글 아름답게 / hangeul.naver.com — official webfont CDN',
    f'  {font_src}',
    '',
    'Licence evidence gathered at fetch time:',
]
lines += [f'  - {e}' for e in evidence]
if ofl_text:
    lines += ['', 'The face is licensed under the SIL Open Font License 1.1; full text follows.', '', ofl_text]
else:
    lines += ['', 'See hangeul.naver.com for the governing licence terms. The font file is', 'redistributed byte-for-byte unmodified with the copyright notice above.']
with open(f'{OUT}/LICENSE.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

with open(f'{OUT}/PROVENANCE.txt', 'w', encoding='utf-8') as f:
    f.write(
        'MaruBuri SemiBold — provenance\n'
        f'font source : {font_src}\n'
        f'font sha256 : {font_sha}\n'
        f'font bytes  : {len(font)}\n'
        'modification: NONE — redistributed byte-for-byte; Hangul-only scoping is done\n'
        '              by the CSS @font-face unicode-range, not by editing the font\n'
        f'ofl_confirmed_at_fetch: {ofl_confirmed}\n'
        'note        : if subsetting is ever wanted, re-check the licence first — OFL\n'
        '              Reserved Font Names forbid keeping the name on modified fonts\n')
print('done', flush=True)
