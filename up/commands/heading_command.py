from up.commands.command import BaseCommand, BaseCommandHandler


class HeadingCommand(BaseCommand):
    MODE_KEY = 'mode'
    HEADING_KEY = 'heading'

    NAME = 'up.heading.change'
    SET_MODE_REQUIRED = 'required'
    SET_MODE_ACTUAL = 'actual'

    def __init__(self):
        super().__init__(HeadingCommand.NAME)


class HeadingCommandFactory:
    @staticmethod
    def create(heading, mode) -> HeadingCommand:
        cmd = HeadingCommand()
        cmd.data = {HeadingCommand.HEADING_KEY: heading, HeadingCommand.MODE_KEY: mode}


class HeadingCommandHandler(BaseCommandHandler):
    def __init__(self, provider):
        super().__init__()
        self.__heading_provider = provider

    def run_action(self, command):
        if command is None:
            return None
        heading = command.data.get(HeadingCommand.HEADING_KEY, None)
        mode = command.data.get(HeadingCommand.MODE_KEY, None)
        if mode == HeadingCommand.SET_MODE_REQUIRED:
            self.heading_provider.required_heading = heading
        elif mode == HeadingCommand.SET_MODE_ACTUAL:
            self.heading_provider.actual_heading = heading
        else:
            self.logger.error("SET MODE '%s' not supported" % mode)

    @property
    def heading_provider(self):
        return self.__heading_provider
