import unittest
from core import Service,PolicyError,protected_html,plain
class Store:
 def __init__(self):self.cache={};self.chars=0;self.calls=0
 def get(self,k):return self.cache.get(k)
 def put(self,k,v):self.cache[k]=v
 def reserve(self,client,chars,limit):
  self.calls+=1
  if self.chars+chars>limit or self.calls>90:raise PolicyError('Capacity')
  self.chars+=chars
class TranslationPolicy(unittest.TestCase):
 def setUp(self):
  self.store=Store();self.calls=[]
  def provider(lang,texts):self.calls.append((lang,texts));return texts
  self.service=Service(['Public title','Contact Dominique Duncan-Nelson'],self.store,provider)
 def test_private_text_never_reaches_google(self):
  result=self.service.translate({'target':'es','texts':['Private client information','Public title']},'a');self.assertEqual(result['translations'][0],'Private client information');self.assertEqual(self.calls[0][1],['Public title'])
 def test_cache_avoids_repeat_provider_calls(self):
  payload={'target':'fa','texts':['Public title']};self.service.translate(payload,'a');self.service.translate(payload,'a');self.assertEqual(len(self.calls),1)
 def test_source_changes_invalidate_cache(self):
  self.service.allowed.add('Updated public title');self.service.translate({'target':'es','texts':['Public title']},'a');self.service.translate({'target':'es','texts':['Updated public title']},'a');self.assertEqual(len(self.calls),2)
 def test_protected_strings(self):
  self.assertIn('translate="no">Dominique Duncan-Nelson',protected_html('Contact Dominique Duncan-Nelson'));self.assertEqual(plain(protected_html('818-296-6896 & DommyDom')),'818-296-6896 & DommyDom')
 def test_budget_reserved_before_provider(self):
  self.service.daily_limit=1
  with self.assertRaises(PolicyError):self.service.translate({'target':'es','texts':['Public title']},'a')
  self.assertEqual(self.calls,[])
 def test_validation(self):
  for payload in [{'target':'bad','texts':['Public title']},{'target':'es','texts':[]},{'target':'es','texts':['x'*12001]}]:
   with self.assertRaises(PolicyError):self.service.translate(payload,'a')
 def test_provider_failure_does_not_poison_cache(self):
  self.service.provider=lambda *_:[]
  with self.assertRaises(RuntimeError):self.service.translate({'target':'ru','texts':['Public title']},'a')
  self.assertFalse(self.store.cache)
if __name__=='__main__':unittest.main()
