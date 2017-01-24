import os
from abc import ABCMeta, abstractmethod

import yaml
from termcolor import colored


class UpRegistrar(metaclass=ABCMeta):
    EXTERNAL_MODULES_FILE = 'external_modules.yml'
    CONFIG_PATH = 'config'

    def __init__(self, cog_name):
        self.__cog_name = cog_name
        self.__external_modules = None
        self.__path = None

    @abstractmethod
    def register(self):
        pass

    def _load_external_modules(self, path=None):
        self.__path = path
        if self.__path is None:
            self.__path = os.path.join(os.getcwd(), UpRegistrar.EXTERNAL_MODULES_FILE)
        if not os.path.isfile(self.__path):
            UpRegistrar._print_error('File %s does not exist' % self.__path)
            return False
        self._print_info('Working with external_modules file at \'%s\'' % self.__path)
        with open(self.__path) as f:
            self.__external_modules = yaml.load(f)
            if self.__external_modules is None:
                self.__external_modules = {}
            if self.__external_modules.get(self.__cog_name, None) is None:
                self.__external_modules[self.__cog_name] = {}
            if self.__external_modules[self.__cog_name].get('modules', None) is None:
                self.__external_modules[self.__cog_name]['modules'] = []
            if self.__external_modules[self.__cog_name].get('recorders', None) is None:
                self.__external_modules[self.__cog_name]['recorders'] = []
            return self.__external_modules

    def _register_module(self, name, prefix):

        entry = {'class_name': name, 'prefix': prefix}
        modules = self.__external_modules[self.__cog_name]['modules']
        if entry not in modules:
            modules.append(entry)
            self._print_info('Registering %s.%s' % (prefix, name))
        else:
            self._print_warning('%s.%s already registered' % (prefix, name))

    def _write_external_modules(self):
        with open(self.__path, 'w') as f:
            yaml.dump(self.__external_modules, f)

    def _create_config(self, name, content, path=None):
        configs_root_path = path
        if configs_root_path is None:
            configs_root_path = os.path.join(os.getcwd(), self.CONFIG_PATH)
        if not os.path.isdir(configs_root_path):
            os.mkdir(configs_root_path)
        config_path = os.path.join(configs_root_path, name)
        if not os.path.isfile(config_path):
            self._print_info('Creating %s at %s' % (name, config_path))
            with open(config_path, 'w+') as f:
                f.write(content)
        else:
            self._print_warning('Config %s at %s already exists' % (name, config_path))

    @staticmethod
    def _print_error(message):
        print("\t[%s] - %s" % (colored('ERROR', 'red'), message))

    @staticmethod
    def _print_warning(message):
        print("\t[%s] - %s" % (colored('WARNING', 'yellow'), message))

    @staticmethod
    def _print_ok(message):
        print("\t[%s] - %s" % (colored('OK', 'green'), message))

    @staticmethod
    def _print_info(message):
        print("\t[%s] - %s" % (colored('INFO', 'blue'), message))
