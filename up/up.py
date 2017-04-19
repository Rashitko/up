from twisted.internet import reactor

from up.base_started_module import BaseStartedModule
from up.commands.command_executor import CommandExecutor
from up.commands.command_receiver import CommandReceiver
from up.commands.stop_command import BaseStopCommand, BaseStopCommandHandler
from up.modules.up_heading_provider import UpHeadingProvider
from up.modules.up_location_provider import UpLocationProvider
from up.modules.base_mission_control_provider import BaseMissionControlProvider
from up.providers.base_rx_provider import BaseRXProvider
from up.modules.telemetry_controller import TelemetryController
from up.utils.up_logger import UpLogger


class Up:
    def __init__(self, modules, recorders, flight_controller=None):
        self.__logger = UpLogger.get_logger()
        self.__modules = modules
        self.__started_modules = []

        self.__orientation_provider = None
        self.__flight_control_provider = None
        self.__mission_control_provider = None
        self._rx_provider = None

        self.__telemetry_controller = TelemetryController()
        self.__modules.append(self.telemetry_controller)
        self.__logger.debug("Telemetry Controller loaded")

        self.__modules.append(UpLocationProvider())
        self.__modules.append(UpHeadingProvider())

        for module in self.__modules:
            if issubclass(type(module), BaseStartedModule):
                self.__started_modules.append(module)
            if issubclass(type(module), BaseMissionControlProvider) :
                self.__logger.debug("Mission Control Provider loaded")
                self.__mission_control_provider = module

        self.__flight_controller = flight_controller
        if self.__flight_controller:
            self.__modules.append(self.__flight_controller)
        if self.__flight_controller is None:
            self.__logger.info("Flight Controller unavailable")

        self.__command_receiver = CommandReceiver()
        self.__modules.append(self.__command_receiver)

        self.__command_executor = CommandExecutor()
        self.__modules.append(self.__command_executor)
        self.__register_commands()

    def __register_commands(self):
        self.command_executor.register_command(BaseStopCommand.NAME, BaseStopCommandHandler())

    def initialize(self):
        for module in self.__modules:
            if module:
                module.initialize(self)

    def run(self):
        for module in self.__started_modules:
            if module:
                module.start()
        reactor.run()

    def stop(self):
        for module in self.__started_modules:
            if module:
                module.stop()

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def get_module(self, module_class):
        for module in self.__modules:
            if isinstance(module, module_class) or issubclass(module.__class__, module_class):
                return module
        return None

    @property
    def _modules(self):
        return self.__modules

    @property
    def command_receiver(self) -> CommandReceiver:
        return self.__command_receiver

    @property
    def command_executor(self) -> CommandExecutor:
        return self.__command_executor

    @property
    def flight_control(self) -> BaseMissionControlProvider:
        return self.__flight_control_provider

    @property
    def telemetry_controller(self) -> TelemetryController:
        return self.__telemetry_controller

    @property
    def rx_provider(self) -> BaseRXProvider:
        return self._rx_provider

    @property
    def mission_control_provider(self) -> BaseMissionControlProvider:
        return self.__mission_control_provider
