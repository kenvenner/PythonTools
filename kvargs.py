"""
@author:   Ken Venner
@contact:  ken@venerllc.com
@version:  1.04

Library of tools used in command line processing with configuration files

"""

import logging
import logging.config

logger = logging.getLogger(__name__)

from attrdict import AttrDict
import argparse
import json
import os

AppVersion = '1.04'


def merge_settings(args, conf_files=None, args_default=None, req_flds=None):
    # set defaults if not passed in
    if conf_files is None:
        conf_files = []
    if args_default is None:
        args_default = {}
    if req_flds is None:
        req_flds = []
        
    # convert the command line options into a dictionary
    vargs = AttrDict(vars(args))

    # make a copy so we can look up in this - rather than leave it a NameSpace
    args = AttrDict(vars(args))

    # make sure we have an array of files to be processed
    if conf_files and not isinstance(conf_files, list):
        conf_files = [conf_files]
        
    # load the configuration files if the exist
    confloaded = list()
    for conffile in conf_files:
        if os.path.exists(conffile):
            with open(conffile, 'r') as json_conf:
                try:
                    fileargs = json.load(json_conf)
                except Exception as e:
                    print('ERROR:  {} not loaded due to error:  {}'.format(conffile, e))
                    logger.error('skipped using: %s : due to error: %s', conffile, e)
                    continue
            confloaded.append(conffile)
            for k, v in fileargs.items():
                if (k in args_default and args[k] and args[k] != args_default[k]) or (
                        k not in args_default and k in args and args[k]):
                    # command line was changed from default setting - keep the command line setting
                    logger.debug(
                        'keep command line setting - ignore conf file setting-file:{}:key:{}'.format(conffile, k))
                    continue

                # overwrite current value with value from conf file
                vargs[k] = v

    # set defaults if variable is not set - and it should have a default
    for k, v in args_default.items():
        if k not in vargs or not vargs[k]:
            vargs[k] = v

    # create a configuration variable to capture files that were loaded
    if confloaded:
        logger.debug('Loaded conf files: %s', confloaded)
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
