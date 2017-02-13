from up.base_started_module import BaseStartedModule
from up.commands.location_command import LocationCommand, LocationCommandHandler


class BaseLocationProvider(BaseStartedModule):
    def __init__(self):
        super().__init__()
        self.__latitude = None
        self.__longitude = None
        self.__altitude = None
        self.__distance_from_home = None
        self.__required_bearing = None
        self.__location_change_handle = None

    def _execute_start(self):
        super()._execute_start()
        self.__location_change_handle = self.up.command_executor.register_command(LocationCommand.NAME,
                                                                                  LocationCommandHandler(self))
        return True

    def _execute_stop(self):
        super()._execute_stop()
        if self.__location_change_handle:
            self.up.command_executor.unregister_command(LocationCommand.NAME, self.__location_change_handle)

    def _on_location_changed(self):
        pass

    def load(self):
        return True

    @property
    def telemetry_content(self):
        return {
            'location': {
                'latitude': self.latitude,
                'longitude': self.longitude,
                'altitude': self.altitude
            }
        }

    @property
    def latitude(self):
        return self.__latitude

    @property
    def longitude(self):
        return self.__longitude

    @property
    def altitude(self):
        return self.__altitude

    @property
    def location(self):
        return self.latitude, self.longitude

    @location.setter
    def location(self, value):
        self.__latitude = value[0]
        self.__longitude = value[1]
        self.__altitude = value[2]
        self.__distance_from_home = value[3]
        self.required_bearing = value[4]
        self._on_location_changed()

    @property
    def distance_from_home(self):
        return self.__distance_from_home

    @distance_from_home.setter
    def distance_from_home(self, value):
        self.__distance_from_home = value

    @property
    def required_bearing(self):
        return self.__required_bearing

    @required_bearing.setter
    def required_bearing(self, value):
        self.__required_bearing = value
