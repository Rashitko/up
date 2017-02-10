from abc import abstractmethod

from up.base_started_module import BaseStartedModule
from up.commands.telemetry_command import TelemetryCommand


class BaseMissionControlProvider(BaseStartedModule):
    def send_telemetry(self, telemetry_data):
        cmd = TelemetryCommand(telemetry_data)
        self._transmit_telemetry(cmd.serialize())

    @abstractmethod
    def _transmit_telemetry(self, data):
        pass
