import importlib
import os

import yaml
from up.utils.base_module_load_strategy import BaseModuleLoadStrategy

from up.explorer import Explorer
from up.up import Up
from up.utils.up_logger import UpLogger


class NewUpLoader:
    def __init__(self, load_strategy=BaseModuleLoadStrategy):
        self.__modules = []
        self.__recorders = []
        self.__flight_controller = None
        self.__logger = UpLogger.get_logger()
        self.__load_strategy = load_strategy()

    def create(self):
        self.__process_external_dependencies()

        self.__process_defined_modules()
        self.__modules.sort(key=lambda x: x.LOAD_ORDER)

        self.__process_defined_recorders()
        self.__recorders.sort(key=lambda x: x.LOAD_ORDER)

        return Up(self.__modules, self.__recorders, self.__flight_controller)

    def __process_external_dependencies(self):
        path = os.path.join(os.getcwd(), 'external_modules.yml')
        if not os.path.isfile(path):
            return
        with open(path) as f:
            external_modules = yaml.load(f)
            for name, spec in external_modules.items():
                self.__logger.debug('Processing %s from external modules' % name)
                for required_module in spec.get('modules', []):
                    self.__import_module_from_specs(required_module)
                for required_recorder in spec.get('recorders', []):
                        self.__import_recorder_from_specs(required_recorder)

    def __process_defined_modules(self):
        path = os.path.join(os.getcwd(), 'modules')
        if not os.path.isdir(path):
            self.__logger.warning("Modules folder not found")
            return
        explored_modules = Explorer().explore_modules()
        for explored_module in explored_modules:
            self.__import_module_from_specs(explored_module)

    def __import_module_from_specs(self, required_module):
        instance = self.__get_instance_of_imported(required_module)
        if instance.load() and self.__load_strategy.load(instance):
            self.__modules.append(instance)

    def __process_defined_recorders(self):
        path = os.path.join(os.getcwd(), 'recorders')
        if not os.path.isdir(path):
            self.__logger.warning("Recorders folder not found")
            return
        explored_recorders = Explorer().explore_recorders()
        for explored_recorder in explored_recorders:
            self.__import_recorder_from_specs(explored_recorder)

    def __import_recorder_from_specs(self, required_module):
        instance = self.__get_instance_of_imported(required_module)
        if instance.load() and self.__load_strategy.load(instance):
            self.__recorders.append(instance)

    @staticmethod
    def __get_instance_of_imported(required_module):
        mod = importlib.import_module(required_module['prefix'])
        cls = getattr(mod, required_module['class_name'])
        instance = cls()
        return instance
