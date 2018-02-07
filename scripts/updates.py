"""
Searches current directory for Python source files, imports them,
and updates a mapping of FIS file -> OpenERP script so those
scripts can be executed when the matching file changes.

FIS_mapping = {
    <fis_file> : [script, script, ... ],
    }

Scripts will be called with the changed table as the first argument
and possibly 'quick' or 'full' with quick being the default:
- quick -> look for changes against previous version of FIS table
- full -> look for changes agains the corresponding OpenERP records
"""
from __future__ import print_function

from antipathy import Path
from scription import error
from traceback import format_exc

script_verbosity = 0

def get_script_mapping():
    FIS_mapping = {}
    # load the files and extract the mappings
    candidates = [
            p
            for p in Path(__file__).path.glob('*.py')
            if not p.endswith('__init__.py')
            ]
    print(candidates, verbose=2)
    for data in candidates:
        info = {'FIS_mapping': {}}
        try:
            with open(data) as f:
                info.update(eval(f.read()))
            print(info, verbose=3)
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
    for k, v in sorted(FIS_mapping.items()):
        print('%s: %r' % (k, v), verbose=2)
    return FIS_mapping
