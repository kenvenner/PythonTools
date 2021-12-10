"""
@author:   Ken Venner
@contact:  ken@venerllc.com
@version:  1.07

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

AppVersion = '1.07'
__version__ = '1.07'


def load_json_file_to_dict(filename, logger=None):
    """
    Load a JSON file into a dictionary
    and provide helpful information if we have JSON parsing issues

    :param filename: (str) filename/path to json file
    :param logger: (obj) logging object - if set we output a logger line

    : returns json_data: (dict) of the json data loaded
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
                    if logger:
                        logger.error('Error loading JSON file: %s',
                                     {'filename': filename,
                                      'error_line': err_line.group(1),
                                      'json_line': json_lines[err_line_int - 1],
                                      'error': str(e)})
            print('-' * 40)
            raise
    return json_dict


def merge_settings(args, conf_files=None, args_default=None, req_flds=None):
    """
    Merge the values from the command line, configuration files, and default_values

    """
    # set defaults if not passed in
    if conf_files is None:
        conf_files = []
    if args_default is None:
        args_default = {}
    if req_flds is None:
        req_flds = []

    # convert the command line options into a dictionary
    if not isinstance(args, dict):
        vargs = AttrDict(vars(args))

        # make a copy so we can look up in this - rather than leave it a NameSpace
        args = AttrDict(vars(args))
    else:
        vargs = copy.deepcopy(args)

    # make sure we have an array of files to be processed
    if conf_files and not isinstance(conf_files, list):
        conf_files = [conf_files]

    # load the configuration files if the exist
    vars_updated = list()
    confadded = list()
    confloaded = list()
    while conf_files:
        for conffile in conf_files:
            if os.path.exists(conffile):
                try:
                    fileargs = load_json_file_to_dict(conffile, logger)
                except json.decoder.JSONDecodeError:
                    # this error is handled in the function call
                    logger.info('Skipped using: %s', conffile)
                    continue
                except Exception as e:
                    logger.error('Skipped using: %s : due to error: %s', conffile, e)
                    continue
                confloaded.append(conffile)
                if 'conf' in fileargs:
                    confadded.append(fileargs['conf'])
                for k, v in fileargs.items():
                    if (k in args and args[k] is not None):
                        # command line set the value - keep the command line setting
                        logger.debug(
                            'keep command line setting - ignore conf file setting-file:{}:key:{}'.format(conffile, k))
                        continue

                    # overwrite current value with value from conf file
                    vargs[k] = v
                    if k not in vars_updated:
                        vars_updated.append(k)

        # new conf files to be loaded as defined in these files
        # add them to the be loaded list if we have not already seen them
        # and clear the added conf file array
        conf_files = [x for x in confadded if x not in conf_files]
        confadded = list()

    # set defaults if variable is not set - and it should have a default
    for k, v in args_default.items():
        if k not in vargs or vargs[k] is None:
            vargs[k] = v

    # create a configuration variable to capture files that were loaded
    if confloaded:
        logger.info('Loaded conf files: %s', confloaded)
        logger.info('Variables updated from conf files: %s', vars_updated)
        if 'conf_files_loaded' not in vargs:
            vargs['conf_files_loaded'] = confloaded

    return vargs


def missing_settings(vargs, req_flds):
    # validate we have all the required fields
    missingflds = list()
    for reqfld in req_flds:
        if reqfld not in vargs or not vargs[reqfld]:
            missingflds.append(reqfld)
    return missingflds
