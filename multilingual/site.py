"""Lossless HTML localization: edit source spans, never reserialize scripts or styles."""
import argparse
import hashlib
import html
from functools import lru_cache
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'multilingual/config.json').read_text(encoding='utf-8'))
ATTRS = {'alt', 'title', 'placeholder', 'aria-label', 'aria-description'}
SKIP = {'script', 'style', 'code', 'pre', 'svg'}
JSON_TEXT_KEYS = {'button','intro','prompt','options','title','submitText','emailLabel','contactHeading','label','line','headline','description','articleBody','text','name','caption','alternativeHeadline'}
JSON_SCRIPT = re.compile(r'(<script\b[^>]*type=["\']application/(?:ld\+)?json["\'][^>]*>)(.*?)(</script>)',re.S|re.I)

def json_strings(value, callback, name=''):
    if isinstance(value,dict):return {k:json_strings(v,callback,k) for k,v in value.items()}
    if isinstance(value,list):return [json_strings(v,callback,name) for v in value]
    if isinstance(value,str) and name in JSON_TEXT_KEYS and words(value):return callback(value)
    return value

def key(text, language, source='en'):
    return hashlib.sha256((source + '\0' + language + '\0' + text).encode()).hexdigest()

def words(text):
    return bool(re.search(r'[A-Za-z]', text)) and not re.fullmatch(r'[\w.+-]+@[\w.-]+|https?://\S+', text)

class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source, self.spans, self.stack = source, [], []
        self.offsets = [0]
        for line in source.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.feed(source)

    def pos(self):
        line, col = self.getpos()
        return self.offsets[line - 1] + col

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        raw, start = self.get_starttag_text(), self.pos()
        blocked = any(x[1] for x in self.stack) or tag in SKIP or attrs.get('translate') == 'no'
        if not blocked:
            for match in re.finditer(r'''([\w:-]+)\s*=\s*(["'])(.*?)\2''', raw, re.S):
                name, value = match[1].lower(), html.unescape(match[3])
                meta = tag == 'meta' and name == 'content' and (attrs.get('name') in {'description','twitter:title','twitter:description'} or attrs.get('property') in {'og:title','og:description','og:site_name'})
                if (name in ATTRS or meta or (tag == 'input' and attrs.get('type') in {'button','submit'} and name == 'value')) and words(value):
                    self.spans.append((start+match.start(3),start+match.end(3),value,True))
        if tag not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            self.stack.append((tag, blocked))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if any(x[1] for x in self.stack):
            return
        text = html.unescape(data.strip())
        if words(text):
            a = self.pos() + len(data) - len(data.lstrip())
            self.spans.append((a, a + len(data.strip()), text, False))

@lru_cache(maxsize=512)
def document_spans(source):
    return tuple(Document(source).spans)

def pages(root=ROOT):
    # The existing sitemap is the publishing inventory, not audit copies or redirects.
    tree = ET.parse(root / 'sitemap.xml')
    if tree.getroot().tag.endswith('sitemapindex'):
        # After integration the root sitemap indexes all locales. Preserve the
        # complete English publishing inventory, including retained URL aliases.
        tree=ET.parse(root/'sitemap-en.xml')
    found = set()
    for node in tree.iter():
        if node.tag.endswith('}loc'):
            path = urlsplit(node.text).path.lstrip('/') or 'index.html'
            if (root/path).is_file() and path.endswith('.html'):
                found.add(path)
    # New English pages/blogs enter automatically, including nested content folders.
    for folder in ['', 'blog', 'life-changes', 'design-questions', 'short-term-rental-questions']:
        for path in (root/folder).glob('*.html'):
            if not re.search(r'<meta[^>]+http-equiv=["\']refresh', path.read_text(encoding='utf-8'), re.I):
                found.add(path.relative_to(root).as_posix())
    return sorted(found)

