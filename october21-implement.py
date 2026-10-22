from pathlib import Path
from pypdf import PdfReader
import re,json,html

root=Path(__file__).resolve().parent
out=root/'october21-review';out.mkdir(exist_ok=True)
reader=PdfReader(r'C:\Users\Owner\OneDrive\Desktop\DommyDom_October_21_Revised_Blogs_With_Photo_Assignments.pdf')
(out/'pdf-extracted.txt').write_text('\n\n'.join(p.extract_text() for p in reader.pages),encoding='utf-8')
configs=[('mission-hills',1,4,'buy-mission-hills.html','Mission Hills'),('panorama-city',4,7,'valley-guide-north.html','North Valley'),('sun-valley',7,10,'buy-sun-valley.html','Sun Valley')]
template=(root/'blog-living-in-sylmar.html').read_text(encoding='utf-8')
archive=(root/'blog.html').read_text(encoding='utf-8')
records=[];cards=[]
esc=html.escape
for slug,start,end,related,label in configs:
    chunks=[]
    for page in reader.pages[start:end]:
        page.extract_text(visitor_text=lambda t,cm,tm,f,size: chunks.append((size,t.strip())) if t.strip() else None)
    title=' '.join(t for sz,t in chunks if sz==17)
    description=' '.join(t for sz,t in chunks if sz==9 and 'October 21, 2026' not in t).removeprefix('SEO description: ')
    sections=[];heading=None;lines=[];sources=[];in_sources=False
    for sz,t in chunks:
        if sz in (17,9):continue
        if t=='Sources and references':
            if lines:sections.append((heading,' '.join(lines)));lines=[]
            in_sources=True;continue
        if in_sources:
            if t.startswith('http'):sources.append(t)
            elif sources:sources[-1]+=t
        elif sz==12.5:
            if lines:sections.append((heading,' '.join(lines)));lines=[]
            heading=t
        else:lines.append(t)
    assert len(sections)==7,(slug,len(sections))
    filename=f'blog-living-in-{slug}.html';url='https://dommydom.com/'+filename
    body=''.join('<section class="ss4711-section">'+(f'<h2>{esc(h)}</h2>' if h else '')+f'<p>{esc(p)}</p></section>' for h,p in sections)
    # Wrap existing words in links without changing approved prose.
    if slug!='panorama-city':
        body=body.replace(label,f'<a href="{related}">{label}</a>',1)
    else:body=body.replace('Lake Balboa Park','<a href="blog-lake-balboa-park-japanese-garden-fall-guide.html">Lake Balboa Park</a>',1)
    refs=[]
    for source in sources:
        # Phone is printed directly against the final reference in each PDF article.
        target=source.replace('818-296-6896','')
        refs.append(f'<li><a href="{esc(target,quote=True)}" target="_blank" rel="noopener noreferrer">{esc(target)}</a></li>')
    body+='<section class="ss4711-section source-reference-links" id="references"><h2>Sources and references</h2><ul>'+''.join(refs)+'</ul></section>'
    main=f'<main class="ss4711-article oct12-blog-article dommydom-new-blog october21-article" id="main"><header class="ss4711-title"><h1>{esc(title)}</h1><div class="ss4711-date"><time datetime="2026-10-21">October 21, 2026</time></div></header><article class="ss4711-copy">{body}</article></main>'
    s=re.sub(r'<main\b.*?</main>',lambda m:main,template,flags=re.S)
    s=re.sub(r'<title>.*?</title>',lambda m:f'<title>{esc(title)}</title>',s)
    s=s.replace('https://dommydom.com/blog-living-in-sylmar.html',url)
    s=s.replace('What It Is Really Like to Live in Sylmar',esc(title))
    s=s.replace('Sylmar foothill homes, local history, larger lots, and practical considerations for buyers.',esc(description))
    # No image metadata until the filename discrepancy is resolved.
    s=re.sub(r'<meta[^>]*(?:property="og:image"|name="twitter:image")[^>]*>', '',s)
    schema={'@context':'https://schema.org','@type':'BlogPosting','headline':title,'description':description,'url':url,'mainEntityOfPage':url,'datePublished':'2026-10-21','dateModified':'2026-10-21','inLanguage':'en','author':{'@type':'Person','name':'Dominique Duncan-Nelson','url':'https://dommydom.com/about.html'}}
    s=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:'<script type="application/ld+json">'+json.dumps(schema)+'</script>',s,flags=re.S)
    s=re.sub(r'<link rel="alternate"[^>]*>', '',s)
    s=s.replace('"path": "blog-living-in-sylmar.html"',f'"path": "{filename}"')
    # Keep the approved static workflow and avoid links to nonexistent translations.
    s=re.sub(r'("languages": )\{.*?\}(, "api")',r'\1{"en": "English"}\2',s)
    s=re.sub(r'(<select id="dd-language".*?>).*?(</select>)',r'\1<option value="en" selected>English</option>\2',s,flags=re.S)
    s=s.replace('</head>','<style>.october21-article #references a{overflow-wrap:anywhere}</style></head>')
    (root/filename).write_text(s,encoding='utf-8')
    cards.append(f'<article class="loanHubItem" data-october21="{slug}"><div class="final-static-answer"><div class="topic">Posted October 21, 2026</div><h2>{esc(title)}</h2><div class="final-static-answer-copy"><p>{esc(description)}</p></div></div><div class="loanLearn"><a href="{filename}">Read More →</a></div></article>')
    records.append(dict(slug=slug,title=title,description=description,file=filename,sections=sections,sources=sources,photo='Pending filename assignment confirmation'))
archive=archive.replace('<div class="loanHubGrid">','<div class="loanHubGrid">'+''.join(cards),1)
(root/'blog.html').write_text(archive,encoding='utf-8')
sitemap=(root/'sitemap-en.xml').read_text(encoding='utf-8')
for r in records:
    url='https://dommydom.com/'+r['file']
    assert url not in sitemap
    sitemap=sitemap.replace('</urlset>',f'<url><loc>{url}</loc><lastmod>2026-10-21</lastmod></url></urlset>')
(root/'sitemap-en.xml').write_text(sitemap,encoding='utf-8')
(out/'articles.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('Implemented',[(r['file'],len(' '.join(p for h,p in r['sections']).split())) for r in records])
