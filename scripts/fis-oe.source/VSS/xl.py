from functools import partial as _partial
import xlrd
import sys as _sys
_sys.modules['VSS.xl.xlrd'] = xlrd

__all__ = ('xlrd', 'open_workbook')

def _get_sheet(self, index_or_name):
    if isinstance(index_or_name, (int, long)):
        return self.sheet_by_index(index_or_name)
    return self.sheet_by_name(index_or_name)
xlrd.book.Book.__getitem__ = _get_sheet
del _get_sheet

def _get_row_col(self, row_col):
    if isinstance(row_col, (int, long)):
        return self.row(row_col)
    else:
        row, col = row_col
        return self.cell(row, col)
xlrd.sheet.Sheet.__getitem__ = _get_row_col
del _get_row_col

def _rows_gen(self, start_row=0, end_row=None, start_col=0, end_col=None):
    "returns each row as a list of values"
    if end_row is None:
        end_row = self.nrows
    for y in xrange(start_row, end_row):
        yield self.row_values(y, start_col, end_col)
xlrd.sheet.Sheet.rows = _rows_gen
del _rows_gen

open_workbook = _partial(xlrd.open_workbook, on_demand=True)
