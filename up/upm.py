import os

import pip
import yaml


class UpPackageManager:
    def __init__(self):
        print(os.getcwd())
        path = os.path.join(os.getcwd(), 'cogs.yml')
        if not os.path.isfile(path):
            print("Cannot open cogs.yml")
            exit(1)
        self.__cogs = yaml.load(open(path, 'r'))

        if not self.__check_cogs():
            exit(1)
        self.__process_cogs()

    def __check_cogs(self):
        result = True
        for name, spec in self.cogs.items():
            print("Checking %s..." % name)
            if spec is None:
                print("\t [FATAL] %s has not specification." % name)
                continue
            if spec.get('url', None) is None:
                print("\t [FATAL] The URL of %s must be specified." % name)
                result = False
            if spec.get('version', None) is None:
                print("\t [WARNING] The version of %s is not specified. Using latest version." % name)
        return result

    def __process_cogs(self):
        for name, spec in self.cogs.items():
            pip.main(['install', spec['url']])

    @property
    def cogs(self):
        return self.__cogs


if __name__ == "__main__":
    UpPackageManager()
