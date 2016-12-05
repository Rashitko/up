from abc import ABCMeta

from up.utils.up_logger import UpLogger


class BaseModule(metaclass=ABCMeta):
    def __init__(self, silent=False):
        self.__silent = silent
        self.__logger = UpLogger.get_logger()
        self.__raspilot = None

    def initialize(self, raspilot):
        self.__raspilot = raspilot

    def _log_debug(self, message):
        if not self.__silent:
            self.logger.debug(message)

    def _log_info(self, message):
        if not self.__silent:
            self.logger.info(message)

    def _log_warning(self, message):
        if not self.__silent:
            self.logger.warning(message)

    def _log_error(self, message):
        if not self.__silent:
            self.logger.error(message)

    def _log_critical(self, message):
        if not self.__silent:
            self.logger.critical(message)

    def load(self):
        return False

    @property
    def logger(self):
        return self.__logger

    @property
    def class_name(self):
        """

        :rtype: str
        """
        return self.__class__.__name__

    @property
    def raspilot(self):
        return self.__raspilot
