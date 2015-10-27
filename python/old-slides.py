import xml.dom

class Slide(object):
    def __init__(self, presentation):
        self.pr = presentation

class Cover(Slide):
    def __init__(self, presentation, **args):
        super(Cover, self).__init__(presentation)

    def render(self, doc):
        section = doc.createElement('section')
        section.setAttribute('class', 'slide cover')
        section.setAttribute('id', 'Cover')
        for child in children: section.appendChild(child)

        style = doc.createElement('style')
        text = doc.createTextNode(unicode("""
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
        """))
        style.appendChild(text)
        section.appendChild(style)
        return section



class Presentation(object):
    def __init__(self, title='title', author='author'):
        impl = xml.doc.getDOMImplementation()
        self.doc = impl.createDocument('', '', impl.createDocumentType('HTML'))
        self.root = self.doc.documentElement
        elt = self.elt

        html = elt('html', { 'lang': 'en' },
            elt('head', {},
                elt('title', {}, title)
                elt('meta', { 'charset': 'utf-8' })
                elt('meta', { 'name': 'viewport', 'content': 'width/792, user-scalable=no' })
                elt('meta', { 'http-equiv': 'x-ua-compatible', 'content': 'ie=edge' })
                elt('link', { 'rel': 'stylesheet', 'href': 'shower/themes/ribbon/styles/screen.css' })))
        self.root.appendChild(html)

        self.body = elt('body', { 'class': 'list' }))
        self.root.appendChild(body)

    def elt(self, tag, attributes, **children):
        e = self.doc.createElement(tag)
        for (key, value) in attributes.items():
            e.setAttribute(key, value)
        for child in children:
            if instanceof(child, str):
                child = doc.createTextNode(unicode(child))
            e.appendChild(child)
        return e

    def slide(self, **args):
        self.body.appendChild(self.elt(**args))

    def cover(self, **args):
        self.body.appendChild(

