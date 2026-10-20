"""Apply the supplied six articles and October 18 audit to local English sources."""
import hashlib
import html
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from multilingual.site import ROOT,pages,strip_integration

SOURCE=Path('C:/Users/Owner/Downloads/dommydom_six_blogs_with_photo_filenames.md')
ORIGINAL=Path('C:/Users/Owner/Downloads/dommydom_revised_blogs.md')
SPECS=[
 ('living-in-porter-ranch','dommydom_porter_ranch.jpg','The Vineyards entrance, palm trees, shops and foothills in Porter Ranch',['buy-porter-ranch.html','blog-porter-ranch-housing-market.html']),
 ('living-in-valley-village','dommydom_valley_village.jpg','Valley Village Park sign beside a tree-lined lawn and neighborhood sidewalk',['buy-valley-village.html','blog-studio-city-or-valley-village-which-one-should-i-choose.html']),
 ('living-in-sylmar','dommydom_sylmar.jpg','Water cascading over stepped concrete spillways among rocks and the Sylmar foothills',['buy-sylmar.html','valley-guide-north.html']),
 ('encino-home-prices-2026','dommydom_encino.jpg','Ventura Boulevard street sign, palm trees and businesses in Encino',['buy-encino.html','buyer-question-south-of-ventura-boulevard.html']),
 ('california-earnest-money-deposit','dommydom_earnest_money.jpg','House keys and a gold house-shaped key ring on a purchase agreement beside a pen',['down-payment-needed.html','buyer-closing-costs.html']),
 ('airbnb-aircover-rental-insurance','dommydom_airbnb_insurance.jpg','Furnished rental home with a swimming pool, patio seating and a sun umbrella',['blog-is-my-property-a-good-fit-for-airbnb.html','blog-los-angeles-short-term-rental-rules-2026.html'])
]

def parse():
    text=SOURCE.read_text(encoding='utf-8');original=ORIGINAL.read_text(encoding='utf-8')
    attribution=re.search(r'\*\*Author attribution for every article:\*\* (.*)',text)[1]
    note=re.search(r'\*\*Editorial note:\*\* (.*)',text)[1]
    articles=[]
    for index,part in enumerate(re.split(r'^## ',text,flags=re.M)[1:]):
        title,body=part.split('\n',1);body=body.split('\n---\n')[0]
        filename=re.search(r'\*\*Featured photo filename:\*\* `([^`]+)`',body)[1]
        assert filename==SPECS[index][1]
        assert re.search(r'\*\*Blog card photo filename:\*\* `([^`]+)`',body)[1]==filename
        description=re.search(r'\*\*Meta description:\*\* (.*)',body)[1]
        resources=[s.strip() for s in re.search(r'\*\*Resources:\*\* (.*)',body)[1].split(' ; ')]
        cleaned=re.sub(r'^\*\*(?:Featured photo filename|Blog card photo filename|Image instructions|Meta description|Resources):\*\*.*$','',body,flags=re.M).strip()
        blocks=[x.strip() for x in re.split(r'\n\s*\n',cleaned) if x.strip()]
        paragraphs=[x for x in blocks if not x.startswith('### ')]
        assert all(p in original for p in paragraphs),'Article text differs from the supplied revised Markdown'
        assert title in original and description in original
        slug,_,alt,related=SPECS[index]
        articles.append({'title':title.strip(),'path':'blog-'+slug+'.html','image':'assets/blogs/'+filename,'alt':alt,'description':description,'blocks':blocks,'paragraphs':paragraphs,'resources':resources,'author':attribution,'editorial_note':note,'related':related})
    assert len(articles)==6
    return articles

def meta(source,name,value):
    found=False
    def replace(match):
        nonlocal found
        tag=match[0]
        if re.search(r'(?:name|property)=["\']'+re.escape(name)+r'["\']',tag,re.I):
            found=True
            return re.sub(r'content=(["\']).*?\1','content="'+html.escape(value,quote=True)+'"',tag,flags=re.S)
        return tag
    source=re.sub(r'<meta\b[^>]*>',replace,source,flags=re.I)
    if not found:source=source.replace('</head>',f'<meta name="{name}" content="{html.escape(value,quote=True)}"></head>',1)
    return source

