from __future__ import print_function
import re
import sys
import xml.dom

leading_whitespace = re.compile(r'^\s*')

# Remove a leading newline, and then any common indentation.
# This allows functions to to accept strings like:
#   f("""
#     some indented text
#        perhaps code
#     """)
#
# and convert that to the string "some indented text\n   perhaps code\n"
def clean_text(text):
    text = text.lstrip('\n')
    text = text.rstrip('\n ')
    lines = text.splitlines()
    if not lines:
        return text

    def indentation(line):
        return leading_whitespace.match(line).end()
    common = min(map(indentation, filter((lambda l: l != ''), lines)))
    if common > 0:
        lines = [line[common:] for line in lines]
    if lines[len(lines) - 1] == '':
        lines = lines[:-1]
    return '\n'.join(lines) + '\n'

markdown_pattern = re.compile(r'(\*([^*]+)\*)|(`([^`]+)`)')

def dumb_markdown(pres, text):
    elt = pres.elt
    spans = []
    last_end = 0
    for match in markdown_pattern.finditer(text):
        if last_end < match.start():
            spans.append(pres.doc.createTextNode(text[last_end : match.start()]))

        if match.group(1):  # bold
            e = elt('b', {}, match.group(2))
        elif match.group(3):  # tt
            e = elt('code', {}, match.group(4))
        assert e

        spans.append(e)
        last_end = match.end()

    if last_end < len(text):
        spans.append(pres.doc.createTextNode(text[last_end : ]))

    return spans

class Presentation(object):
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.slides = []

    def add(self, slide):
        self.slides.append(slide)

    def elt(self, tag, attributes, *children):
        e = self.doc.createElement(tag)
        for (key, value) in attributes.items():
            e.setAttribute(key, value)
        for child in children:
            if isinstance(child, str) or isinstance(child, unicode):
                child = self.doc.createTextNode(unicode(child))
            e.appendChild(child)
        # Hack for HTML weirdness.
        if tag == 'script' and not children:
            e.appendChild(self.doc.createTextNode(''))
        return e

    def render(self, output):
        impl = xml.dom.getDOMImplementation()
        self.doc = impl.createDocument('', 'html', impl.createDocumentType('HTML', '', ''))
        self.root = self.doc.documentElement
        self.root.setAttribute('lang', 'en')

        elt = self.elt
        head = elt('head', {},
                   elt('title', {}, self.title),
                   elt('meta', { 'charset': 'utf-8' }),
                   elt('meta', { 'name': 'viewport', 'content': 'width=792, user-scalable=no' }),
                   elt('meta', { 'http-equiv': 'x-ua-compatible', 'content': 'ie=edge' }),
                   elt('link', { 'rel': 'stylesheet', 'href': 'shower/themes/ribbon/styles/screen.css' }),
                   elt('link', { 'rel': 'stylesheet', 'href': 'custom.css' }))
        self.root.appendChild(head)

        self.body = elt('body', { 'class': 'list' },
                        elt('header', { 'class': 'caption' },
                            elt('h1', {}, self.title),
                            elt('p', {}, self.author)))
        self.root.appendChild(self.body)

        for slide in self.slides:
            render = slide.render(self)
            if isinstance(render, list):
                for subslide in render:
                    self.body.appendChild(subslide)
            else:
                self.body.appendChild(slide.render(self))

        self.body.appendChild(elt('div', { 'class': 'progress' },
                                  elt('div', {})))
        self.body.appendChild(elt('script', { 'src': 'shower/shower.min.js' }))

        self.doc.writexml(output)
        output.write('\n')

class Slide(object):
    def __init__(self, title, *children):
        self.title = title
        self.children = children

    def render(self, pres):
        elt = pres.elt
        div = elt('div', {})
        if self.title:
            div.appendChild(elt('h2', {}, *dumb_markdown(pres, self.title)))
        for child in self.children:
            div.appendChild(child.render(pres))
        return elt('section', { 'class': 'slide' }, div)

class Content(object):
    def __init__(self):
        self.reveal_flag = False

    def reveal(self):
        self.reveal_flag = True
        return self

class Cover(Slide):
    def __init__(self, title, subtitle, background, id_='Cover'):
        super(Cover, self).__init__(title)
        self.subtitle = subtitle
        self.background = background
        self.id_ = id_

    def render(self, pres):
        elt = pres.elt
        return elt('section', { 'class': 'slide cover', 'id': self.id_ },
                   elt('div', {},
                       elt('h2', {}, *dumb_markdown(pres, self.title)),
                       elt('p', {}, self.subtitle),
                       elt('img', { 'src': self.background, 'alt': '' }),
                       elt('style', {}, """
                           #Cover h2 {
                                   margin:30px 0 0;
                                   color:#FFF;
                                   text-align:center;
                                   font-size:70px;
                                   }
                           #Cover p {
                                   margin:10px 0 0;
                                   text-align:center;
                                   color:#FFF;
                                   font-style:italic;
                                   font-size:20px;
                                   }
                           #Cover p a {
                                   color:#FFF;
                                   }
                           """)))

