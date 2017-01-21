from up.commands.heading_command import HeadingCommand, HeadingCommandHandler
from up.base_started_module import BaseStartedModule


class BaseHeadingProvider(BaseStartedModule):
    def __init__(self):
        super().__init__()
        self.__actual_heading = None
        self.__required_heading = None
        self.__command_handle = None

    def _execute_start(self):
        self.__command_handle = self.up.command_executor.register_command(HeadingCommand.NAME,
                                                                          HeadingCommandHandler(self))
        return True

    def _execute_stop(self):
        self.up.command_executor.unregister_command(HeadingCommand.NAME, self.__command_handle)
        pass

    def _on_actual_heading_changed(self, new_actual_heading):
        cmd = HeadingCommand()
        cmd.data = {'mode': HeadingCommand.SET_MODE_ACTUAL, 'heading': new_actual_heading}
        self.up.command_executor.execute_command(cmd)

    def _on_required_heading_changed(self, new_required_heading):
        cmd = HeadingCommand()
        cmd.data = {'mode': HeadingCommand.SET_MODE_REQUIRED, 'heading': new_required_heading}
        self.up.command_executor.execute_command(cmd)

    def load(self):
        return True

    @property
    def actual_heading(self):
        return self.__actual_heading

    @actual_heading.setter
    def actual_heading(self, value):
        self.__actual_heading = value
        self._on_actual_heading_changed(value)

    @property
    def required_heading(self):
        return self.__required_heading

    @required_heading.setter
    def required_heading(self, value):
        self.__required_heading = value
        self._on_required_heading_changed(value)
