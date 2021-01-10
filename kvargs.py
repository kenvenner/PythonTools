import logging
import logging.config

logger = logging.getLogger(__name__)

from attrdict import AttrDict
import argparse
import os

def merge_settings( args, conf_files=[], args_default={}, req_flds=[] ):
        
    # convert the command line options into a dictionary
    vargs = AttrDict(vars(args))

    if conf_files and not isinstance(conf_files,list):
        conf_files=[conf_files]
        
    # load the configuration files if the exist
    confloaded=list()
    for conffile in conf_files:
        if os.path.exists(conffile):
            with open(conffile, 'r') as json_conf:
                fileargs = json.load(json_conf)
            confloaded.append(conffile)
            for k, v in fileargs.items():
                if (k in args_default and args[k] and args[k] != args_default[k]) or (k not in args_default and k in args and args[k]):
                    # command line was changed from default setting - keep the command line setting
                    logger.debug('keep command line setting - ignore conf file setting-file:{}:key:{}'.format(conffile,k))
                    continue
                
                # overwrite current value with value from conf file
                vargs[k] = v

    logger.debug('loaded conf files:', confloaded)

    # set defaults if variable is not set - and it should have a default
    for k, v in args_default.items():
        if k not in vargs or not vargs[k]:
            vargs[k] = v
            
    return vargs

def missing_settings( vargs, req_flds ):
    # validate we have all the required fields
    missingflds = list()
    for reqfld in req_flds:
        if not vargs[reqfld]:
            missingflds.append(reqfld)
    return missingflds

