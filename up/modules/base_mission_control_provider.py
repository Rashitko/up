from abc import abstractmethod

from up.base_started_module import BaseStartedModule
from up.commands.telemetry_command import TelemetryCommand


class BaseMissionControlProvider(BaseStartedModule):
    def send_telemetry(self, telemetry_data):
        cmd = TelemetryCommand(telemetry_data)
        self._transmit_data(cmd.serialize())

    def send_command(self, cmd):
        self._transmit_data(cmd.serialize())

    @abstractmethod
    def _transmit_data(self, data):
        pass
