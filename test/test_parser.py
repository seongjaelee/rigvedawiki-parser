import os
from bs4 import BeautifulSoup
from rigvedawiki.element import Element
from rigvedawiki.parser import Parser

def test_create():
    raw_dir = 'test/data/raw'
    html_dir = 'test/data/html'

    parser = Parser()

    for raw_filename in os.listdir(raw_dir):
        raw_path = os.path.join(raw_dir, raw_filename)
        html_path = os.path.join(html_dir, os.path.splitext(raw_filename)[0] + '.html')
        assert os.path.isfile(html_path)

        raw = open(raw_path, 'r').read()
        html = open(html_path, 'r').read()

        root = Element(None)
        parser.parse_block(root, raw)

        actual = BeautifulSoup(root.to_html()).prettify()
        expected = BeautifulSoup(html).prettify()

        # It is a shame, but there is always one more '\n' at the end of expected.
        assert expected[:-1] == actual
