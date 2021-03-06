from abc import abstractmethod

from up.base_started_module import BaseStartedModule


class BaseRXProvider(BaseStartedModule):
    @abstractmethod
    def get_channels(self):
        pass

    @abstractmethod
    def set_channels(self, values):
        pass

    @property
    def telemetry_content(self):
        return {
            'rx': self.get_channels()
        }