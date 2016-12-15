import time

from up.base_system_state_recorder import BaseSystemStateRecorder
from up.base_thread_module import BaseThreadModule


class LoadGuardController(BaseThreadModule):
    def __init__(self, load_guard, delay=0.5):
        super().__init__()
        self.__delay = delay
        self.__load_guard = load_guard

    def initialize(self, up):
        super().initialize(up)
        self.__load_guard.initialize(up)

    def _loop(self):
        while self._run:
            try:
                self.__load_guard.record_state()
            except Exception as e:
                self.logger.critical("Error occurred checking system load. Error was {}".format(e))
            time.sleep(self.__delay)

    @property
    def load_guard(self):
        return self.__load_guard


class BaseLoadGuardStateRecorder(BaseSystemStateRecorder):
    pass
