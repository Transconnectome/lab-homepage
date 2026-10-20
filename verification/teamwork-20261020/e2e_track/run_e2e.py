#!/usr/bin/env python3
"""Opaque-box contract suite. Never imports or reads site implementation.
Expected outputs come from ORIGINAL_REQUEST, PROJECT, AGENTS and public editorial guidelines.
One registered case is one count, irrespective of locale/viewport subchecks.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import time
import traceback
from urllib.parse import urljoin, urlparse, unquote
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CHROME = '/home/juke/.cache/ms-playwright/chromium-1217/chrome-linux/chrome'
CASES = []
LOCALES = ('ko', 'en')
CORE = ('', 'research', 'join')
ROUTES = ('', 'research', 'join', 'publications', 'team', 'news', 'radar', 'ideas')
GUIDE = 'docs/research-editorial-guidelines.md'
REVIEW = 'docs/homepage-editorial-review-2026-10-20.md'


def case(feature, tier, title, expected, source=GUIDE):
    def decorate(fn):
        num = 1 + sum(c['feature'] == feature and c['tier'] == tier for c in CASES)
        CASES.append(dict(id=f'{feature}-T{tier}-{num:02}', feature=feature, tier=tier,
                          title=title, expected=expected, source=source, fn=fn))
        return fn
    return decorate


def require(condition, explanation):
    if not condition:
        raise AssertionError(explanation)


def route(locale, name=''):
    return ('/en/' if locale == 'en' else '/') + name


class Run:
    def __init__(self, browser, base, out):
        self.browser, self.base, self.out = browser, base.rstrip('/'), out
        self.contexts = []
        self.events = []
        self.visits = []

    def page(self, locale='ko', name='', width=1440, js=True):
        c = self.browser.new_context(viewport={'width': width, 'height': 1000},
                                     java_script_enabled=js, reduced_motion='reduce')
        self.contexts.append(c)
        p = c.new_page()
        p.set_default_timeout(7000)
        p.on('pageerror', lambda error: self.events.append(str(error)))
        response = p.goto(self.base + route(locale, name), wait_until='networkidle')
        require(response is not None and response.status == 200,
                f'{p.url}: HTTP {response.status if response else None}')
        visit={'url':p.url,'response_url':response.url,'viewport_width':width,'javascript':js,'status':response.status,
               'rendered_dom_sha256':hashlib.sha256(p.content().encode()).hexdigest()}
        try:
            visit['response_html_sha256']=hashlib.sha256(response.body()).hexdigest()
        except Exception as error:
            # Chromium can discard a redirect response after the destination commits.
            # Retain this evidence gap explicitly; the route assertions still execute.
            visit['response_html_sha256']=None
            visit['response_body_error']=str(error)
        self.visits.append(visit)
        require(p.locator('main').count() == 1, f'{p.url}: expected one main landmark')
        return p

    def doc(self, name=REVIEW):
        p = ROOT / name
        require(p.is_file(), f'Missing public deliverable: {p}')
        return p.read_text()

    def close(self):
        for c in self.contexts:
            c.close()


def text(p):
    return p.locator('main').inner_text()


def match(value, pattern, why):
    require(re.search(pattern, value, re.I | re.S), why)


def visible_links(p, scope='main'):
    return p.locator(f'{scope} a[href]:visible').evaluate_all(
        '(xs)=>xs.map(e=>({text:(e.innerText||e.getAttribute("aria-label")||"").trim(),href:e.getAttribute("href")}))')


def research_links(p):
    return [x for x in visible_links(p)
            if urlparse(urljoin(p.url,x['href'])).path.rstrip('/').endswith('/research')
            and bool(urlparse(urljoin(p.url,x['href'])).fragment)]


def go_link(p, item):
    href = item['href'] if isinstance(item, dict) else item
    locator = p.locator('a[href]:visible')
    candidates = locator.all()
    found = next((x for x in candidates if x.get_attribute('href') == href), None)
    require(found is not None, f'No visible navigable link {href}')
    found.click()
    p.wait_for_load_state('networkidle')
    return p


def no_overflow(p):
    value = p.evaluate('({w:innerWidth,doc:document.documentElement.scrollWidth,body:document.body.scrollWidth})')
    require(max(value['doc'], value['body']) <= value['w'] + 1, f'{p.url} overflow: {value}')


def external_sources(p):
    return [x for x in visible_links(p) if re.match(r'https?://', x['href'])]


def all_imgs_loaded(p):
    images = p.locator('main img').all()
    require(images, f'{p.url}: expected informative images')
    for image in images:
        image.scroll_into_view_if_needed()
        image.evaluate('(e)=>e.loading="eager"')
        image.evaluate('(e)=>e.decode().catch(()=>{})')
        require(image.evaluate('(e)=>e.complete && e.naturalWidth>0'), f'Broken image {image.get_attribute("src")}')


def application_link(p, locale):
    matches = [x for x in visible_links(p) if urlparse(x['href']).path.rstrip('/') == route(locale, 'join').rstrip('/')]
    require(matches, f'{p.url}: no visible application path')
    return matches[0]


def mail(p):
    links = p.locator('main a[href^="mailto:"]:visible')
    require(links.count() > 0, 'No usable public application email link')
    address = links.first.get_attribute('href')[7:].split('?')[0]
    match(address, r'^[^\s@]+@[^\s@]+\.[^\s@]+$', f'Invalid application address {address}')
    return address


@case('F1', 1, 'Human-centered bilingual mission', 'Both homepages explain people and genes/brain/behavior/environment, rather than model names alone.')
def f1_mission(r):
    for lang in LOCALES:
        t = text(r.page(lang))
        for pattern in (('유전', '뇌', '행동', '환경') if lang == 'ko' else ('genes|genetic', 'brain', 'behavio', 'environment')):
            match(t, pattern, f'{lang}: missing mission dimension {pattern}')


@case('F1', 1, 'Four question-led entry points', 'Homepage exposes four distinct question links to detailed research.', 'README.md#Design')
def f1_questions(r):
    for lang in LOCALES:
        links = research_links(r.page(lang))
        require(len({x['href'] for x in links}) >= 4, f'{lang}: fewer than four distinct research question destinations')
        require(sum('?' in x['text'] or '까' in x['text'] for x in links) >= 4, f'{lang}: question wording missing')


@case('F1', 1, 'Question to method explanation', 'Research overview visibly explains at least one data/design choice for each research direction.')
def f1_methods(r):
    for lang in LOCALES:
        t = text(r.page(lang, 'research'))
        for pattern in ('fMRI', 'EEG', 'PGS|polygenic|다유전자', 'quantum|양자', 'VR|virtual|가상'):
            match(t, pattern, f'{lang}: missing method context {pattern}')


@case('F1', 1, 'Demonstrated examples have research sources', 'Research page shows concrete study examples and external publication references.')
def f1_examples(r):
    for lang in LOCALES:
        p = r.page(lang, 'research')
        match(text(p), r'SwiFT|MBBN|DIVER', f'{lang}: no representative concrete research example')
        links = external_sources(p)
        require(any(re.search(r'doi\.org|arxiv\.org|nature\.com|pubmed|openreview|proceedings', x['href']) for x in links), f'{lang}: no publication source')


@case('F1', 1, 'Limits remain visible beside research', 'Research explanation includes predictive/causal boundary and unvalidated next-step language.')
def f1_limits(r):
    for lang in LOCALES:
        t = text(r.page(lang, 'research'))
        match(t, '인과|causal', f'{lang}: causal boundary absent')
        match(t, '추가 검증|검증.*필요|한계|제약|remain|further|limitation|constraint', f'{lang}: limits absent')


@case('F1', 2, 'No-JavaScript research meaning', 'Disabling scripts preserves all four questions and substantial explanatory research text.')
def f1_nojs(r):
    for lang in LOCALES:
        p = r.page(lang, 'research', js=False)
        require(len(text(p)) > 1500, f'{lang}: substantive research explanation depends on JS')
        require(len({x['href'] for x in research_links(p)}) >= 4, f'{lang}: research fallback links missing')


@case('F1', 2, 'Homepage layer links to detail', 'Each unique homepage research question link reaches its corresponding visible explanatory section.')
def f1_depth(r):
    for lang in LOCALES:
        p = r.page(lang)
        links = {x['href']: x for x in research_links(p)}
        require(len(links) >= 4, f'{lang}: missing detail entry points')
        for href in links:
            p.goto(r.base + href)
            anchor = unquote(urlparse(href).fragment)
            e = p.locator(f'[id="{anchor}"]')
            require(e.count() == 1 and e.is_visible(), f'{lang}: missing visible detail target {href}')
            require(len(e.inner_text()) > 250, f'{href}: detail section lacks explanatory depth')


@case('F1', 2, 'No unsupported superlative promise', 'Homepage does not promise guaranteed admission, guaranteed results or world-best ranking as fact.')
def f1_promises(r):
    for lang in LOCALES:
        t = text(r.page(lang))
        require(not re.search(r'세계\s*(최고|1위).*보장|합격.*보장|guaranteed\s+(admission|success)|world.s\s+(best|number one)\s+lab', t, re.I), 'Unsupported superlative/guarantee wording')


@case('F1', 2, 'Research locale coverage parity', 'Both locales expose the same four research directions through corresponding anchors.')
def f1_parity(r):
    sets = []
    for lang in LOCALES:
        links = research_links(r.page(lang))
        sets.append({urlparse(x['href']).fragment.removesuffix('-en') for x in links})
    require(sets[0] == sets[1] and len(sets[0]) >= 4, f'Research locale coverage differs: {sets}')


@case('F1', 2, 'Narrow-screen explanation readability', 'Research prose at 320px is visible, has no replacement characters or clipped horizontal extent.')
def f1_narrow(r):
    for lang in LOCALES:
        p = r.page(lang, 'research', 320)
        no_overflow(p)
        require('\ufffd' not in text(p) and '\x00' not in text(p), f'{lang}: text encoding damaged')
        p.locator('main h1').scroll_into_view_if_needed()
        require(p.locator('main h1').is_visible(), 'Heading not readable')


@case('F2', 1, 'Homepage research figure loads', 'Each homepage includes a rendered informative research image.')
def f2_loaded(r):
    for lang in LOCALES:
        p = r.page(lang)
        require(p.locator('main figure img').count() > 0, f'{lang}: no research figure')
        all_imgs_loaded(p)


@case('F2', 1, 'Figure caption carries scientific meaning', 'Homepage research caption explains the represented observation and its interpretation boundary.')
def f2_caption(r):
    for lang in LOCALES:
        p = r.page(lang)
        captions = p.locator('main figcaption:visible').all_text_contents()
        require(captions, f'{lang}: no visible figure caption')
        match(' '.join(captions), '모델|연결|model|connectivity', f'{lang}: caption does not explain depicted result')
        match(' '.join(captions), '인과|원인|causal|cause', f'{lang}: causal interpretation boundary missing from caption')


@case('F2', 1, 'Figure credit is a traceable link', 'A visible source link is associated with the homepage research figure.')
def f2_source(r):
    for lang in LOCALES:
        p = r.page(lang)
        figures = p.locator('main figure').all()
        require(any(f.locator('a[href^="http"]:visible').count() for f in figures), f'{lang}: no linked figure provenance')


@case('F2', 1, 'Research surface labeled as reference', 'The research illustration is identified as a reference surface with a source, not a result localization map.')
def f2_reference(r):
    for lang in LOCALES:
        t = text(r.page(lang, 'research'))
        match(t, 'FreeSurfer', f'{lang}: reference-surface source missing')
        match(t, '표면|surface', f'{lang}: surface interpretation missing')


@case('F2', 1, 'Informative image alternatives', 'Every rendered research/homepage image has an alt attribute; figure images have nonempty alternatives.')
def f2_alts(r):
    for lang in LOCALES:
        for path in ('', 'research'):
            p = r.page(lang, path)
            for im in p.locator('main img').all():
                require(im.get_attribute('alt') is not None, f'{p.url}: image missing alt')
            for im in p.locator('main figure img').all():
                require(bool((im.get_attribute('alt') or '').strip()), f'{p.url}: informative figure has empty alt')


@case('F2', 2, 'Narrow figure and caption containment', 'Figures and their captions stay inside the 320px viewport.')
def f2_contain(r):
    for lang in LOCALES:
        p = r.page(lang, width=320)
        for el in p.locator('main figure,main figcaption').all():
            box = el.bounding_box()
            require(box and box['width'] > 0 and box['x'] >= -1 and box['x'] + box['width'] <= 321, f'{lang}: figure/caption outside narrow viewport: {box}')


@case('F2', 2, 'Figure source works without scripts', 'Caption, credit link and decoded figure remain available when JavaScript is disabled.')
def f2_nojs(r):
    for lang in LOCALES:
        p = r.page(lang, js=False)
        require(p.locator('figcaption:visible').count() > 0, f'{lang}: no static figure caption')
        require(p.locator('main figure a[href^="http"]:visible').count() > 0, f'{lang}: no static figure credit')
        all_imgs_loaded(p)


@case('F2', 2, 'Missing image retains explanation', 'When image responses fail, textual figure alternative and visible caption still explain the content.')
def f2_missing(r):
    for lang in LOCALES:
        p = r.page(lang)
        p.route('**/*', lambda request: request.abort() if request.request.resource_type == 'image' else request.continue_())
        p.reload(wait_until='networkidle')
        require(p.locator('main figcaption:visible').count(), f'{lang}: image failure loses caption')
        im = p.locator('main figure img').first
        require(bool(im.get_attribute('alt')), f'{lang}: image failure lacks alternative')


@case('F2', 2, 'Image provenance locale parity', 'Both locales use the same homepage research figure source and credit destination.')
def f2_parity(r):
    values=[]
    for lang in LOCALES:
        p=r.page(lang)
        values.append((p.locator('main figure img').first.get_attribute('src'),
                       sorted(p.locator('main figure a[href^="http"]').evaluate_all('(xs)=>xs.map(e=>e.href)'))))
    require(values[0] == values[1], f'Locale figure provenance differs: {values}')


@case('F2', 2, 'Image license stays visible', 'Research figure attribution states the license in both languages.')
def f2_license(r):
    for lang in LOCALES:
        p = r.page(lang)
        match(' '.join(p.locator('main figcaption').all_text_contents()), r'CC\s*BY\s*4\.0', f'{lang}: figure license missing')


@case('F3', 1, 'Homepage offers application path', 'A reader can click a visible homepage action and reach the locale-appropriate join page.')
def f3_home(r):
    for lang in LOCALES:
        p = r.page(lang)
        go_link(p, application_link(p,lang))
        require(urlparse(p.url).path.rstrip('/') == route(lang, 'join').rstrip('/'), f'{lang}: application action misroutes')


@case('F3', 1, 'Application route names supported roles', 'Join page identifies graduate, postdoctoral and undergraduate/intern routes without inventing openings.')
def f3_roles(r):
    for lang in LOCALES:
        t = text(r.page(lang, 'join'))
        for regex in (('대학원', '박사후', '인턴') if lang == 'ko' else ('graduate', 'postdoc', 'intern')):
            match(t, regex, f'{lang}: unsupported/missing route {regex}')


@case('F3', 1, 'Concrete application materials', 'Applicants see CV, transcript and a research-interest statement requirement.')
def f3_materials(r):
    for lang in LOCALES:
        t = text(r.page(lang, 'join'))
        for regex in (r'Curriculum Vitae|\bCV\b', '성적|transcript', '질문|research.*interest|question'):
            match(t, regex, f'{lang}: missing application preparation {regex}')


@case('F3', 1, 'Public contact action', 'Join includes a syntactically valid usable mailto application contact.')
def f3_contact(r):
    for lang in LOCALES:
        mail(r.page(lang, 'join'))


@case('F3', 1, 'Research culture gives concrete expectations', 'Join explains independence, learning, collaboration and research completion.')
def f3_culture(r):
    for lang in LOCALES:
        t = text(r.page(lang, 'join'))
        for regex in (('질문', '배우|학습', '동료', '완성|책임') if lang == 'ko' else ('question', 'learn', 'colleague|one another|peer', 'complete|completion|responsib')):
            match(t, regex, f'{lang}: missing concrete culture dimension {regex}')


@case('F3', 2, 'Openings uncertainty preserved', 'Join asks readers to verify current openings and distinguishes formal university admission.')
def f3_openings(r):
    for lang in LOCALES:
        t=text(r.page(lang,'join'))
        match(t,'현재 모집|current openings|availability', f'{lang}: current openings qualification absent')
        match(t,'입시 일정|admission.*schedule|university.*admission', f'{lang}: official admission distinction absent')


@case('F3', 2, 'Keyboard-operable FAQ', 'FAQ question can be focused and expanded with Enter, revealing its answer.')
def f3_faq(r):
    for lang in LOCALES:
        p=r.page(lang,'join')
        s=p.locator('main details summary').first
        require(s.count(),f'{lang}: no native FAQ disclosure')
        s.focus(); s.press('Enter')
        require(s.evaluate('(e)=>e.parentElement.open'),f'{lang}: Enter fails to open FAQ')
        require(len(s.locator('..').inner_text()) > len(s.inner_text())+20, f'{lang}: FAQ answer missing')


@case('F3', 2, 'Application without JavaScript', 'No-JS visitors can reach application instructions and contact.')
def f3_nojs(r):
    for lang in LOCALES:
        p=r.page(lang,js=False)
        go_link(p,application_link(p,lang)); mail(p)
        match(text(p),'성적|transcript',f'{lang}: no-JS instructions missing')


@case('F3', 2, 'Application locale contact parity', 'Both languages direct applications to the same verified public mailbox and matching program families.')
def f3_parity(r):
    addresses=[]
    for lang in LOCALES:
        p=r.page(lang,'join'); addresses.append(mail(p))
        for pattern in ('IPAI','BCS'):
            match(text(p),pattern,f'{lang}: program missing {pattern}')
    require(addresses[0]==addresses[1],f'Locale contacts differ: {addresses}')


@case('F3', 2, 'Mobile application anchor', 'At 390px the join page application anchor reaches visible preparation/contact instructions.')
def f3_anchor(r):
    for lang in LOCALES:
        p=r.page(lang,'join',390)
        candidates=[x for x in visible_links(p) if x['href'].startswith('#')]
        require(candidates,f'{lang}: no direct application anchor')
        go_link(p,candidates[0])
        anchor=unquote(urlparse(p.url).fragment)
        target=p.locator(f'[id="{anchor}"]')
        require(target.count()==1 and target.is_visible(),f'{lang}: broken application anchor')
        match(target.inner_text(),'성적|transcript|Curriculum',f'{lang}: anchor does not reach preparation')


@case('F4',1,'Responsive home layout','Both homepages fit 320/390/1440px without horizontal overflow.', 'PROJECT.md#F4')
def f4_home(r):
    for lang in LOCALES:
        for width in (320,390,1440): no_overflow(r.page(lang,width=width))


@case('F4',1,'Responsive research layout','Both research pages fit 320/390/1440px without horizontal overflow.', 'PROJECT.md#F4')
def f4_research(r):
    for lang in LOCALES:
        for width in (320,390,1440): no_overflow(r.page(lang,'research',width))


@case('F4',1,'Responsive join layout','Both join pages fit 320/390/1440px without horizontal overflow.', 'PROJECT.md#F4')
def f4_join(r):
    for lang in LOCALES:
        for width in (320,390,1440): no_overflow(r.page(lang,'join',width))


@case('F4',1,'Reading landmarks and heading','Core pages provide one visible h1, main landmark and named document language.', 'PROJECT.md#F4')
def f4_landmarks(r):
    for lang in LOCALES:
        for path in CORE:
            p=r.page(lang,path)
            require(p.locator('main h1:visible').count()==1,f'{p.url}: main h1 count')
            require(p.locator('html').get_attribute('lang').startswith(lang),f'{p.url}: document language mismatch')


@case('F4',1,'Controls have accessible names','All visible core-page interactive controls have usable names.', 'PROJECT.md#F4')
def f4_names(r):
    for lang in LOCALES:
        for path in CORE:
            p=r.page(lang,path)
            for e in p.locator('main button:visible, main a:visible, main input:visible, main select:visible').all():
                name=e.evaluate('(e)=>e.getAttribute("aria-label")||e.getAttribute("title")||e.innerText||e.labels?.[0]?.innerText||e.querySelector("img")?.alt||""')
                require(name.strip(),f'{p.url}: unnamed {e.evaluate("e=>e.outerHTML.slice(0,180)")}')


@case('F4',2,'Keyboard mobile menu','A keyboard user opens mobile navigation and follows Research.', 'PROJECT.md#F4')
def f4_menu(r):
    for lang in LOCALES:
        p=r.page(lang,width=320)
        b=p.get_by_role('button',name=re.compile('menu|메뉴',re.I)).first
        require(b.is_visible(),f'{lang}: no visible mobile menu')
        b.focus(); b.press('Enter')
        links=[x for x in visible_links(p,'nav') if urlparse(x['href']).path.rstrip('/')==route(lang,'research').rstrip('/')]
        require(links,f'{lang}: research nav inaccessible after keyboard menu open')
        go_link(p,links[0]); require('/research' in p.url,'Keyboard menu misroutes')


@case('F4',2,'Keyboard focus remains perceptible','Focused primary application link has visible outline or box-shadow focus styling.', 'PROJECT.md#F4')
def f4_focus(r):
    for lang in LOCALES:
        p=r.page(lang)
        link=application_link(p,lang)
        e=p.locator(f'main a[href="{link["href"]}"]:visible').first
        p.keyboard.press('Tab'); e.focus()
        value=e.evaluate('(e)=>{let s=getComputedStyle(e);return {outline:s.outlineStyle,width:s.outlineWidth,shadow:s.boxShadow}}')
        require((value['outline']!='none' and value['width']!='0px') or value['shadow']!='none',f'{lang}: imperceptible focus {value}')


@case('F4',2,'Native research navigation without scripts','At 320px all four native research links remain usable with JavaScript disabled.', 'PROJECT.md#F4')
def f4_native(r):
    for lang in LOCALES:
        p=r.page(lang,width=320,js=False)
        links=research_links(p)
        require(len({x['href'] for x in links})>=4,f'{lang}: fallback loses research pathways')
        go_link(p,links[0]); require(bool(urlparse(p.url).fragment),'No-JS detail navigation failed')


@case('F4',2,'Text enlargement does not clip content','Core pages at 200% root text sizing remain readable without horizontal overflow.', 'PROJECT.md#F4')
def f4_zoom(r):
    for lang in LOCALES:
        for path in CORE:
            p=r.page(lang,path,390)
            p.add_style_tag(content='html { font-size: 200% !important; }')
            no_overflow(p)


@case('F4',2,'Reduced motion preserves content','Reduced-motion readers retain headline, research links, figures and application action.', 'PROJECT.md#F4')
def f4_motion(r):
    for lang in LOCALES:
        p=r.page(lang)
        require(p.evaluate('matchMedia("(prefers-reduced-motion: reduce)").matches'),'Reduced-motion emulation failed')
        require(p.locator('main h1').is_visible(),'Headline unavailable with reduced motion')
        require(research_links(p),'Research unavailable with reduced motion')
        application_link(p,lang)
        require(p.locator('main figure:visible').count(),'Figure unavailable with reduced motion')


@case('F5',1,'Public route preservation','All eight established public routes load in both languages.', 'README.md')
def f5_routes(r):
    for lang in LOCALES:
        for path in ROUTES: r.page(lang,path)


@case('F5',1,'Locale switch preserves route','Core pages offer the counterpart locale and follow it without losing page intent.', 'AGENTS.md')
def f5_locale(r):
    for lang in LOCALES:
        other='en' if lang=='ko' else 'ko'
        for path in CORE:
            p=r.page(lang,path)
            wanted=route(other,path).rstrip('/') or '/'
            links=[x for x in visible_links(p,'body') if (urlparse(urljoin(p.url,x['href'])).path.rstrip('/') or '/')==wanted]
            require(links,f'{p.url}: locale counterpart missing')
            go_link(p,links[0])
            require(p.locator('html').get_attribute('lang').startswith(other),f'{p.url}: locale action failed')


@case('F5',1,'Core internal destinations resolve','Every visible core-page local link has a successful response; fragment IDs exist.', 'AGENTS.md')
def f5_links(r):
    seen=set()
    for lang in LOCALES:
        for path in CORE:
            p=r.page(lang,path)
            for item in visible_links(p):
                href=item['href']; url=urljoin(p.url,href)
                if urlparse(url).netloc!=urlparse(r.base).netloc or url in seen: continue
                seen.add(url)
                q=p.context.new_page(); response=q.goto(url,wait_until='domcontentloaded')
                require(response and response.status==200,f'Broken internal link {url}')
                fragment=unquote(urlparse(url).fragment)
                if fragment: require(q.locator(f'[id="{fragment}"]').count()==1,f'Missing fragment {url}')
                q.close()


@case('F5',1,'Core assets decode','All main images on home, research and join decode successfully.', 'AGENTS.md')
def f5_assets(r):
    for lang in LOCALES:
        for path in CORE:
            p=r.page(lang,path)
            if p.locator('main img').count(): all_imgs_loaded(p)


@case('F5',1,'Page metadata describes each route','Each core locale page has distinct title and nonempty description plus HTTPS canonical.', 'README.md')
def f5_metadata(r):
    titles=[]
    for lang in LOCALES:
        for path in CORE:
            p=r.page(lang,path); titles.append(p.title())
            require(len(p.title())>5,'Empty page title')
            require(bool(p.locator('meta[name="description"]').get_attribute('content')),'Missing description')
            require(p.locator('link[rel="canonical"]').get_attribute('href').startswith('https://'),'Canonical is not HTTPS')
    require(len(set(titles))==len(titles),f'Duplicate locale/route title: {titles}')


@case('F5',2,'Legacy Korean redirects','Established /ko and /ko/research links reach Korean content.', 'README.md')
def f5_redirect(r):
    for path in ('ko/','ko/research'):
        p=r.page('ko',path)
        p.wait_for_timeout(300)
        require(not urlparse(p.url).path.startswith('/ko'),f'Legacy URL not redirected: {p.url}')
        require(p.locator('html').get_attribute('lang').startswith('ko'),'Legacy URL changes language')


@case('F5',2,'Graceful unknown route','Unknown URL returns a genuine 404 with a visible explanation, not a blank page or false-success homepage.', 'PROJECT.md#F5')
def f5_404(r):
    c=r.browser.new_context(); r.contexts.append(c); p=c.new_page()
    response=p.goto(r.base+'/this-page-does-not-exist-teamwork-20261020',wait_until='domcontentloaded')
    require(response and response.status==404,'Unknown route must return HTTP 404')
    match(p.locator('body').inner_text(),'404|not found|찾을 수 없|없습니다','404 lacks readable explanation')


@case('F5',2,'Publication no-match and recovery','Impossible publication search explains zero results; clearing restores publications.', 'README.md')
def f5_nomatch(r):
    for lang in LOCALES:
        p=r.page(lang,'publications')
        search=p.locator('main input[type="search"],main input[type="text"]').first
        require(search.count(),'Publication search unavailable')
        search.fill('NO_MATCH_7b59f2'); p.wait_for_timeout(250)
        match(text(p),r'없|no .*found|no .*match|0\s*(papers|publications|편|건)','No-match response missing')
        search.fill(''); p.wait_for_timeout(250)
        match(text(p),'MBBN|Learning brain dynamics','Clearing search does not restore publication')


@case('F5',2,'Runtime console remains error-free','Core-page loads and native disclosures cause no browser page errors.', 'PROJECT.md#F5')
def f5_errors(r):
    for lang in LOCALES:
        for path in CORE:
            p=r.page(lang,path)
            for s in p.locator('main details summary').all()[:2]: s.click()
    require(not r.events,f'Browser runtime errors: {r.events}')


@case('F5',2,'Deep-link reload preserves target','A research link can be bookmarked and reloaded, retaining a valid visible section.', 'PROJECT.md#F5')
def f5_reload(r):
    for lang in LOCALES:
        p=r.page(lang); links=research_links(p); require(links,'No research deep links')
        go_link(p,links[-1]); before=p.url; p.reload(wait_until='networkidle')
        require(p.url==before,'Reload lost deep link')
        anchor=unquote(urlparse(p.url).fragment)
        require(p.locator(f'[id="{anchor}"]').is_visible(),'Reload lost research section')


@case('F6',1,'Dated public review artifact','Request-scoped public review exists and explicitly records the 2026-10-20 revision.', 'AGENTS.md#완료 보고')
def f6_review(r):
    match(r.doc(),r'2026[-.]10[-.]20','No dated request-specific editorial record')


@case('F6',1,'Concrete before-after examples','Public review includes concrete before/after text and the rationale for changes.', GUIDE+'#8')
def f6_beforeafter(r):
    t=r.doc()
    for pattern in ('수정 전|개편 전|Before','수정 후|개편 후|After','이유|근거|rationale|reason'):
        match(t,pattern,'Before/after rationale missing: '+pattern)
    require(len(t)>1000,'Editorial review lacks substantive before/after record')


@case('F6',1,'Claim-source mapping','Public review maps claims to identifiable source URLs and section/figure/table locators.', GUIDE+'#3')
def f6_claimmap(r):
    t=r.doc()
    match(t,'주장|claim','Claim mapping missing')
    match(t,r'https://(?:doi\.org|arxiv\.org|www\.nature\.com|nature\.com|openreview\.net|pmc\.ncbi\.nlm\.nih\.gov)','No primary study source URL')
    match(t,r'그림|Figure|Fig\.|절|Table|표|section','Source locator missing')


@case('F6',1,'Image provenance record','Image record identifies source and license plus excerpt/transformation provenance.', GUIDE+'#6')
def f6_image(r):
    t=r.doc()+'\n'+r.doc('public/assets/site/README.md')
    for pattern in ('https://','CC BY|license|라이선스','발췌|excerpt|crop|panel|패널'):
        match(t,pattern,'Image provenance record incomplete: '+pattern)


@case('F6',1,'Scope and remaining verification','Public review distinguishes executed work from unresolved verification and PI decisions.', GUIDE+'#8')
def f6_scope(r):
    t=r.doc()
    match(t,'남은|미확인|확인하지|unresolved|remaining|not verified|한계','No unresolved/limit record')
    match(t,'PI|교수|승인|배포|deploy','No approval/deployment scope record')


@case('F6',2,'Public artifact local links resolve','All local Markdown link targets in the request-specific review exist.', GUIDE+'#8')
def f6_doclinks(r):
    t=r.doc(); count=0
    for dest in re.findall(r'\]\(([^)]+)\)',t):
        dest=dest.split('#')[0].split(' "')[0].strip('<>')
        if not dest or re.match(r'[a-z]+://|mailto:',dest): continue
        target=Path(dest) if dest.startswith('/') else (ROOT/'docs'/dest)
        require(target.exists(),f'Broken public review link: {dest} -> {target}')
        count+=1
    require(count>0,'No resolvable local deliverable references in public review')


@case('F6',2,'Public documentation contains no private operational paths','Review does not expose home-directory paths, credentials, private workspace links or secret-bearing strings.', 'AGENTS.md#검증과 변경 범위')
def f6_public(r):
    t=r.doc()
    for pattern in (r'/home/[^\s)]+',r'/Users/[^\s)]+',r'(?i)(?:api[_-]?key|access[_-]?token)\s*[=:]\s*[A-Za-z0-9_-]{16,}',r'https://[^\s)]*(?:100\.92\.111\.86|spark-3a4c)'):
        require(not re.search(pattern,t),f'Private operational information matched: {pattern}')


@case('F6',2,'Verification is reproducible','Public review records actual build/browser verification commands or links to their report, and distinguishes science review.', GUIDE+'#8')
def f6_repro(r):
    t=r.doc()
    match(t,'npm run build|TEST_READY|TEST_INFRA|run_e2e|검증 보고','No reproducible verification reference')
    match(t,'과학|scientific|원문','No separation of scientific validation')


@case('F6',2,'Maintenance and future updates documented','Public review states how reviewed content and sources should be updated or revalidated.', GUIDE+'#8')
def f6_updates(r):
    match(r.doc(),'업데이트|갱신|향후|update|maintain|재검증','No future maintenance guidance')


@case('F6',2,'New review is indexed by canonical content review','Canonical content review mentions this dated revision or links its public report.', 'AGENTS.md#완료 보고')
def f6_index(r):
    match(r.doc('docs/research-content-review.md'),'2026-10-20|homepage-editorial-review-2026-10-20','Canonical content review does not index latest work')


@case('F1+F2',3,'Question-to-evidence reading path','A homepage reader follows a research figure/context link and finds question, representative study and limits.', 'PROJECT.md#F1-F2')
def t3_explain_image(r):
    for lang in LOCALES:
        p=r.page(lang)
        require(p.locator('main figcaption:visible').count(),'Research figure context absent')
        links=research_links(p); require(links,'No figure-to-research supporting pathway')
        go_link(p,links[0]); t=text(p)
        match(t,'fMRI|EEG','Method evidence missing'); match(t,'한계|검증|causal|validation|limit','Limits missing')


@case('F1+F3',3,'Research interest becomes application','After reading a research question visitors can reach locale-correct application information from navigation.', 'PROJECT.md#F1-F3')
def t3_interest_apply(r):
    for lang in LOCALES:
        p=r.page(lang)
        go_link(p,research_links(p)[0])
        links=[x for x in visible_links(p,'body') if urlparse(x['href']).path.rstrip('/')==route(lang,'join').rstrip('/')]
        require(links,'Research reader has no application route'); go_link(p,links[0]); mail(p)


@case('F2+F4',3,'Mobile visual explanation','At 390px decoded research figure, explanatory caption and credit remain readable together.', 'PROJECT.md#F2-F4')
def t3_mobile_image(r):
    for lang in LOCALES:
        p=r.page(lang,width=390); all_imgs_loaded(p); no_overflow(p)
        f=p.locator('main figure').first; f.scroll_into_view_if_needed()
        require(f.locator('figcaption').is_visible(),'Mobile caption hidden')
        require(f.locator('a[href^="http"]:visible').count(),'Mobile source link hidden')


@case('F3+F4',3,'Keyboard mobile applicant flow','At 320px applicant follows visible CTA by Enter then opens a FAQ and can reach contact.', 'PROJECT.md#F3-F4')
def t3_keyboard_apply(r):
    for lang in LOCALES:
        p=r.page(lang,width=320); item=application_link(p,lang)
        e=p.locator(f'main a[href="{item["href"]}"]:visible').first
        e.focus(); e.press('Enter'); p.wait_for_load_state('networkidle'); mail(p)
        s=p.locator('main details summary').first; s.focus(); s.press('Enter')
        require(s.evaluate('e=>e.parentElement.open'),'Keyboard FAQ does not reveal answer'); no_overflow(p)


@case('F4+F5',3,'Mobile locale round trip','At 390px language switching twice preserves research route and no overflow.', 'PROJECT.md#F4-F5')
def t3_locale_roundtrip(r):
    p=r.page('ko','research',390)
    for lang in ('en','ko'):
        wanted=route(lang,'research').rstrip('/')
        links=[x for x in visible_links(p,'body') if urlparse(x['href']).path.rstrip('/')==wanted]
        if not links:
            b=p.get_by_role('button',name=re.compile('menu|메뉴',re.I)).first; b.click()
            links=[x for x in visible_links(p,'body') if urlparse(x['href']).path.rstrip('/')==wanted]
        require(links,'Mobile locale switch unavailable'); go_link(p,links[0]); no_overflow(p)
        require(p.locator('html').get_attribute('lang').startswith(lang),'Locale roundtrip lost language')


@case('F2+F6',3,'Visible figure ties to provenance record','The homepage credit source is explicitly traceable in public image/review documentation.', 'PROJECT.md#F2-F6')
def t3_doc_image(r):
    p=r.page(); links=p.locator('main figure a[href^="http"]').evaluate_all('(xs)=>xs.map(e=>e.href)')
    t=r.doc()+'\n'+r.doc('public/assets/site/README.md')
    require(links,'No visible figure credit')
    require(any(url in t for url in links),'Visible credit URL absent from public provenance docs')


@case('ALL',4,'Korean mobile prospective graduate','390px Korean visitor reads mission, research detail, application preparation and contact.', 'ORIGINAL_REQUEST.md + PROJECT.md')
def t4_ko_applicant(r):
    p=r.page('ko',width=390); require(len(text(p))>300,'Homepage explanation missing')
    go_link(p,research_links(p)[1]); match(text(p),'유전|정서|뇌','Research topic lost')
    links=[x for x in visible_links(p,'body') if urlparse(x['href']).path.rstrip('/')=='/join']
    if not links:
        p.get_by_role('button',name=re.compile('menu|메뉴',re.I)).first.click()
        links=[x for x in visible_links(p,'body') if urlparse(x['href']).path.rstrip('/')=='/join']
    require(links,'Application unavailable from mobile research'); go_link(p,links[0]); mail(p); match(text(p),'성적증명서','Preparation missing'); no_overflow(p)


@case('ALL',4,'English desktop researcher','1440px English reader reviews image credit, follows research evidence, then finds publications and application.', 'ORIGINAL_REQUEST.md + PROJECT.md')
def t4_en_researcher(r):
    p=r.page('en'); require(p.locator('main figure a[href^="http"]:visible').count(),'Figure source not exposed')
    go_link(p,research_links(p)[0]); require(external_sources(p),'No external evidence for researcher')
    links=[x for x in visible_links(p,'body') if urlparse(x['href']).path.rstrip('/')=='/en/publications']
    require(links,'No publication route'); go_link(p,links[0]); match(text(p),'Learning brain dynamics','Representative paper absent')
    links=[x for x in visible_links(p,'body') if urlparse(x['href']).path.rstrip('/')=='/en/join']
    require(links,'Application route lost'); go_link(p,links[0]); mail(p)


@case('ALL',4,'Low-script narrow-screen applicant','320px visitor with scripts disabled can read question, its evidence, and prepare an application.', 'ORIGINAL_REQUEST.md + PROJECT.md')
def t4_nojs(r):
    p=r.page('ko',width=320,js=False); go_link(p,research_links(p)[0]); require(len(text(p))>1500,'Static detailed explanation missing')
    p.goto(r.base+'/join'); mail(p); match(text(p),'Curriculum Vitae|CV','Static preparation missing'); no_overflow(p)


@case('ALL',4,'Bilingual reader compares meaning boundaries','Reader switches homepage language, sees same figure/source and matching scope dimensions, then follows research.', 'ORIGINAL_REQUEST.md + PROJECT.md')
def t4_bilingual(r):
    p=r.page('ko'); source=p.locator('main figure img').first.get_attribute('src')
    links=[x for x in visible_links(p,'body') if urlparse(x['href']).path.rstrip('/')=='/en']
    require(links,'English switch missing'); go_link(p,links[0])
    require(p.locator('main figure img').first.get_attribute('src')==source,'Locale switch changes scientific figure')
    match(text(p),'causal|cause','English caption lacks causal boundary'); go_link(p,research_links(p)[0]); match(text(p),'environment','English research breadth lost')


@case('ALL',4,'Skeptical visitor recovers from no-match search','Publication visitor sees empty-state feedback, clears it, finds evidence, and returns to research navigation.', 'ORIGINAL_REQUEST.md + PROJECT.md')
def t4_recovery(r):
    p=r.page('en','publications',390)
    search=p.locator('main input[type="search"],main input[type="text"]').first
    search.fill('not-a-real-publication-20261020'); p.wait_for_timeout(250)
    match(text(p),r'no .*found|no .*match|0\s*(papers|publications)','No visible empty state')
    search.fill('brain'); p.wait_for_timeout(250); match(text(p),'Learning brain dynamics','Relevant evidence not recovered')
    search.fill(''); p.wait_for_timeout(150)
    b=p.get_by_role('button',name=re.compile('menu|메뉴',re.I)).first
    if b.is_visible(): b.click()
    links=[x for x in visible_links(p,'body') if urlparse(x['href']).path.rstrip('/')=='/en/research']
    require(links,'Recovery loses research navigation'); go_link(p,links[0]); no_overflow(p)



@case('F1+F4',3,'Question links remain keyboard readable','At 320px keyboard activation of a question reaches a visible explanatory heading without clipping.', 'PROJECT.md#F1-F4')
def t3_question_keyboard(r):
    for lang in LOCALES:
        p=r.page(lang,width=320); item=research_links(p)[0]
        e=p.locator(f'main a[href="{item["href"]}"]:visible').first
        e.focus(); e.press('Enter'); p.wait_for_load_state('networkidle')
        anchor=unquote(urlparse(p.url).fragment)
        target=p.locator(f'[id="{anchor}"]')
        require(target.is_visible(),'Keyboard question destination hidden')
        require(target.locator('h2,h3').count(),'Question destination lacks reading heading')
        no_overflow(p)


@case('F1+F5',3,'Research breadth survives route reload and locale change','All four question destinations still resolve after navigation and the paired locale retains all four.', 'PROJECT.md#F1-F5')
def t3_research_routes(r):
    p=r.page('ko'); links={x['href'] for x in research_links(p)}
    require(len(links)>=4,'Korean question coverage missing')
    for href in links:
        response=p.goto(r.base+href); require(response.status==200,'Question route failed')
        p.reload(wait_until='networkidle')
        anchor=unquote(urlparse(p.url).fragment)
        require(len(p.locator(f'[id="{anchor}"]').inner_text())>250,'Reload loses explanation')
    p=r.page('en'); require(len({x['href'] for x in research_links(p)})==len(links),'Locale question coverage differs')


@case('F1+F6',3,'Research examples tie to public claim record','A named representative model in the rendered research explanation is present in the public claim/source review.', 'PROJECT.md#F1-F6')
def t3_claim_record(r):
    p=r.page('en','research'); doc=r.doc()
    names=re.findall(r'\b(?:MBBN|SwiFT|SwiFUN|DIVER-0|DIVER-1|Q-DIVER|NeuroMamba)\b',text(p))
    require(names,'No identifiable demonstrated research example')
    require(any(name in doc for name in names),'Public review not linked to a rendered concrete research example')
    match(doc,'인과|causal|한계|limitation','Claim record lacks scientific interpretation boundaries')


@case('F2+F3',3,'Figure reading does not dead-end applicant','After viewing homepage evidence and source credit, an applicant can reach instructions without leaving the locale.', 'PROJECT.md#F2-F3')
def t3_figure_apply(r):
    for lang in LOCALES:
        p=r.page(lang,width=390); f=p.locator('main figure').first
        f.scroll_into_view_if_needed(); require(f.locator('figcaption:visible').count(),'Figure context hidden')
        require(f.locator('a[href^="http"]:visible').count(),'Figure source hidden')
        go_link(p,application_link(p,lang))
        require(p.locator('html').get_attribute('lang').startswith(lang),'Figure-to-application changes language')
        mail(p)


@case('F2+F5',3,'Figure assets survive language navigation','A decoded figure and its provenance remain available after switching locale and reloading.', 'PROJECT.md#F2-F5')
def t3_figure_route(r):
    p=r.page('ko'); all_imgs_loaded(p)
    source=p.locator('main figure img').first.get_attribute('src')
    links=[x for x in visible_links(p,'body') if urlparse(x['href']).path.rstrip('/')=='/en']
    require(links,'Locale switch missing'); go_link(p,links[0]); p.reload(wait_until='networkidle')
    require(p.locator('main figure img').first.get_attribute('src')==source,'Localized route loses shared figure')
    all_imgs_loaded(p)
    require(p.locator('main figure a[href^="http"]:visible').count(),'Reload loses provenance')


@case('F3+F5',3,'Application route reload and locale equivalence','A bookmarked application page retains preparation and same contact after locale change and reload.', 'PROJECT.md#F3-F5')
def t3_apply_route(r):
    p=r.page('ko','join'); address=mail(p); p.reload(wait_until='networkidle')
    match(text(p),'성적','Application reload loses preparation')
    links=[x for x in visible_links(p,'body') if urlparse(x['href']).path.rstrip('/')=='/en/join']
    require(links,'Join locale counterpart missing'); go_link(p,links[0]); p.reload(wait_until='networkidle')
    require(mail(p)==address,'Join route locale changes contact'); match(text(p),'transcript','English preparation missing')


@case('F3+F6',3,'Applicant edits have a durable scope record','Working public application path is accompanied by a public review of recruitment/application changes and remaining approval boundaries.', 'PROJECT.md#F3-F6')
def t3_apply_record(r):
    p=r.page(); go_link(p,application_link(p,'ko')); mail(p)
    doc=r.doc()
    match(doc,'지원|합류|모집|applica|recruit|join','Public review omits applicant journey changes')
    match(doc,'현재 모집|모집 여부|미확인|승인|PI|opening|approval','Applicant review omits uncertainty/approval boundary')


@case('F4+F6',3,'Responsive evidence records actual target widths','Public review records the 320/390/1440 browser conditions whose homepage behavior is reproducible.', 'PROJECT.md#F4-F6')
def t3_responsive_record(r):
    doc=r.doc()
    for width in (320,390,1440):
        match(doc,str(width),f'Public review omits responsive condition {width}')
        p=r.page('ko',width=width); no_overflow(p)
    match(doc,'한국어|한영|한·영|KO|Korean','Review does not identify locale validation')


@case('F5+F6',3,'Reproducible verification points to current public route contract','Documented verification references coexist with reachable locale core routes and the canonical record indexes the same revision.', 'PROJECT.md#F5-F6')
def t3_route_record(r):
    doc=r.doc()
    match(doc,'npm run build|TEST_READY|TEST_INFRA|run_e2e|검증 보고','Public review lacks reproducible route/build verification reference')
    match(r.doc('docs/research-content-review.md'),'2026-10-20|homepage-editorial-review-2026-10-20','Canonical revision index stale')
    for lang in LOCALES:
        for path in CORE:
            p=r.page(lang,path)
            require(p.locator('html').get_attribute('lang').startswith(lang),'Recorded core locale route invalid')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--url',default='http://127.0.0.1:4389')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--list',action='store_true')
    parser.add_argument('--only',default='')
    args=parser.parse_args()
    specs=[{k:v for k,v in c.items() if k!='fn'} for c in CASES]
    require(len(CASES)==80,f'Expected exactly 80 distinct cases, got {len(CASES)}')
    if args.list:
        print(json.dumps(specs,ensure_ascii=False,indent=2)); return 0
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out=args.output or HERE/'runs'/stamp
    require(not out.exists(),f'Refusing to overwrite prior run evidence {out}')
    out.mkdir(parents=True)
    (out/'coverage.json').write_text(json.dumps(specs,ensure_ascii=False,indent=2))
    results=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=CHROME,headless=True)
        failed_tier = None
        for c in sorted(CASES, key=lambda item: item['tier']):
            if failed_tier is not None and c['tier'] > failed_tier:
                continue
            if args.only and args.only not in c['id']: continue
            run=Run(browser,args.url,out); started=time.monotonic()
            item={k:v for k,v in c.items() if k!='fn'}
            try:
                c['fn'](run); item['status']='PASS'
            except Exception as error:
                item['status']='FAIL'; item['error']=str(error); item['traceback']=traceback.format_exc()
                failed_tier = c['tier']
                for idx,ctx in enumerate(run.contexts):
                    for j,p in enumerate(ctx.pages):
                        try: p.screenshot(path=str(out/f'{c["id"]}-ctx{idx}-page{j}.png'),full_page=True)
                        except Exception: pass
            finally:
                item['seconds']=round(time.monotonic()-started,3); item['pageerrors']=run.events
                item['visits']=run.visits
                run.close()
            results.append(item)
            print(f'{item["status"]} {item["id"]} {item["title"]}'+(' :: '+item['error'] if 'error' in item else ''),flush=True)
            (out/'results.partial.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
        browser.close()
    counts=dict(Counter(x['status'] for x in results))
    report={'created_utc':stamp,'url':args.url,'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'counts':counts,'tiers':dict(Counter(str(x['tier']) for x in results)),
            'public_document_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in (REVIEW,GUIDE,'docs/research-content-review.md','public/assets/site/README.md') if (ROOT/name).exists()},
            'independence':'Expected outputs derived from original request, PROJECT and public requirements; no implementation code/report used.',
            'limitations':['Browser presence/behavior checks do not prove scientific source validity, translation equivalence, visual excellence, recruitment conversion or world ranking.','External source availability not crawled; HTTP(S) presence and public documentation provenance only.','No deployment assertion.'],
            'not_run':[c['id'] for c in specs if c['id'] not in {x['id'] for x in results}],
            'halted_after_failed_tier':failed_tier, 'cases':results}
    (out/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({'output':str(out),'counts':counts,'tiers':report['tiers']},ensure_ascii=False))
    return 1 if counts.get('FAIL') else 0


if __name__=='__main__':
    sys.exit(main())
