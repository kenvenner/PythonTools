__version__ = '1.12'
BuildVersion = '1'

"""
@author:   Ken Venner
@contact:  ken@venerllc.com
@version:  1.12

Tooling that creates a new major/minor version on a file

"""
import re
import os
import subprocess
import argparse

import kvutil
import kvargs

# may comment out in the future
import pprint

pp = pprint.PrettyPrinter(indent=4)

# logging
import sys
import kvlogger

# pick the log file structure from list below
# single file that is rotated
config = kvlogger.get_config(kvutil.filename_create(__file__, filename_ext='log', path_blank=True),
                             loggerlevel='NOTSET')  # single file
# one file per day of month
# config=kvlogger.get_config(kvutil.filename_log_day_of_month(__file__, ext_override='log'), 'logging.FileHandler') # one file per day of month
kvlogger.dictConfig(config)
logger = kvlogger.getLogger(__name__)


# added logging feature to capture and log unhandled exceptions
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # if this is a keyboard interrupt - we dont' want to handle it here
        # reset and return
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # other wise catch/log this error
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


# create overall hook to catch uncaught exceptions
sys.excepthook = handle_exception

# application variables
optiondictconfig = {
    'AppVersion': {
        'value': '1.12',
        'description': 'defines the version number for the app',
    },
    'input_folder': {
        'value': './',
        'description': 'defines the folder that we do the git status and then evaluate git diff and do version increments',
    },
    'input_file': {
        'value': '',
        'description': 'when set defines the file that we are incrementing the version number for',
    },
    'input_list': {
        'value': None,
        'type': 'liststr',
        'description': 'defines the comma separated list of definition xls files we are parsing and processing',
    },
    'input_glob': {
        'value': None,
        'description': 'defines the file glob used to define the list of definition xls files to be read in and processed',
    },
    'input_list_file': {
        'value': None,
        'description': 'defines the file that contains filenames to be read - one line per file',
    },
    'exclude_list_file': {
        'value': None,
        'description': 'defines the file that contains filenames to be read excluded - one line per file',
    },
    'major_update': {
        'value': False,
        'type': 'bool',
        'description': 'flag when set drives a major version upgrade vs minor version upgrade',
    },
    'buildonly': {
        'value': False,
        'type': 'bool',
        'description': 'flag when set drives a build version only update',
    },
    'test': {
        'value': False,
        'type': 'bool',
        'description': 'flag when set does not cause a file update',
    },
    'debug': {
        'value': False,
        'type': 'bool',
        'description': 'flag when set causes intermediate prints to track program activity',
    },
}

# -- CONSTANTS -- #
rePgmVerLine = re.compile(r'__version__\s* =\s* \'(\d+)\.(\d+)')
reVerLine = re.compile(r'@version:\s+(\d+)\.(\d+)')
reAppVerLine = re.compile(r'AppVersion\s+=\s+\'(\d+)\.(\d+)\'')
reBuildVerLine = re.compile(r'(BuildVersion\s*=\s*\'(\d+)\')')

reOptVerLine = re.compile(r'AppVersion\'\s*:\s*{')
reOptValueLine = re.compile(r'^\s+\'value\'\s*:\s*\'(\d+)\.(\d+)\'')

reSearchList = [rePgmVerLine, reVerLine, reAppVerLine]

reGitModified = re.compile(r'\s+modified:\s+(.*)')

fmtVersion2d = '{}.{:02d}'
fmtVersion3d = '{}.{:03d}'
fmtOptValue = "        'value': '{}',\n"
fmtVerLine = '@version:  {}\n'
fmtAppVerLine = 'AppVersion = \'{}\'\n'
fmtPgmVerLine = '__version__ = \'{}\'\n'

fmtBuildVerLine = 'BuildVersion = \'{}\''

fmtSearchList = [fmtPgmVerLine, fmtVerLine, fmtAppVerLine]

