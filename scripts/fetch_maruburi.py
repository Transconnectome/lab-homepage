#!/usr/bin/env python3
"""Fetch Naver MaruBuri SemiBold plus its licence, subset to Hangul, and write
both into public/fonts/maruburi/ (HANDOFF 5.3).

Runs on the Actions runner (the dev container has no egress). Font comes from
the official hangeul.pstatic.net CDN (URL parsed out of Naver's own webfont
CSS). The licence text comes, in order of preference, from the font's own
name table (ID 13 licence text / ID 0 copyright / ID 14 URL — Naver embeds
these), else from a GitHub mirror with provenance logged. Refuses to finish
without a licence text — MaruBuri is under Naver's font licence (not OFL):
self-hosting and subsetting are permitted only with the copyright notice and
licence text shipped alongside.
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
import zipfile

OUT = 'public/fonts/maruburi'
UA = {'User-Agent': 'Mozilla/5.0 (lab-homepage font tooling; contact: repo Transconnectome/lab-homepage)'}


def get(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def try_get(url):
    try:
        b = get(url)
        print(f'OK  {url} ({len(b)} bytes)', flush=True)
        return b
    except Exception as e:
        print(f'--  {url}: {e}', flush=True)
        return None


font = None
font_src = None

# 1) Official webfont CSS names the real font URLs.
for css_url in (
    'https://hangeul.pstatic.net/hangeul_static/css/maru-buri.css',
    'https://hangeul.pstatic.net/hangeul_static/css/MaruBuri.css',
):
    css = try_get(css_url)
    if not css:
        continue
    urls = re.findall(r'url\(["\']?(https?://[^"\')]+)["\']?\)', css.decode('utf-8', 'replace'))
    for ext in ('.ttf', '.otf', '.woff2'):
        cands = [u for u in urls if 'semibold' in u.lower() and u.lower().endswith(ext)]
        if cands:
            font = try_get(cands[0])
            if font:
                font_src = cands[0]
                break
    if font:
        break

if font is None:
    for url in (
        'https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-SemiBold.ttf',
        'https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri/MaruBuri-SemiBold.woff2',
    ):
        font = try_get(url)
        if font:
            font_src = url
            break

if font is None:
    sys.exit('FATAL: no MaruBuri SemiBold obtained from any source.')

print(f'font: {font_src} ({len(font)} bytes, sha256 {hashlib.sha256(font).hexdigest()})', flush=True)
src_path = '/tmp/maruburi-semibold.src'
with open(src_path, 'wb') as f:
    f.write(font)

# 2) Licence: prefer the font's own name table — Naver embeds the notice.
from fontTools.ttLib import TTFont  # noqa: E402  (after pip install in CI)

lic_text = None
lic_src = None
tt = TTFont(src_path, fontNumber=0, lazy=True)
names = {}
for rec in tt['name'].names:
    if rec.nameID in (0, 13, 14) and rec.nameID not in names:
        try:
            names[rec.nameID] = rec.toUnicode()
        except Exception:
            pass
print('name table: copyright=%r' % names.get(0, '')[:120], flush=True)
print('name table: licence text length=%d, url=%r' % (len(names.get(13, '')), names.get(14, '')), flush=True)
if len(names.get(13, '')) >= 200:
    parts = []
    if names.get(0):
        parts.append(names[0].strip())
    parts.append(names[13].strip())
    if names.get(14):
        parts.append('Licence URL: ' + names[14].strip())
    lic_text = '\n\n'.join(parts) + '\n'
    lic_src = f'embedded in the font file (name table IDs 0/13/14) — {font_src}'

# 3) Fallback: licence file from a GitHub mirror, loudly logged.
if lic_text is None:
    print('No usable embedded licence; falling back to GitHub mirror search...', flush=True)
    try:
        res = subprocess.run(['gh', 'api', 'search/repositories?q=maruburi&per_page=5'],
                             capture_output=True, text=True, check=True)
        items = json.loads(res.stdout).get('items', [])
        print('mirrors:', [i['full_name'] for i in items], flush=True)
        for it in items:
            full, branch = it['full_name'], it.get('default_branch') or 'main'
            tree = subprocess.run(['gh', 'api', f'repos/{full}/git/trees/{branch}?recursive=1'],
                                  capture_output=True, text=True)
            if tree.returncode != 0:
                print(f'  {full}: tree fetch failed: {tree.stderr[:200]}', flush=True)
                continue
            paths = [e['path'] for e in json.loads(tree.stdout).get('tree', []) if e.get('type') == 'blob']
            cands = sorted((p for p in paths if re.search(r'license|licence|ofl', p, re.I)), key=len)
            print(f'  {full}: licence candidates: {cands[:5]}', flush=True)
            for p in cands:
                b = try_get(f'https://raw.githubusercontent.com/{full}/{branch}/{urllib.parse.quote(p)}')
                if b and len(b) >= 200:
                    lic_text = b.decode('utf-8', 'replace')
                    lic_src = f'https://github.com/{full} :: {p} (mirror — verify against official text)'
                    break
            if lic_text:
                break
    except Exception as e:
        print(f'mirror search failed: {e}', flush=True)

if lic_text is None:
    sys.exit('FATAL: font obtained but no licence text; refusing to self-host without it.')

print(f'licence source: {lic_src}', flush=True)
print('--- licence text ---', flush=True)
print(lic_text[:2000], flush=True)

os.makedirs(OUT, exist_ok=True)
with open(f'{OUT}/LICENSE.txt', 'w', encoding='utf-8') as f:
    f.write(lic_text)

# 4) Subset: KS X 1001 syllables (the EUC-KR encodable 2,350) + Jamo + Compat
# Jamo. A rare out-of-set syllable falls through to the next family in the
# display stack (Hahmlet's Hangul), never to a system face.
def euc(c):
    try:
        chr(c).encode('euc_kr')
        return True
    except Exception:
        return False


cps = [c for c in range(0xAC00, 0xD7A4) if euc(c)]
cps += list(range(0x1100, 0x1200)) + list(range(0x3130, 0x3190))
runs, start, prev = [], cps[0], cps[0]
for c in cps[1:]:
    if c != prev + 1:
        runs.append((start, prev))
        start = c
    prev = c
runs.append((start, prev))
ranges = ','.join(f'U+{a:04X}-{b:04X}' if a != b else f'U+{a:04X}' for a, b in runs)
print(f'subsetting to {len(cps)} codepoints in {len(runs)} ranges', flush=True)

from fontTools import subset  # noqa: E402
out_font = f'{OUT}/MaruBuri-SemiBold.hangul.woff2'
subset.main([src_path, f'--unicodes={ranges}', '--flavor=woff2',
             '--layout-features=*', f'--output-file={out_font}'])

size = os.path.getsize(out_font)
sha = hashlib.sha256(open(out_font, 'rb').read()).hexdigest()
print(f'subset: {out_font} ({size} bytes, sha256 {sha})', flush=True)

with open(f'{OUT}/PROVENANCE.txt', 'w', encoding='utf-8') as f:
    f.write(
        'MaruBuri SemiBold — provenance\n'
        f'font source   : {font_src}\n'
        f'font sha256   : {hashlib.sha256(font).hexdigest()}\n'
        f'licence source: {lic_src}\n'
        f'subset        : Hangul only (KS X 1001 syllables + Jamo U+1100-11FF + Compat Jamo U+3130-318F)\n'
        f'subset sha256 : {sha}\n'
        'tool          : fonttools subset, --flavor=woff2 --layout-features=*\n'
        'licence       : see LICENSE.txt in this directory (ships with the font per Naver font licence)\n')
print('done', flush=True)
