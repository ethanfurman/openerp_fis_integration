# -*- coding: utf-8 -*-

# imports
from openerp.addons.web import http
from openerp.addons.web.controllers.main import content_disposition
from antipathy import Path
import logging
import mimetypes
import werkzeug

_logger = logging.getLogger(__name__)
bmp_base = Path('/mnt/labeltime/Labels/')
png_base = Path('/PNG_labels/')

# work horses

class ProductLabel(http.Controller):
    _cp_path = "/fis/product"

    @http.httprequest
    def label(self, request, **kw):
        # i.e. /fis/product/label/000065MK-20200117T08:33:41.png
        #
        # isolate filename
        target_file = Path(request.httprequest.path[19:])
        # remove timestamp
        target_file = png_base + target_file.dirname + target_file.stem[:-20] + target_file.ext
        # continue normally
        #
        try:
            if not target_file.exists():
                raise MissingFile(target_file)
            with (target_file).open('rb') as fh:
                file_data = fh.read()
            return request.make_response(
                    file_data,
                    headers=[
                        ('Content-Disposition',  content_disposition(target_file.filename, request)),
                        ('Content-Type', mimetypes.guess_type(target_file.filename)[0] or 'octet-stream'),
                        ('Content-Length', len(file_data)),
                        ('Cache-Control', 'no-cache'),
                        ],
                    )
        except MissingFile:
            return request.not_found('file %r not found' % (target_file, ))
        except Exception:
            _logger.exception('Error processing %r', target_file)
            return werkzeug.exceptions.InternalServerError(
                    'An error occured attempting to access %r; please let IT know.'
                    % (str(target_file.filename),))


class MissingFile(Exception):
    pass
