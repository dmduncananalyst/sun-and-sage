"""Import the supplied four-page editorial PDF without shortening its article."""
from pathlib import Path
import hashlib,html,json,re,shutil,struct,sys
import xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from pypdf import PdfReader
from multilingual.site import ROOT,strip_integration
from scripts.implement_october_audit import meta

PDF=Path('C:/Users/Owner/Downloads/DommyDom_REVISED_WITH_REFERENCES.pdf')
PHOTO=Path('C:/Users/Owner/OneDrive/Desktop/Luxury Living Room at Sunset.png')
PATH='blog-midterm-rentals-los-angeles.html'
IMAGE='assets/blogs/dommydom_midterm_rentals.png'
TITLE='Midterm Rentals in Los Angeles: What Owners and Renters Should Know'
HEADINGS=['A home between a hotel stay and an annual lease','What extended stay renters actually notice','The San Fernando Valley has different kinds of demand','Why a higher monthly rate is not the same as higher profit','Rules, insurance, and clear expectations','Making the home genuinely ready for someone to live in']

def normalize(value):return ' '.join(value.split())

def extract():
    reader=PdfReader(PDF);assert len(reader.pages)==4
    layout=[re.sub(r'^Original editorial draft for local review.*$','',p.extract_text(extraction_mode='layout'),flags=re.M).strip() for p in reader.pages]
    first=layout[0][layout[0].index(HEADINGS[0]):]
    third=layout[2].split('Developer instructions')[0].strip()
    body=first+'\n\n'+layout[1].rstrip()+' '+third
    blocks=[normalize(b) for b in re.split(r'\n\s*\n',body) if b.strip()]
    assert [b for b in blocks if b in HEADINGS]==HEADINGS
    description=normalize(layout[0].split('SEO meta description:')[1].split(HEADINGS[0])[0])
    refs=layout[3].split('Developer placement:')[0]
    refs=[normalize(b) for b in re.split(r'\n\s*\n',refs) if b.strip()][2:]
    assert len(refs)==12 and all(refs[i].startswith('https://') for i in [1,4,7,10])
    references=[{'title':refs[i],'url':refs[i+1],'description':refs[i+2]} for i in range(0,12,3)]
    assert not re.search(r'[\u2013\u2014]', ''.join(blocks))
    return blocks,description,references

def context_links(text):
    value=html.escape(text)
    for words,target in [('Furnished monthly rentals','property-management.html'),('local restrictions','blog-los-angeles-short-term-rental-rules-2026.html'),('Encino','buy-encino.html'),('Chatsworth','buy-chatsworth.html'),('Sherman Oaks','buy-sherman-oaks.html')]:
        if words in value:
            assert (ROOT/target).exists(),target
            value=value.replace(words,'<a href="'+target+'">'+words+'</a>',1)
    return value

