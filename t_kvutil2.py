import kvutil

# this test program is used to validate the command line parsing and reporting
#
# test1:  python t_kvutil2.py - it should terminate with error message
# test2:  python t_kvutil2.py workingdir=. alldir=1 - should run display but not terminate
# test2:  python t_kvutil2.py help=1 - should run display long list and terminate
#
#

# logging - 
import sys
import kvlogger
config=kvlogger.get_config(kvutil.filename_create(__file__, filename_ext='log', path_blank=True))
kvlogger.dictConfig(config)
logger=kvlogger.getLogger(__name__)

# added logging feature to capture and log unhandled exceptions
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception


# ability to fast track set a configuration
super_config = {
    ### SUB #####
    # we are using the date from the subdirectory to put dates on records
    # we are leaving the records in the filename order
    # we are NOT looking up the datetime on the JPG files
    'sub' : {
        'datefrom' : 'cleanup',
        'defaultdatefrom' : 'subdir',
        'addcnt' : False,
        'adddate' : True,
    },
}
super_config['subdir'] = super_config['sub']


# program option configuration
optiondictconfig = {
    'AppVersion' : {
        'value' : '1.08',
        'description' : 'defines the version number for the app',
    },
    'copytodir' : {
        'description' : 'directory we will copy files into with new filename',
        'type' : 'dir',
    },
    'workingdir' : {
        'description' : 'directory we will be processing files from (default: current directory)',
        'type' : 'dir',
    },
    'fileglob' : {
        'description' : 'file search string (globing)',
    },
    'outfile' : {
        'value' : 'file.bat',
        'description' : 'output filename that holds commands generated',
    },
    'addcnt' : {
        'value' : True,
        'description' : 'flag, if true, output filename includes a count "CNT####-"',
        'type' : 'bool',
    },
    'adddate' :  {
        'value' : False,
        'description' : 'flag, if true, output filename includes a date "YYYY-MM-DD-"',
        'type' : 'bool',
    },
    'timedelta' : {
        'description' : 're.compile_string:offset_seconds_int:range1_int:range2_int_optional',
        # compile string should fully match the filename and have a grouping clause to extract the picture number (e.g. ".*DSC(\d+).*"
        # range1 used if only matching 1 picture, range2 used if you are matching a range of pictures (e.g. :1:10000 is a range)
        # example:  timedelta=".*DSC(\d+).*:3480:3000:4000
        #    - files with DSC in them in the number range from 3000-4000 will have 3480 seconds added to their picture time (58 minutes)
    },
    'onlygtdate' : {
        'description' : 'only process files with an image date greater than this date',
        'type' : 'date',
    },
    'onlyltdate' : {
        'description' : 'only process files with an image date less than this date',
        'type' : 'date',
    },
    'onlynondate' : {
        'description' : 'flag, if true, update only files that do not have dates already',
        'type' : 'bool',
    },
    'datefrom'    : {
        'value'   : 'jpg',
        'description' : 'defines what method used to assign dates to files',
        'type'    : 'inlist',
        'valid'   : ['jpg','jpgdefault','filename','filecreate','forced','cleanup'],
                     # look at kvjpg.py for the explanation on each of these settings
                     # def get_date_sorted_filelists()
    },
    'nonjpgdatefrom'    : {
        'value'   : 'filecreate',
        'description' : 'defines what method used to assign dates to non-JPG files when datefrom is jpg',
        'type'    : 'inlist',
        'valid'   : ['filename','filecreate','forced','cleanup'],
    },
    'defaultdate' : {
        'description' : 'default date to assign to photos when a default is needed',
        'type' : 'date',
    },
    'defaultdatefrom' : {
        'value'   : 'default',
        'description' : 'defines where we get the defaultdate from',
        'type'    : 'inlist',
        'valid'   : ['subdir','now','default','cmdline'],
                     # subdir - take the date from the directory name housing the files
                     # now - take current date/time
                     # default - use epoch (1901-01-01 00:00:01)
                     # cmdline - take the value from defaultdate on the command line
    },
    'debug' : {
        'description' : 'flag, if true, display debugging information',
        'type' : 'bool',
    },
    'super_config' : {
        'description' : 'defines a preconfigured configuration - overrides settings',
        'type'  : 'inlist',
        'valid' : list(super_config.keys()),
    },


    # legacy options - NOT USED
    'alldir' : {
        'description' : 'NOT USED - would be flag to specify to walk file system',
        'type' : 'bool',
    },
    'adate' : {
        'value' : None,
        'description' : 'NOT USED - would be used to capture different meta dates',
        'type' : 'bool',
    },
        
    'allfiles' : {
        'value' : None,
        'description' : 'NOT USED',
        'type' : 'bool',
    },
    'recount' :  {
        'value' : None,
        'description' : 'NOT USED',
        'olddescription' : 'flag, if true, file date taken from filename, if false, date takeing from file meta data',
        'type' : 'bool',
    },

}

# the remapping of command line options to their proper value
keymapdict = {
    'superconfig' : 'super_config',
}


# print('start:', optiondictconfig)
optiondict = kvutil.kv_parse_command_line( optiondictconfig, debug=False )
# kvutil.kv_parse_command_line_display( optiondictconfig, optiondict, debug=False )
print('\n\nProgram completed - did not terminate')
