import importlib
import os

import pip
import yaml
from termcolor import colored

SPEC_URL_KEY = 'url'
SPEC_PYPI_KEY = 'pypi'
SPEC_VERSION_KEY = 'version'


class UpPackageManager:
    def load(self, cog_file_path='Cogfile.yml'):
        with open(cog_file_path) as cog_file:
            print('Loading cogs from %s' % self.__print_info(cog_file_path))
            yaml_load = yaml.load(cog_file)
            for (cog, spec) in yaml_load.items():
                print('Processing %s:' % self.__print_info(cog))
                self.__validate_cog_spec(spec)
                if spec.get(SPEC_URL_KEY) is not None:
                    print('Loading %s' % self.__print_info(spec[SPEC_URL_KEY]))
                    pip.main(['install', "git+%s" % spec[SPEC_URL_KEY]])
                elif spec.get(SPEC_PYPI_KEY) is not None:
                    pypi_name = spec[SPEC_PYPI_KEY]
                    if spec.get(SPEC_VERSION_KEY) is not None:
                        pypi_name += '==%s' % spec[SPEC_VERSION_KEY]
                    print('Loading %s' % self.__print_info(pypi_name))
                    pip.main(['install', pypi_name])
                print()

    def register(self, name):
        print("Registering %s" % self.__print_info(name))
        try:
            mod = importlib.import_module('%s.registrar' % name)
            cls = getattr(mod, 'Registrar')
            registrar = cls()
            if registrar.register():
                print("\t[%s] - Module %s registered" % (self.__print_ok('OK'), name))
            else:
                print("\t[%s] - Module %s NOT registered" % (self.__print_error('ERROR'), name))
        except ImportError:
            print("\t[%s] - Module %s cannot be imported. Have you installed it?" % (self.__print_error('CRITICAL'), name))

    @staticmethod
    def __validate_cog_spec(spec):
        if spec is None:
            print(UpPackageManager.__print_error('\t[FATAL]\tMissing spec'))
            exit(1)
        if SPEC_URL_KEY not in spec.keys() and SPEC_PYPI_KEY not in spec.keys():
            print(UpPackageManager.__print_error('\t[FATAL]\tMissing url or pypi'))
            exit(1)

    @staticmethod
    def __print_error(message):
        return colored(message, 'red')

    @staticmethod
    def __print_warning(message):
        return colored(message, 'yellow')

    @staticmethod
    def __print_ok(message):
        return colored(message, 'green')

    @staticmethod
    def __print_info(message):
        return colored(message, 'blue')
