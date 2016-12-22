import importlib
import os

import pip
import yaml


class UpPackageManager:
    def __init__(self):
        print(os.getcwd())
        path = os.path.join(os.getcwd(), 'circuits.yml')
        if not os.path.isfile(path):
            print("Cannot open circuits.yml")
            exit(1)
        self.__circuits = yaml.load(open(path, 'r'))

        lock_path = os.path.join(os.getcwd(), 'circuits.lock')
        if not self.__check_circuits():
            exit(1)
        print()
        with open(lock_path, 'w+') as lock_file:
            self.__lock = yaml.load(open(lock_path, 'r'))
            self.__process_circuits(lock_file)

    def __check_circuits(self):
        result = True
        for name, spec in self.circuits.items():
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

    def __process_circuits(self, lock_file):
        for name, spec in self.circuits.items():
            circuits_root_path = os.path.join(os.getcwd(), 'circuits')
            circuit_path = os.path.join(circuits_root_path, name)
            pip.main(['install', '--no-deps', '-t', circuit_path, '--upgrade', spec['url']])

    @property
    def circuits(self):
        return self.__circuits

    @property
    def lock(self):
        return self.__lock


if __name__ == "__main__":
    UpPackageManager()
