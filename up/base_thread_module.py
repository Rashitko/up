from abc import abstractmethod
from threading import Thread

from up.base_started_module import BaseStartedModule


class BaseThreadModule(BaseStartedModule):
    def __init__(self):
        super().__init__()
        self.__thread = None

    def _execute_initialization(self):
        super()._execute_initialization()

    def _execute_start(self):
        super()._execute_start()
        self.__thread = Thread(target=self._loop, name="Thread-%s" % self.__class__.__name__)
        self.__run = True
        self.__thread.start()
        return True

    def _execute_stop(self):
        super()._execute_stop()
        self.__run = False
        if self.__thread:
            self.__thread.join()
        self.__thread = None

    @abstractmethod
    def _loop(self):
        pass

    @property
    def _run(self):
        return self.__run
