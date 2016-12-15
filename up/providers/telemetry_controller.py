import time

from up.base_system_state_recorder import BaseSystemStateRecorder
from up.base_thread_module import BaseThreadModule


class TelemetryController(BaseThreadModule):
    DEFAULT_DELAY = 0.1

    def __init__(self, state_recorder):
        super().__init__()
        self.__state_recorder = state_recorder
        self.__delay = self.DEFAULT_DELAY

    def initialize(self, up):
        super().initialize(up)
        self.__state_recorder.initialize(up)

    def _notify_loop(self):
        while self._run:
            try:
                self.__state_recorder.record_state()
            except Exception as e:
                self.logger.critical("Telemetry transmission failed. Error was {}".format(e))
            time.sleep(self.__delay)

    @property
    def delay(self):
        return self.__delay

    @delay.setter
    def delay(self, value):
        self.__delay = value


class BaseTelemetryStateRecorder(BaseSystemStateRecorder):
    pass
