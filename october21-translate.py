"""Authorized, incremental local translation of the October 21 blogs only."""
from pathlib import Path
import os,json,re
from concurrent.futures import ThreadPoolExecutor,as_completed
from multilingual.site import CONFIG,document_spans,JSON_SCRIPT,json_strings,key,pages,render,strip_integration
from multilingual import local_generate

root=Path(__file__).resolve().parent
os.environ['CLOUDSDK_CONFIG']=str(root/'.tools/gcloud-profile')
records=json.loads((root/'october21-review/articles.json').read_text(encoding='utf-8'))
paths=[r['file'] for r in records]+['blog.html']
sources={path:(root/path).read_text(encoding='utf-8') for path in paths}
texts=set()
for source in sources.values():
    clean=strip_integration(source)
    texts.update(x[2] for x in document_spans(clean))
    for m in JSON_SCRIPT.finditer(clean):
        json_strings(json.loads(m[2]),lambda t:texts.add(t) or t)
cache=json.loads((root/'multilingual/translations.json').read_text(encoding='utf-8'))
missing=[(lang,t) for lang in CONFIG['languages'] if lang!='en' for t in texts if key(t,lang) not in cache]
cost=sum(len(t) for lang,t in missing)*CONFIG['translation_usd_per_million_characters']/1_000_000
print(json.dumps({'missing_segments':len(missing),'maximum_additional_usd':cost,'local_only':True}),flush=True)
if cost>6:raise RuntimeError('Scoped translation exceeds the approved $6 estimate')
local_generate.initialize()
with ThreadPoolExecutor(max_workers=3) as pool:
    jobs=[pool.submit(local_generate.worker,lang,sorted(texts),True) for lang in CONFIG['languages'] if lang!='en']
    for job in as_completed(jobs):print('Saved:',job.result(),flush=True)
local_generate.checkpoint()
cache=json.loads((root/'multilingual/translations.json').read_text(encoding='utf-8'))
assert all(key(t,lang) in cache for lang in CONFIG['languages'] if lang!='en' for t in texts)
listing=pages(root)
for lang in CONFIG['languages']:
    for path,source in sources.items():
        destination=root/('' if lang=='en' else lang)/path
        destination.write_text(render(source,path,lang,cache,listing),encoding='utf-8')
    if lang=='en':continue
    catalog_path=root/f'assets/locales/{lang}.js'
    existing=catalog_path.read_text(encoding='utf-8')
    catalog=json.loads(existing.removeprefix('window.DOMMYDOM_TRANSLATIONS=').rstrip().removesuffix(';'))
    catalog.update({t:cache[key(t,lang)] for t in texts})
    catalog_path.write_text('window.DOMMYDOM_TRANSLATIONS='+json.dumps(catalog,ensure_ascii=False).replace('<','\\u003c')+';',encoding='utf-8')
    sitemap_path=root/f'sitemap-{lang}.xml';sitemap=sitemap_path.read_text(encoding='utf-8')
    for record in records:
        url=CONFIG['origin']+'/'+lang+'/'+record['file']
        if url not in sitemap:sitemap=sitemap.replace('</urlset>',f'<url><loc>{url}</loc><lastmod>2026-10-21</lastmod></url></urlset>')
    sitemap_path.write_text(sitemap,encoding='utf-8')
(root/'october21-review/translation-generation.json').write_text(json.dumps({'local_only':True,'translated_article_pages':27,'translated_archives':9,'new_translation_segments':len(missing),'maximum_gross_usd':cost,'languages':list(CONFIG['languages']),'published':False},indent=2))
print('Completed 27 translated articles, nine archives, selectors, catalogs and sitemaps.',flush=True)
