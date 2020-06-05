import pprint
import logging
import logging.config
import kvlogger
logger= logging.getLogger(__name__)

'''
log_path='t_kvlogger.log'
config = {
    'disable_existing_loggers': False,
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s:%(lineno)d %(funcName)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': log_path,
            'maxBytes': 1024,
            'backupCount': 3
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}

'''

config=kvlogger.get_config('t_kvlogger.log')
print('config:')
pprint.pprint(config)
logging.config.dictConfig(config)
# logger=kvlogger.get_logger(__name__, 't_kvutil.log')
logger.debug('send out a message')
logger.info('send out an info message')
