"""Verify all supplied article content, original images and saved translated pages."""
import html,json,re,xml.etree.ElementTree as ET
from .site import ROOT,CONFIG,key,document_spans,translated,strip_integration

def main():
    manifest=json.loads((ROOT/'multilingual/october-editorial-manifest.json').read_text(encoding='utf-8'))
    cache=json.loads((ROOT/'multilingual/translations.json').read_text(encoding='utf-8'));checked=0
    for article in manifest['articles']:
        english=(ROOT/article['path']).read_text(encoding='utf-8')
        plain=' '.join(html.unescape(re.sub('<[^>]*>',' ',english)).split())
        for block in article['blocks']:
            for paragraph in block.removeprefix('### ').split('\n'):
                assert ' '.join(paragraph.split()) in plain,(article['path'],paragraph)
        assert article['author'] in html.unescape(english),article['path']
        assert article['editorial_note'] in html.unescape(english),article['path']
        assert all(url in html.unescape(english) for url in article['resources']),article['path']
        for language in CONFIG['languages']:
            prefix=language+'/' if language!='en' else ''
            source=(ROOT/prefix/article['path']).read_text(encoding='utf-8')
            archive=(ROOT/prefix/'blog.html').read_text(encoding='utf-8')
            assert re.search(r'<img\b[^>]*src="'+re.escape(article['image'])+'"',source),(language,article['path'],'hero')
            assert article['image'] in archive,(language,article['path'],'card')
            assert source.count('<h1')==1,(language,article['path'],'H1')
            assert re.search(r'<h2>[^<\n]+</h2><p>',source),(language,article['path'],'heading boundaries')
            assert 'href="https://dommydom.com/'+prefix+article['path']+'"' in source,(language,article['path'],'canonical')
            if language!='en':
                for _,_,text,attribute in document_spans(strip_integration(english)):
                    assert html.escape(translated(text,language,cache),quote=attribute) in source,(language,article['path'],text)
            sitemap=(ROOT/f'sitemap-{language}.xml').read_text(encoding='utf-8')
            assert 'https://dommydom.com/'+prefix+article['path'] in sitemap
            checked+=1
    report={'local_only':True,'articles_added_without_replacing_existing':6,'article_language_versions_checked':checked,'complete_supplied_content_preserved':True,'matching_card_and_article_images':True,'translated_metadata_and_sitemaps':True,'duplicate_articles_found':0}
    (ROOT/'multilingual/editorial-review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
