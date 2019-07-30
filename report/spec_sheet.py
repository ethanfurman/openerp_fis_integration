# -*- coding: utf-8 -*-

from __future__ import division
from aenum import NamedTuple
import re
import urllib
from PIL import Image, ImageChops
from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

# from openerp import osv
from openerp.report.interface import report_int
from openerp.report.render import render

from openerp import pooler
# import time
# import unicodedata


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

        # now = time.strftime('%Y-%m-%d')

        product_product = pooler.get_pool(cr.dbname).get('product.product')
        datas = product_product.read(
                cr, uid, product_ids,
                fields=['label_server_stub', 'xml_id', 'name', 'ean13'],
                context=context,
                )

        # create canvas
        pdf_io = BytesIO()
        display = Canvas(pdf_io, pagesize=letter, bottomup=1)
        display.setFontSize(20)
        for data in datas:
            # download images and convert width and align
            image_specs = re.findall(
                    r'''<img src="([^"]*)" width=(\d*)% align="([^"]*)"''',
                    data['label_server_stub'],
                    )
            images = []
            for url, width, align in image_specs:
                try:
                    align = {'right':1, 'middle':0, 'center':0, 'left':-1}[align.lower()]
                    width = int(width.rstrip('%')) / 100
                except KeyError:
                    raise ValueError('unknown alignment: %r' % (align, ))
                except ValueError:
                    raise ValueError('unknown width format: %r' % (width, ))
                else:
                    try:
                        connection = urllib.urlopen(url)
                    except IOError:
                        images.append(ImageBox(None, width, align))
                    else:
                        try:
                            image_data = connection.read()
                            image = Image.open(BytesIO(image_data))
                            if not image.mode == 'RGB':
                                image = image.convert('RGB')
                            image = trim(image)
                            images.append(ImageBox(image, width, align))
                        except IOError:
                            images.append(ImageBox(None, width, align))
                        finally:
                            connection.close()
            #
            # sort images into rows
            #
            rows = []
            row = []
            total_width = 0
            for ibox in images:
                if total_width + ibox.width > 1:
                    rows.append(row)
                    row = []
                    total_width = 0
                total_width += ibox.width
                for i, el in enumerate(row):
                    if ibox.align <= el.align:
                        row.insert(i, ibox)
                        break
                else:
                    row.append(ibox)
            rows.append(row)

            page = Area(*letter)
            viewable_area = Area(page.width - 1.5*inch, page.height - 1.5*inch)
            left_margin = 0.75*inch
            bottom_margin = 0.75*inch
            right_margin = page.width - 0.75*inch
            top_margin = page.height - 0.75*inch
            top_left = Point(left_margin, top_margin)
            anchor = top_left
            # draw header
            display.drawString(left_margin, top_margin-0.25*inch, data['name'])
            display.drawRightString(right_margin, top_margin-0.25*inch, data['xml_id'])
            upc = data['ean13']
            upc = upc[:1], upc[1:6], upc[6:11], upc[11:12]  # discard 13th digit
            display.drawString(left_margin, top_margin-0.75*inch, 'UPC Code: %s-%s-%s-%s' % upc)
            anchor = Point(left_margin, top_margin - 1.25*inch)
            max_height = 0
            # for ibox in images:
            for row in rows:
                for ibox in row:

                    bbox = get_bounding_box(viewable_area, ibox.image, ibox.width)

                    if anchor.x + bbox.width > right_margin:
                        anchor = Point(left_margin, anchor.y - max_height - 0.25*inch)
                        max_height = 0
                    if anchor.y - bbox.height < bottom_margin:
                        display.showPage()
                        anchor = top_left
                        max_height = 0
                    max_height = max(max_height, bbox.height)
                    if ibox.image is not None:
                        x0, y0 = anchor
                        x1, y1 = anchor.x+bbox.width, anchor.y-bbox.height
                        display.drawImage(ImageReader(ibox.image), x0, y1, bbox.width, bbox.height, preserveAspectRatio=True)
                        if False:
                            display.lines(((x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)))
                    anchor = Point(anchor.x + bbox.width, anchor.y)
            display.showPage()
        display.save()
        #
        self.obj = external_pdf(pdf_io.getvalue())
        self.obj.render()
        return (self.obj.pdf, 'pdf')
report_spec_sheet('report.product.product.spec_sheet')


class Area(NamedTuple):
    width = 0
    height = 1

class Point(NamedTuple):
    x = 0
    y = 1

class ImageBox(NamedTuple):
    image = 0
    width = 1
    align = 2

def get_bounding_box(available_area, image, portion):
    box_width = round(portion * available_area.width)
    if image is None:
        box_height = 72
    else:
        image_percent = box_width / image.width
        box_height = round(image_percent * image.height)
    return Area(box_width, box_height)

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
