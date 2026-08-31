#!/usr/bin/env python3
"""Fetch Naver MaruBuri SemiBold plus its licence, subset to Hangul, and write
both into public/fonts/maruburi/ (HANDOFF 5.3).

Runs on the Actions runner (the dev container has no egress). Sources are
tried in order of authority: the official hangeul.pstatic.net webfont CSS and
download zips first, then direct path guesses, and only as a logged last
resort a GitHub mirror. Refuses to finish without a licence text — MaruBuri
is under Naver's font licence (not OFL): self-hosting and subsetting are
permitted only with the copyright notice and full licence text alongside.
"""
import hashlib
import io
import json
import os
import re
import subprocess
import sys
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
        print(f'OK  {url} ({len(b)} bytes)')
        return b
    except Exception as e:
        print(f'--  {url}: {e}')
        return None


font = lic = None
font_src = lic_src = None

# 1) Official webfont CSS names the real font URLs.
for css_url in (
    'https://hangeul.pstatic.net/hangeul_static/css/maru-buri.css',
    'https://hangeul.pstatic.net/hangeul_static/css/MaruBuri.css',
    'https://hangeul.pstatic.net/hangeul_static/css/maruburi.css',
):
    css = try_get(css_url)
    if not css:
        continue
    urls = re.findall(r'url\(["\']?(https?://[^"\')]+)["\']?\)', css.decode('utf-8', 'replace'))
    print('css font urls:', *urls[:16], sep='\n  ')
    for ext in ('.ttf', '.otf', '.woff2'):
        cands = [u for u in urls if 'semibold' in u.lower() and u.lower().endswith(ext)]
        if cands:
            font = try_get(cands[0])
            if font:
                font_src = cands[0]
                break
    if font:
        break

# 2) Official download zips carry the licence text alongside the fonts.
for zip_url in (
    'https://hangeul.pstatic.net/hangeul_static/webfont/zips/maru-buri.zip',
    'https://hangeul.pstatic.net/hangeul_static/webfont/zips/MaruBuri.zip',
    'https://hangeul.pstatic.net/hangeul_static/zips/maru-buri.zip',
):
    if font and lic:
        break
    zb = try_get(zip_url)
    if not zb:
        continue
    try:
        zf = zipfile.ZipFile(io.BytesIO(zb))
    except Exception as e:
        print(f'--  {zip_url}: not a zip ({e})')
        continue
    names = zf.namelist()
    print('zip contains:', *names[:40], sep='\n  ')
    if font is None:
        for ext in ('.ttf', '.otf'):
            c = sorted(n for n in names if 'semibold' in n.lower() and n.lower().endswith(ext))
            if c:
                font = zf.read(c[0])
                font_src = f'{zip_url} :: {c[0]}'
                break
    if lic is None:
        c = sorted((n for n in names if re.search(r'license|licence|라이선스|ofl', n, re.I)), key=len)
        if c:
            lic = zf.read(c[0])
            lic_src = f'{zip_url} :: {c[0]}'

# 3) Direct path guesses on the official CDN.
if font is None or lic is None:
    for base in (
        'https://hangeul.pstatic.net/hangeul_static/webfont/MaruBuri',
        'https://hangeul.pstatic.net/hangeul_static/webfont/maru-buri',
    ):
        if font is None:
            for name in ('MaruBuri-SemiBold.ttf', 'MaruBuri-SemiBold.otf', 'MaruBuri-SemiBold.woff2'):
                b = try_get(f'{base}/{name}')
                if b:
                    font, font_src = b, f'{base}/{name}'
                    break
        if lic is None:
            for name in ('LICENSE.txt', 'LICENSE', 'license.txt'):
                b = try_get(f'{base}/{name}')
                if b:
                    lic, lic_src = b, f'{base}/{name}'
                    break

# 4) Last resort: top GitHub mirror, provenance logged loudly.
if font is None or lic is None:
    print('Falling back to GitHub mirror search...')
    try:
        res = subprocess.run(
            ['gh', 'api', 'search/repositories?q=maruburi&per_page=5'],
            capture_output=True, text=True, check=True)
        items = json.loads(res.stdout).get('items', [])
        print('mirrors:', [i['full_name'] for i in items])
        for it in items:
            full, branch = it['full_name'], it.get('default_branch', 'main')
            tree = subprocess.run(
                ['gh', 'api', f'repos/{full}/git/trees/{branch}?recursive=1'],
                capture_output=True, text=True)
            if tree.returncode != 0:
                continue
            paths = [e['path'] for e in json.loads(tree.stdout).get('tree', []) if e.get('type') == 'blob']
            raw = f'https://raw.githubusercontent.com/{full}/{branch}'
            if font is None:
                c = sorted(p for p in paths if 'semibold' in p.lower() and p.lower().endswith(('.ttf', '.otf')))
                if c:
                    b = try_get(f'{raw}/{urllib.request.quote(c[0])}')
                    if b:
                        font, font_src = b, f'{full} :: {c[0]}'
            if lic is None:
                c = sorted((p for p in paths if re.search(r'license|licence|ofl', p, re.I)), key=len)
                if c:
                    b = try_get(f'{raw}/{urllib.request.quote(c[0])}')
                    if b:
                        lic, lic_src = b, f'{full} :: {c[0]}'
            if font and lic:
                break
    except Exception as e:
        print(f'mirror search failed: {e}')

if font is None:
    sys.exit('FATAL: no MaruBuri SemiBold obtained from any source.')
if lic is None:
    sys.exit('FATAL: font obtained but no licence text; refusing to self-host without it.')

print(f'font   : {font_src} ({len(font)} bytes, sha256 {hashlib.sha256(font).hexdigest()})')
print(f'licence: {lic_src} ({len(lic)} bytes)')
print('--- licence head ---')
print(lic.decode('utf-8', 'replace')[:1200])

os.makedirs(OUT, exist_ok=True)
src_path = '/tmp/maruburi-semibold.src'
with open(src_path, 'wb') as f:
    f.write(font)
with open(f'{OUT}/LICENSE.txt', 'wb') as f:
    f.write(lic)

# Subset: KS X 1001 syllables (the EUC-KR encodable 2,350) + Jamo + Compat
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
print(f'subsetting to {len(cps)} codepoints in {len(runs)} ranges')

from fontTools import subset  # noqa: E402  (import after pip install in CI)
out_font = f'{OUT}/MaruBuri-SemiBold.hangul.woff2'
subset.main([src_path, f'--unicodes={ranges}', '--flavor=woff2',
             '--layout-features=*', f'--output-file={out_font}'])

size = os.path.getsize(out_font)
sha = hashlib.sha256(open(out_font, 'rb').read()).hexdigest()
print(f'subset : {out_font} ({size} bytes, sha256 {sha})')

with open(f'{OUT}/PROVENANCE.txt', 'w') as f:
    f.write(
        'MaruBuri SemiBold — provenance\n'
        f'font source   : {font_src}\n'
        f'font sha256   : {hashlib.sha256(font).hexdigest()}\n'
        f'licence source: {lic_src}\n'
        f'subset        : Hangul only (KS X 1001 syllables + Jamo U+1100-11FF + Compat Jamo U+3130-318F)\n'
        f'subset sha256 : {sha}\n'
        'tool          : fonttools subset, --flavor=woff2 --layout-features=*\n'
        'licence       : see LICENSE.txt in this directory (ships with the font per Naver font licence)\n')
print('done')
