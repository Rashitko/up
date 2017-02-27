from up.commands.command import BaseCommand


class TelemetryCommand(BaseCommand):
    NAME = 'up.telemetry.update'

    def __init__(self, telemetry):
        super().__init__(TelemetryCommand.NAME, telemetry)

    def suppress_warnings(self):
        return True
