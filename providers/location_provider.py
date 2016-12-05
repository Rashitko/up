from abc import abstractmethod

from base_started_module import BaseStartedModule


class BaseLocationProvider(BaseStartedModule):
    @abstractmethod
    def get_location(self):
        pass

    def load(self):
        return True