'''
line='BuildVersion=\'3\'   ## comments'
bld_version_found=False
new_bld_version=''
'''
def build_version_update(line, bld_version_found, new_bld_version) -> tuple[str, bool, str, str]:
    """
    check the  line to see if a bld version updates is needed and cause the update

    inputs:
        line - str - the line in the file
        bld_version_found - bool - have we previously found a bld_version line
        new_bld_version - str - the bld version set by the last record we got

    returns
        line - the same or new line with build version updated
        bld_version_found - bool - flag if this line is a bld versoin update line
        bld_version_old - int - the found value on this record for the bld version
        bld_version_new - int - the found value on this record for the bld version
        new_bld_version - str - the new value for bld version

    """

    # create the new here  the rest are passed in
    bld_version_old = None
    bld_version_new = None
    
    if not line:
        return line, bld_version_found, bld_version_old, bld_version_new, new_bld_version

    # search the line
    m = reBuildVerLine.search(line)

    # not a build line
    if not m:
        return line, bld_version_found, bld_version_old, bld_version_new, new_bld_version

    # capture the bld_version from this line
    bld_version_old = int(m.group(2))

    # check to see if we already saw and set the build version
    if not bld_version_found:
        # previously set and changed
        bld_version_found = True
        bld_version_new = bld_version_old+1
        new_bld_version = fmtBuildVerLine.format(str(bld_version_new))
        line=line.replace(m.group(1), new_bld_version)
    else:
        line=line.replace(m.group(1), new_bld_version)
        bld_version_new = int(new_bld_version.split(' ')[2].replace("'",""))
        
    # return what we found
    return line, bld_version_found, bld_version_old, bld_version_new, new_bld_version
    
def update_file_version(filename, major_update=False, buildonly=False, test=False, debug=False):
    file_tmp = kvutil.filename_create(filename, filename_ext='tmp')
    file_bak = kvutil.filename_create(filename, filename_ext='bak')

    if debug:
        print('update_file_version:start')
        print('update_file_version:filename:', filename)
        print('update_file_version:file_bak:', file_bak)
        print('update_file_version:file_tmp:', file_tmp)
        print('update_file_version:major_update:', major_update)
        print('update_file_version:buildonly:', buildonly)
        print('update_file_version:test:', test)

    app_ver = ''
    new_app_ver = ''
    bld_ver = ''
    new_bld_ver = ''
    
    bld_version = ''
    new_bld_version = ''
    version_found = False
    bld_version_found = False
    opt_ver_found = False

    version_changed = False

    with open(file_tmp, 'w') as fpOut:
        with open(filename, 'r') as fpIn:
            filelines = fpIn.readlines()

        for line in filelines:
            # cpature if this is a build update
            if buildonly:
                # process this line for build version update
                line, bld_version_found, bld_version_old, bld_version_new, new_bld_version = build_version_update(line, bld_version_found, new_bld_version)

                # capture a version change
                if not version_changed and bld_version_found:
                    version_changed = True
                    version_found = True

                    bld_ver = str(bld_version_old)
                    new_bld_ver = str(bld_version_new)
                    
                # output this line
                fpOut.write(line)
                continue
            
            # do the major/minor version update
            if version_found:
                if opt_ver_found:
                    # clear the flag no matter what
                    opt_ver_found = False
                    # this next line should be the value line to test for it
                    if reOptValueLine.search(line):
                        version_changed = True
                        fpOut.write(fmtOptValue.format(new_app_ver))
                        continue

                if reOptVerLine.search(line):
                    opt_ver_found = True
                elif reAppVerLine.search(line):
                    if debug:
                        print('AppVerLine')
                        print('line:', line)
                        print('now.:', fmtAppVerLine.format(new_app_ver))
                    version_changed = True
                    fpOut.write(fmtAppVerLine.format(new_app_ver))
                    continue
                elif rePgmVerLine.search(line):
                    if debug:
                        print('PgmVerLine')
                        print('line:', line)
                        print('now.:', fmtPgmVerLine.format(new_app_ver))
                    version_changed = True
                    fpOut.write(fmtPgmVerLine.format(new_app_ver))
                    continue
                elif reVerLine.search(line):
                    if debug:
                        print('VerLine')
                        print('line:', line)
                        print('now.:', VerLine.format(new_app_ver))
                    version_changed = True
                    fpOut.write(fmtVerLine.format(new_app_ver))
                    continue
            else:
                # find the first version defintion and use it to set the version
                for srch_idx, reSearchRegex in enumerate(reSearchList):
                    m = reSearchRegex.search(line)
                    if m:
                        # app_ver = m.group(1)
                        major_ver = int(m.group(1))
                        minor_ver = int(m.group(2))
                        app_ver = '{}.{}'.format(m.group(1), m.group(2))

                        if debug:
                            print('matching line:', line)
                            print('major_ver:', major_ver)
                            print('minor_ver:', minor_ver)

                        if major_update:
                            new_major_ver = major_ver + 1
                            new_minor_ver = 1
                        else:
                            new_major_ver = major_ver
                            new_minor_ver = minor_ver + 1

                        if new_minor_ver < 100:
                            new_app_ver = fmtVersion2d.format(new_major_ver, new_minor_ver)
                        else:
                            new_app_ver = fmtVersion3d.format(new_major_ver, new_minor_ver)

                        if debug:
                            print('major_ver-updt:', new_major_ver)
                            print('minor_ver-updt:', new_minor_ver)
                            print('new_app_ver:', new_app_ver)
                            print('srch_idx:', srch_idx)
                            print('line:', line)
                            print('new.:', fmtSearchList[srch_idx].format(new_app_ver))

                        version_found = True
                        version_changed = True
                        fpOut.write(fmtSearchList[srch_idx].format(new_app_ver))
                        break

                if version_found:
                    continue

            fpOut.write(line)

    if debug:
        print('update_file_version:version_found:', version_found)
        print('update_file_version:version_changed:', version_changed)
        print('update_file_version:test:', test)

    # create temp file determine if we take existing file
    # convert to bak and make tmp the current file
    if version_found and version_changed:
        if not test:
            if os.path.exists(file_bak):
                kvutil.remove_filename(file_bak)
            os.rename(filename, file_bak)
            os.rename(file_tmp, filename)
        return app_ver, new_app_ver, filename, file_bak, bld_ver, new_bld_ver
    else:
        return app_ver, None, None, None, None, None


