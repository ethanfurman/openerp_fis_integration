# -*- coding: utf-8 -*-

from __future__ import division
from aenum import NamedTuple
import re
import requests
from PIL import Image, ImageChops
from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

from openerp.osv import fields
from openerp.report.interface import report_int
from openerp.report.render import render

from openerp import pooler
# import time
# import unicodedata
from aenum import NamedConstant, export
import logging

_logger = logging.getLogger(__name__)

GUTTER = 5

class external_pdf(render):
    def __init__(self, pdf):
        render.__init__(self)
        self.pdf = pdf
        self.output_type='pdf'

    def _render(self):
        return self.pdf


class report_spec_sheet(report_int):

    def create(self, cr, uid, ids, datas, context=None):
        if context is None:
            context = {}
        product_ids = ids
        xml_ids = set()
        product_product = pooler.get_pool(cr.dbname).get('product.product')
        today = fields.date.today(product_product, cr, localtime=True)
        datas = product_product.read(
                cr, uid, product_ids,
                fields=['label_server_stub', 'xml_id', 'name', 'ean13'],
                context=context,
                )
        # create canvas
        pdf_io = BytesIO()
        display = Canvas(pdf_io, pagesize=letter, bottomup=1)
        display.setAuthor('Sunridge Farms')
        display.setSubject('Product Specification Labels')
        if len(datas) == 1:
            display.setTitle('%s' % (datas[0]['name'], ))
        else:
            display.setTitle('Various Products')
        for data in datas:
            xml_id = data['xml_id']
            display.bookmarkPage(xml_id)
            display.addOutlineEntry('Product %s' % xml_id, xml_id)
            xml_ids.add(xml_id)
            # download images and convert width and align
            image_specs = re.findall(
                    r'''<img src="([^"]*)" width=(\d*)% align="([^"]*)" *(oe_header)?''',
                    data['label_server_stub'],
                    )
            images = []
            for url, width, align, header in image_specs:
                try:
                    align = {'right':1, 'middle':0, 'center':0, 'left':-1}[align.lower()]
                    width = int(width.rstrip('%')) / 100
                    print '\n\n%r\n%r\n' % (header, bool(header))
                    header = not header
                except KeyError:
                    raise ValueError('unknown alignment: %r' % (align, ))
                except ValueError:
                    raise ValueError('unknown width format: %r' % (width, ))
                try:
                    images.append(get_label(url, width, align, header))
                except (LabelAcquisitionError, MissingImageFile):
                    images.append(ImageLayout(None, width, align, False))
            #
            # sort images into rows
            #
            requested_rows = []
            row = []
            total_width = 0
            for layout in images:
                if total_width + layout.width > 1:
                    requested_rows.append(row)
                    row = []
                    total_width = 0
                total_width += layout.width
                for i, el in enumerate(row):
                    if layout.align <= el.align:
                        row.insert(i, layout)
                        break
                else:
                    row.append(layout)
            requested_rows.append(row)
            page = Area(*letter)
            viewable_area = Area(page.width - 1.5*inch, page.height - 1.25*inch)
            left_margin = 0.75*inch
            bottom_margin = 0.50*inch
            right_margin = page.width - 0.75*inch
            top_margin = page.height - 0.75*inch
            top_left = Point(left_margin, top_margin)
            anchor = top_left
            # draw header
            display.setFontSize(10)
            display.drawString(left_margin-0.25*inch, top_margin+0.25*inch, today)
            display.setFontSize(19)
            lines = format_lines(data['name'], 50, split=('nongmo','organic','eco-farmed','sunridge'))
            display.drawString(left_margin, top_margin-0.25*inch, lines[0])
            if len(lines) > 1:
                display.drawString(left_margin, top_margin-0.5*inch, lines[1])
            display.drawRightString(right_margin, top_margin+0.125*inch, xml_id)
            upc = data['ean13']
            upc = upc[:1], upc[1:6], upc[6:11], upc[11:12]  # discard 13th digit
            display.drawString(left_margin, top_margin-0.875*inch, 'UPC Code: %s-%s-%s-%s' % upc)
            anchor = Point(left_margin, top_margin - 1.25*inch)
            max_height = 0
            # now sort into final rows and pages
            pages = []
            page = []
            for row in requested_rows:
                # separate into left, center, and right segments
                left = []
                center = []
                right = []
                header = True
                for layout in row:
                    header = min(header, layout.header)
                    bbox = get_bounding_box(viewable_area, layout.image, layout.width)
                    if anchor.x + bbox.width > right_margin:
                        if header:
                            anchor = Point(left_margin, anchor.y - max_height - 0.10*inch)
                        else:
                            anchor = Point(left_margin, anchor.y - max_height - 0.25*inch)
                        max_height = 0
                        if left or right or center:
                            page.append((left, right, center))
                        left, right, center = [], [], []
                    if anchor.y - bbox.height < bottom_margin:
                        pages.append(page)
                        page = []
                        # display.showPage()
                        anchor = top_left
                        max_height = 0
                    max_height = max(max_height, bbox.height)
                    if layout.align == -1:
                        # maintain original order
                        left.append((anchor, bbox, layout))
                    elif layout.align == 0:
                        # maintain original order
                        center.append((anchor, bbox, layout))
                    elif layout.align == 1:
                        # reverse order (first image is the far right one
                        right.insert(0, (anchor, bbox, layout))
                    anchor = Point(anchor.x + bbox.width, anchor.y)
                if left or right or center:
                    page.append((left, right, center))
            # make sure and grab any stragglers
            if left or right or center:
                page.append((left, right, center))
            if page:
                pages.append(page)
            # calculate actual positions and print
            for page in pages:
                for left, right, center in page:
                    center_left = left_margin
                    center_right = right_margin
                    for anchor, bbox, layout in left:
                        display_image(display, anchor, bbox, layout)
                        center_left = anchor.x + bbox.width
                    if right:
                        anchor, bbox, layout = right[0]
                        delta = right_margin - (anchor.x + bbox.width)
                    for anchor, bbox, layout in right:
                        delta_anchor = Point(anchor.x + delta, anchor.y)
                        display_image(display, delta_anchor, bbox, layout)
                        center_right = anchor.x
                    if center:
                        # get left-most point
                        anchor, bbox, layout = center[0]
                        left_anchor = anchor
                        # center requires two passes:
                        # - calculate total space used and delta
                        # - adjust and print
                        total_width = 0
                        for anchor, bbox, layout in center:
                            total_width += bbox.width
                        # width calculated, now for delta
                        center_point = (center_left + center_right) // 2
                        half_width = total_width // 2
                        delta = center_point - half_width - left_anchor.x
                        for anchor, bbox, layout in center:
                            delta_anchor = Point(anchor.x + delta, anchor.y)
                            display_image(display, delta_anchor, bbox, layout)
                display.showPage()
        display.save()
        #
        xml_ids = sorted(xml_ids)
        if len(xml_ids) == 1:
            self._filename = '%s-Spec_Sheet' % (xml_ids[0], )
        elif xml_ids:
            self._filename = 'Spec_Sheets-%s-%s' % (xml_ids[0], xml_ids[-1])
        self.obj = external_pdf(pdf_io.getvalue())
        self.obj.render()
        return (self.obj.pdf, 'pdf')