def article_html(article,template):
    e=html.escape
    copy=[];section=[]
    for block in article['blocks']:
        if block.startswith('### '):
            if section:copy.append('<section class="ss4711-section">'+''.join(section)+'</section>')
            heading,*paragraphs=block[4:].split('\n',1)
            section=['<h2>'+e(heading)+'</h2>']
            if paragraphs:section.append('<p>'+e(paragraphs[0])+'</p>')
        else:section.append('<p>'+e(block)+'</p>')
    if section:copy.append('<section class="ss4711-section">'+''.join(section)+'</section>')
    copy.append('<section class="ss4711-section source-reference-links" id="references"><h2>Resources</h2><ul>'+''.join('<li><a href="'+e(url,quote=True)+'" target="_blank" rel="noopener noreferrer">'+e(url)+'</a></li>' for url in article['resources'])+'</ul></section>')
    copy.append('<section class="ss4711-section article-attribution"><p>'+e(article['author'])+'</p><p>'+e(article['editorial_note'])+'</p></section>')
    related=[]
    for path in article['related']:
        assert (ROOT/path).exists(),path
        text=(ROOT/path).read_text(encoding='utf-8');heading=re.search(r'<h1\b[^>]*>(.*?)</h1>',text,re.S)
        label=html.unescape(re.sub('<[^>]+>','',heading[1])) if heading else path
        related.append('<li><a href="'+path+'">'+e(label)+'</a></li>')
    copy.append('<section class="ss4711-section"><h2>Related reading</h2><ul>'+''.join(related)+'</ul><p><a href="blog.html">Blog</a></p></section>')
    main='<main class="ss4711-article oct12-blog-article dommydom-new-blog" id="main"><header class="ss4711-title"><h1>'+e(article['title'])+'</h1><div class="ss4711-date">October 20, 2026</div></header><figure class="ss4711-photo" data-full-photo-frame="true"><img src="'+article['image']+'" alt="'+e(article['alt'],quote=True)+'" width="1800" height="1500" loading="eager" fetchpriority="high" decoding="async" data-full-photo="true"></figure><article class="ss4711-copy">'+''.join(copy)+'</article></main>'
    source=strip_integration(template)
    source=re.sub(r'<main\b.*?</main>',lambda _:main,source,count=1,flags=re.S)
    source=re.sub(r'<title>.*?</title>',lambda _:'<title>'+e(article['title'])+' | Dominique Duncan-Nelson</title>',source,count=1,flags=re.S)
    canonical='https://dommydom.com/'+article['path']
    source=re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>',lambda _:'<link rel="canonical" href="'+canonical+'">',source,flags=re.I)
    for name,value in [('description',article['description']),('og:title',article['title']),('og:description',article['description']),('og:url',canonical),('og:image','https://dommydom.com/'+article['image']),('twitter:title',article['title']),('twitter:description',article['description']),('twitter:image','https://dommydom.com/'+article['image'])]:source=meta(source,name,value)
    source=re.sub(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>','',source,flags=re.S)
    schema={'@context':'https://schema.org','@type':'BlogPosting','headline':article['title'],'description':article['description'],'url':canonical,'mainEntityOfPage':canonical,'image':'https://dommydom.com/'+article['image'],'datePublished':'2026-10-20','dateModified':'2026-10-20','inLanguage':'en','author':{'@type':'Person','name':'Dominique Duncan-Nelson','url':'https://dommydom.com/about.html'}}
    source=source.replace('</head>','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script><link rel="stylesheet" href="assets/audit-corrections.css"></head>',1)
    source=re.sub(r'<link\b[^>]*as=["\']image["\'][^>]*>','',source,flags=re.I)
    return source

def card(article):
    e=html.escape
    return '<article class="loanHubItem" data-editorial-batch="20261020"><a class="ss18-card-photo v27-photo-frame" data-full-photo-frame="true" href="'+article['path']+'"><img src="'+article['image']+'" alt="'+e(article['alt'],quote=True)+'" width="1800" height="1500" loading="lazy" decoding="async" data-full-photo="true"></a><div class="final-static-answer"><div class="topic">Posted October 20, 2026</div><h2>'+e(article['title'])+'</h2><div class="final-static-answer-copy"><p>'+e(article['paragraphs'][0])+'</p></div></div><div class="loanLearn"><a href="'+article['path']+'">Read More →</a></div></article>'

def main():
    articles=parse();template=(ROOT/'blog-living-in-chatsworth.html').read_text(encoding='utf-8')
    existing={}
    for path in ROOT.glob('blog-*.html'):
        source=path.read_text(encoding='utf-8');h1=re.search(r'<h1\b[^>]*>(.*?)</h1>',source,re.S)
        if h1:existing[html.unescape(re.sub('<[^>]+>','',h1[1])).strip().casefold()]=path.name
    for article in articles:
        duplicate=existing.get(article['title'].casefold())
        target=ROOT/article['path']
        if duplicate and duplicate!=article['path']:raise RuntimeError('Duplicate article: '+duplicate)
        if target.exists():
            text=html.unescape(re.sub('<[^>]+>',' ',target.read_text(encoding='utf-8')))
            assert all(p in text for p in article['paragraphs']),'Existing article differs; refusing overwrite: '+target.name
        else:target.write_text(article_html(article,template),encoding='utf-8')
    archive=ROOT/'blog.html';source=archive.read_text(encoding='utf-8')
    cards=''.join(card(a) for a in articles if ('href="'+a['path']+'"') not in source)
    source=source.replace('<div class="loanHubGrid">','<div class="loanHubGrid">'+cards,1);archive.write_text(source,encoding='utf-8')
    alts={'assets/editorial-v16/social-preview.webp':'Property marketing preview on a phone beside a printed home brochure','assets/editorial-v16/digital-preview.webp':'Property website preview on a desktop monitor with home and interior photographs','assets/editorial-v16/email-preview.webp':'Property email marketing preview on a tablet showing a home and swimming pool','assets/editorial-v16/evening-showing.webp':'Illuminated home and swimming pool at dusk for an evening property showing','assets/rise-logo.lossless.webp':'Rise Real Estate and Real Brokerage logo'}
    marketing=ROOT/'sell-marketing-your-property.html';text=marketing.read_text(encoding='utf-8');alt_count=0
    def fix_alt(match):
        nonlocal alt_count
        tag=match[0];src=re.search(r'src=["\']([^"\']+)',tag)
        if src and src[1] in alts and re.search(r'alt=["\']["\']',tag):
            alt_count+=1;return re.sub(r'alt=["\']["\']','alt="'+alts[src[1]]+'"',tag)
        return tag
    marketing.write_text(re.sub(r'<img\b[^>]*>',fix_alt,text),encoding='utf-8')
    form_count=0
    for path in pages():
        target=ROOT/path;source=target.read_text(encoding='utf-8')
        def form(match):
            nonlocal form_count
            def required(select):
                nonlocal form_count
                if 'required' in select[0]:return select[0]
                form_count+=1;return select[0][:-1]+' required>'
            return re.sub(r'<select\b[^>]*name=["\']city["\'][^>]*>',required,match[0])
        updated=re.sub(r'<form\b[^>]*data-sun-conversation-form[^>]*>.*?</form>',form,source,flags=re.S)
        def home(match):
            block=match[0]
            block=re.sub(r'<button\b([^>]*)>',lambda m:'<a'+re.sub(r'\s+type=["\']button["\']','',m[1]).replace('class="dd-feature-trigger"','class="dd-feature-trigger dd-home"')+' href="index.html">',block,count=1)
            block=block.replace('</button>','</a>',1).replace('<span>Neighborhoods</span>','<span>Home</span>')
            return block
        updated=re.sub(r'<div class="dd-feature dd-neighborhoods"><button\b.*?</button>',home,updated,flags=re.S)
        if updated!=source:target.write_text(updated,encoding='utf-8')
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';ET.register_namespace('',ns)
    sitemap=ROOT/'sitemap-en.xml';tree=ET.parse(sitemap)
    urls={node.text for node in tree.iter() if node.tag.endswith('}loc')}
    for article in articles:
        url='https://dommydom.com/'+article['path']
        if url not in urls:
            node=ET.SubElement(tree.getroot(),'{'+ns+'}url');ET.SubElement(node,'{'+ns+'}loc').text=url;ET.SubElement(node,'{'+ns+'}lastmod').text='2026-10-20'
    tree.write(sitemap,encoding='utf-8',xml_declaration=True)
    report={'markdown_source':str(SOURCE),'original_revised_content_verified':True,'articles':articles,'duplicate_existing_articles_overwritten':0,'marketing_empty_alt_fixed':alt_count,'search_city_fields_made_required':form_count,'local_only':True,'published':False}
    (ROOT/'multilingual/october-editorial-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'articles_ready':len(articles),'alt_fixed':alt_count,'search_forms_required':form_count,'existing_blogs_overwritten':0}))

if __name__=='__main__':main()
