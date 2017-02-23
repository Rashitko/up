import sys
import time

from up.base_thread_module import BaseThreadModule
from up.commands.telemetry_frequency_command import TelemetryFrequencyCommand, TelemetryFrequencyCommandHandler
from up.modules.base_mission_control_provider import BaseMissionControlProvider


class TelemetryController(BaseThreadModule):
    LOAD_ORDER = sys.maxsize
    DEFAULT_FREQUENCY = 0.05

    def __init__(self):
        super().__init__()
        self.__frequency = self.DEFAULT_FREQUENCY
        self.__mission_control_provider = None

    def _execute_start(self):
        self.__mission_control_provider = self.up.get_module(BaseMissionControlProvider)
        if self.__mission_control_provider is None:
            self.logger.error("Mission Control Provider not available")
            return False
        return super()._execute_start()

    def _execute_initialization(self):
        super()._execute_initialization()
        self.up.command_executor.register_command(TelemetryFrequencyCommand.NAME,
                                                  TelemetryFrequencyCommandHandler(self))

    def _loop(self):
        while self._run:
            try:
                telemetry_data = {}
                for module in self.up._modules:
                    module_content = module.telemetry_content
                    self.__merge(telemetry_data, module_content)
                self.__mission_control_provider.send_telemetry(telemetry_data)
            except Exception as e:
                self.logger.critical("Telemetry transmission failed. Error was {}".format(e))
            time.sleep(self.__frequency)

    @staticmethod
    def __merge(first, second, path=None):
        """Merges second into first"""
        if second is None:
            return first

        if path is None:
            path = []
        for key in second:
            if key in first:
                if isinstance(first[key], dict) and isinstance(second[key], dict):
                    TelemetryController.__merge(first[key], second[key], path + [str(key)])
                elif first[key] == second[key]:
                    pass  # both contains the same value
                else:
                    raise ValueError("Conflict at %s" % '.'.join(path + [str(key)]))
            else:
                first[key] = second[key]
        return first

    @property
    def frequency(self):
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        self.__frequency = value
        self.logger.info('Telemetry frequency set to %ss' % value)
