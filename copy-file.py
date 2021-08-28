__version__ = '1.04'

import argparse
import sys
from attrdict import AttrDict
from pathlib import Path, PurePath
import subprocess

def create_copy_list(srcdir, destdir, mtime_diff=False, diff=False, no_diff_chk=False):
    cmd = 'diff' if diff else 'copy'
    
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
        if mtime_diff:
            if srcfile.stat().st_mtime == destfile.stat().st_mtime:
                continue
            elif srcfile.stat().st_mtime < destfile.stat().st_mtime:
                # swap the order
                srcfile, destfile = destfile, srcfile
        
        #run diff check next to make sure they are not the same
        if not no_diff_chk:
            # convert files into *NIX format as that is what the command is expecting
            cmdline = ['diff', str(srcfile).replace('\\','/'), str(destfile).replace('\\','/')]
            try:
                result = subprocess.check_output(cmdline)
                # result = subprocess.getoutput(cmdline)
            except subprocess.CalledProcessError as e:
                result = e.output
                
            result_ascii = result.decode('ascii')
            if not result_ascii:
                continue

        # generate the output command
        print(f'{cmd} "{srcfile}" "{destfile}"')


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
    parser.add_argument('--diff', action="store_true", default=False,
                        help="run diff rather than copy when timestamps are different")
    parser.add_argument('--no_diff_chk', action="store_true", default=False,
                        help="Disable when timestamps are different run diff to see if they are the same")
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


    create_copy_list(args.src, args.dest, args.mtime, args.diff, args.no_diff_chk)
