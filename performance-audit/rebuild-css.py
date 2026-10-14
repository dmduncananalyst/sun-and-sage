"""Regenerate CSS bundles after editing their original stylesheets. No dependencies."""
import hashlib,json,os,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DIRECTORY=ROOT/'assets/performance-css'
manifest_file=ROOT/'performance-audit/css-bundles.json'
manifest=json.loads(manifest_file.read_text(encoding='utf-8'))
replacements={}; updated={}
for old_name,sources in manifest.items():
 chunks=[]
 for name in sources:
  source=ROOT/name;css=source.read_text(encoding='utf-8-sig')
  if re.search(r'@import|@charset',css,re.I):raise ValueError(f'{name}: font imports/charset must remain separate stylesheets')
  def rebase(m):
   value=m[2].strip()
   if value.startswith(('data:','http:','https:','//','/','#')):return m[0]
   filename=value.split('?')[0].split('#')[0];target=(source.parent/filename).resolve()
   relative=os.path.relpath(target,DIRECTORY).replace('\\','/')
   return 'url('+m[1]+relative+value[len(filename):]+m[1]+')'
  css=re.sub(r'url\(\s*([\"\']?)(.*?)\1\s*\)',rebase,css,flags=re.I)
  chunks.append('/* '+name+' */\n'+css+'\n')
 content='\n'.join(chunks);new_name=hashlib.sha256(content.encode()).hexdigest()[:16]+'.css'
 (DIRECTORY/new_name).write_text(content,encoding='utf-8');updated[new_name]=sources
 if old_name!=new_name:replacements[old_name]=new_name
pages=json.loads((ROOT/'performance-audit/original-invariants.json').read_text())
for name in pages:
 path=ROOT/name;before=path.read_bytes().decode('utf-8');after=before
 for old,new in replacements.items():after=after.replace('performance-css/'+old,'performance-css/'+new)
 if after!=before:path.write_bytes(after.encode('utf-8'))
manifest_file.write_text(json.dumps(updated,indent=2),encoding='utf-8')
# Remove only replaced generated bundles after every page reference has been updated.
for old in replacements:
 file=DIRECTORY/old
 if old not in updated and file.is_file():file.unlink()
print(f'Rebuilt {len(updated)} bundles; updated {len(replacements)} bundle names. Rerun visual checks.')
