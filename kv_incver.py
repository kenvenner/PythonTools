__version__ = '1.12'
BuildVersion = '3'

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
rePgmVerLine = re.compile(r'(__version__\s*=\s*\'((\d+)\.(\d+))\')')
reAtVerLine = re.compile(r'(\@version\s*:\s*((\d+)\.(\d+)))')
reAtQuoteVerLine = re.compile(r'(\@version\s*:\s*\'((\d+)\.(\d+))\')')
reAppVerLine = re.compile(r'(AppVersion\s*=\s*\'((\d+)\.(\d+))\')')
reBuildVerLine = re.compile(r'(BuildVersion\s*=\s*\'(\d+)\')')

reOptVerLine = re.compile(r'AppVersion\'\s*:\s*{')
reOptValueLine = re.compile(r'^\s+(\'value\'\s*:\s*\'((\d+)\.(\d+))\')')

reSearchList = [rePgmVerLine, reAtVerLine, reAppVerLine]

reGitModified = re.compile(r'\s+modified:\s+(.*)')

fmtVersion2d = '{}.{:02d}'
fmtVersion3d = '{}.{:03d}'
fmtOptValue = "'value': '{}'"
fmtAtVerLine = '@version: {}'
fmtAtQuoteVerLine = '@version: \'{}\''
fmtAppVerLine = 'AppVersion = \'{}\''
fmtPgmVerLine = '__version__ = \'{}\''

fmtBuildVerLine = 'BuildVersion = \'{}\''

fmtSearchList = [fmtPgmVerLine, fmtAtVerLine, fmtAppVerLine]

SEARCH4VERSION = [
    (reAppVerLine, fmtAppVerLine, 'AppVerLine'),
    (rePgmVerLine, fmtPgmVerLine, 'PgmVerLine'),
    (reAtVerLine, fmtAtVerLine, 'AtVerLine'),
    (reAtQuoteVerLine, fmtAtQuoteVerLine, 'AtQuoteVerLine')
]


def debug_print(msg, new_app_ver, new_version, m, line, version_changed, opt_ver_found):
    """
    Display the variables of interest
    """
    print(msg)
    print(f'{new_app_ver=}')
    print(f'{new_version=}')
    print(f'{m.group(0)=}')
    print(f'{m.group(1)=}')
    print(f'{m.group(2)=}')
    print(f'{m.group(3)=}')
    print(f'{m.group(4)=}')
    print(f'{line=}')
    print(f'{version_changed=}')
    print(f'{opt_ver_found=}')

'''
line='BuildVersion=\'3\'   ## comments'
bld_version_found=False
new_bld_version=''
'''
def build_version_update(line: str, bld_version_found: bool, new_bld_version: str) -> tuple[str, bool, str, str]:
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

def calc_new_app_ver(m, major_update: bool, debug: bool=False) -> str:
    """
    Take in the re results that has groups 
    extract out the major and minor versoins
    increment them and return back the versoin string

    inputs:
        m - restuls of an re search where group 3 is the major versoin and group 4 is the minor versoin
        major_update - bool - when true we are incrementing ht emajor version and setting minor to 1

    returns 
        new_app_ver - str of the major  and minor versoins concatenated
    """

    # first time we are finding a version so grap it and increment it
    if major_update:
        major_version = int(m.group(3))+1
        minor_version = 1
    else:
        major_version = int(m.group(3))
        minor_version = int(m.group(4))+1
    if minor_version > 99:
        new_app_ver = fmtVersion3d.format(major_version, minor_version)
    else:
        new_app_ver = fmtVersion2d.format(major_version, minor_version)

    if debug:
        print('calc_new_app_ver')
        print(f'{major_update=}')
        print(f'{major_version=}')
        print(f'{minor_version=}')
        print(f'{new_app_ver=}')
        
    return new_app_ver


