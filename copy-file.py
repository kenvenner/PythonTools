__version__ = '1.08'

import argparse
import sys
#from attrdict import AttrDict
from pathlib import Path, PurePath
import subprocess

def create_copy_list(srcdir, destdir, mtime_diff=False, diff=False, no_diff_chk=False, ext=None, winmerge=False, wmcmd=None):
    if ext is None:
        ext = 'py'

    if diff:
        cmd = 'diff'
    elif winmerge:
        cmd = wmcmd
    else:
        cmd = 'copy'
    
    srcdir = Path(srcdir)
    destdir = Path(destdir)

    file_glob_string = '*.' + ext
    
    srcfiles = list(srcdir.glob(file_glob_string))
    destfiles = list(destdir.glob(file_glob_string))
                    
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

        # now inspect the file to see if there is a version number in the file
        with open(srcfile, 'r') as t:
            filelines = t.readlines()

            src_version_lines = [x.strip('\n') for x in filelines if '__version__' in x or 'AppVersion' in x]
            
        with open(destfile, 'r') as t:
            filelines = t.readlines()

            dest_version_lines = [x.strip('\n') for x in filelines if '__version__' in x or 'AppVersion' in x]

        if False:
            print('src_version_lines:', src_version_lines)
            print('dest_version_lines:', dest_version_lines)

        if src_version_lines and dest_version_lines:
            if dest_version_lines[0] > src_version_lines[0]:
                if False:
                    print('swapped order:')
                    print(srcfile)
                    print(destfile)
                    print(src_version_lines[0])
                    print(dest_version_lines[0])

                destfile, srcfile = srcfile, destfile

        # generate the output command
        print(f'{cmd} "{srcfile}" "{destfile}"')


def create_compile_list(srcdir, ext=None):
    if ext is None:
        ext = 'py'

    file_glob_string = '*.' + ext

    srcdir = Path(srcdir)

    for file in srcdir.glob(file_glob_string):
        print(f'python -m py_compile {file}')


# ---------------------------------------------------------------------------
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Windows copy command for same files in two dirs ')
    parser.add_argument('dest',
                        help="Destination directory to compare")
    parser.add_argument("--src", '-s', default=Path('.'),
                        help="Source directory (default: current directory)")
    parser.add_argument("--ext",
                        help="File extension we are looking for - no period (default: py)")
    parser.add_argument('--mtime', action="store_true", default=False,
                        help="Copy when time stamps are different")
    parser.add_argument('--diff', action="store_true", default=False,
                        help="run diff rather than copy when timestamps are different")
    parser.add_argument('--winmerge', action="store_true", default=False,
                        help="run winmerge diff rather than copy when timestamps are different")    
    parser.add_argument('--no_diff_chk', action="store_true", default=False,
                        help="Disable when timestamps are different run diff to see if they are the same")
    parser.add_argument("--wmcmd", '-w', default='"C:\\Program Files\\WinMerge\\WinMergeU.exe"',
                        help="the format string used to generate the command to execute winmerge diff")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)



    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args = vars(args)

    # directory check on two directories
    for dir in ['dest', 'src']:
        dir2chk = args[dir]
        
        if not Path(dir2chk).is_dir():
            print(f'{dir} is not an existing directory: {dir2chk}')
            sys.exit(1)

    # call the routine
    create_copy_list(args['src'], args['dest'], args['mtime'], args['diff'], args['no_diff_chk'], args['ext'], args['winmerge'], args['wmcmd'])

# eof
