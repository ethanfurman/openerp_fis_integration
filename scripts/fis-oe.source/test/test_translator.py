from VSS.utils import translator
try:
    from string import letters, digits, lowercase, uppercase
except ImportError:
    from string import ascii_letters as letters, digits, ascii_lowercase as lowercase, ascii_uppercase as uppercase

def test_alpha():
    alpha = translator(keep=letters)
    assert alpha('ethan7') == 'ethan'
    assert alpha('1234z') == 'z'
    assert alpha('ABCdef') == 'ABCdef'
    assert alpha('1234') == ''

def test_no_alpha():
    no_alpha = translator(delete=letters)
    assert no_alpha('ethan7') == '7'
    assert no_alpha('1234z') == '1234'
    assert no_alpha('ABCdef') == ''
    assert no_alpha('1234') == '1234'
    assert no_alpha('+|%.') == '+|%.'

def test_replacement():
    replace = translator(to=' ', keep=letters)
    assert replace('ethan7') == 'ethan '
    assert replace('1234z') == '    z'
    assert replace('ABCdef') == 'ABCdef'
    assert replace('1234') == '    '
    assert replace('ABC-def') == 'ABC def'

def test_replacement_condense():
    replace = translator(to=' ', keep=letters, compress=True)
    assert replace('ethan7') == 'ethan'
    assert replace('1234z') == 'z'
    assert replace('ABCdef') == 'ABCdef'
    assert replace('1234') == ''
    assert replace('ABC-def') == 'ABC def'
    assert replace('ABC-def//GhI') == 'ABC def GhI'

def test_upper():
    upper = translator(frm=lowercase, to=uppercase)
    assert upper('ethan7') == 'ETHAN7'
    assert upper('1234z') == '1234Z'
    assert upper('ABCdef') == 'ABCDEF'
    assert upper('1234') == '1234'
    assert upper('ABC-def') == 'ABC-DEF'
    assert upper('ABC-def//GhI') == 'ABC-DEF//GHI'

def test_mostly_upper():
    upper = translator(frm=lowercase, to=uppercase, delete=digits)
    assert upper('ethan7') == 'ETHAN'
    assert upper('1234z') == 'Z'
    assert upper('ABCdef') == 'ABCDEF'
    assert upper('1234') == ''
    assert upper('ABC-def') == 'ABC-DEF'
    assert upper('ABC-def//789...GhI') == 'ABC-DEF//...GHI'
