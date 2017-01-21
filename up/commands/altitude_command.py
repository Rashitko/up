from up.commands.command import BaseCommand, BaseCommandHandler


class AltitudeCommand(BaseCommand):
    NAME = 'up.altitude.change'

    def __init__(self):
        super().__init__(AltitudeCommand.NAME)


class AltitudeCommandHandler(BaseCommandHandler):
    def __init__(self, provider):
        super().__init__()
        self.__altitude_provider = provider

    def run_action(self, command):
        if command.data['altitude'] is not None:
            self.__altitude_provider.altitude = command.data['altitude']