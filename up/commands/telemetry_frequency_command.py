from up.commands.command import BaseCommand, BaseCommandHandler


class TelemetryFrequencyCommand(BaseCommand):
    NAME = 'up.telemetry.frequency'
    FREQ_KEY = 'frequency'

    def __init__(self):
        super().__init__(self.NAME)


class TelemetryFrequencyCommandHandler(BaseCommandHandler):
    def __init__(self, callbacks):
        super().__init__()
        self.__callbacks = callbacks

    def run_action(self, command):
        data = command.data
        frequency = data.get(TelemetryFrequencyCommand.FREQ_KEY, None)
        if frequency is not None:
            self.callbacks.frequency = frequency

    @property
    def callbacks(self):
        return self.__callbacks
