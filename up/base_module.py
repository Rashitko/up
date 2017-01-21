from abc import ABCMeta

from up.utils.up_logger import UpLogger


class BaseModule(metaclass=ABCMeta):

    LOAD_ORDER = 0

    def __init__(self, silent=False):
        self.__silent = silent
        self.__logger = UpLogger.get_logger()
        self.__up = None

    def initialize(self, up):
        self.__up = up
        self._log_debug("Initializing {}".format(self.class_name))
        self._execute_initialization()

    def _execute_initialization(self):
        """
        Subclasses must override this method. Initialize the provider here.
        :return: None
        """
        pass

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

    def is_a(self, module_name):
        return self.__class__.__name__ == module_name

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
    def up(self):
        return self.__up

    @classmethod
    def instance(cls, up):
        up.get_module(cls)