def dynamic_strings(root=ROOT):
    result = {'Language','Messages and voice','Your message','Communication unavailable. Please try again.','Original message','Listen','Voice translation unavailable.','Call segment ended. Select Start translated call to continue.','Language preference could not be saved.','Send message','Refresh messages','Record voice message','Send voice message','Start translated call','Stop','Sign in to view your messages.'}
    result.update({'Please fill out this field.','Please enter a valid email address.','Please match the requested format.','Please enter a value in the allowed range.','Please check this value.'})
    for path in (root/'assets').glob('*.js'):
        if path.name.startswith('multilingual'):
            continue
        source = path.read_text(encoding='utf-8')
        # Literal UI copy and text inside JS-generated HTML; code is never rewritten.
        for match in re.finditer(r'''(["'`])((?:\\.|(?!\1).)*?)\1''', source, re.S):
            text = match[2]
            if '<' in text and '>' in text:
                result.update(s[2] for s in Document(text).spans if '${' not in s[2])
            elif words(text) and not re.search(r'[{}<>\\]|\$\{|https?://', text) and ((' ' in text and len(text)<1000) or text in {'Continue','Back','Menu','Close','Sending…','Submit','Search','Other'}):
                result.add(text)
    for path in pages(root):
        source = (root/path).read_text(encoding='utf-8')
        for match in JSON_SCRIPT.finditer(source):
            try:
                obj = json.loads(match[2])
            except ValueError:
                continue
            json_strings(obj,lambda value:result.add(value) or value)
        for inline in re.finditer(r'<script\b(?![^>]*\bsrc=)[^>]*>(.*?)</script>',source,re.S|re.I):
            if re.search(r'^\s*[\[{]',inline[1]):continue
            for match in re.finditer(r'''"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`''',inline[1]):
                value=match[0][1:-1]
                if words(value) and ' ' in value and len(value)<500 and not re.search(r'[{}<>\\]|https?://',value):result.add(value)
    return result

def inventory(root=ROOT):
    texts = dynamic_strings(root)
    listing = pages(root)
    for path in listing:
        texts.update(s[2] for s in document_spans((root/path).read_text(encoding='utf-8')))
    return listing, sorted(texts)

def translated(text, language, cache):
    return cache[key(text, language)]

def copy_if_changed(source,destination):
    """Avoid rewriting large unchanged photos/videos during incremental builds."""
    source,destination=Path(source),Path(destination)
    if destination.is_file():
        a,b=source.stat(),destination.stat()
        if a.st_size==b.st_size and a.st_mtime_ns==b.st_mtime_ns:return str(destination)
    return shutil.copy2(source,destination)

def local_url(path, language):
    return '/' + (language+'/' if language != 'en' else '') + ('' if path == 'index.html' else path)

def strip_integration(source):
    return re.sub(r'<!-- dommydom-i18n:(head|selector):start -->.*?<!-- dommydom-i18n:\1:end -->','',source,flags=re.S)

def integration(path,language,cache):
    origin=CONFIG['origin']
    head=''.join(f'<link rel="alternate" hreflang="{lang}" href="{origin}{local_url(path,lang)}">' for lang in CONFIG['languages'])
    head+=f'<link rel="alternate" hreflang="x-default" href="{origin}{local_url(path,"en")}">'
    manifest={'language':language,'path':path,'rootPrefix':'../'*(path.count('/')+(language!='en')) or './','languages':CONFIG['languages'],'api':CONFIG['communications_api']}
    head+='<link rel="stylesheet" href="assets/multilingual.css?v=header-globe-v3"><link rel="stylesheet" href="assets/audit-corrections.css"><script id="dommydom-locale" type="application/json">'+json.dumps(manifest,ensure_ascii=False).replace('<','\\u003c')+'</script>'
    if language!='en':head+=f'<script src="assets/locales/{language}.js"></script>'
    head+='<script defer src="assets/multilingual.js?v=header-globe-v3"></script>'
    if CONFIG['communications_api']:head+='<script defer src="assets/multilingual-communications.js"></script>'
    label='Language' if language=='en' else cache.get(key('Language',language),'Language')
    options=''.join('<option value="'+code+'"'+(' selected' if code==language else '')+'>'+html.escape(name)+'</option>' for code,name in CONFIG['languages'].items())
    globe='<svg aria-hidden="true" focusable="false" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6.5h14M5 17.5h14"/></svg>'
    selector='<div class="dd-language-selector" translate="no">'+globe+'<select id="dd-language" name="website-language" aria-label="'+html.escape(label)+'">'+options+'</select></div>'
    return '<!-- dommydom-i18n:head:start -->'+head+'<!-- dommydom-i18n:head:end -->','<!-- dommydom-i18n:selector:start -->'+selector+'<!-- dommydom-i18n:selector:end -->'