def git_modified_files_in_folder(folder_path='', debug=False):
    files_modified = list()

    if folder_path == './':
        folder_path = ''

    if debug:
        print('git_modified_files_in_folder:folder_path:', folder_path)

    # define when we stop looking
    untracked = "Untracked files:"

    # git status call to find files that changed
    if folder_path:
        result = subprocess.run(['git', 'status', folder_path], stdout=subprocess.PIPE)
    else:
        result = subprocess.run(['git', 'status'], stdout=subprocess.PIPE)

    for line in result.stdout.decode('utf-8').split('\n'):
        if debug:
            print('git_modified_files_in_folder:line:', line)

        if line == untracked:
            if debug:
                print('git_modified_files_in_folder:encountered the untracked line, files modified list is:',
                      files_modified)
            return files_modified

        m = reGitModified.search(line)
        if m:
            filename = m.group(1)
            basename = os.path.basename(filename)
            dirname = os.path.dirname(filename)
            if debug:
                print('git_modified_files_in_folder:dirname:', dirname)
            if folder_path == dirname:
                files_modified.append(filename)
                if debug:
                    print('git_modified_files_in_folder:filename:', filename)

    return files_modified


def version_changed_in_git_branch(filename, debug=False):
    MAXLINES_CHECKED = 100
    # get the diff on this file with what was last committed to git
    result = subprocess.run(['git', 'diff', filename], stdout=subprocess.PIPE)

    if debug:
        print('version_changed_in_git_branch:maxlines_checked:', filename)
        print('version_changed_in_git_branch:maxlines_checked:', MAXLINES_CHECKED)
        print('version_changed_in_git_branch:results of git diff:\n', result)

    linecnt = 0
    for line in result.stdout.decode('utf-8').split('\n'):
        linecnt += 1
        if debug:
            print('{:02d}:line:{}'.format(linecnt, line))
        if reVerLine.search(line) and line.startswith('-'):
            return True
        if linecnt > MAXLINES_CHECKED:
            if debug:  print('Maxline met before finding field of interest')
            return False

    return False


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    args_default = dict()
    req_flds = list()

    parser = argparse.ArgumentParser(description='Increment version of files')
    parser.add_argument("input_file", nargs="*",
                        help="file we are updating the version on")
    parser.add_argument("--input_folder", default="./",
                        help="folder of files to be analyzed and processed")
    parser.add_argument("--input_list",
                        help="list of files to be processed")
    parser.add_argument("--input_glob",
                        help="file glob files to be processed")
    parser.add_argument("--major_update", "--major", "--major_ver", action="store_true", dest="major_update",
                        help="Perform a major version update")
    parser.add_argument("--minor_update", "--minor", "--minor_ver", action="store_true", dest="minor_update",
                        help="Perform a minor version update")
    parser.add_argument("--buildonly", "--build", "--compile", action="store_true", dest="buildonly",
                        help="Perform a build version only update")
    parser.add_argument("--conf",
                        help="configuration file")
    parser.add_argument("--test", action="store_true",
                        help="Run in test mode")
    parser.add_argument("--debug", action="store_true",
                        help="Run in debug mode")
    parser.add_argument("--disp_vargs", action="store_true",
                        help="Display command line options")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__ + '.' + BuildVersion)

    # elimniate AttrDict so now need to deal with a dict
    vargs = kvargs.prep_parse_and_merge_settings(parser, args_default)

    # display the settings
    if vargs.get('disp_vargs'):
        print('vargs:')
        pp.pprint(vargs)

    if vargs.get('major_update') and vargs.get('minor_update'):
        print("Set only one true:  minor_update, major_update")
        sys.exit(1)
    elif vargs.get('buildonly'):
        vargs['minor_update'] = False
        vargs['major_update'] = False
    elif not vargs.get('major_update') and not vargs.get('minor_update'):
        vargs['minor_update'] = True

    # get the list of files to be processed
    filelist = kvutil.filename_list(vargs['input_file'], vargs['input_list'], vargs['input_glob'], glob_filename=True)

    # our behavior is controlled if we set the input_file, if we don't the we do the git evaluation
    if filelist:
        vargs['input_folder'] = ''

        logger.info('files to be processed:%s', filelist)

        for chk_file in filelist:
            # check for the existance of the file
            if not os.path.exists(chk_file):
                print('File does not exist - skipped:', chk_file)
                continue
            
            appVer, newAppVer, filename, file_bak, bldVer, newBldVer = update_file_version(chk_file,
                                                                        major_update=vargs['major_update'],
                                                                        buildonly=vargs['buildonly'],
                                                                        test=vargs['test'],
                                                                        debug=vargs['debug'])
            logger.info(
                'version changed in git for:%s:outputs are appVer:%s, newAppVer:%s, filename:%s, file_bak:%s, bldVer:%s, newBldVer:%s',
                chk_file, appVer, newAppVer, filename, file_bak, bldVer, newBldVer)

    else:
        logger.info('folder to be processed:%s', vargs['input_folder'])

        files_to_check = git_modified_files_in_folder(vargs['input_folder'], debug=vargs['debug'])

        if vargs['debug']:
            print('files_to_check:', files_to_check)

        if not files_to_check:
            logger.info('no files to be checked for this folder')

        for chk_file in files_to_check:
            # check for the existance of the file
            if not os.path.exists(chk_file):
                print('File does not exist - skipped:', chk_file)
                continue
            
            if vargs['debug']:
                print('-' * 40, '\nInspecting for version  number file:', chk_file)

            if not version_changed_in_git_branch(chk_file, debug=vargs['debug']):

                appVer, newAppVer, filename, file_bak = update_file_version(chk_file,
                                                                            major_update=vargs['major_update'],
                                                                            test=vargs['test'],
                                                                            debug=vargs['debug'])
                logger.info(
                    'version changed in git for:%s:outputs are appVer:%s, newAppVer:%s, filename:%s, file_bak:%s'.
                        chk_file, appVer, newAppVer, filename, file_bak)
            else:
                logger.info('version previously changed in git for: %s', chk_file)
