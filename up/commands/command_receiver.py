from up.base_module import BaseModule


class CommandReceiver(BaseModule):
    def execute_command(self, command):
        self.up.command_executor.execute_command(command)
