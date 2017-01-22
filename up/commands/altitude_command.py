from up.commands.command import BaseCommand, BaseCommandHandler


class AltitudeCommand(BaseCommand):
    NAME = 'up.altitude.change'

    ALTITUDE_KEY = 'altitude'

    def __init__(self):
        super().__init__(AltitudeCommand.NAME)


class AltitudeCommandFactory:
    @staticmethod
    def create(altitude) -> AltitudeCommand:
        cmd = AltitudeCommand()
        cmd.data = {AltitudeCommand.ALTITUDE_KEY: altitude}
        return cmd


class AltitudeCommandHandler(BaseCommandHandler):
    def __init__(self, provider):
        super().__init__()
        self.__altitude_provider = provider

    def run_action(self, command):
        if command.data.get(AltitudeCommand.ALTITUDE_KEY, None) is not None:
            self.__altitude_provider.altitude = command.data[AltitudeCommand.ALTITUDE_KEY]