report_spec_sheet('report.product.product.spec_sheet')

def display_image(canvas, anchor, bbox, layout):
    """put the image on the page

    - canvas: draws the image
    - anchor: upper-left corner of area to draw in
    - bbox: area to draw
    - layout: image info
    """
    x0, y0 = anchor
    x1, y1 = anchor.x+bbox.width, anchor.y-bbox.height
    if layout.image is not None:
        _logger.info('bbox: %r  layout.image: %r x %r', bbox, layout.image.width, layout.image.height)
        canvas.drawImage(
                ImageReader(layout.image),
                x0+GUTTER, y1+GUTTER,
                bbox.width-2*GUTTER, bbox.height-2*GUTTER,
                preserveAspectRatio=True,
                )
        if layout.header:
            canvas.lines(((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)))

class Area(NamedTuple):
    width = 0
    height = 1

class Point(NamedTuple):
    x = 0
    y = 1

class ImageLayout(NamedTuple):
    image = 0   # image itself
    width = 1   # percantage of total horizontal space
    align = 2   # left, right, center
    header = 3  # header image?  (True implies no border)

def get_bounding_box(available_area, image, portion):
    """return actual area needed for image
    
    - available_area: what is available
    - image: image to place
    - portion: %-width allotted for image
    """
    box_width = round(portion * available_area.width)
    if image is None:
        box_height = 72
    elif box_width < image.width:
        image_percent = box_width / image.width
        box_height = round(image_percent * image.height)
    else:
        box_height = image.height
    return Area(box_width, box_height)

