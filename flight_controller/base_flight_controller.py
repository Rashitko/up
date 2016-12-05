from base_thread_module import BaseThreadModule
from providers.base_rx_provider import BaseRXProvider
from providers.orientation_provider import BaseOrientationProvider


class BaseFlightController(BaseThreadModule):
    def _execute_initialization(self):
        super()._execute_initialization()
        if not self.raspilot.rx_provider:
            raise ValueError("Flight Controller cannot be used without RX Provider")
        if not self.raspilot.orientation_provider:
            raise ValueError("Flight Controller cannot be used without Orientation Provider")

    def _execute_start(self):
        super()._execute_start()
        return True

    def load(self):
        return True

    @property
    def _rx_provider(self) -> BaseRXProvider:
        return self.raspilot.rx_provider

    @property
    def _orientation_provider(self) -> BaseOrientationProvider:
        return self.raspilot.orientation_provider