class BigPicture(Slide):
    def __init__(self, image):
        super(BigPicture, self).__init__(None)
        self.image = image

    def render(self, pres):
        elt = pres.elt
        return elt('section', { 'class': 'slide cover bigpicture' },
                   elt('div', {},
                       elt('img', { 'src': self.image, 'alt': '' })))

class Picture(Content):
    def __init__(self, image):
        super(Picture, self).__init__()
        self.image = image

    def render(self, pres):
        elt = pres.elt
        return elt('img', { 'src': self.image, 'alt': '' })

class Points(Content):
    def __init__(self, *points):
        super(Points, self).__init__()
        self.points = points
        self.reveal_flag = False

    def reveal(self):
        self.reveal_flag = True
        return self

    def render(self, pres):
        elt = pres.elt
        ul = elt('ul', {})
        first = True
        for point in self.points:
            li = elt('li', {}, point)
            if self.reveal_flag and not first:
                li.setAttribute('class', 'next')
            ul.appendChild(li)
            first = False
        return ul

class Quote(Content):
    def __init__(self, text, writer):
        super(Quote, self).__init__()
        self.text = clean_text(text)
        self.writer = writer

    def render(self, pres):
        elt = pres.elt
        return elt('figure', {},
                   elt('blockquote', {},
                       elt('p', {}, self.text)),
                   elt('figcaption', {}, self.writer))

class Para(Content):
    def __init__(self, text):
        super(Para, self).__init__()
        self.text = clean_text(text)
        self.center_flag = False

    def render(self, pres):
        elt = pres.elt
        para = elt('center' if self.center_flag else 'p', {},
                   *dumb_markdown(pres, self.text))
        if self.reveal_flag:
            para.setAttribute('class', 'next')
        return para

    def center(self):
        self.center_flag = True
        return self

class BigPoint(Slide):
    def __init__(self, text):
        self.text = clean_text(text)

    def render(self, pres):
        elt = pres.elt
        return elt('section', { 'class': 'slide big' },
                   elt('div', {},
                       elt('p', {}),
                       elt('p', {}, self.text)))

class Code(Content):
    def __init__(self, code):
        super(Code, self).__init__()
        self.code = clean_text(code)

    def render(self, pres):
        elt = pres.elt
        return elt('pre', {},
                   elt('code', {},
                       self.code))

#                               1         2    3          4          5  6         7
callout_pattern = re.compile(r"`([^`\$]*)`(.)|`([^`\$]*)\$([^`\$]+)\$(.)([^`\$]*)`(.)")

class CodeCallout(Slide):
    def __init__(self, title, code):
        super(CodeCallout, self).__init__(title)
        self.title = title
        self.code = clean_text(code)

    def highlight(self, pres, selected):
        elt = pres.elt
        spans = []
        last_end = 0
        for match in callout_pattern.finditer(self.code):
            if last_end < match.start():
                spans.append(pres.doc.createTextNode(self.code[last_end : match.start()]))

            if match.group(2):
                if match.group(2) == selected:
                    spans.append(elt('span', { 'class': 'highlighted' }, match.group(1)))
                else:
                    spans.append(pres.doc.createTextNode(match.group(1)))

            elif match.group(7):
                if match.group(5) == selected:
                    spans.append(pres.doc.createTextNode(match.group(3)))
                    spans.append(elt('span', { 'class': 'highlighted' }, match.group(4)))
                    spans.append(pres.doc.createTextNode(match.group(6)))
                elif match.group(7) == selected:
                    spans.append(elt('span', { 'class': 'highlighted' },
                                     match.group(3) + match.group(4) + match.group(6)))
                else:
                    spans.append(match.group(3) + match.group(4) + match.group(6))

            last_end = match.end()

        if last_end < len(self.code):
            spans.append(pres.doc.createTextNode(self.code[last_end :]))

        return spans

    def render(self, pres):
        elt = pres.elt

        labels = set()
        for match in callout_pattern.finditer(self.code):
            if match.group(2):
                labels.add(match.group(2))
            elif match.group(7):
                labels.add(match.group(5))
                labels.add(match.group(7))
        has_zero = '0' in labels
        labels = list(labels)
        labels.sort()

        # If there's no label '0', then don't highlight anything immediately.
        if not has_zero:
            labels = [False] + labels

        slides = []
        for label in labels:
            code = elt('code', {}, *self.highlight(pres, label))
            code.normalize()
            div = elt('div', {},
                      elt('h2', {}, *dumb_markdown(pres, self.title)),
                      elt('pre', {}, code))
            slides.append(elt('section', { 'class': 'slide' }, div))

        return slides

class GnuPlot(Slide):
    def __init__(self, title, slide):
        self.title = title
        self.slide = slide

    def render(self, pres):
        elt = pres.elt

        return elt('section', { 'class': 'slide' },
                   elt('div', {},
                       elt('h2', {}, *dumb_markdown(pres, self.title)),
                       elt('img', { 'class': 'gnuplot', 'src': self.slide })))