def place_selector(source,selector):
    search=re.search(r'<a\b[^>]*class=["\'][^"\']*\bdd-search\b[^"\']*["\'][^>]*>.*?</a>',source,re.S|re.I)
    if search:return source[:search.end()]+selector+source[search.end():]
    closing=re.search(r'</header\s*>',source,re.I)
    if closing:return source[:closing.end()]+selector+source[closing.end():]
    opening=re.search(r'<body\b[^>]*>',source,re.I)
    if not opening:raise RuntimeError('Cannot place language selector: page has no body')
    return source[:opening.end()]+selector+source[opening.end():]

def set_html_language(source,language):
    def replace(match):
        tag=re.sub(r'''\s+(?:lang|dir)\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)''','',match[0][:-1],flags=re.I).rstrip()
        return tag+f' lang="{language}" dir="{"rtl" if language in CONFIG["rtl"] else "ltr"}">'
    return re.sub(r'<html\b[^>]*>',replace,source,count=1,flags=re.I)

def render(source, path, language, cache, listing):
    source=strip_integration(source)
    origin = CONFIG['origin']
    original_base=re.search(r'<base\b[^>]*href=["\']([^"\']*)',source,re.I)
    source_base=urljoin(origin+'/'+path,original_base[1]) if original_base else origin+'/'+path
    if language != 'en':
        for a,b,text,attribute in reversed(document_spans(source)):
            source = source[:a] + html.escape(translated(text,language,cache), quote=attribute) + source[b:]
        def localize_json(match):
            try:obj=json.loads(match[2])
            except ValueError:return match[0]
            localized=json_strings(obj,lambda text:translated(text,language,cache))
            def localized_urls(value):
                if isinstance(value,list):return [localized_urls(v) for v in value]
                if isinstance(value,dict):
                    result={k:localized_urls(v) for k,v in value.items()}
                    if 'inLanguage' in result:result['inLanguage']=language
                    return result
                if isinstance(value,str) and value.startswith(origin+'/'):
                    parsed=urlsplit(value);target=parsed.path.lstrip('/') or 'index.html'
                    if target in listing:return origin+local_url(target,language)+('#'+parsed.fragment if parsed.fragment else '')
                return value
            localized=localized_urls(localized)
            return match[1]+json.dumps(localized,ensure_ascii=False).replace('<','\\u003c')+match[3]
        source=JSON_SCRIPT.sub(localize_json,source)
        # A legacy homepage listener assigns its English title after load.
        # Localize that literal as well as the static title element.
        def title_literal(match):
            value=match[3]
            return match[1]+json.dumps(cache.get(key(value,language),value),ensure_ascii=False)
        source=re.sub(r'''(document\.title\s*=\s*)(["'])(.*?)\2''',title_literal,source)
    source = re.sub(r'<link\b[^>]*\brel=["\'](?:canonical|alternate)["\'][^>]*>', '', source, flags=re.I)
    source = set_html_language(source,language)
    # Root absolute resource paths keep CSS, JS, images and fetches correct in nested locales.
    def link(match):
        name, quote, value = match[1], match[2], html.unescape(match[3])
        if value.startswith(('#','mailto:','tel:','data:','javascript:','//')):
            return match[0]
        resolved = urlsplit(urljoin(source_base, value))
        if resolved.netloc != urlsplit(origin).netloc:
            return match[0]
        target = resolved.path.lstrip('/') or 'index.html'
        suffix = ('?'+resolved.query if resolved.query else '') + ('#'+resolved.fragment if resolved.fragment else '')
        if name.lower() == 'href' and target in listing:
            value = (language+'/' if language!='en' else '')+target+suffix
        else:
            value = target+suffix
        return name+'='+quote+html.escape(value,quote=True)+quote
    # Restrict URL edits to actual tags, never inline JavaScript strings.
    source = re.sub(r'<(?:a|link|script|img|source|video|audio|form)\b[^>]*>', lambda m: re.sub(r'''\b(href|src|poster|action)\s*=\s*(["'])(.*?)\2''',link,m[0],flags=re.I), source,flags=re.I)
    def srcset(match):
        items=[]
        for part in match[2].split(','):
            tokens=part.strip().split()
            if not tokens:continue
            resolved=urlsplit(urljoin(source_base,tokens[0]))
            if resolved.netloc==urlsplit(origin).netloc:tokens[0]=resolved.path.lstrip('/')
            items.append(' '.join(tokens))
        return match[1]+'="'+', '.join(items)+'"'
    source = re.sub(r'\b(srcset|imagesrcset)="([^"]*)"',srcset,source)
    source = re.sub(r'url\((["\']?)/assets/', r'url(\1assets/',source)
    def seo_url(match):
        if not re.search(r'(?:property|name)=["\'](?:og:url|twitter:url)["\']',match[0],re.I):return match[0]
        return re.sub(r'content=(["\']).*?\1',lambda _: 'content="'+origin+local_url(path,language)+'"',match[0],flags=re.S)
    source=re.sub(r'<meta\b[^>]*>',seo_url,source,flags=re.I)
    source = re.sub(r'<base\b[^>]*>', '', source, flags=re.I)
    root_prefix='../'*(path.count('/')+(language!='en')) or './'
    source=re.sub(r'<head\b[^>]*>',lambda m:m[0]+f'<base href="{root_prefix}">',source,count=1,flags=re.I)
    seo = f'<link rel="canonical" href="{origin}{local_url(path,language)}">'
    head,selector=integration(path,language,cache)
    return place_selector(source.replace('</head>',seo+head+'</head>',1),selector)

