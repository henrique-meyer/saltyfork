"""Rebuild the three genuine SVG icon variants from the approved outline master.

Requires Python 3.12, Pillow, and vtracer==0.6.15.
"""
from copy import deepcopy
from pathlib import Path
import re
import tempfile
import xml.etree.ElementTree as ET

from PIL import Image
import vtracer

ASSETS = Path(__file__).resolve().parent.parent
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)


def tag(name):
    return f'{{{NS}}}{name}'


def bounds(path):
    numbers = list(map(float, re.findall(r'-?\d+(?:\.\d+)?', path.get('d'))))
    points = list(zip(numbers[::2], numbers[1::2]))
    translation = list(map(float, re.findall(r'-?\d+(?:\.\d+)?', path.get('transform'))))
    return (min(x for x, y in points) + translation[0],
            min(y for x, y in points) + translation[1],
            max(x for x, y in points) + translation[0],
            max(y for x, y in points) + translation[1])


image = Image.open(ASSETS / 'icon-chef-salty-black-transparent-master.png').convert('RGBA')
palette = []
for r, g, b, alpha in image.getdata():
    if alpha < 128:
        palette.append((0, 0, 0, 0))
    elif max(r, g, b) < 100:
        palette.append((0, 0, 0, 255))
    elif r > g * 1.5 and r > b * 1.5:
        palette.append((239, 75, 66, 255))
    else:
        palette.append((250, 248, 243, 255))
image.putdata(palette)

with tempfile.TemporaryDirectory(prefix='saltyfork-icon-') as directory:
    source = Path(directory) / 'palette.png'
    traced = Path(directory) / 'trace.svg'
    image.save(source)
    vtracer.convert_image_to_svg_py(
        str(source), str(traced), colormode='color', hierarchical='stacked',
        mode='spline', filter_speckle=24, color_precision=8, layer_difference=16,
        corner_threshold=60, length_threshold=4, max_iterations=10,
        splice_threshold=45, path_precision=2)
    paths = list(ET.parse(traced).getroot())

variants = (
    ('icon-chef-salty.svg', '#0C2340', '#0C2340'),
    ('icon-chef-salty-black-transparent.svg', '#000000', None),
    ('icon-chef-salty-black-blue.svg', '#000000', '#0C2340'),
)
for filename, ink, background in variants:
    root = ET.Element(tag('svg'), {
        'viewBox': f'0 0 {image.width} {image.height}',
        'width': '512', 'height': '512', 'role': 'img',
        'aria-labelledby': 'icon-title',
    })
    ET.SubElement(root, tag('title'), {'id': 'icon-title'}).text = 'SaltyFork chef icon'
    defs = ET.SubElement(root, tag('defs'))
    gradient = ET.SubElement(defs, tag('linearGradient'), {
        'id': 'silver', 'x1': '0', 'y1': '0', 'x2': '1', 'y2': '0',
    })
    for offset, color in [('0', '#E9EDF0'), ('0.45', '#D5DCE2'), ('1', '#EEF1F4')]:
        ET.SubElement(gradient, tag('stop'), {'offset': offset, 'stop-color': color})
    if background:
        ET.SubElement(root, tag('rect'), {
            'width': str(image.width), 'height': str(image.height), 'fill': background,
        })
    for original in paths:
        path = deepcopy(original)
        fill = path.get('fill').upper()
        if fill == '#FAF8F3':
            left, top, right, bottom = bounds(path)
            # The connected fork face/prongs and lower handle get silver;
            # the hat and isolated eye highlights retain their ivory fill.
            if bottom > 900 and bottom - top > 80:
                path.set('fill', 'url(#silver)')
                path.set('data-part', 'fork')
        elif max(int(fill[i:i + 2], 16) for i in (1, 3, 5)) < 32:
            path.set('fill', ink)
        root.append(path)
    for x, y in [(500, 749), (707, 733)]:
        ET.SubElement(root, tag('circle'), {
            'cx': str(x), 'cy': str(y), 'r': '8', 'fill': '#FAF8F3',
        })
    ET.indent(root, space='  ')
    ET.ElementTree(root).write(ASSETS / filename, encoding='unicode', xml_declaration=False)
    print(filename, 'paths:', len(paths), 'embedded rasters: 0')
