from twisted.internet import reactor

from up.base_started_module import BaseStartedModule
from up.commands.command_executor import CommandExecutor
from up.commands.command_receiver import CommandReceiver
from up.commands.stop_command import BaseStopCommand, BaseStopCommandHandler
from up.providers.base_rx_provider import BaseRXProvider
from up.providers.black_box_controller import BaseBlackBoxStateRecorder, BlackBoxController
from up.providers.load_guard_controller import LoadGuardController, BaseLoadGuardStateRecorder
from up.providers.mission_control_provider import BaseMissionControlProvider
from up.providers.orientation_provider import BaseOrientationProvider
from up.providers.telemetry_controller import BaseTelemetryStateRecorder, TelemetryController
from up.utils.up_logger import UpLogger


class Up:
    def __init__(self, modules, recorders, flight_controller=None):
        self.__logger = UpLogger.get_logger()
        self.__modules = modules
        self.__started_modules = []

        self.__orientation_provider = None
        self.__flight_control_provider = None
        self._rx_provider = None
        for module in self.__modules:
            if issubclass(type(module), BaseStartedModule):
                self.__started_modules.append(module)
                self.__orientation_provider = module
                self.__logger.debug("Orientation Provider loaded")
            if issubclass(type(module), BaseMissionControlProvider):
                self.__flight_control_provider = module
                self.__logger.debug("Flight Control Provider loaded")
            if issubclass(type(module), LoadGuardController):
                self.__logger.debug("Load Guard loaded")
            if issubclass(type(module), BaseRXProvider):
                self._rx_provider = module
                self.__logger.debug("RX Provider loaded")
        for recorder in recorders:
            if issubclass(type(recorder), BaseTelemetryStateRecorder):
                telemetry_controller = TelemetryController(recorder)
                self.__telemetry_controller = telemetry_controller
                self.__modules.append(telemetry_controller)
                self.__started_modules.append(telemetry_controller)
                self.__logger.debug("Telemetry Controller loaded")
            if issubclass(type(recorder), BaseBlackBoxStateRecorder):
                black_box_controller = BlackBoxController(recorder)
                self.__modules.append(black_box_controller)
                self.__started_modules.append(black_box_controller)
                self.__logger.debug("Black Box Controller loaded")
            if issubclass(type(recorder), BaseLoadGuardStateRecorder):
                self.__load_guard_controller = LoadGuardController(recorder)
                self.__modules.append(self.__load_guard_controller)
                self.__started_modules.append(self.__load_guard_controller)
                self.__logger.debug("Load Guard Controller loaded")

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

    def get_module(self, module_name):
        for module in self.__modules:
            if module.is_a(module_name):
                return module
        return None

    @property
    def command_receiver(self) -> CommandReceiver:
        return self.__command_receiver

    @property
    def command_executor(self) -> CommandExecutor:
        return self.__command_executor

    @property
    def orientation_provider(self) -> BaseOrientationProvider:
        return self.__orientation_provider

    @property
    def flight_control(self) -> BaseMissionControlProvider:
        return self.__flight_control_provider

    @property
    def load_guard_controller(self) -> LoadGuardController:
        return self.__load_guard_controller

    @property
    def telemetry_controller(self) -> TelemetryController:
        return self.__telemetry_controller

    @property
    def rx_provider(self) -> BaseRXProvider:
        return self._rx_provider
