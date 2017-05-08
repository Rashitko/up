import os

import yaml


class BaseModuleLoadStrategy:
    def __init__(self):
        self.__disabled_modules = None

        self.__load_disabled_modules()

    def load(self, module):
        fqn = "%s.%s" % (module.__module__, module.__class__.__name__)
        return fqn not in self.disabled_modules and module.load()

    def __load_disabled_modules(self):
        path = os.path.join(os.getcwd(), 'config', 'disabled_modules.yml')
        self.__disabled_modules = None
        if os.path.isfile(path):
            with open(path) as f:
                content = yaml.load(f)
                if content is not None:
                    self.__disabled_modules = content.get('disabled modules')
        if self.disabled_modules is None:
            self.__disabled_modules = []

    @property
    def disabled_modules(self):
        return self.__disabled_modules
