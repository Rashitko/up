import os

import pip
import yaml
from termcolor import colored

SPEC_URL_KEY = 'url'


class UpPackageManager:
    def load(self, cog_file_path='Cogfile.yml'):
        with open(cog_file_path) as cog_file:
            print('Loading cogs from %s' % self.__print_info(cog_file_path))
            yaml_load = yaml.load(cog_file)
            for (cog, spec) in yaml_load.items():
                print('Processing %s:' % self.__print_info(cog))
                self.__validate_cog_spec(spec)
                print('Loading %s' % self.__print_info(spec[SPEC_URL_KEY]))
                os.environ['UPM_INSTALL_PATH'] = os.getcwd()
                pip.main(['install', "git+%s" % spec[SPEC_URL_KEY]])
                print()

    @staticmethod
    def __validate_cog_spec(spec):
        if spec is None:
            print(UpPackageManager.__print_error('\t[FATAL]\tMissing spec'))
            exit(1)
        if SPEC_URL_KEY not in spec.keys():
            print(UpPackageManager.__print_error('\t[FATAL]\tMissing url'))
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
