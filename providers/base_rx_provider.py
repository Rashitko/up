from abc import abstractmethod

from base_started_module import BaseStartedModule


class BaseRXProvider(BaseStartedModule):
    @abstractmethod
    def get_channels(self):
        pass

    def load(self):
        return True