def main():
    blocks,description,references=extract();target=ROOT/PATH
    for existing in ROOT.glob('blog-*.html'):
        source=existing.read_text(encoding='utf-8');heading=re.search(r'<h1\b[^>]*>(.*?)</h1>',source,re.S)
        if heading and normalize(html.unescape(re.sub('<[^>]*>','',heading[1]))).casefold()==TITLE.casefold() and existing!=target:
            raise RuntimeError('Duplicate article already exists: '+existing.name)
    state=ROOT/'.translation-state/midterm-before-import';state.mkdir(parents=True,exist_ok=True)
    for name in ['blog.html','sitemap-en.xml']:
        if not (state/name).exists():shutil.copy2(ROOT/name,state/name)
    (ROOT/IMAGE).parent.mkdir(parents=True,exist_ok=True)
    if (ROOT/IMAGE).exists():assert (ROOT/IMAGE).read_bytes()==PHOTO.read_bytes(),'Assigned filename already contains a different image'
    else:shutil.copy2(PHOTO,ROOT/IMAGE)
    raw=PHOTO.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n';width,height=struct.unpack('>II',raw[16:24])
    copy=[]
    for block in blocks:
        copy.append('<h2>'+html.escape(block)+'</h2>' if block in HEADINGS else '<p>'+context_links(block)+'</p>')
    copy.append('<section class="ss4711-section" id="sources-and-references"><h2>Sources and References</h2><ul>'+''.join('<li><a href="'+html.escape(r['url'],quote=True)+'" target="_blank" rel="noopener noreferrer">'+html.escape(r['title'])+'</a><p>'+html.escape(r['description'])+'</p></li>' for r in references)+'<li><a href="https://housing.lacity.gov/" target="_blank" rel="noopener noreferrer">City of Los Angeles Housing Department</a></li><li><a href="https://planning.lacity.gov/" target="_blank" rel="noopener noreferrer">Los Angeles City Planning</a></li></ul></section>')
    caption='Illustrative AI image, not a photograph of a specific listing.'
    alt='Illustrative AI image of a furnished living room overlooking Los Angeles at sunset'
    article='<main class="ss4711-article oct12-blog-article dommydom-new-blog" id="main"><header class="ss4711-title"><h1>'+TITLE+'</h1><div class="ss4711-date">October 20, 2026</div></header><figure class="ss4711-photo midterm-hero" data-full-photo-frame="true"><img src="'+IMAGE+'" alt="'+alt+'" width="'+str(width)+'" height="'+str(height)+'" loading="eager" fetchpriority="high" decoding="async" data-full-photo="true"><figcaption>'+caption+'</figcaption></figure><article class="ss4711-copy">'+''.join(copy)+'</article><p class="midterm-back"><a href="blog.html">Blog</a></p></main>'
    template=strip_integration((ROOT/'blog-living-in-porter-ranch.html').read_text(encoding='utf-8'))
    template=re.sub(r'<main\b.*?</main>',lambda _:article,template,count=1,flags=re.S)
    template=re.sub(r'<title>.*?</title>',lambda _:'<title>'+TITLE+' | Dominique Duncan-Nelson</title>',template,count=1,flags=re.S)
    canonical='https://dommydom.com/'+PATH
    template=re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>',lambda _:'<link rel="canonical" href="'+canonical+'">',template,flags=re.I)
    for name,value in [('description',description),('og:title',TITLE),('og:description',description),('og:url',canonical),('og:image','https://dommydom.com/'+IMAGE),('twitter:title',TITLE),('twitter:description',description),('twitter:image','https://dommydom.com/'+IMAGE)]:template=meta(template,name,value)
    template=re.sub(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>.*?</script>','',template,flags=re.S)
    schema={'@context':'https://schema.org','@type':'BlogPosting','headline':TITLE,'description':description,'url':canonical,'mainEntityOfPage':canonical,'image':{'@type':'ImageObject','url':'https://dommydom.com/'+IMAGE,'width':width,'height':height,'caption':caption},'articleBody':'\n\n'.join(blocks),'datePublished':'2026-10-20','dateModified':'2026-10-20','inLanguage':'en','author':{'@type':'Person','name':'Dominique Duncan-Nelson','url':'https://dommydom.com/about.html'},'citation':[r['url'] for r in references]}
    # The complete body is in the article itself; avoid billing again for a
    # second, concatenated copy of those same paragraphs in structured data.
    schema.pop('articleBody')
    template=template.replace('</head>','<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script><link rel="stylesheet" href="assets/midterm-blog.css"></head>',1)
    if target.exists():assert target.read_text(encoding='utf-8')==template,'Article already exists with changes, refusing overwrite'
    else:target.write_text(template,encoding='utf-8')
    archive=ROOT/'blog.html';text=archive.read_text(encoding='utf-8')
    if 'data-midterm-article="true"' not in text:
        preview=description
        card='<article class="loanHubItem" data-midterm-article="true"><a class="ss18-card-photo v27-photo-frame" href="'+PATH+'"><img src="'+IMAGE+'" alt="'+alt+'" width="'+str(width)+'" height="'+str(height)+'" loading="lazy" decoding="async"></a><div class="final-static-answer"><div class="topic">Posted October 20, 2026</div><h2>'+TITLE+'</h2><div class="final-static-answer-copy"><p>'+html.escape(preview)+'</p></div></div><div class="loanLearn"><a href="'+PATH+'">Read More →</a></div></article>'
        assert '<div class="loanHubGrid">' in text
        text=text.replace('<div class="loanHubGrid">','<div class="loanHubGrid">'+card,1)
    if 'href="assets/midterm-blog.css"' not in text:text=text.replace('</head>','<link rel="stylesheet" href="assets/midterm-blog.css"></head>',1)
    archive.write_text(text,encoding='utf-8')
    sitemap=ROOT/'sitemap-en.xml';tree=ET.parse(sitemap);ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
    if canonical not in {n.text for n in tree.iter(ns+'loc')}:ET.SubElement(ET.SubElement(tree.getroot(),ns+'url'),ns+'loc').text=canonical
    ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9');tree.write(sitemap,encoding='utf-8',xml_declaration=True)
    manifest={'source_pdf':str(PDF),'pdf_pages_read':4,'title':TITLE,'path':PATH,'image':IMAGE,'image_source':str(PHOTO),'image_sha256':hashlib.sha256(raw).hexdigest(),'image_width':width,'image_height':height,'description':description,'blocks':blocks,'headings':HEADINGS,'references':references,'illustration_disclosure':caption,'local_only':True,'published':False}
    (ROOT/'multilingual/midterm-editorial-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'created_article':PATH,'headings':len(HEADINGS),'paragraphs':sum(b not in HEADINGS for b in blocks),'references':len(references),'exact_original_png_preserved':True,'image_dimensions':[width,height]},indent=2))

if __name__=='__main__':main()
