"""
@author:   Ken Venner
@contact:  ken@venerllc.com
@version:  1.08

Library of tools used in command line processing with configuration files

"""

from attrdict import AttrDict
# import argparse
import json
import os
import re

# import logging
import logging.config
import copy

logger = logging.getLogger(__name__)

AppVersion = '1.08'
__version__ = '1.08'


def load_json_file_to_dict(filename):
    """
    Load a JSON file into a dictionary
    and provide helpful information if we have JSON parsing issues

    :param filename: (str) filename/path to json file

    :returns json_data: (dict) of the json data loaded
    """
    with open(filename, 'r') as json_in:
        try:
            json_dict = json.load(json_in)
        except json.decoder.JSONDecodeError as e:
            with open(filename, 'r') as json_error:
                json_lines = json_error.readlines()
            err_line = re.search(r'line\s+(\d+)\s+', str(e))
            print('-' * 40)
            if err_line:
                err_line_int = int(err_line.group(1))
                if err_line_int < len(json_lines):
                    print('Error on line: ', err_line_int)
                    print(json_lines[err_line_int - 1])
                    logger.error('Error loading JSON file: %s',
                                 {'filename': filename,
                                  'error_line': err_line.group(1),
                                  'json_line': json_lines[err_line_int - 1],
                                  'error': str(e)})
            print('-' * 40)
            raise
    return json_dict


def conf_settings(conf_files=None):
    """
    Load up the settings defined by configuration file(s)
    this configuratoin files can call out additional configuration files
    last file with a setting is the setting we return

    :param conf_files: (list) list of files to read configurations from
                              generally taken as arg.conf

    :return conf_settings: (dict) list of settings read in from the conf file

    """

    # set defaults if not passed in
    if conf_files is None:
        conf_files = []

    # add vargs-conffile
    add_vargs_conf_files = True if conf_files else False

    # make sure we have an array of files to be processed
    if conf_files and not isinstance(conf_files, list):
        conf_files = [conf_files]

    # create the object that will carry the conf_settings
    vargs = AttrDict()

    # load the configuration files if the exist
    conf_added = list()
    conf_loaded = list()
    while conf_files:
        for conffile in conf_files:
            if os.path.exists(conffile):
                # read in the configuration file
                try:
                    fileargs = load_json_file_to_dict(conffile)
                except json.decoder.JSONDecodeError:
                    # this error is handled in the function call
                    logger.info('Skipped using: %s', conffile)
                    continue
                except Exception as e:
                    logger.error('Skipped using: %s : due to error: %s', conffile, e)
                    continue
                # loaded it - so add this to the list we loaded
                conf_loaded.append(conffile)
                if 'conf' in fileargs:
                    # this configuration file has more conf files to be loaded
                    # add this to the list of things added
                    conf_added.append(fileargs['conf'])
                # update the current setting with these new settings
                vargs.update(fileargs)

        # create a unique list of configuration files to load
        conf_added = list(set(conf_added))

        # new conf files to be loaded as defined in these files
        # add them to the be loaded list if we have not already seen them
        conf_files = [x for x in conf_added if x not in conf_files and x not in conf_loaded]

        # and clear the added conf file array
        conf_added = list()

    if add_vargs_conf_files:
        vargs['conf_files_loaded'] = conf_loaded

    # return back the final definition of values set by configuration file
    return vargs, conf_loaded


def missing_settings(vargs, req_flds):
    # validate we have all the required fields
    missingflds = list()
    for reqfld in req_flds:
        if reqfld not in vargs or not vargs[reqfld]:
            missingflds.append(reqfld)
    return missingflds


