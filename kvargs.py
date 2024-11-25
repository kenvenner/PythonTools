"""
@author:   Ken Venner
@contact:  ken@venerllc.com
@version:  1.17

Library of tools used in command line processing with configuration files

"""

# from attrdict import AttrDict
# import argparse
import json
import os
import re
import sys

# import logging
import logging.config
import copy

import pprint

pp = pprint.PrettyPrinter(indent=4)

logger = logging.getLogger(__name__)

AppVersion = '1.17'
__version__ = '1.17'


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
    this configuration files can call out additional configuration files
    last file with a setting is the setting we return

    :param conf_files: (list) list of files to read configurations from
                              generally taken as arg.conf

    :return conf_settings: (dict) list of settings read in from the conf file
    :return conf_loaded: (list) list of conf files that were loaded
    """

    # determine if we got any conf files to load
    add_vargs_conf_files = True if conf_files else False

    # set defaults if not passed in
    if conf_files is None:
        conf_files = []
    # make sure we have an array of files to be processed
    if conf_files and not isinstance(conf_files, list):
        conf_files = [conf_files]

    # create the object that will carry the conf_settings
    #    args_conf = AttrDict()
    args_conf = dict()
    
    # load the configuration files if the exist
    conf_added = list()
    conf_loaded = list()
    vargs_updated_by = dict()
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
                args_conf.update(fileargs)

                # now capture what was set
                conf_update = 'conf:' + conffile
                for key in fileargs:
                    updated_by(vargs_updated_by, key, conf_update)

        # create a unique list of configuration files to load
        conf_added = list(set(conf_added))

        # new conf files to be loaded as defined in these files
        # add them to the be loaded list if we have not already seen them
        conf_files = [x for x in conf_added if x not in conf_files and x not in conf_loaded]

        # and clear the added conf file array
        conf_added = list()

    if add_vargs_conf_files:
        args_conf['conf_files_loaded'] = conf_loaded

    # return back the final definition of values set by configuration file
    return args_conf, conf_loaded, vargs_updated_by


def missing_settings(vargs, req_flds):
    """
    Determine which required fields are not populated

    :param vargs: (dict) - values entered in the command line
    :param req_flds: (list) - list of fields that must be populated

    :return missingflds: (list) - fields that are not populated
    """
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

    # convert the command line options into a dictionary
    if not isinstance(args, dict):
        # args = AttrDict(vars(args))
        args = vars(args)
#    elif not isinstance(args, AttrDict):
#        args = AttrDict(args)

    # and make a deep copy of this into vargs
    vargs = copy.deepcopy(args)

    # get the configuration file settings
    args_conf, conf_loaded, args_updated_by = conf_settings(conf_files)

    # now merge command line and configuratoin 
    for k, v in args_conf.items():
        if k in vargs and vargs[k] is not None:
            # key was set by command line so skip the update
            continue
        # set the value
        vargs[k] = v

    # set defaults if variable is not set - and it should have a default
    for k, v in args_default.items():
        if k not in vargs or vargs[k] is None:
            vargs[k] = v

    # create a configuration variable to capture files that were loaded
    if conf_loaded:
        logger.info('Loaded conf files: %s', conf_loaded)
        if 'conf_files_loaded' not in vargs:
            vargs['conf_files_loaded'] = conf_loaded

    return vargs


def parser_defaults(parser, set_to_none=None):
    """
    Pull out the default settings from the parser

    :param parser: (obj) ArgParser object
    :param set_to_none: (bool) - when set, we force the default to None

    :return arg_parser_defaults: (dict)
           keyed by command line setting
           returns
               dest = setting this updates (can be the same as the key)
               value = the default value
               cmd = command line switch
               const = bool defining if this is a const 
               first = bool the first default found for dest
    """
    # args_parser_default = AttrDict()
    args_parser_default = dict()
    dest_found = list()
    for cmd in parser.__dict__['_option_string_actions']:
        parser_obj = parser.__dict__['_option_string_actions'][cmd]
        cmd_str = cmd.replace('-', '')
        dest = parser_obj.dest
        default = parser.get_default(dest)
        const = parser_obj.const

        # skip this if the default is NOne
        if default is None or default == '==SUPPRESS==':
            continue

        args_parser_default[cmd_str] = {
            'dest': dest,
            'value': default,
            'cmd': cmd,
            'const': const is not None,
            'first': dest not in dest_found
        }

        # tracking when we first see the destination
        dest_found.append(dest)

    # if we set it to None
    if set_to_none:
        for dest in dest_found:
            parser.set_defaults(**{dest: None})

    return args_parser_default


def updated_by(updated_dict, key, value):
    """
    update the updated_dict - key with value which can be an item or a list

    :param updated_dict: (dict)
    :param key: (str)
    :param value: (list or value)

    """
    if not isinstance(updated_dict, dict):
        raise TypeError('updated_dict not type dict')

    if key not in updated_dict:
        updated_dict[key] = []
    if isinstance(value, list):
        updated_dict[key].extend(value)
    else:
        updated_dict[key].append(value)


def parser_merge_settings(parser, args, conf_files=None, args_default=None, args_parser_default=None,
                          test_args_conf=None):
    """
    Merge the values from the command line, configuration files, and default_values

    :param parser: (obj) - argparse object
    :param args: (obj) - output from parser.args_parse() - becomes args_cmdline/args_cmdline_set
    :param conf_files: (list) - list of config files to load
    :param args_default: (dict) - dictionary of program defined default values (key=value)
    :param args_parser_default: (dict) - extract of argparse defaults - multi-level dict
    :param test_args_conf:

    :return vargs: (dict) - key/value settings
    """
    # set defaults if not passed in
    if conf_files is None:
        conf_files = []
    if args_default is None:
        args_default = {}
    if args_parser_default is None:
        args_parser_default = {}

    vargs_updated_by = dict()

    # -- GET COMMMAND LINE --

    # convert the command line options into a dictionary
    if not isinstance(args, dict):
        # args_cmdline = AttrDict(vars(args))
        args_cmdline = vars(args)
#    elif not isinstance(args, AttrDict):
#        args_cmdline = AttrDict(args)
    else:
        args_cmdline = args

    # create the dictionary housing only values set on the command line
    args_cmdline_set = {k: v for k, v in args_cmdline.items() if v is not None}

    # DEBUGGING
    if False:
        print('args:', args)
        print('args_cmdline:', args_cmdline)
        print('args_cmdline_set:', args_cmdline_set)
    
    # -- GET DEFAULT ARGS / SET VARGS --
    
    # we build up the answer by updating
    # args_default
    # args_parser_default - that are not set in args_default
    #  step through args_parser_default
    # args_conf - for keys where not const, command = dest, copy value
    # args_conf - for keys where const, execute these command option if value = True and not in args_cmdline_set
    #
    # step through args_conf
    # args_conf - where key not matched to vargs key
    # args_cmdline
    # vargs = AttrDict(copy.deepcopy(args_default))
    vargs = copy.deepcopy(args_default)

    # print('vargs-start:', vargs)

    # define what is set by args
    for k in vargs:
        updated_by(vargs_updated_by, k, 'args_default')

    # -- GET ARGS CONFIGURATION  --

    # get the configuration files settings
    if test_args_conf is None:
        # get the configuration file settings
        args_conf, conf_loaded, args_updated_by = conf_settings(conf_files)
    else:
        logger.warning('Running with test_args_conf: %s', test_args_conf)
        args_conf = copy.deepcopy(test_args_conf)
        conf_loaded = 'test_args_conf'
        args_conf['conf_files_loaded'] = [conf_loaded]
        args_updated_by = {k: ['conf:test_args_conf'] for k in test_args_conf}

    # print('cmd:', args_cmdline)
    # print('cmdset:', args_cmdline_set)
    # print('args_default:', args_default)
    # print('args_parser_default:', args_parser_default)

    # -- ARGS PARSER DEFAULTS into VARGS --

    # set vargs from args_parser_default when
    # not already set in args_default.
    # if set in args_default - that is the master
    for k, v in args_parser_default.items():
        if v['dest'] not in args_default and \
                v['first']:
            vargs[v['dest']] = v['value']
            updated_by(vargs_updated_by, v['dest'], 'args_parser_default')

    # print('vargs1-def-parser:', vargs)

    # -- ARGS CONF into VARGS ---
    #  step through args_parser_default
    # args_conf - for keys where not const, and dest (or key) in args_conf copy value
    # args_conf - for keys where const, execute these command option if value = True, and not in args_cmdline
    #
    # step through args_conf
    # args_conf - where key not matched to vargs key
    # args_cmdline

    # print('args-conf-before:', args_conf)

    # args_conf - for keys where not const, and dest (or key) in args_conf copy value
    for k, v in args_parser_default.items():
        # print('args_conf-not-const:k,v:', k, v)
        if not v['const'] and v['first']:
            # print('match')
            if v['dest'] in args_conf:
                # print('setting-vargs-conf-dest:', dest)
                vargs[v['dest']] = args_conf[v['dest']]
                updated_by(vargs_updated_by, v['dest'], args_updated_by[v['dest']])
                del args_conf[v['dest']]
            elif k in args_conf:
                # print('setting-vargs-conf-k:', k)
                vargs[v['dest']] = args_conf[k]
                updated_by(vargs_updated_by, v['dest'], args_updated_by[k])
                del args_conf[k]

    # update vargs
    # print('args-conf-after:', args_conf)
    # print('vargs-conf-not-const:', vargs)

    # args_conf - for keys where const, execute these command option if value = True and not in args_cmdline_set
    #args_update = AttrDict()
    args_update = dict()
    for k, v in args_parser_default.items():
        # print('k:v', k, v)
        if v['const'] and \
                k in args_conf and \
                k not in args_cmdline_set:
            # print('updates from const-conf:', v['cmd'], k)
            args_update[k] = v

    # update vargs
    if False:
        print('args-conf-for-conf-const:', args_conf)
        print('vargs-conf-const:', vargs)
        print('args_update:', args_update)

    # been through all - if we have any that need to be called call them
    # so that they process like they were done on the commadn line
    # and we do this because these have defined actions done by argparser
    # and from this command in statement - pull back out the values
    # of interest
    # print('args_update:', args_update)
    if args_update:
        # get the list of command line commands
        parser_list = [v['cmd'] for v in args_update.values()]
        # DEBUGGING
        if False:
            print('parser_list:', parser_list)
            print('sys.argv:', sys.argv)
        # pull in the original command line arguments add them to this
        # as their may be required values we need to parse
        # exclude the program that was called in position 0
        if False:
            print('sys.argv[1:]:', sys.argv[1:])
        parser_list.extend(sys.argv[1:])
        # print('parser_list:', parser_list)
        # parse them to get their values
        args = vars(parser.parse_args(parser_list))
        # print('args-parser-list:', args)
        # for things that got updated based on this
        for k, v in args_update.items():
            # print('k:v:vdest:', k, v, v['dest'])
            # print('args:', args)
            # print('args_parser_k:', args_parser_default[k])
            if args[v['dest']] is not None:
                vargs[v['dest']] = args[v['dest']]
                updated_by(vargs_updated_by, v['dest'], args_updated_by[k])
                # remove the args_conf entry for this command line option
                # print('del args_conf:', k,  v['cmd'], v, args_update)
                del args_conf[k]

    # print('args_conf-sm:', args_conf)
    # print('vargs2-cmd_update:', vargs)

    # now apply settings from configuration files
    # we set all variables except ones set by the command line
    # that remain because we have already removed the ones we
    # processed earlier
    for k, v in args_conf.items():
        if k in ('vargs_updated_by',):
            continue
        if k not in args_cmdline_set:
            vargs[k] = v
            if k in args_updated_by:
                updated_by(vargs_updated_by, k, args_updated_by[k])
    # print('args_conf:', args_conf)
    # print('v4:', vargs)

    # now apply command line
    # print('cmdset:', args_cmdline_set)
    vargs.update(args_cmdline_set)
    # print('v5:', vargs)
    for k, v in args_cmdline_set.items():
        updated_by(vargs_updated_by, k, 'cmdline')

    # now apply settings from argscmdline
    for k, v in args_cmdline.items():
        if k not in vargs:
            vargs[k] = v
    # print('args_cmdline:', args_cmdline)
    # print('v6:', vargs)

    # add  the updated by into vargs
    vargs['vargs_updated_by'] = vargs_updated_by

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
        # (cmd, cmd_str, dest, default)

        # clear the default
        parser.set_defaults(**{dest: None})

    return args_default


def parse_and_parser_merge_settings(parser, args_default=None, args_parser_default=None,
                                    cmd_line=None, test_args_conf=None):
    """
    Merge the values from the command line, configuration files, and default_values

    Assumes we have already called parser_extract_default_and_set_to_none - so we have
    all the default values in the args_default and the default value of all entries is None

    :param parser: (obj) ArgParser object
    :param args_default: (dict) default values for arguments
    :param args_parser_default: (dict) default values for arguments

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

    return parser_merge_settings(parser, args, conf_files, args_default, args_parser_default, test_args_conf)


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
    args_parser_default = parser_defaults(parser, set_to_none=True)

    # parse and merge - return vargs
    return parse_and_parser_merge_settings(parser, args_default, args_parser_default, cmd_line, test_args_conf)

# eof
