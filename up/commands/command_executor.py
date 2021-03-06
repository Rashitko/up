import uuid
from queue import Queue

from twisted.internet import reactor

from up.base_module import BaseModule


class CommandExecutor(BaseModule):
    def __init__(self):
        super().__init__()
        self.__handlers = {}
        self.__queue = Queue()

    def register_command(self, name, handler):
        handle = uuid.uuid1()
        if self.__handlers.get(name, None) is None:
            self.__handlers[name] = {}
        self.__handlers[name][handle] = handler
        self._log_debug("Handler {} for {} registered".format(handle, name))
        return handle

    def unregister_command(self, name, handle):
        if self.__handlers.get(name, None) is not None:
            if handle in self.__handlers[name]:
                self._log_debug("Handler {} for {} unregistered".format(handle, name))
                return self.__handlers.pop(handle, None)
        return None

    def remote_handler(self, command_name):
        self.__handlers[command_name] = None

    def execute_command(self, command):
        if command is not None:
            handlers = self.__handlers.get(command.name, None)
            if handlers:
                for handler in handlers.values():
                    reactor.callFromThread(handler.run_action, command)
            elif not command.suppress_warnings:
                self._log_warning("Unknown command {} received".format(command.name))
