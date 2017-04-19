import configparser
import datetime
import logging
import os
import sys

from colorlog import ColoredFormatter

from up.utils.config_reader import ConfigReader
from up.utils.path_utils import PathUtils


class UpLogger:
    LOGGER_NAME = 'up-log'
    TRANSMISSION_LEVEL_NUM = 9
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    initialized = False

    @staticmethod
    def __initialize():
        configparser.ConfigParser()
        cfg = ConfigReader.instance().global_config
        log_level = cfg.get('log level')
        log_level = log_level.upper()
        log_path = os.path.join(os.getcwd(), 'logs')

        logging.addLevelName(UpLogger.TRANSMISSION_LEVEL_NUM, "TRANSMISSION")
        logger = logging.getLogger(UpLogger.LOGGER_NAME)
        logger.setLevel(log_level)

        path = os.path.abspath(log_path)
        path = PathUtils.expand_user(path)
        if not os.path.exists(path):
            os.makedirs(path)
        if not path.endswith('/'):
            path += '/'
        fh = logging.FileHandler("{}{}-{}.log".format(path, UpLogger.LOGGER_NAME,
                                                      datetime.datetime.now().strftime("%Y-%m-%d")))
        fh.setLevel(log_level)
        message_format = '==============================\n%(log_color)s[%(levelname)s] %(asctime)s%(reset)s\n\t''%(message)s\n\n\t''[FILE] %(pathname)s:%(lineno)s\n\t''[THREAD] %(threadName)s\n==============================\n\n'
        formatter = ColoredFormatter(message_format, UpLogger.DATE_FORMAT)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.propagate = False
        UpLogger.initialized = True

    @staticmethod
    def get_logger():
        if not UpLogger.initialized:
            UpLogger.__initialize()
        return logging.getLogger(UpLogger.LOGGER_NAME)
