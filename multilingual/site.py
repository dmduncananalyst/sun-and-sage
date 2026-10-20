"""Lossless HTML localization: edit source spans, never reserialize scripts or styles."""
import argparse
import hashlib
import html
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

def pages(root=ROOT):
    # The existing sitemap is the publishing inventory, not audit copies or redirects.
    tree = ET.parse(root / 'sitemap.xml')
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
        texts.update(s[2] for s in Document((root/path).read_text(encoding='utf-8')).spans)
    return listing, sorted(texts)

def translated(text, language, cache):
    return cache[key(text, language)]

def local_url(path, language):
    return '/' + (language+'/' if language != 'en' else '') + ('' if path == 'index.html' else path)

def render(source, path, language, cache, listing):
    if language != 'en':
        for a,b,text,attribute in reversed(Document(source).spans):
            source = source[:a] + html.escape(translated(text,language,cache), quote=attribute) + source[b:]
        def localize_json(match):
            try:obj=json.loads(match[2])
            except ValueError:return match[0]
            localized=json_strings(obj,lambda text:translated(text,language,cache))
            return match[1]+json.dumps(localized,ensure_ascii=False).replace('<','\\u003c')+match[3]
        source=JSON_SCRIPT.sub(localize_json,source)
    origin = CONFIG['origin']
    source = re.sub(r'<link\b[^>]*\brel=["\'](?:canonical|alternate)["\'][^>]*>', '', source, flags=re.I)
    source = re.sub(r'<html\b[^>]*>', f'<html lang="{language}" dir="{"rtl" if language in CONFIG["rtl"] else "ltr"}">', source, count=1, flags=re.I)
    # Root absolute resource paths keep CSS, JS, images and fetches correct in nested locales.
    def link(match):
        name, quote, value = match[1], match[2], html.unescape(match[3])
        if value.startswith(('#','mailto:','tel:','data:','javascript:','//')):
            return match[0]
        resolved = urlsplit(urljoin(origin+'/'+path, value))
        if resolved.netloc != urlsplit(origin).netloc:
            return match[0]
        target = resolved.path.lstrip('/') or 'index.html'
        suffix = ('?'+resolved.query if resolved.query else '') + ('#'+resolved.fragment if resolved.fragment else '')
        if name.lower() == 'href' and target in listing:
            value = local_url(target,language)+suffix
        else:
            value = '/'+target+suffix
        return name+'='+quote+html.escape(value,quote=True)+quote
    # Restrict URL edits to actual tags, never inline JavaScript strings.
    source = re.sub(r'<(?:a|link|script|img|source|video|audio|form)\b[^>]*>', lambda m: re.sub(r'''\b(href|src|poster|action)\s*=\s*(["'])(.*?)\2''',link,m[0],flags=re.I), source,flags=re.I)
    source = re.sub(r'\b(srcset|imagesrcset)="([^"]*)"',lambda m:m[1]+'="'+re.sub(r'(?<![\w/])assets/', '/assets/',m[2])+'"',source)
    source = re.sub(r'url\((["\']?)assets/', r'url(\1/assets/',source)
    source = re.sub(r'(<meta[^>]*(?:property|name)=["\'](?:og:url|twitter:url)["\'][^>]*content=)["\'][^"\']*["\']',lambda m:m[1]+'"'+origin+local_url(path,language)+'"',source)
    source = re.sub(r'<base\b[^>]*>', '', source, flags=re.I)
    seo = f'<base href="/"><link rel="canonical" href="{origin}{local_url(path,language)}">'
    seo += ''.join(f'<link rel="alternate" hreflang="{lang}" href="{origin}{local_url(path,lang)}">' for lang in CONFIG['languages'])
    seo += f'<link rel="alternate" hreflang="x-default" href="{origin}{local_url(path,"en")}">'
    manifest = {'language':language,'path':path,'languages':CONFIG['languages'],'api':CONFIG['communications_api']}
    seo += '<link rel="stylesheet" href="/assets/multilingual.css"><script id="dommydom-locale" type="application/json">'+json.dumps(manifest,ensure_ascii=False).replace('<','\\u003c')+'</script>'
    if language != 'en':
        seo += f'<script src="/assets/locales/{language}.js"></script>'
    seo += '<script defer src="/assets/multilingual.js"></script>'
    if CONFIG['communications_api']:
        seo += '<script defer src="/assets/multilingual-communications.js"></script>'
    return source.replace('</head>',seo+'</head>',1)

def build(root=ROOT, output=None):
    listing,texts = inventory(root)
    cache = json.loads((root/'multilingual/translations.json').read_text(encoding='utf-8'))
    missing = [(lang,text) for lang in CONFIG['languages'] if lang!='en' for text in texts if key(text,lang) not in cache]
    if missing:
        raise RuntimeError(f'{len(missing)} translations missing; refusing partial multilingual publication')
    output = output or root/'dist'
    output.mkdir(exist_ok=True,parents=True)
    shutil.copytree(root/'assets',output/'assets',dirs_exist_ok=True)
    for media in root.iterdir():
        if media.is_file() and media.suffix.lower() in {'.png','.jpg','.jpeg','.webp','.gif','.svg','.pdf','.mp4','.webm','.ico','.woff','.woff2'}:
            shutil.copy2(media,output/media.name)
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
            destination.write_text(render((root/path).read_text(encoding='utf-8'),path,lang,cache,listing),encoding='utf-8')
            urls.append(CONFIG['origin']+local_url(path,lang))
        sitemap=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
        for url in urls: ET.SubElement(ET.SubElement(sitemap,'url'),'loc').text=url
        ET.ElementTree(sitemap).write(output/f'sitemap-{lang}.xml',encoding='utf-8',xml_declaration=True)
        if lang!='en':
            folder=output/'assets/locales'; folder.mkdir(exist_ok=True)
            catalog={text:translated(text,lang,cache) for text in texts}
            (folder/f'{lang}.js').write_text('window.DOMMYDOM_TRANSLATIONS='+json.dumps(catalog,ensure_ascii=False).replace('<','\\u003c')+';',encoding='utf-8')
    index=ET.Element('sitemapindex',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
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
