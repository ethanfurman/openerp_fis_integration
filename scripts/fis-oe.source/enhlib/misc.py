import sys as _sys

PY_VER = _sys.version_info[:2]

if PY_VER < (3, 0):
    bytes = str
    str = unicode
    unicode = unicode
    basestring = bytes, unicode
    long = long
    baseinteger = int, long
    xrange = xrange
    import __builtin__ as builtins
else:
    bytes = bytes
    str = str
    unicode = str
    basestring = unicode,
    long = int
    baseinteger = int,
    xrange = range
    import builtins

_bi_ord = builtins.ord

def ord(int_or_char):
    if isinstance(int_or_char, baseinteger):
        return int_or_char
    else:
        return _bi_ord(int_or_char)


