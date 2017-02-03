from up.base_started_module import BaseStartedModule


class BaseOrientationProvider(BaseStartedModule):

    ORIENTATION_PRECISION = 2

    def __init__(self):
        super().__init__()
        self.__yaw = None
        self.__pitch = None
        self.__roll = None

    def _execute_start(self):
        super()._execute_start()
        return True

    def _execute_stop(self):
        super()._execute_stop()

    def load(self):
        return True

    @property
    def telemetry_content(self):
        yaw = self.yaw
        if yaw:
            round(yaw, self.ORIENTATION_PRECISION)
        pitch = self.pitch
        if pitch:
            round(pitch, self.ORIENTATION_PRECISION)
        roll = self.roll
        if roll:
            round(roll, self.ORIENTATION_PRECISION)
        return {
            'orientation': {
                'yaw': yaw,
                'pitch': pitch,
                'roll': roll,
            }
        }

    @property
    def yaw(self):
        return self.__yaw

    @yaw.setter
    def yaw(self, value):
        self.__yaw = value

    @property
    def pitch(self):
        return self.__pitch

    @pitch.setter
    def pitch(self, value):
        self.__pitch = value

    @property
    def roll(self):
        return self.__roll

    @roll.setter
    def roll(self, value):
        self.__roll = value
