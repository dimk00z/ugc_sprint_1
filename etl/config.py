import os
import logging

BATCH_SIZE = 100

KAFKA_HOST = os.getenv('KAFKA_HOST', ['localhost'])
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', '')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID')

CH_HOST = os.getenv('CH_HOST', 'localhost')
CH_TABLE = os.getenv('CH_TABLE', 'movies')

log_config = {
    "version": 1,
    "root": {
        "handlers": ["console"],
        "level": "DEBUG"
    },
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        }
    },
    "formatters": {
        "std_out": {
            "format": "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : (Process Details : (%(process)d, %(processName)s), Thread Details : (%(thread)d, %(threadName)s))\nLog : %(message)s",
            "datefmt": "%d-%m-%Y %I:%M:%S"
        }
    },
}