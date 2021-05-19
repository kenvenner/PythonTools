__version__ = '1.01'

import argparse
import sys
from attrdict import AttrDict
from pathlib import Path, PurePath

def create_copy_list(srcdir, destdir, mtime_diff=False):
    srcdir = Path(srcdir)
    destdir = Path(destdir)

    srcfiles = list(srcdir.glob('*.py'))
    destfiles = list(destdir.glob('*.py'))
                    
    srcfilenames = [x.name for x in srcfiles]
    destfilenames = [x.name for x in destfiles]

    copyfilenames = [x for x in srcfilenames if x in destfilenames]

    for filename in copyfilenames:
        # get the Path version of the filename
        srcfile = [x for x in srcfiles if x.name == filename][0]
        destfile = [x for x in destfiles if x.name == filename][0]

        # if we enable time checks - and files are same timestamp skip
        if mtime_diff and srcfile.stat().st_mtime == destfile.stat().st_mtime:
            continue
        
        print(f'copy {srcfile} {destfile}')

def create_compile_list(srcdir):
    srcdir = Path(srcdir)

    for file in srcdir.glob('*.py'):
        print(f'python -m py_compile {file}')


# ---------------------------------------------------------------------------
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Windows copy command for same files in two dirs ')
    parser.add_argument('dest',
                        help="Destination directory to compare")
    parser.add_argument("--src", '-s', default=Path('.'),
                        help="Source directory (default: current directory)")
    parser.add_argument('--mtime', action="store_true", default=False,
                        help="Copy when time stamps are different")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args = AttrDict(vars(args))

    for dir in ['dest', 'src']:
        dir2chk = args[dir]
        
        if not Path(dir2chk).is_dir():
            print(f'{dir} is not an existing directory: {dir2chk}')
            sys.exit(1)


    create_copy_list(args.src, args.dest, args.mtime)