def build(root=ROOT, output=None):
    listing,texts = inventory(root)
    cache = json.loads((root/'multilingual/translations.json').read_text(encoding='utf-8'))
    missing = [(lang,text) for lang in CONFIG['languages'] if lang!='en' for text in texts if key(text,lang) not in cache]
    if missing:
        raise RuntimeError(f'{len(missing)} translations missing; refusing partial multilingual publication')
    output = output or root/'dist'
    output.mkdir(exist_ok=True,parents=True)
    sources={path:(root/path).read_text(encoding='utf-8') for path in listing}
    shutil.copytree(root/'assets',output/'assets',dirs_exist_ok=True,copy_function=copy_if_changed)
    for media in root.iterdir():
        if media.is_file() and media.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.gif','.svg','.pdf','.mp4','.webm','.ico','.woff','.woff2'}:
            copy_if_changed(media,output/media.name)
    # Preserve published redirect aliases as well as canonical content.
    for folder in ['', 'blog', 'life-changes', 'design-questions', 'short-term-rental-questions']:
        for alias in (root/folder).glob('*.html'):
            relative=alias.relative_to(root)
            if relative.as_posix() not in listing:
                dest=output/relative;dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(alias,dest)
    for name in ['CNAME','favicon.svg','robots.txt','llms.txt']:
        if (root/name).exists(): shutil.copy2(root/name,output/name)
    for lang in CONFIG['languages']:
        urls=[]
        for path in listing:
            destination=output/(lang if lang!='en' else '')/path
            destination.parent.mkdir(parents=True,exist_ok=True)
            destination.write_text(render(sources[path],path,lang,cache,listing),encoding='utf-8')
            urls.append(CONFIG['origin']+local_url(path,lang))
        sitemap=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
        for url in urls: ET.SubElement(ET.SubElement(sitemap,'url'),'loc').text=url
        ET.ElementTree(sitemap).write(output/f'sitemap-{lang}.xml',encoding='utf-8',xml_declaration=True)
        if lang!='en':
            folder=output/'assets/locales'; folder.mkdir(exist_ok=True)
            catalog={text:translated(text,lang,cache) for text in texts}
            (folder/f'{lang}.js').write_text('window.DOMMYDOM_TRANSLATIONS='+json.dumps(catalog,ensure_ascii=False).replace('<','\\u003c')+';',encoding='utf-8')
    index=ET.Element('sitemapindex',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    from .aliases import write_aliases
    write_aliases(output,listing,CONFIG['languages'],CONFIG['origin'])
    for lang in CONFIG['languages']:
        ET.SubElement(ET.SubElement(index,'sitemap'),'loc').text=CONFIG['origin']+f'/sitemap-{lang}.xml'
    ET.ElementTree(index).write(output/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    return {'pages':len(listing),'languages':len(CONFIG['languages']),'saved_translations':len(cache)}

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('command',choices=['audit','build']); args=parser.parse_args()
    if args.command=='build': print(json.dumps(build(),indent=2))
    else:
        listing,texts=inventory(); cache=json.loads((ROOT/'multilingual/translations.json').read_text())
        counts={lang:sum(key(t,lang) in cache for t in texts) for lang in CONFIG['languages'] if lang!='en'}
        report={'english_pages':len(listing),'unique_segments':len(texts),'characters_per_language':sum(map(len,texts)),'cached_segments':counts,'google_project_identified':bool(CONFIG['google_project_id'])}
        print(json.dumps(report,indent=2))