def format_lines(line, cpl, split=()):
    # build line
    # split line if necessary
    split = [s.lower() for s in split]
    line = ' '.join(line.split())
    words = line.split()
    width = 0
    lines = []
    line = []
    good_sep = None
    has_split = False
    for word in words:
        if len(line) > 2 and word.lower() in split and not has_split:
            good_sep = len(line)
            word_width = cpl
        else:
            word_width = _width(word)
        if width == 0:
            line.append(word[:cpl])
            width += word_width
            if word == '-' and not good_sep:
                good_sep = len(line)
            elif word.endswith(','):
                good_sep = len(line)
        elif width + 1 + word_width <= cpl:
            line.append(word)
            width += 1 + word_width
            if word == '-' and not good_sep:
                good_sep = len(line)
            elif word.endswith(','):
                good_sep = len(line)
        else:
            new_line = []
            if good_sep and good_sep > 3 and (len(line) - good_sep <= 4):
                new_line = line[good_sep:]
                line = line[:good_sep]
            lines.append(' '.join(line))
            line = new_line
            width = 0
            good_sep = None
            line.append(word)
            width = sum([_width(word) for word in line])
            has_split = True
    if line:
        lines.append(' '.join(line))
    return tuple(lines)

def _width(word):
    narrow = "1iltfj!,.;:-'"
    wide = "WM"
    width = len(word)
    for ch in narrow:
        width -= word.count(ch) * 0.5
    for ch in wide:
        width += word.count(ch) * 1.5
    return width

# from https://stackoverflow.com/questions/10615901/trim-whitespace-using-pil
def trim(image):
    bg = Image.new(image.mode, image.size, image.getpixel((0,0)))
    diff = ImageChops.difference(image, bg)
    # diff = ImageChops.add(diff, diff) # should be whitespace trim only
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    else:
        return image

def get_label(url, width, align, header):
    """acquire product label image

    - url: location of image
    - width: %-width of available space (passed to ImageLayout)
    - align: left, right, center (passed to ImageLayout)
    """
    # get url
    _logger.debug('getting %s with width %s and align %s', url, width, align)
    with requests.get(url) as image_request:
        if image_request.status_code != 200:
            _logger.exception(
                    'unable to retrieve image data: status code %s\n%s',
                    image_request.status_code,
                    image_request.content,
                    )
            raise LabelAcquisitionError('unable to retrieve image data')
        image_data = image_request.content
    # process image
    try:
        image = Image.open(BytesIO(image_data))
    except IOError:
        _logger.exception('unable to process image data from %r' % url)
        raise UnknownImageFormat
    else:
        if not image.mode == 'RGB':
            image = image.convert('RGB')
        image = trim(image)
        return ImageLayout(image, width, align, header)

@export(globals())
class Konstants(NamedConstant):
    RAISE_EXCEPTION = 'raise'
    RETURN_ORIGINAL = 'original url'
    RETURN_LAST = 'last url'

class LabelAcquisitionError(Exception):
    pass

class LabelServerConnectionError(LabelAcquisitionError):
    pass

class MissingImageFile(LabelAcquisitionError):
    pass

class UnknownImageFormat(LabelAcquisitionError):
    pass
