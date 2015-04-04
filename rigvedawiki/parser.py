import os
import re
from element import Element, TextElement

class Parser(object):

    def __init__(self):
        pass

    def _apply(self, parent, match, prefix):
        if match:
            data = dict(((str(k), v) for k, v in match.groupdict().items() if v is not None and str(k) is not match.lastgroup))
            func = '{0}_{1}_repl'.format(prefix, match.lastgroup)
            getattr(self, func)(parent, **data)

    inline_link = r'(?P<link>\[\[(?P<link_text>.*?)\]\])'
    inline_strong = r'(?P<strong>\'{3}(?P<strong_text>(\'\'[^\']+?\'\'|[^\']+?)+?)\'{3}(?!\'))'
    inline = (
        inline_link,
        inline_strong,
    )
    inline_re = re.compile('|'.join(inline), re.X | re.U)

    def inline_link_repl(self, parent, link_text):
        elem = Element(parent, 'a', {'href':link_text})
        self.parse_inline(elem, link_text)

    def inline_strong_repl(self, parent, strong_text):
        self.parse_inline(Element(parent, 'strong'), strong_text)

    def parse_inline(self, parent, text):
        pos = 0
        for match in self.inline_re.finditer(text):
            TextElement(parent, text[pos:match.start()])
            self._apply(parent, match, 'inline')
            pos = match.end()
        TextElement(parent, text[pos:])

    line_head = r'(?P<head>^(?P<head_head>=+)\s(?P<head_text>.*?)\s(?P=head_head)\s*$)'
    line_text = r'(?P<text>(?P<text_text>.+))'
    line = (
        line_head,
        line_text,
    )
    line_re = re.compile('|'.join(line), re.X | re.U | re.M)
    linebreak_re = re.compile(r'\r\n|\n', re.M)

    def line_head_repl(self, parent, head_head, head_text):
        self.parse_inline(Element(parent, 'h%d' % (len(head_head) + 1)), head_text)

    def line_text_repl(self, parent, text_text):
        self.parse_inline(Element(parent, 'p'), text_text)

    def normalize_split_text(self, text):
        return self.linebreak_re.split(text)

    def parse_line(self, parent, text):
        for line in self.normalize_split_text(text):
            match = self.line_re.match(line)
            self._apply(parent, match, 'line')

    block_quote = r'(?P<quote>(?P<quote_text>(^\>\s[^\n]*\n|(?<=\n)\>\s[^\n]*\n)+))'
    # block_indent = r'(?P<indent>((^\s[^\n]*\n)|((?<=\n)\s[^\n]*\n))+)'
    block = (
        block_quote,
        # block_indent,
    )
    block_re = re.compile('|'.join(block), re.X)
    block_quote_re = re.compile(r'^\>\s', re.M)

    def block_quote_repl(self, parent, quote_text):
        self.parse_block(Element(parent, 'blockquote'), re.sub(self.block_quote_re, '', quote_text))

    # def block_indent_repl(self, parent, indent):
    #     text = re.sub(re.compile(r'^\s', re.M), '', indent)
    #     list = Element(parent, 'ul')
    #     for match in re.compile(r'((?<=^)|(?<=\n))\*\s(?P<text>.*)((?=\n\*)|(?=$))').finditer(text):
    #         list_item = Element(list, 'li')
    #         self.parse_block(list_item, match.group('text'))

    def parse_block(self, parent, text):
        pos = 0
        for match in self.block_re.finditer(text):
            self.parse_line(parent, text[pos:match.start()])
            self._apply(parent, match, 'block')
            pos = match.end()
        self.parse_line(parent, text[pos:])

html = Element(None, 'html')
head = Element(html, 'head')
Element(head, 'meta', {'charset':'utf-8'}, close=False)
Element(head, 'link', {'href':'../web/style.css', 'rel':'stylesheet'}, close=False)
body = Element(html, 'body')

converter = Parser()
raw_file = open('test/data/LightNovel.txt', 'r')
converter.parse_block(body, raw_file.read())
raw_file.close()

if not os.path.exists('out'):
    os.makedirs('out')
html_file = open('out/LightNovel.html', 'w')
html_file.write('<!DOCTYPE html>' + html.to_html())
html_file.close()