def major_minor_version_update(line: str, new_app_ver: str, version_found: bool, opt_ver_found: bool, major_update: bool=False, debug: bool=False ) -> tuple[str, bool, bool, str, bool]:
    """
    take in a line and the inputs and return back the same line or a new line with a versoin change

    inputs:
        line - str - the line we are processing
        new_app_ver - str - the new application version string if we already set it or blank
        version_found - bool - flag telling us if we have found a version # for this file and reuse the set version number or we need to calculate a new version number
        major_update - bool - if we are calculating a version number - is it a minor versoin change or a major version change
        debug - bool - display print messages so we can track along

    returns:
        line - str - the original or updated line
        version_found - bool - did we find a version object on this line to update
        opt_ver_found - bool - did this line have a optiondictconfig that defines a version number
        new_app_ver - str - exiting or new app version that we are setting
        version_changed - bool - was this line changed

    """
    version_changed = False

    if debug:
        print('\n'+'-'*40)
        print(f'{line=}')
        print(f'{new_app_ver=}')
        print(f'{version_found=}')
        print(f'{opt_ver_found=}')
        print(f'{major_update=}')
        print('-'*20)
        
    # we already found a version change record
    if opt_ver_found:
        # prior line was an option versoin of this - need to find the value
        if debug:
            print('opt_ver_found...')
                
        # this next line of interest should be the value line to test for it
        if reOptValueLine.search(line):
            # clear the flag because we found the value tied to this key
            opt_ver_found = False
                
            m = reOptValueLine.search(line)

            # create the new_app_ver if it is not already set
            if not version_found:
                new_app_ver = calc_new_app_ver(m, major_update, debug=debug)
                version_found = True
                
            # optiondict set with version and need to update it
            version_changed = True
            new_version=fmtOptValue.format(new_app_ver)
            line=line.replace(m.group(1), new_version)

            # this is a version line in the header called AppVersion='value.value'
            if debug:
                debug_print('OptValueLine', new_app_ver, new_version, m, line, version_changed, opt_ver_found)
                       
        # now return
        return line, version_found, opt_ver_found, new_app_ver, version_changed

    # ----------------------------------------
        
    # not working through values for a dictionary - first check for optiondictconfig setting to set opt_ver_found
    if reOptVerLine.search(line):
        # found the key in the dictionary 
        m = reOptVerLine.search(line)
        # this is a version line in the optiondict dict with key called AppVersion
        opt_ver_found = True
        # this is a version line in the header called AppVersion='value.value'
        if debug:
            print('OptVerLine - found and now looking for the value tied to this variable')
            print(f'{line=}')
            print(f'{version_changed=}')
            print(f'{opt_ver_found=}')
            
        # now return
        return line, version_found, opt_ver_found, new_app_ver, version_changed
                
    # ----------------------------------------

    # now just see if this line has any other version type information
            
    # look for a matching string for version settings
    for (reval, fmtval, name) in SEARCH4VERSION:
        if debug:
            print('checking: '+name)
                
        m =  reval.search(line)
        if m:
            # we found a match
            if not version_found:
                # calculate a new version
                new_app_ver = calc_new_app_ver(m, major_update, debug=debug)
                # and set the flag
                version_found = True
            elif debug:
                print('version_found...')

            # create the new version from what we were passed or what we calculated
            version_changed = True
            new_version = fmtval.format(new_app_ver)
            line=line.replace(m.group(1), new_version)
            
            if debug:
                debug_print(name, new_app_ver, new_version, m, line, version_changed, opt_ver_found)
                
            break    

    # now return
    return line, version_found, opt_ver_found, new_app_ver, version_changed

    #### DEAD CODE BELOW #####
    
    # version line
    if reAppVerLine.search(line):
        m = reAppVerLine.search(line)

        version_changed = True
        new_version=fmtAppVerLine.format(new_app_ver)
        line=line.replace(m.group(1), new_app_ver)
        # line=line.replace(m.group(1), new_version)
        
        if debug:
            debug_print('AppVerLine', new_app_ver, new_version, m, line, version_changed, opt_ver_found)
            
        # now return
        return line, version_found, opt_ver_found, new_app_ver, version_changed
        
    elif rePgmVerLine.search(line):
        m = rePgmVerLine.search(line)
        # this is the __version__ = 'value.value' versoin number
        version_changed = True
        new_version = fmtPgmVerLine.format(new_app_ver)
        #line=line.replace(m.group(1), new_app_ver)
        line=line.replace(m.group(1), new_version)
        if debug:
            debug_print('PgmVerLine', new_app_ver, new_version, m, line, version_changed, opt_ver_found)
                

        # now return
        return line, version_found, opt_ver_found, new_app_ver, version_changed

    elif reAtVerLine.search(line):
        m = reAtVerLine.search(line)
        # this is the @AppVersion = 'value.value' version
        version_changed = True
        new_version = fmtAtVerLine.format(new_app_ver)
        #line=line.replace(m.group(1), new_app_ver)
        line=line.replace(m.group(1), new_version)
            
        if debug:
            debug_print('AtVerLine', new_app_ver, new_version, m, line, version_changed, opt_ver_found)
                

        # now return
        return line, version_found, opt_ver_found, new_app_ver, version_changed

    elif reAtQuoteVerLine.search(line):
        m = reAtQuoteVerLine.search(line)
        # this is the @AppVersion = 'value.value' version
        version_changed = True
        new_version = fmtAtQuoteVerLine.format(new_app_ver)
        #line=line.replace(m.group(1), new_app_ver)
        line=line.replace(m.group(1), new_version)
        
        if debug:
            debug_print('AtQuoteVerLine', new_app_ver, new_version, m, line, version_changed, opt_ver_found)

        # now return
        return line, version_found, opt_ver_found, new_app_ver, version_changed
    
    elif debug:
        print('no matches')
            
    # now return
    return line, version_found, opt_ver_found, new_app_ver, version_changed
    


    
def update_file_version(filename: str, major_update: bool=False, buildonly: bool=False, test: bool=False, debug: bool=False):
    """
    check the  line to see if a bld version updates is needed and cause the update

    inputs:
        filename: str
        major_update: bool=False
        buildonly: bool=False
        test: bool=False
        debug: bool=False

    returns
        app_ver
        new_app_ver
        filename
        file_bak
        bld_ver
        new_bld_ver

    """

    # calculate the filenames we need
    file_tmp = kvutil.filename_create(filename, filename_ext='tmp')
    file_bak = kvutil.filename_create(filename, filename_ext='bak')

    # debugging
    if debug:
        print('update_file_version:start')
        print('update_file_version:filename:', filename)
        print('update_file_version:file_bak:', file_bak)
        print('update_file_version:file_tmp:', file_tmp)
        print('update_file_version:major_update:', major_update)
        print('update_file_version:buildonly:', buildonly)
        print('update_file_version:test:', test)

    # set up variables
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
    
    # open file output file and then input file and process
    with open(file_tmp, 'w') as fpOut:
        # input file opened to read lines - we are reading in all lines into a list
        # TODO:  make this a recursive call so we don't load up memory
        with open(filename, 'r') as fpIn:
            filelines = fpIn.readlines()

        # for each line we got
        for line in filelines:
            # capture if this is a build update - and we ONLY Process for build changes not major/minor changes
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

                # get next line 
                continue

            # NOT BUILD CHANGE - this is a major/minor change

            line, version_found, opt_ver_found, new_app_ver, line_version_changed = major_minor_version_update(line, new_app_ver, version_found, opt_ver_found, major_update=major_update, debug=debug)

            # capture a version change
            if not version_changed and line_version_changed:
                version_changed = True

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
        if reAtVerLine.search(line) and line.startswith('-'):
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
