import re,json,html
from pathlib import Path
from PIL import Image,ImageOps
root=Path.cwd(); originals=json.loads((root/'performance-audit/original-invariants.json').read_text());mapping={};changed=[]
for page in originals:
 path=root/page;text=path.read_bytes().decode('utf-8');base=re.search(r'<base\b[^>]*href="([^"]+)"',text,re.I);asset_base=(path.parent/base[1]).resolve() if base else path.parent
 for m in re.finditer(r'<img\b[^>]*\bsrc="([^"]+\.png)"[^>]*>',text,re.I):
  source=(asset_base/html.unescape(m[1])).resolve();candidate=source.with_name(source.stem+'.performance.webp')
  if source.is_file() and source.stat().st_size>=500000 and not candidate.exists() and not any(word in source.name.lower() for word in ['logo','key-script']):
   with Image.open(source) as original:
    if original.getexif().get(274,1)==1:
     kwargs={'lossless':True,'method':3}
     if original.info.get('icc_profile'):kwargs['icc_profile']=original.info['icc_profile']
     original.save(candidate,'WEBP',**kwargs)
  if source in mapping or not source.is_file() or not candidate.is_file() or source.stat().st_size<500000:continue
  with Image.open(source) as a,Image.open(candidate) as b:
   if a.size==b.size and a.info.get('icc_profile')==b.info.get('icc_profile') and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes() and candidate.stat().st_size<source.stat().st_size*.8:mapping[source]=candidate
for page in originals:
 path=root/page;text=path.read_bytes().decode('utf-8');before=text;base=re.search(r'<base\b[^>]*href="([^"]+)"',text,re.I);asset_base=(path.parent/base[1]).resolve() if base else path.parent
 def img(m):
  tag=m[0];src=re.search(r'\bsrc="([^"]+)"',tag);file=(asset_base/html.unescape(src[1])).resolve() if src else None
  if file not in mapping or re.search(r'\bsrcset=',tag):return tag
  import os
  candidate=os.path.relpath(mapping[file],asset_base).replace('\\','/')
  import urllib.parse
  candidate=urllib.parse.quote(candidate,safe='/')
  return tag[:-2]+' srcset="'+candidate+'"/>' if tag.endswith('/>') else tag[:-1]+' srcset="'+candidate+'">'
 # Keep branding assets and navigation outside main untouched.
 text=re.sub(r'(<main\b[^>]*>)(.*?)(</main>)',lambda m:m[1]+re.sub(r'<img\b[^>]*>',img,m[2],flags=re.I)+m[3],text,flags=re.I|re.S)
 def preload(m):
  tag=m[0]
  if 'preload' not in tag or 'image' not in tag or 'imagesrcset=' in tag:return tag
  src=re.search(r'\bhref="([^"]+)"',tag);file=(asset_base/html.unescape(src[1])).resolve() if src else None
  if file not in mapping:return tag
  import os
  candidate=os.path.relpath(mapping[file],asset_base).replace('\\','/')
  import urllib.parse
  candidate=urllib.parse.quote(candidate,safe='/')
  return tag[:-2]+' imagesrcset="'+candidate+'"/>' if tag.endswith('/>') else tag[:-1]+' imagesrcset="'+candidate+'">'
 text=re.sub(r'<link\b[^>]*>',preload,text,flags=re.I)
 if text!=before:path.write_bytes(text.encode('utf-8'));changed.append(page)
report={'modified_pages':changed,'verified_pixel_identical_images':[{'original':str(a.relative_to(root)),'candidate':str(b.relative_to(root)),'original_bytes':a.stat().st_size,'optimized_bytes':b.stat().st_size} for a,b in mapping.items()]}
used=set(mapping.values())
for candidate in root.glob('assets/**/*.performance.webp'):
 if candidate not in used:candidate.unlink()
(root/'performance-audit/lossless-images.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
