"""Correct heading/paragraph boundaries in the newly imported six articles only."""
import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'multilingual/october-editorial-manifest.json').read_text(encoding='utf-8'))
for article in manifest['articles']:
    path=root/article['path'];source=path.read_text(encoding='utf-8')
    source=re.sub(r'<h2>([^<\n]+)\n([^<]+)</h2>',lambda m:'<h2>'+m[1]+'</h2><p>'+m[2]+'</p>',source)
    path.write_text(source,encoding='utf-8')
