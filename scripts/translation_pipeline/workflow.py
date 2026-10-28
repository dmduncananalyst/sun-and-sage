"""Lossless source-span inventory. Technical attributes and executable code stay intact."""
import html
import re
from html.parser import HTMLParser

def normal(value):
    return re.sub(r'\s+', ' ', value).strip()

def valid_value(source, value):
    return isinstance(value, str) and bool(value.strip()) and '\x00' not in value

def apply_edits(markup, edits):
    ordered = sorted(edits)
    boundary = 0
    for start, end, value in ordered:
        if not 0 <= boundary <= start <= end <= len(markup):
            raise ValueError('Overlapping or invalid translation span')
        boundary = end
    for start, end, value in reversed(ordered):
        markup = markup[:start] + value + markup[end:]
    return markup

class Inventory(HTMLParser):
    def __init__(self, markup):
        super().__init__(convert_charrefs=True)
        self.markup, self.slots, self.stack = markup, [], []
        self.offsets = [0]
        for line in markup.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))
        self.feed(markup)

    def pos(self):
        line, column = self.getpos()
        return self.offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        blocked = any(item[1] for item in self.stack) or tag in {'script', 'style', 'code', 'pre', 'svg'} or attrs.get('translate') == 'no'
        if not blocked:
            raw, offset = self.get_starttag_text(), self.pos()
            for match in re.finditer(r'''([\w:-]+)\s*=\s*(["'])(.*?)\2''', raw, re.S):
                name = match[1].lower()
                meta = tag == 'meta' and name == 'content' and (attrs.get('name') in {'description', 'twitter:title', 'twitter:description'} or attrs.get('property') in {'og:title', 'og:description'})
                if name in {'alt', 'title', 'placeholder', 'aria-label', 'aria-description'} or meta:
                    self.add(offset + match.start(3), offset + match.end(3), html.unescape(match[3]), 'attribute')
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append((tag, blocked))

    def handle_startendtag(self, tag, attrs):
        before = len(self.stack)
        self.handle_starttag(tag, attrs)
        del self.stack[before:]

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def add(self, start, end, source, kind):
        source = normal(source)
        if source and re.search('[A-Za-z]', source):
            self.slots.append(dict(start=start, end=end, source=source, kind=kind))

    def handle_data(self, data):
        if any(item[1] for item in self.stack):
            return
        start = self.pos()
        end = self.markup.find('<', start)
        if end < 0:
            end = len(self.markup)
        self.add(start, end, html.unescape(self.markup[start:end]), 'text')
