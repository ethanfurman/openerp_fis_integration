"""
Searches current directory for Python source files, imports them,
and updates a mapping of FIS file -> OpenERP script so those
scripts can be executed when the matching file changes.

FIS_mapping = {
    <fis_file> : [script, script, ... ],
    }
"""

from antipathy import Path
from scription import error
from traceback import format_exc

def get_script_mapping():
    FIS_mapping = {}
    # load the files and extract the mappings
    candidates = [
            p
            for p in Path(__file__).path.glob('*.py')
            if not p.endswith('__init__.py')
            ]
    print candidates
    for data in candidates:
        info = {'FIS_mapping': {}}
        try:
            with open(data) as f:
                info.update(eval(f.read()))
            print info
            for fis, scripts in info['FIS_mapping'].items():
                if isinstance(scripts, str):
                    scripts = [scripts]
                current_scripts = FIS_mapping.setdefault(fis, set())
                for s in scripts:
                    if not isinstance(s, str):
                        raise ValueError('file %r, invalid script: %r ' % (data, s))
                for s in scripts:
                    current_scripts.add(s)
        except Exception:
            tb = format_exc()
            error('=' * 50, 'file: %s' % data, tb, '=' * 50, sep='\n')
            continue
    return FIS_mapping
