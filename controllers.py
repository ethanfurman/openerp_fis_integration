# -*- coding: utf-8 -*-

# imports
from openerp.addons.web import http
from openerp.addons.web.controllers.main import content_disposition
from antipathy import Path
from urllib import urlopen
import logging
import mimetypes
import re
import werkzeug

_logger = logging.getLogger(__name__)
bmp_base = Path('/mnt/newlabeltimexpvm/xfer/LabelDirectory/')
png_base = Path('/PNG_labels/')
markem_base = Path('http://192.168.11.16:8000/')
markem_status = 'mkPngXfStatus.htm'

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
        full_target_file = png_base / target_file.stem[:-20] + target_file.ext
        # continue normally
        #
        try:
            if not full_target_file.exists():
                raise MissingFile(full_target_file)
            with (full_target_file).open('rb') as fh:
                file_data = fh.read()
            return request.make_response(
                    file_data,
                    headers=[
                        ('Content-Disposition',  content_disposition(full_target_file.filename, request)),
                        ('Content-Type', mimetypes.guess_type(full_target_file.filename)[0] or 'octet-stream'),
                        ('Content-Length', len(file_data)),
                        ('Cache-Control', 'no-cache'),
                        ],
                    )
        except MissingFile:
            _logger.error('missing file: %s at %s', target_file, full_target_file)
            return request.not_found('file %r not found' % (target_file, ))
        except Exception:
            _logger.exception('Error processing %r', target_file)
            return werkzeug.exceptions.InternalServerError(
                    'An error occured attempting to access %r; please let IT know.'
                    % (str(target_file.filename),))


class MarkemStatus(http.Controller):
    _cp_path = "/fis/markem"

    def _fix_url(self, matches):
        for t in matches.groups():
            if t.startswith(markem_base):
                t = t[len(markem_base):]
            # t = '"http://localhost:8069/fis/markem/status/%s"' % t
            t = '"/fis/markem/status/%s"' % t
            return t

    def _get_url(self, target):
        url = None
        try:
            url = urlopen(target)
            return url.info(), url.read()
        finally:
            if url is not None:
                url.close()

    @http.httprequest
    def status(self, request, **kw):
        _logger.debug('request path: %r', request.httprequest.path)
        target_path = markem_base / (request.httprequest.path[19:] or markem_status)
        _logger.debug('getting %r', target_path)
        info, data = self._get_url(target_path)
        _logger.debug('info: %r  %r', info.gettype(), info.getplist())
        if info.gettype() != 'text/html':
            return request.make_response(
                    data,
                    headers=[
                        ('Content-Disposition',  content_disposition(target_path.filename, request)),
                        ('Content-Type', info.gettype()),
                        ('Content-Length', len(data)),
                        ],
                    )
        data = re.sub('(?<=href=)("[^"]*"|.*?)(?=\s|>)', self._fix_url, data)
        data = re.sub('(?<=src=)("[^"]*"|.*?)(?=\s|>)', self._fix_url, data)
        return request.make_response(
                data,
                headers=[
                    ('Content-Type', 'text/html'),
                    ('Content-Length', len(data)),
                    ],
                )





class MissingFile(Exception):
    pass
