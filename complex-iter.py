import sys
import xml.dom
from svgpicture import SVGPicture, setAttributes

def axis(pic, start, width, height, (lower, upper)):
    step = width / (upper - lower)
    g = pic.group(stroke='black')

    main = pic.line(start, (start[0] + width, start[1]))
    main.setAttribute('stroke-width', '3')
    g.appendChild(main)

    for unit_tick in range(0, upper - lower + 1):
        x = unit_tick * step
        if lower + unit_tick == 0:
            tick = pic.line((start[0] + x, start[1] - height * 2),
                            (start[0] + x, start[1] + height * 2))
        else:
            tick = pic.line((start[0] + x, start[1] - height),
                            (start[0] + x, start[1] + height))
        tick.setAttribute('stroke-width', '3')
        g.appendChild(tick)

    for minor_tick

    return g

if __name__ == '__main__':
    pageSizeNominalPixels = ('1280px', '720px')
    size = (1280, 720)
    center = (size[0]/2, size[1]/2)
    picture = SVGPicture(pageSizeNominalPixels, size)

    # Background.
    picture.root.appendChild(picture.rect((0, 0), size, fill='white', stroke='none'))

    # Real axis.
    picture.root.appendChild(axis(picture, (-50, center[1]), size[0] + 100, 6, (-3, 3)))

    picture.save_as('complex-iter.svg')
