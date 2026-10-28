"""Complete the owner-authorized local translations using the existing Google workflow.

No Git, deployment, quota, IAM, billing, credential-file or budget-policy changes.
Existing public translations are immutable cache hits. Provider requests use the
shared durable reservation/deduplication adapter, without uncertain-call retries.
"""
from pathlib import Path
import argparse
import html
import importlib.util
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'tools'))
from multilingual import site
from source_section_policy import clean as clean_citation_sections
from translation_pipeline.pipeline import atomic, encoded, google_translate, digest
from translation_pipeline.connection import PROJECT, private_path
from translation_pipeline.budget import Budget, ExistingBudget


def paper_module():
    spec = importlib.util.spec_from_file_location(
        'approved_paper_translation', ROOT.parent / 'paper-trail/tools/paper-trail-translations.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def groups(values):
    batch, size = [], 0
    for value in values:
        if len(value) > 30000:
            raise RuntimeError('Source exceeds existing provider guard')
        if batch and (len(batch) >= 50 or size + len(value) > 4500):
            yield batch
            batch, size = [], 0
        batch.append(value)
        size += len(value)
    if batch:
        yield batch


def generate(work):
    paper = paper_module()
    paper.OUT = work / 'google-preflight'
    # The existing preflight obtains a memory-only token and verifies the existing
    # project. It does not enable services or change account permissions.
    token = paper.preflight()
    ledger = private_path('DOMMYDOM_SHARED_BUDGET_DB', 'shared-usage.sqlite')
    budget = ExistingBudget(ledger) if ledger.exists() else Budget(ledger)
    output = ROOT / 'multilingual/translations.json'
    cache = json.loads(output.read_text(encoding='utf-8'))
    listing, texts = site.inventory(ROOT)
    saved = paper.load_cache()
    state = ROOT / '.translation-build-cache'
    receipts = state / 'project-provider-responses'
    fields_path = state / 'dommydom-workflow-fields.json'
    fields = json.loads(fields_path.read_text(encoding='utf-8')) if fields_path.exists() else {}
    # Completed receipts can recover a local checkpoint failure without another
    # provider request. Uncertain provider operations are never repeated.
    for receipt in sorted(receipts.glob('*.json')):
        row = json.loads(receipt.read_text(encoding='utf-8'))
        for source, value in zip(row['sources'], row['values']):
            fields[paper.key(source, row['locale'])] = {
                'source': source, 'locale': row['locale'], 'text': value,
                'provenance': 'google', 'receipt': receipt.name}
    reused, calls, completed = 0, 0, 0
    for language in site.CONFIG['languages']:
        if language == 'en':
            continue
        for text in texts:
            target_key = site.key(text, language)
            if target_key in cache:
                continue
            record = fields.get(paper.key(text, language)) or saved.get(paper.key(text, language))
            if record and record.get('text'):
                cache[target_key] = record['text']
                reused += 1
        atomic(output, encoded(cache))
        missing = [text for text in texts if site.key(text, language) not in cache]
        print(language + ': completing ' + str(len(missing)) + ' uncached segments', flush=True)
        for batch in groups(missing):
            reservation = budget.reserve('dommydom', sum(map(len, batch)))
            if not reservation['allowed']:
                raise RuntimeError('Existing usage accounting refused the request')
            outcome = 'uncertain'
            try:
                values = google_translate(language, batch, PROJECT, token)
                name = reservation['reservation'] + '.json'
                atomic(receipts / name, encoded({
                    'locale': language, 'sources': batch, 'values': values,
                    'received_at': time.time()}))
                for text, value in zip(batch, values):
                    cache.setdefault(site.key(text, language), value)
                    fields[paper.key(text, language)] = {
                        'source': text, 'locale': language, 'text': value,
                        'provenance': 'google', 'receipt': name}
                atomic(fields_path, encoded(fields))
                atomic(output, encoded(cache))
                outcome = 'complete'
                calls += 1
                completed += len(batch)
            finally:
                budget.finish(reservation['reservation'], outcome)
        print(language + ': saved translations complete', flush=True)
    missing = [(language, text) for language in site.CONFIG['languages'] if language != 'en'
               for text in texts if site.key(text, language) not in cache]
    result = {'canonical_english_pages': len(listing), 'provider_requests': calls,
              'new_segments': completed, 'reused_segments': reused,
              'remaining_segments': len(missing), 'published': False}
    atomic(work / 'dommydom-generation.json', encoded(result))
    if missing:
        raise RuntimeError('Translations remain incomplete')
    print(json.dumps(result), flush=True)


def append_sitemap(path, urls):
    ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'
    ET.register_namespace('', ns)
    tree = ET.parse(path)
    root = tree.getroot()
    present = {node.text for node in root.iter() if node.tag.split('}')[-1] == 'loc'}
    for url in urls:
        if url not in present:
            ET.SubElement(ET.SubElement(root, '{' + ns + '}url'), '{' + ns + '}loc').text = url
            present.add(url)
    atomic(path, ET.tostring(root, encoding='utf-8', xml_declaration=True))


def integrate(work):
    listing, texts = site.inventory(ROOT)
    cache = json.loads((ROOT / 'multilingual/translations.json').read_text(encoding='utf-8'))
    missing = [(language, text) for language in site.CONFIG['languages'] if language != 'en'
               for text in texts if site.key(text, language) not in cache]
    if missing:
        raise RuntimeError('Refusing partial multilingual integration')
    sources = {path: (ROOT / path).read_text(encoding='utf-8') for path in listing}
    hero_pattern = r'<section\b[^>]*class="[^"]*videoHero.*?</section>'
    approved_heroes = {}
    for language in site.CONFIG['languages']:
        path = ROOT / ('' if language == 'en' else language) / 'index.html'
        approved_heroes[language] = re.search(hero_pattern, path.read_text(encoding='utf-8'), re.S).group()
    manifest_path = ROOT / 'tools/production-pages.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    created, updated = [], []
    for language in site.CONFIG['languages']:
        if language == 'en':
            # Preserve English markup, media and page layout. Refresh only the
            # existing integration block so new pages switch to their real peers.
            for path, source in sources.items():
                body = site.strip_integration(source)
                head, selector = site.integration(path, 'en', cache)
                rendered = site.place_selector(body.replace('</head>', head + '</head>', 1), selector)
                if rendered != source:
                    atomic(ROOT / path, rendered.encode('utf-8'))
            continue
        for path, source in sources.items():
            destination = ROOT / language / path
            rendered = site.render(source, path, language, cache, listing)
            if path == 'index.html':
                rendered = re.sub(hero_pattern, lambda _: approved_heroes[language], rendered, count=1, flags=re.S)
            rendered = clean_citation_sections(rendered, language + '/' + path)
            existed = destination.exists()
            if not existed or destination.read_text(encoding='utf-8') != rendered:
                atomic(destination, rendered.encode('utf-8'))
                (updated if existed else created).append(destination.relative_to(ROOT).as_posix())
        # Existing alias files remain intact, including their canonical redirects
        # and Clarity loaders. Only the actual canonical pages are rendered above.
        manifest['locales'][language] = sorted(set(manifest['locales'][language]) | set(listing))
        append_sitemap(ROOT / ('sitemap-' + language + '.xml'),
                       [site.CONFIG['origin'] + site.local_url(path, language) for path in listing])
        catalog = {text: site.translated(text, language, cache) for text in texts}
        atomic(ROOT / 'assets/locales' / (language + '.js'),
               ('window.DOMMYDOM_TRANSLATIONS=' + json.dumps(catalog, ensure_ascii=False).replace('<', '\\u003c') + ';').encode('utf-8'))
        print(language + ': actual localized HTML, cards, navigation and sitemap integrated', flush=True)
    atomic(manifest_path, encoded(manifest))
    for language, approved in approved_heroes.items():
        path = ROOT / ('' if language == 'en' else language) / 'index.html'
        assert re.search(hero_pattern, path.read_text(encoding='utf-8'), re.S).group() == approved
    result = {'new_localized_pages': created, 'updated_localized_pages': updated,
              'languages': list(site.CONFIG['languages']), 'hero_preserved': True,
              'remaining_segments': 0, 'published': False}
    atomic(work / 'dommydom-integration.json', encoded(result))
    print(json.dumps({k: len(v) if k.endswith('_pages') else v for k, v in result.items()}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['generate', 'integrate'])
    parser.add_argument('--work', type=Path, required=True)
    parser.add_argument('--owner-authorized', action='store_true')
    args = parser.parse_args()
    if args.phase == 'generate' and not args.owner_authorized:
        raise SystemExit('Explicit owner authorization required for provider requests')
    args.work.mkdir(parents=True, exist_ok=True)
    if args.phase == 'generate':
        lock = ROOT / '.translation-state/generation.lock'
        lock.parent.mkdir(exist_ok=True)
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        try:
            generate(args.work)
        finally:
            lock.unlink()
    else:
        integrate(args.work)
