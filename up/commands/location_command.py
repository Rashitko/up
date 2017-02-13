from up.commands.command import BaseCommand, BaseCommandHandler


class LocationCommand(BaseCommand):
    NAME = 'up.location.change'

    LAT_KEY = 'latitude'
    LON_KEY = 'longitude'
    ALT_KEY = 'altitude'
    DISTANCE_FROM_HOME_KEY = 'distance_from_home'
    REQUIRED_BEARING_KEY = 'required_bearing'

    def __init__(self):
        super().__init__(LocationCommand.NAME)


class LocationCommandFactory:
    @staticmethod
    def create(lat, lon, distance_from_home, required_bearing) -> LocationCommand:
        command = LocationCommand()
        command.data = {LocationCommand.LAT_KEY: lat, LocationCommand.LON_KEY: lon,
                        LocationCommand.DISTANCE_FROM_HOME_KEY: distance_from_home,
                        LocationCommand.REQUIRED_BEARING_KEY: required_bearing}
        return command


class LocationCommandHandler(BaseCommandHandler):
    def __init__(self, callbacks):
        super().__init__()
        self.__callbacks = callbacks

    def run_action(self, command):
        data = command.data
        if data.get(LocationCommand.LAT_KEY, None) is not None and data.get(LocationCommand.LON_KEY,
                                                                            None) is not None and data.get(
            LocationCommand.ALT_KEY) is not None and data.get(
            LocationCommand.DISTANCE_FROM_HOME_KEY) is not None and data.get(
            LocationCommand.REQUIRED_BEARING_KEY) is not None:
            self.callbacks.location = (
                data[LocationCommand.LAT_KEY], data[LocationCommand.LON_KEY], data[LocationCommand.ALT_KEY],
                data[LocationCommand.DISTANCE_FROM_HOME_KEY],
                data[LocationCommand.REQUIRED_BEARING_KEY])

    @property
    def callbacks(self):
        return self.__callbacks
