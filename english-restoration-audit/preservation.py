from pathlib import Path
import json,re,subprocess
out=Path('english-restoration-audit');paths=json.loads((out/'pages.json').read_text());issues=[];formpages=[]
for n in paths:
 s=Path(n).read_text(encoding='utf-8');old=(Path('translation-audit/source-before')/n).read_text(encoding='utf-8');clean=re.sub(r'<link rel="stylesheet" href="(?:\.\./)*assets/tablet-navigation.css[^\"]*"/>\n','',s)
 assert clean==old,n
 if re.search(r'google-translation|homepage-ai-chat|dd-language|translate.google|dd-homepage-language',s):issues.append(n)
 for cl in ['contactPageForm','regionRequestForm','homeValuationForm']:
  if re.search(r'class="[^"]*\b'+cl+r'\b',s):formpages.append({'page':n,'class':cl})
assert Path('assets/dominique-conversation.js').read_bytes()==Path('final-nine-language-audit/before-dominique-conversation.js').read_bytes()
original=subprocess.check_output(['git','show','HEAD:.gitignore']); current=Path('.gitignore').read_text(); stripped=current
for line in ['.env','.env.*','*credentials*.json','*service-account*.json']:stripped=stripped.replace(line+'\n','')
assert stripped.replace('\r\n','\n')==original.decode().replace('\r\n','\n')
Path('.gitignore').write_bytes(original)
(out/'legacy-forms.json').write_text(json.dumps(formpages,indent=2));(out/'preservation.json').write_text(json.dumps({'pagesUnchangedExceptNavigationStylesheet':len(paths),'originalChatByteIdentical':True,'multilingualPageReferences':issues,'legacyForms':formpages},indent=2))
print('Preservation passed for all 352 pages. Original chat byte-identical. Language references:',issues,'Legacy forms:',formpages)