def merge_settings(args, conf_files=None, args_default=None):
    """
    Merge the values from the command line, configuration files, and default_values

    """
    # set defaults if not passed in
    if conf_files is None:
        conf_files = []
    if args_default is None:
        args_default = {}

    # local variables
    vars_updated = list()

    # convert the command line options into a dictionary
    if not isinstance(args, dict):
        args = AttrDict(vars(args))
    elif not instance(args, AttrDict):
        args = AttrDict(args)

    # and make a deep copy of this into vargs
    vargs = copy.deepcopy(args)

    # get the configuratoin file settings
    args_conf, conf_loaded = conf_settings(conf_files)

    # now merge command line and configuratoin 
    for k, v in args_conf.items():
        if k in vargs and vargs[k] is not None:
            # key was set by command line so skip the update
            continue
        # set the value
        vargs[k] = v
        vars_updated.append(k)

    # set defaults if variable is not set - and it should have a default
    for k, v in args_default.items():
        if k not in vargs or vargs[k] is None:
            vargs[k] = v

    # create a configuration variable to capture files that were loaded
    if conf_loaded:
        logger.info('Loaded conf files: %s', conf_loaded)
        logger.info('Variables updated from conf files: %s', vars_updated)
        if 'conf_files_loaded' not in vargs:
            vargs['conf_files_loaded'] = conf_loaded

    return vargs


def parser_merge_settings(parser, args, conf_files=None, args_default=None, test_args_conf=None):
    """
    Merge the values from the command line, configuration files, and default_values

    """
    # set defaults if not passed in
    if conf_files is None:
        conf_files = []
    if args_default is None:
        args_default = {}

    # local variables
    vars_updated = list()

    # convert the command line options into a dictionary
    if not isinstance(args, dict):
        args = AttrDict(vars(args))
    elif not instance(args, AttrDict):
        args = AttrDict(args)

    # and make a deep copy of this into vargs
    vargs = copy.deepcopy(args)

    # get the configuration files settings
    if test_args_conf is None:
        # get the configuratoin file settings
        args_conf, conf_loaded = conf_settings(conf_files)
    else:
        logger.warning('Running with test_args_conf: %s', test_args_conf)
        args_conf = copy.deepcopy(test_args_conf)
        conf_loaded = 'test_args_conf'

    # args_conf will have setting that match command line options
    # some will have dest=<value>
    # and some will cause action to take place and we wnat to
    # allow that action
    # 
    # we need to find and execute those with action - and cause them to execute
    # we need to find those with dest and not action and cause them to update
    # the right value in vargs
    #
    # step through the command line options
    # - skip anything that does not have a args_conf equivalent - there is no action
    #
    # if it is a const - then we want to fire this rule off - capture this - get next
    # if this has dest then take the value and apply it to dest
    #
    parser_list = list()
    vargs_conf = dict()
    for cmd in parser.__dict__['_option_string_actions']:
        parser_obj = parser.__dict__['_option_string_actions'][cmd]
        cmd_str = cmd.replace('-', '')
        dest = parser_obj.dest
        if cmd_str not in args_conf:
            # no conf update - nothing to worry about
            continue

        # capture events that we will take action on
        if parser_obj.const:
            if args_conf[cmd_str]:
                # value was in conf but and true
                # add this to the command line so we can execute it
                parser_list.append(cmd)

        elif vargs.get(dest, None) is not None:
            # not set by command line so set it here
            # in a dictionary we will use to update with
            # after reprocessing the args processing
            vargs_conf[dest] = args_conf[cmd_str]

        else:
            # did not process this one
            continue

        # capture that we did process this update string
        vars_updated.append(cmd_str)

        # remove this value from args_conf as we processed it a different way
        del args_conf[cmd_str]

    # been through all - if we have any that need to be called call them
    # so that they process like they were done on the commadn line
    # and we do this because these have defined actions done by argparser
    if parser_list:
        args = AttrDict(vars(parser.parse_args(parser_list)))
        vargs = copy.deepcopy(args)

    # now apply the vargs_conf to this output
    vargs.update(vargs_conf)

    # now take any conf settings
    # and copy them in if the command line did
    # not already set the value
    for k, v in args_conf.items():
        if k in vargs and vargs[k] is not None:
            # key was set by command line so skip the update
            continue
        # set the value
        vargs[k] = v
        vars_updated.append(k)

    # set defaults if variable is not set - and it should have a default
    for k, v in args_default.items():
        if k not in vargs or vargs[k] is None:
            vargs[k] = v

    # create a configuration variable to capture files that were loaded
    if conf_loaded:
        logger.info('Loaded conf files: %s', conf_loaded)
        logger.info('Variables updated from conf files: %s', vars_updated)
        if 'conf_files_loaded' not in vargs:
            vargs['conf_files_loaded'] = conf_loaded

    return vargs


