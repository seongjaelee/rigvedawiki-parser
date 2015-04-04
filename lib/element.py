#!/usr/bin/env python3

class Element(object):

    def __init__(self, parent, tag, attrib=None, close=True):
        self.parent = parent
        self.tag = tag
        self.children = []
        self.attrib = attrib if attrib != None else {}
        self.close = close
        if parent != None:
            parent.append_child(self)

    def append_child(self, e):
        self.children.append(e)
        return e

    def get_parent(self):
        return self.parent

    def to_xml(self):
        ret = '<%s' % self.tag
        for k, v in self.attrib.items():
            ret += ' %s="%s"' % (k, v)
        ret += '>'
        for child in self.children:
            ret += child.to_xml()
        if self.close:
            ret += '</%s>' % self.tag
        return ret

class TextElement(Element):

    def __init__(self, parent, text = ''):
        Element.__init__(self, parent, None)
        self.text = text

    def append_child(self, e):
        assert False

    def to_xml(self):
        return self.text
