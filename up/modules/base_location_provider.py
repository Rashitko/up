from up.base_started_module import BaseStartedModule
from up.commands.location_command import LocationCommand, LocationCommandHandler, LocationCommandFactory


class BaseLocationProvider(BaseStartedModule):
    def __init__(self):
        super().__init__()
        self.__latitude = None
        self.__longitude = None
        self.__location_change_handle = None

    def _execute_start(self):
        self.__location_change_handle = self.up.command_executor.register_command(LocationCommand.NAME,
                                                                                  LocationCommandHandler(self))
        return True

    def _execute_stop(self):
        self.up.command_executor.unregister_command(LocationCommand.NAME, self.__location_change_handle)

    def _on_location_changed(self, lat, lon):
        self.up.command_executor.execute_command(LocationCommandFactory.create(lat, lon))

    @property
    def latitude(self):
        return self.__latitude

    @property
    def longitude(self):
        return self.__longitude

    @property
    def location(self):
        return self.latitude, self.longitude

    @location.setter
    def location(self, value):
        self.__latitude = value[0]
        self.__longitude = value[1]
        self._on_location_changed(value[0], value[1])
