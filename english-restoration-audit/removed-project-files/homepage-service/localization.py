"""Homepage-localization plan and protected source helpers. Never handles visitor messages."""
import hashlib,html,json,re
from pathlib import Path
LANGUAGES={'es':('Spanish','Español'),'fa':('Farsi','فارسی'),'hy':('Armenian','Հայերեն'),'zh-CN':('Mandarin','中文'),'ko':('Korean','한국어'),'tl':('Tagalog','Tagalog'),'te':('Telugu','తెలుగు'),'ru':('Russian','Русский'),'ar':('Arabic','العربية')}
NOTICE="Only this homepage is available in [language]. Other pages are currently in English. You can chat with Dominique's assistant in [language] to ask questions or request a consultation."
PROTECTED=re.compile(r'Dominique Duncan-Nelson|Dominique|DommyDom|RISE\s*[×x]\s*REAL|https?://[^\s<>]+|[\w.+-]+@[\w.-]+\.[A-Za-z]+|\+?\d[\d() .-]{7,}\d',re.I)
def key(text):return hashlib.sha256(text.encode()).hexdigest()
def protect(text):
 out=[];last=0
 for m in PROTECTED.finditer(text):out.extend([html.escape(text[last:m.start()]),'<span translate="no">'+html.escape(m[0])+'</span>']);last=m.end()
 return ''.join(out)+html.escape(text[last:])
def sources(catalog,language):return list(dict.fromkeys(catalog['strings']+list(catalog['ui'].values())+[NOTICE.replace('[language]',LANGUAGES[language][1])]))
def plan(catalog):
 counts={lang:sum(len(protect(t)) for t in sources(catalog,lang)) for lang in LANGUAGES}
 return {'homepage_unique_characters':sum(map(len,catalog['strings'])),'homepage_source_occurrence_characters':catalog['occurrenceCharacters'],'homepage_unique_segments':len(catalog['strings']),'target_languages':len(LANGUAGES),'google_input_codepoints_per_language_including_html_ui_notice':counts,'google_input_codepoints_nine_versions':sum(counts.values()),'gross_standard_nmt_usd_before_any_shared_credit':round(sum(counts.values())*20/1000000,4),'paid_calls_made':0,'note':'Planning estimate only. Standard NMT input includes protected HTML markup and whitespace. Shared monthly credit is not a hard spending cap. AI chat, hosting and storage are separate.'}
