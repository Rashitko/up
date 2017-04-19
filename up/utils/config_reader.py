import configparser
import os

import yaml

from up.utils.singleton import Singleton


class ConfigReader(metaclass=Singleton):
    CONFIG_DIR = os.path.join(os.getcwd(), 'config')
    MODULES_CONFIG_PATH = os.path.join(CONFIG_DIR, 'disabled_modules.yml')
    GLOBAL_CONFIG_PATH = os.path.join(CONFIG_DIR, 'config.yml')

    def __init__(self):
        current_path = os.path.dirname(__file__)

        self.__modules_config_path = os.path.abspath(os.path.join(current_path, self.MODULES_CONFIG_PATH))
        self.__modules_config = None
        with open(self.__modules_config_path) as f:
            self.__modules_config = yaml.load(f)

        self.__global_config_path = os.path.abspath(os.path.join(current_path, self.GLOBAL_CONFIG_PATH))
        with open(self.__global_config_path) as f:
            self.__global_config = yaml.load(f)

    def module_enabled(self, module):
        module_name = module.__class__.__name__
        if self.__modules_config and self.__modules_config.get('disabled modules') is not None:
            if module_name in self.__modules_config['disabled modules']:
                return False
        return True

    @property
    def global_config(self):
        return self.__global_config

    @property
    def global_config_path(self):
        return self.__global_config_path

    @staticmethod
    def instance():
        return ConfigReader()
