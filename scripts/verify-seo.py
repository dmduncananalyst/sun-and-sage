"""Check sitemap canonicals, blog URL consolidation, and discovery links.

Run with Python 3 from any directory. Uses only the standard library.
"""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://dommydom.com/"


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.canonicals = []
        self.main_links = set()
        self.resources = []
        self.refresh = None
        self.in_main = False
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "main":
            self.in_main = True
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonicals.append(attrs.get("href"))
        if tag == "a" and self.in_main:
            self.main_links.add(attrs.get("href"))
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.refresh = attrs.get("content")
        for attr in ("src", "href", "poster"):
            if attrs.get(attr):
                self.resources.append(attrs[attr])

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False


def local_path(url):
    return ROOT / (unquote(urlsplit(url).path).lstrip("/") or "index.html")


def verify():
    pages = {}

    def page(path):
        if path not in pages:
            pages[path] = Page(path)
        return pages[path]

    sitemap = ET.parse(ROOT / "sitemap.xml")
    urls = [node.text for node in sitemap.findall("{*}url/{*}loc")]
    assert len(urls) == len(set(urls)), "Duplicate sitemap URL"
    for url in urls:
        assert url.startswith(ORIGIN), f"Unexpected sitemap origin: {url}"
        path = local_path(url)
        assert path.is_file(), f"Missing sitemap target: {url}"
        target = page(path)
        assert target.canonicals == [url], f"Canonical mismatch: {url}: {target.canonicals}"
        assert target.refresh is None, f"Redirect included in sitemap: {url}"
        assert "/blog/" not in url, f"Alternate blog URL in sitemap: {url}"

    cities = {path.name for path in ROOT.glob("buy-*.html")} - {"buy-a-home.html"}
    for name in ("buy-a-home.html",):
        missing = cities - page(ROOT / name).main_links
        assert not missing, f"Missing neighborhood links on {name}: {missing}"

    posts = {path.name for path in ROOT.glob("blog-*.html")}
    archive_links = page(ROOT / "blog.html").main_links
    assert posts <= archive_links, f"Blog archive missing: {posts - archive_links}"
    for name in posts:
        url = ORIGIN + name
        assert url in urls, f"Blog post missing from sitemap: {name}"
        assert page(ROOT / name).canonicals == [url], f"Blog canonical mismatch: {name}"

    aliases = list((ROOT / "blog").glob("*.html"))
    for alias in aliases:
        target = page(alias)
        assert len(target.canonicals) == 1, f"Missing redirect canonical: {alias}"
        canonical = target.canonicals[0]
        assert canonical in urls, f"Redirect target absent from sitemap: {alias}"
        assert target.refresh == "0; url=" + canonical, f"Missing immediate redirect: {alias}"
        assert page(local_path(canonical)).canonicals == [canonical], f"Redirect chain: {alias}"

    # Check local links and assets in moved articles at their new base paths.
    moved = {page(alias).canonicals[0] for alias in aliases}
    for url in moved:
        for resource in page(local_path(url)).resources:
            resolved = urljoin(url, resource)
            if resolved.startswith(ORIGIN):
                assert local_path(resolved).is_file(), f"Broken moved-page reference: {url}: {resource}"

    print(f"PASS: {len(urls)} unique, self-canonical sitemap URLs")
    print(f"PASS: {len(cities)} city links in buying-page main content")
    print(f"PASS: {len(posts)} canonical articles linked from the blog index and listed in sitemap")
    print(f"PASS: {len(aliases)} legacy blog URLs redirect directly to canonical articles")
    print(f"PASS: local links and assets resolve for all {len(moved)} moved articles")


if __name__ == "__main__":
    verify()
