__version__ = '1.01'

# import libraries that are being used
import kvutil

# may comment out in the future
import pprint

# logging
import sys
import kvlogger
pp = pprint.PrettyPrinter(indent=4)

"""
@author:   Ken Venner
@contact:  ken@venerllc.com
@version:  1.01

<Describe what this tool does here>

"""


# pick the log file structure from list below
# single file that is rotated
config = kvlogger.get_config(kvutil.filename_create(__file__, filename_ext='log', path_blank=True),
                             loggerlevel='INFO')  # single file
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
}

# ---- put local functions here ---- #


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    # capture the command line
    # optional setttings in code
    #   raise_error = True - if we have a problem parsing option we raise an error rather than pass silently
    #   keymapdict = {} - dictionary of mis-spelling of command options that are corrected for through this mapping
    #   debug = True - provide insight to what is going on as we parse conf_json files and command line options
    optiondict = kvutil.kv_parse_command_line(optiondictconfig, debug=False)
