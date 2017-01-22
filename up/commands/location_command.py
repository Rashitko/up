from up.commands.command import BaseCommand, BaseCommandHandler


class LocationCommand(BaseCommand):
    NAME = 'up.location.change'

    LAT_KEY = 'lat'
    LON_KEY = 'lon'

    def __init__(self):
        super().__init__(LocationCommand.NAME)


class LocationCommandFactory:
    @staticmethod
    def create(lat, lon) -> LocationCommand:
        command = LocationCommand()
        command.data = {LocationCommand.LAT_KEY: lat, LocationCommand.LON_KEY: lon}
        return command


class LocationCommandHandler(BaseCommandHandler):
    def __init__(self, callbacks):
        super().__init__()
        self.__callbacks = callbacks

    def run_action(self, command):
        data = command.data
        if data.get(LocationCommand.LAT_KEY, None) is not None and data.get(LocationCommand.LON_KEY, None) is not None:
            self.callbacks.location = (data[LocationCommand.LAT_KEY], data[LocationCommand.LON_KEY])

    @property
    def callbacks(self):
        return self.__callbacks
