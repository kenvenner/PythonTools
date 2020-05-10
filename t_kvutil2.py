import kvutil

# this test program is used to validate the command line parsing and reporting
#
# test1:  python t_kvutil2.py - it should terminate with error message
# test2:  python t_kvutil2.py workingdir=. alldir=1 - should run display but not terminate
# test2:  python t_kvutil2.py help=1 - should run display long list and terminate
#
#

# program option configuration
optiondictconfig = {
    'AppVersion' : {
        'value' : '1.02',
        'description' : 'defines the version number for the app',
    },
    'copytodir' : {
        'description' : 'directory we will copy files into with new filename',
        'type' : 'dir',
    },
    'workingdir' : {
        'description' : 'directory we will be processing files from (default: current directory)',
        'type' : 'dir',
        'required': True,
    },
    'fileglob' : {
        'description' : 'file search string (globing)',
    },
    'outfile' : {
        'value' : 'file.bat',
        'description' : 'output filename that holds commands generated',
    },
    'alldir' : {
        'description' : 'NOT USED - would be flag to specify to walk file system',
        'type' : 'bool',
        'required' : True, 
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
    'adate' : {
        'description' : 'NOT USED - would be used to capture different meta dates',
        'type' : 'bool',
    },
        
    'allfiles' : {
        'description' : 'NOT USED',
        'type' : 'bool',
    },
    'recount' :  {
        'value' :  False,
        'description' : 'flag, if true, file date taken from filename, if false, date takeing from file meta data',
        'type' : 'bool',
    },
    'timedelta' : {
        'description' : 're.compile_string:offset_seconds_int:range1_int:range2_int_optional',
    },
    'debug' : {
        'description' : 'flag, if true, display debugging information',
        'type' : 'bool',
    },
}

# print('start:', optiondictconfig)
optiondict = kvutil.kv_parse_command_line( optiondictconfig, debug=False )
# kvutil.kv_parse_command_line_display( optiondictconfig, optiondict, debug=False )
print('\n\nProgram completed - did not terminate')
