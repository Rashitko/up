from abc import abstractmethod

from up.base_started_module import BaseStartedModule


class BaseMissionControlProvider(BaseStartedModule):
    @abstractmethod
    def send_message(self, message):
        pass