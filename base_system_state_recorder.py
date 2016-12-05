from abc import abstractmethod

from base_module import BaseModule


class BaseSystemStateRecorder(BaseModule):
    @abstractmethod
    def record_state(self):
        pass

    def load(self):
        return True
