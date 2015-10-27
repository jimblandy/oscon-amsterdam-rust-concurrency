from xml.sax.saxutils import escape

class Element(object):
    def __init__(self, tag, attributes, **children):
        self.tag = tag
        self.attributes = attributes
        self.children = children

    def render(self, output):
        write = output.write
        write('<{}'.format(self.tag))
        if self.attributes:
            write(' ')
            for (key, value) in self.attributes.items():
                
