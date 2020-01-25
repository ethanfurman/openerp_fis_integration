# -*- coding: utf-8 -*-

# imports
from openerp.addons.web import http
from openerp.addons.web.controllers.main import content_disposition
from antipathy import Path
import logging
import mimetypes
import re
import werkzeug

_logger = logging.getLogger(__name__)
base = Path('/mnt/labeltime/Labels')

IMAGE_ALTERNATES = {'MK': 'CC', 'B': 'PKG'}

# work horses

class ProductLabel(http.Controller):
    _cp_path = "/fis/product"

    @http.httprequest
    def label(self, request, **kw):
        # i.e. /fis/product/label/000065MK.BMP
        target_file = Path(request.httprequest.path[19:])
        backups = []
        last_type = None
        for key, value in IMAGE_ALTERNATES.items():
            if target_file.base.upper().endswith(key):
                last_type = key
                backups = value
                if isinstance(backups, basestring):
                    backups = (backups, )
                backups = list(backups)
                break
        item_no = target_file[:6]
        path_file = base / item_no / target_file
        #
        tried_files = []
        tried_paths = []
        while True:
            if path_file.exists() and not path_file.isdir():
                break
            tried_files.append(path_file.filename)
            tried_paths.append(path_file)
            if not backups:
                _logger.warning('missing: %s', ', '.join(tried_paths))
                return request.not_found('missing: %s' % (', '.join(tried_files), ))
            new_type = backups.pop(0)
            new_base = re.sub(last_type+'$', new_type, path_file.base)
            path_file = path_file.scheme / path_file.dirs / new_base + path_file.ext
            last_type = new_type
        #
        try:
            with (path_file).open('rb') as fh:
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
        except Exception:
            _logger.exception('error accessing %r', path_file)
            return werkzeug.exceptions.InternalServerError(
                    'An error occured attempting to access %r; please let IT know.'
                    % (str(path_file.filename),))

