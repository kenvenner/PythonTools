'''
@author:   Ken Venner
@contact:  ken@venerllc.com
@version:  1.01

Tooling that creates a new major/minor version on a file

'''
import re
import os
import subprocess

import kvutil

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
        'value': '1.01',
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



### CONSTANTS ###
reVerLine = re.compile('@version:\s+((\d+)\.(\d+))')
reOptVerLine = re.compile('AppVersion\':\s+{')
reOptValueLine = re.compile('^(\s+)\'value')
reAppVerLine = re.compile('AppVersion\s+=\s+\'\d+\.\d+\'')

reGitModified = re.compile('\s+modified:\s+(.*)')

fmtVersion2d='{}.{:02d}'
fmtVersion3d='{}.{:03d}'
fmtOptValue="        'value': '{}',\n"
fmtVerLine='@version:  {}\n'
fmtAppVerLine='AppVersion = \'{}\'\n'


def update_file_version(filename, major_update=False, test=False, debug=False):
    file_tmp = kvutil.filename_create(filename, filename_ext='tmp')
    file_bak = kvutil.filename_create(filename, filename_ext='bak')

    if debug:
        print('filename:', filename)
        print('file_bak:', file_bak)
        print('file_tmp:', file_tmp)
        print('major_update:', major_update)
        print('test:', test)
        
    appVer = ''
    newAppVer = ''
    version_found = False
    opt_ver_found = False
    app_ver_found = False
    opt_or_app_value_changed=False
    
    with open(file_tmp, 'w') as fpOut:
        with open(filename, 'r') as fpIn:
            filelines=fpIn.readlines()

        for line in filelines:
            if version_found:
                if not opt_or_app_value_changed:
                    if opt_ver_found:
                        if reOptValueLine.search(line):
                            opt_or_app_value_changed = True
                            fpOut.write(fmtOptValue.format(newAppVer))
                            continue
                    elif reOptVerLine.search(line):
                        opt_ver_found = True
                    elif reAppVerLine.search(line):
                        app_ver_found = True
                        opt_or_app_value_changed = True
                        fpOut.write(fmtAppVerLine.format(newAppVer))
                        continue
            else:
                m=reVerLine.search(line)
                if m:
                    appVer=m.group(1)
                    majorVer=int(m.group(2))
                    minorVer=int(m.group(3))

                    if major_update:
                        newMajorVer = majorVer + 1
                        newMinorVer = 1
                    else:
                        newMajorVer = majorVer
                        newMinorVer = minorVer + 1

                    if newMinorVer < 100:
                        newAppVer = fmtVersion2d.format(newMajorVer, newMinorVer)
                    else:
                        newAppVer = fmtVersion3d.format(newMajorVer, newMinorVer)
                    
                    version_found = True
                    fpOut.write(fmtVerLine.format(newAppVer))
                    continue

            fpOut.write(line)

    if debug:
        print('version_found:', version_found)
        print('opt_or_app_value_changed:', opt_or_app_value_changed)
        
    # create temp file determine if we take existing file
    # convert to bak and make tmp the current file
    if version_found and opt_or_app_value_changed and not test:
        if os.path.exists(file_bak):
            kvutil.remove_file(file_bak)
        os.rename(filename, file_bak)
        os.rename(file_tmp, filename)
        return appVer, newAppVer, filename, file_bak
    else:
        return appVer, None, None, None
        
def git_modified_files_in_folder(folder_path='', debug=False):
    files_modified=list()

    if folder_path == './':
        folder_path = ''

    if debug:
        print('git_modified_files_in_folder:folder_path:', folder_path)
    
    # define when we stop looking
    untracked="Untracked files:"
    
    # git status call to find files that changed
    if folder_path:
        result=subprocess.run(['git','status', folder_path],stdout=subprocess.PIPE)
    else:
        result=subprocess.run(['git','status'],stdout=subprocess.PIPE)

    for line in result.stdout.decode('utf-8').split('\n'):
        if debug:
            print('line:',line)
        
        if line == untracked:
            return files_modified
        
        m=reGitModified.search(line)
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
    MAXLINES_CHECKED=50
    # get the diff on this file with what was last committed to git
    result=subprocess.run(['git','diff', filename],stdout=subprocess.PIPE)

    if debug:
        print('version_changed_in_git_branch:maxlines_checked:', MAXLINES_CHECKED)
        
    linecnt=0
    for line in result.stdout.decode('utf-8').split('\n'):
        linecnt += 1
        if debug:
            print('{:02d}:line:{}'.format(linecnt, line))
        if reVerLine.search(line) and line.startswith('-'):
            return True
        if linecnt > MAXLINES_CHECKED:
            return False
            
    return False
        

# ---------------------------------------------------------------------------
if __name__ == '__main__':

    # capture the command line

    # optional setttings in code
    #   raise_error = True - if we have a problem parsing option we raise an error rather than pass silently
    #   keymapdict = {} - dictionary of mis-spelling of command options that are corrected for through this mapping
    #   debug = True - provide insight to what is going on as we parse conf_json files and command line options
    optiondict = kvutil.kv_parse_command_line(optiondictconfig, debug=False)

    # get the list of files to be processed
    filelist = kvutil.filename_list(optiondict['input_file'], optiondict['input_list'], optiondict['input_glob'],
                                    includelist_filename=optiondict['input_list_file'],
                                    excludelist_filename=optiondict['exclude_list_file'])
    
    # our behavior is controlled if we set the input_file, if we don't the we do the git evaluation
    if filelist:
        optiondict['input_folder'] = ''

        logger.info('files to be processed:%s', filelist)
    else:
        logger.info('folder to be processed:%s', optiondict['input_folder'])
        
        files_to_check = git_modified_files_in_folder(optiondict['input_folder'], debug=optiondict['debug'])

        if not files_to_check:
            logger.info('no files to be checked for this folder')

        for chk_file in files_to_check:
            if not version_changed_in_git_branch( chk_file, debug=optiondict['debug'] ):
                appVer, newAppVer, filename, file_bak = update_file_version(chk_file, major_update=optiondict['major_update'], test=optiondict['test'], debug=optiondict['debug'])
                logger.info('version changed in git for:{}:outputs:{},{},{},{}'.format(chk_file, appVer, newAppVer, filename, file_bak))
            else:
                logger.info('version previously changed in git for:{}'.format(chk_file))
