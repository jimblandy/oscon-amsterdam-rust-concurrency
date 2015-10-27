from __future__ import print_function
import xml.dom

# Bookkeeping helpers for an SVG XML document. self.root is an xml.dom
# document element in the document self.doc.
class SVGPicture(object):
    def __init__(self, (realWidth, realHeight), pixelWidthHeight):
        impl = xml.dom.getDOMImplementation()
        doctype = impl.createDocumentType('svg', '-//W3C//DTD SVG 1.1//EN',
                                          'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd')
        self.doc = impl.createDocument('http://www.w3.org/2000/svg', 'svg', doctype)
        self.root = self.doc.documentElement
        self.root.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
        self.root.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        self.root.setAttribute('version', '1.1')
        self.root.setAttribute('width', realWidth)
        self.root.setAttribute('height', realHeight)
        self.root.setAttribute('viewBox', '0 0 %d %d' % pixelWidthHeight) # user unit is pt

    def save_as(self, name):
        with open(name, 'w') as f:
            self.doc.writexml(f, addindent='  ', newl='\n')
            print(file=f)

    def line(self, (x1, y1), (x2, y2), **attributes):
        attributes.update({'x1':x1, 'y1':y1, 'x2':x2, 'y2':y2})
        return setAttributes(self.doc.createElement('line'), **attributes)

    def rect(self, (x, y), (width, height), **attributes):
        attributes.update({'x':x, 'y':y, 'width':width, 'height':height})
        return setAttributes(self.doc.createElement('rect'), **attributes)

    def group(self, **attributes):
        return setAttributes(self.doc.createElement('g'), **attributes)

    def path(self, d, **attributes):
        attributes['d'] = d
        return setAttributes(self.doc.createElement('path'), **attributes)

    def textPath(self, content, **attributes):
        tp = self.doc.createElement('textPath')
        tp.appendChild(self.doc.createTextNode(unicode(content)))
        setAttributes(tp, **attributes)
        return tp

    def text(self, content=None, **attributes):
        t = self.doc.createElement('text')
        if content:
            t.appendChild(self.doc.createTextNode(str(content)))
        setAttributes(t, **attributes)
        return t

    def defs(self):
        return self.doc.createElement('defs')

def setAttributes(element, **d):
    for (key, value) in d.items():
        element.setAttribute(key, str(value))
    return element
