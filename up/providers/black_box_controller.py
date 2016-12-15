import time

from up.base_system_state_recorder import BaseSystemStateRecorder
from up.base_thread_module import BaseThreadModule


class BlackBoxController(BaseThreadModule):
    def __init__(self, state_recorder):
        super().__init__()
        self.__state_recorder = state_recorder

    def initialize(self, up):
        super().initialize(up)
        self.__state_recorder.initialize(up)

    def _notify_loop(self):
        while self._run:
            try:
                self.__state_recorder.record_state()
            except Exception as e:
                self.logger.critical("Error occurred during BlackBox data recording. Error was {}".format(e))
            time.sleep(0.5)


class BaseBlackBoxStateRecorder(BaseSystemStateRecorder):
    pass
