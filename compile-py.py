__version__ = '1.01'

import argparse
import sys
from attrdict import AttrDict
from pathlib import Path, PurePath


def create_compile_list(srcdir):
    srcdir = Path(srcdir)

    for file in srcdir.glob('*.py'):
        print(f'python -m py_compile {file}')


# ---------------------------------------------------------------------------
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Compile commands for python files in a directory')
    parser.add_argument("--src", '-s', default=Path('.'),
                        help="Source directory (default: current directory)")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    args = parser.parse_args()
    args = AttrDict(vars(args))

    for dir in ['src']:
        dir2chk = args[dir]

        if not Path(dir2chk).is_dir():
            print(f'{dir} is not an existing directory: {dir2chk}')
            sys.exit(1)

    create_compile_list(args.src)