def parser_extract_default_and_set_to_none(parser, args_default=None):
    """
    Pull the default values from parser for each 
    command line argument, and put these values 
    in args_default, then set the default to None

    args_default is updated in place

    :param parser: (obj) ArgParser object
    :param args_default: (dict) default values for arguments

    :return args_default: (dict) in case we did not pass in this value

    """
    if args_default is None:
        args_default = dict()

    for cmd in parser.__dict__['_option_string_actions']:
        parser_obj = parser.__dict__['_option_string_actions'][cmd]

        # cmd_str = cmd.replace('-', '')
        dest = parser_obj.dest
        default = parser.get_default(dest)

        # because of help we need to skp some
        if default == '==SUPPRESS==':
            continue

        # only update the defaults if they set a value
        if default is not None:
            if parser_obj.const and dest in args_default:
                # we allow args_default to control this setting
                # because we are unsure if they actually set this
                # or we got it as an uexpected default
                # so we either truly set it - or we take the value from the
                # first one we encounter
                # -- best_practice is to default=None when you
                # -- action="store_true" and dest="value" because you
                # -- have two or more entries that toggle this dest setting.
                pass
            else:
                args_default[dest] = default

        # remove this list
        # logger.warning('REMOVE this line')
        # print(cmd, cmd_str, dest, default)

        # clear the default
        parser.set_defaults(**{dest: None})

    return args_default


def parse_and_parser_merge_settings(parser, args_default=None, cmd_line=None, test_args_conf=None):
    """
    Merge the values from the command line, configuration files, and default_values

    Assumes we have already called parser_extract_default_and_set_to_none - so we have
    all the default values in the args_default and the default value of all entries is None

    :param parser: (obj) ArgParser object
    :param args_default: (dict) default values for arguments

    :param cmd_line: (list) - only used for testing - but when passed in we pass this to 
                              parse_args() function rather than calling the command line
                              parser
    :param test_args_conf: (dict) - values that would have been read from the file used for testing

    :return vargs: (dict) - values from cmd_line and defaults and conf files

    """
    # parse the command line
    if cmd_line is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(cmd_line)

    args_dict = vars(args)
    conf_files = args_dict.get('conf', None)

    return parser_merge_settings(parser, args, conf_files, args_default, test_args_conf)


def prep_parse_and_merge_settings(parser, args_default=None, cmd_line=None, test_args_conf=None):
    """
    prep - extract data about the parser
    parse - call the command line parser
    merge - merge command line with configuration files stuff

    :param parser: (obj) ArgParser object
    :param args_default: (dict) default values for arguments

    :param cmd_line: (list) - only used for testing - but when passed in we pass this to 
                              parse_args() function rather than calling the command line
                              parser
    :param test_args_conf: (dict) - values that would have been read from the file used for testing

    :return args_default: (dict) the updated args_default that is the final result of processing
                          usually passed in to vargs variable
    """
    if args_default is None:
        args_default = dict()

    # prep - updates args_default
    args_default = parser_extract_default_and_set_to_none(parser, args_default)
    # parse and merge - return vargs
    return parse_and_parser_merge_settings(parser, args_default, cmd_line, test_args_conf)

# eof
