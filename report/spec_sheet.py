# -*- coding: utf-8 -*-

from __future__ import division
from aenum import NamedTuple
import re
import urllib
from PIL import Image
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
                fields=['label_server_stub'],
                context=context,
                )

        pdf_io = BytesIO()
        display = Canvas(pdf_io, pagesize=letter, bottomup=1)
        for data in datas:
            # download images and convert width and align
            image_specs = re.findall(
                    r'''<img src="([^"]*)" width="([^"]*)" align="([^"]*)"''',
                    data['label_server_stub'],
                    )
            images = []
            for url, width, align in image_specs:
                try:
                    align = {'right':1, 'middle':0, 'left':-1}[align.lower()]
                    width = int(width.rstrip('%')) / 100
                except KeyError:
                    raise ValueError('unknown alignment: %r' % (align, ))
                except ValueError:
                    raise ValueError('unknown width format: %r' % (width, ))
                else:
                    try:
                        connection = urllib.urlopen(url)
                    except IOError:
                        print 'unable to acquire', url
                        images.append(ImageBox(None, width, align))
                    else:
                        try:
                            image_data = connection.read()
                            image = Image.open(BytesIO(image_data))
                            if not image.mode == 'RGB':
                                image = image.convert('RGB')
                            images.append(ImageBox(image, width, align))
                        except IOError:
                            print 'could not load %r' % (url, )
                            images.append(ImageBox(None, width, align))
                        finally:
                            connection.close()
            #
            # sort images into rows
            #
            rows = []
            row = []
            total_width = 0
            print 'sorting into rows'
            for ibox in images:
                print '  processing', ibox
                if total_width + ibox.width > 1:
                    print '    starting new row'
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
            bottom_right = Point(right_margin, bottom_margin)
            print 'top left:', top_left
            print 'bottom right:', bottom_right

            anchor = top_left
            max_height = 0
            # for ibox in images:
            for row in rows:
                for ibox in row:
                    print('*' * 15)
                    print 'anchor:', anchor

                    bbox = get_bounding_box(viewable_area, ibox.image, ibox.width)
                    print 'bounds', bbox

                    if anchor.x + bbox.width > right_margin:
                        anchor = Point(left_margin, anchor.y - max_height)
                        max_height = 0
                        print '  anchor:', anchor
                    if anchor.y - bbox.height < bottom_margin:
                        print 'anchor.y [%r] - bbox.height [%r] < bottom_margin [%r] --> True' % (anchor.y, bbox.height, bottom_margin)
                        display.showPage()
                        anchor = top_left
                        max_height = 0
                    max_height = max(max_height, bbox.height)
                    print 'max height', max_height
                    if ibox.image is not None:
                        print(anchor.x, anchor.y-bbox.height, bbox.width, bbox.height)
                        print('*' * 15)
                        display.drawImage(ImageReader(ibox.image), anchor.x, anchor.y-bbox.height, bbox.width, bbox.height, preserveAspectRatio=True)
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
    print '   ', available_area, image, portion
    box_width = round(portion * available_area.width)
    print '    box width:', box_width
    if image is None:
        box_height = 72
    else:
        image_percent = box_width / image.width
        print '    image percent', image_percent
        box_height = round(image_percent * image.height)
        print '    box height', box_height
    return Area(box_width, box_height)

