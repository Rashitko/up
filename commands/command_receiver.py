from base_module import BaseModule


class CommandReceiver(BaseModule):
    def execute_command(self, command):
        self.raspilot.command_executor.execute_command(command)
