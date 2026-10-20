import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from multilingual import site
from multilingual.cloud import cost_units,reserve_math

class LocalizationTests(unittest.TestCase):
    def test_sitemap_index_preserves_all_published_english_pages(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'index.html').write_text('<html><body>Home</body></html>')
            (root/'old-page.html').write_text('<html><head><meta http-equiv="refresh" content="0;url=index.html"></head><body></body></html>')
            (root/'sitemap.xml').write_text('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><sitemap><loc>https://dommydom.com/sitemap-en.xml</loc></sitemap></sitemapindex>')
            (root/'sitemap-en.xml').write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://dommydom.com/</loc></url><url><loc>https://dommydom.com/old-page.html</loc></url></urlset>')
            self.assertEqual(site.pages(root),['index.html','old-page.html'])

    def test_html_preserves_code_and_translates_attributes(self):
        source='<html><head><title>Welcome home</title></head><body><style>.a{color:red}</style><script>const x="Do not modify";</script><input placeholder="Your name"><p>Hello world</p><p translate="no">Dominique Nelson</p></body></html>'
        document=site.Document(source)
        self.assertEqual({x[2] for x in document.spans},{'Welcome home','Your name','Hello world'})
        cache={site.key(s[2],'es'):'Traducido' for s in document.spans}
        result=site.render(source,'contact.html','es',cache,['contact.html'])
        self.assertIn('<script>const x="Do not modify";</script>',result)
        self.assertIn('placeholder="Traducido"',result)
        self.assertIn('translate="no">Dominique Nelson',result)
        self.assertIn('<html lang="es" dir="ltr">',result)

    def test_rtl_and_reciprocal_seo_for_all_languages(self):
        for lang in site.CONFIG['languages']:
            with self.subTest(language=lang):
                source='<html><head><link rel="canonical" href="old"></head><body><a href="../blog.html#latest">Read More</a><img src="../assets/photo.jpg"><script src="../assets/app.js"></script></body></html>'
                cache={site.key('Read More',lang):'Localized'}
                result=site.render(source,'life-changes/test.html',lang,cache,['life-changes/test.html','blog.html'])
                self.assertEqual(result.count('rel="canonical"'),1)
                self.assertEqual(result.count('hreflang='),11)
                self.assertIn('dir="'+('rtl' if lang in {'fa','ar'} else 'ltr')+'"',result)
                self.assertIn('href="'+site.local_url('blog.html',lang).lstrip('/')+'#latest"',result)
                self.assertIn('src="assets/app.js"',result)
                self.assertIn('<base href="'+('../' if lang=='en' else '../../')+'">',result)

    def test_changed_text_invalidates_only_that_segment(self):
        before=['Existing paragraph','Another paragraph']
        cache={site.key(t,'es'):'translation' for t in before}
        after=['Existing paragraph','Updated paragraph']
        self.assertEqual([t for t in after if site.key(t,'es') not in cache],['Updated paragraph'])

    def test_nested_existing_base_and_toolbar_order_work_from_explorer(self):
        source='<html><head><base href="../../"></head><body><header><div class="dd-header-tools"><a class="dd-home" href="index.html">Home</a><a class="dd-search" href="search.html">Search</a></div></header><img src="assets/photo.jpg"><a href="blog.html">Blog</a></body></html>'
        cache={site.key(t,'es'):'Localized' for t in ['Home','Search','Blog']}
        output=site.render(source,'life-changes/death/test.html','es',cache,['index.html','search.html','blog.html','life-changes/death/test.html'])
        self.assertIn('<base href="../../../">',output)
        self.assertIn('src="assets/photo.jpg"',output)
        self.assertIn('href="es/blog.html"',output)
        self.assertIn('href="es/search.html">Localized</a><!-- dommydom-i18n:selector:start -->',output)
        self.assertIn('<svg aria-hidden="true"',output)
        self.assertLess(output.index('<base '),output.index('<link '))

    def test_structured_seo_and_form_configuration_are_translated(self):
        source='<html><head><script type="application/ld+json">{"@type":"Article","headline":"My article","url":"https://dommydom.com/blog.html"}</script></head><body><script type="application/json">{"prompt":"Your goal","key":"goal"}</script></body></html>'
        cache={site.key(text,'es'):value for text,value in [('My article','Mi artículo'),('Your goal','Tu objetivo')]}
        result=site.render(source,'blog.html','es',cache,['blog.html'])
        self.assertIn('Mi artículo',result)
        self.assertIn('Tu objetivo',result)
        self.assertIn('"key": "goal"',result)
        self.assertIn('"@type": "Article"',result)
        self.assertIn('https://dommydom.com/es/blog.html',result)

    def test_existing_html_classes_are_preserved(self):
        result=site.render('<html class="existing-theme" lang="en"><head></head><body></body></html>','index.html','fa',{},['index.html'])
        self.assertIn('class="existing-theme"',result)
        self.assertIn('lang="fa" dir="rtl"',result)

    def test_legacy_title_listener_and_content_first_social_url_are_localized(self):
        source='<html><head><meta content="https://dommydom.com/" property="og:url"><title>Home title</title><script>document.addEventListener("DOMContentLoaded",()=>{document.title="Home title";});</script></head><body></body></html>'
        result=site.render(source,'index.html','es',{site.key('Home title','es'):'Titulo traducido'},['index.html'])
        self.assertIn('document.title="Titulo traducido"',result)
        self.assertIn('content="https://dommydom.com/es/" property="og:url"',result)
        self.assertLess(result.index('<base '),result.index('<meta '))

    def test_visible_source_selector_is_idempotent_and_regenerates_correct_locale(self):
        source='<html><head><title>Home</title></head><body><header>Home</header><main>Home</main></body></html>'
        english=site.render(source,'index.html','en',{},['index.html'])
        self.assertEqual(english.count('id="dd-language"'),1)
        self.assertIn('</header><!-- dommydom-i18n:selector:start -->',english)
        self.assertEqual(site.render(english,'index.html','en',{},['index.html']).count('id="dommydom-locale"'),1)
        cache={site.key('Home','es'):'Inicio',site.key('Language','es'):'Idioma'}
        spanish=site.render(english,'index.html','es',cache,['index.html'])
        self.assertEqual(spanish.count('id="dd-language"'),1)
        self.assertEqual(spanish.count('id="dommydom-locale"'),1)
        self.assertIn('"language": "es"',spanish)
        self.assertIn('<option value="es" selected>',spanish)
        self.assertIn('aria-label="Idioma"',spanish)
        self.assertNotIn('</label>',spanish)

    def test_budget_limit_and_conservative_cost(self):
        self.assertEqual(cost_units(1_000_000),20_000_000)
        self.assertEqual(reserve_math(14_999_980,20),15_000_000)
        self.assertEqual(reserve_math(19_999_980,20),20_000_000)
        with self.assertRaises(RuntimeError):reserve_math(20_000_000,1)
        with self.assertRaises(RuntimeError):reserve_math(0,-1)

    def test_build_fails_closed_without_translations(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'multilingual').mkdir();(root/'multilingual/translations.json').write_text('{}')
            with patch.object(site,'inventory',return_value=(['index.html'],['A new blog'])):
                with self.assertRaisesRegex(RuntimeError,'9 translations missing'):site.build(root)
            self.assertFalse((root/'dist').exists())

    def test_complete_build_and_new_blog(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'multilingual').mkdir();(root/'assets').mkdir()
            (root/'sitemap.xml').write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://dommydom.com/</loc></url></urlset>')
            (root/'index.html').write_text('<html><head><title>Home</title></head><body><a href="blog-new.html">New blog</a></body></html>')
            (root/'blog-new.html').write_text('<html><head><title>New blog</title></head><body>New blog</body></html>')
            listing,texts=site.inventory(root)
            self.assertIn('blog-new.html',listing)
            cache={site.key(t,lang):'Localized '+lang for t in texts for lang in site.CONFIG['languages'] if lang!='en'}
            (root/'multilingual/translations.json').write_text(json.dumps(cache))
            result=site.build(root)
            self.assertEqual(result['pages'],2)
            for lang in site.CONFIG['languages']:
                prefix='' if lang=='en' else lang+'/'
                self.assertTrue((root/'dist'/prefix/'blog-new.html').exists())
                self.assertTrue((root/'dist'/f'sitemap-{lang}.xml').exists())
            self.assertFalse((root/'dist/multilingual').exists())
            (root/'blog-new.html').write_text('<html><head></head><body>Changed blog</body></html>')
            with self.assertRaisesRegex(RuntimeError,'9 translations missing'):site.build(root)

    def test_browser_has_no_translation_api_or_secrets(self):
        browser=(site.ROOT/'assets/multilingual.js').read_text()
        self.assertNotIn('fetch(',browser)
        self.assertNotIn('googleapis.com',browser)
        self.assertNotIn('apiKey',browser)

if __name__=='__main__':unittest.main()
