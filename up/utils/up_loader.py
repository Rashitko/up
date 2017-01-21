import imp
import importlib
import inspect
import os

import yaml

from up.base_module import BaseModule
from up.base_system_state_recorder import BaseSystemStateRecorder
from up.flight_controller.base_flight_controller import BaseFlightController
from up.up import Up
from up.utils.base_module_load_strategy import BaseModuleLoadStrategy
from up.utils.up_logger import UpLogger


class UpLoader:
    def __init__(self, modules_path=None, modules_prefix=None, recorders_path=None, recorders_prefix=None,
                 flight_controller_path=None,
                 flight_controller_prefix=None):
        self.__flight_controller_prefix = flight_controller_prefix
        self.__flight_controller_path = flight_controller_path
        self.__recorders_prefix = recorders_prefix
        self.__recorders_path = recorders_path
        self.__modules_prefix = modules_prefix
        self.__modules_path = modules_path
        self.__logger = UpLogger.get_logger()
        self.__load_strategy = BaseModuleLoadStrategy()

    @staticmethod
    def __module_module_filter(name, klass):
        return not name.startswith('__') and issubclass(klass, BaseModule)

    @staticmethod
    def __recorders_filter(name, klass):
        return not name.startswith('__') and issubclass(klass, BaseSystemStateRecorder)

    @staticmethod
    def __flight_controller_filter(name, klass):
        return not name.startswith('__') and issubclass(klass, BaseFlightController)

    def create(self, load_condition_class=BaseModuleLoadStrategy, up_class=Up):
        """
        Loads all up modules which are specified in the '{up}/modules/' folder. The up module is
        loaded if it subclasses the BaseModule and has the load flag set.
        :param up_class: up class, if custom up implementation is used. The class is instantiated via
        constructor with one parameter, the up modules array
        :param load_condition_class: Class of the strategy used to determine whether the module should be loaded. Should
         be subclassed from the BaseModuleLoadStrategy class.
        :return: newly created up instance
        :rtype: Up
        """
        self.__load_strategy = load_condition_class()

        external_cogs = {}
        up_modules = []
        up_recorders = []
        flight_controllers = []

        with open('external_modules.yml') as external_cogs_file:
            external_cogs = yaml.load(external_cogs_file)
        for cog, spec in external_cogs.items():
            modules = spec['modules']
            for cog_module in modules:
                mod = importlib.import_module(cog_module['prefix'])
                cls = getattr(mod, cog_module['class_name'])
                up_modules.append(cls())
        importlib.invalidate_caches()

        if self.__modules_path:
            modules_folder = self.__get_modules_folder()
            if not modules_folder:
                return None
            self.__load_modules(self.__modules_prefix, modules_folder, up_modules,
                                self.__module_module_filter, self.__load_strategy)
        up_modules.sort(key=lambda x: x.LOAD_ORDER)

        if self.__recorders_path:
            recorders_folder = self.__get_recorders_folder()
            if not recorders_folder:
                return None
            self.__load_modules(self.__recorders_prefix, recorders_folder, up_recorders,
                                self.__recorders_filter, self.__load_strategy)

        if self.__flight_controller_path:
            flight_controller_folder = self.__get_flight_controller_folder()
            self.__load_modules(self.__flight_controller_prefix, flight_controller_folder,
                                flight_controllers, self.__flight_controller_filter, self.__load_strategy)
        if flight_controllers:
            if len(flight_controllers) > 1:
                self.__logger.warning(
                    "More than one FlightController specified. Using the {}".format(flight_controllers[0].class_name))
            fc = flight_controllers[0]
        else:
            self.__logger.warning("FlightController not found")
            fc = None

        return up_class(up_modules, up_recorders, fc)

    @staticmethod
    def __load_modules(module_prefix, folder, modules_list, module_filter, load_strategy):
        for module_file in os.listdir(folder):
            if not module_file.startswith('__') and module_file.endswith('.py'):
                file_name_limit = module_file.index('.')
                module_name = module_file[0:file_name_limit]
                modules_module = importlib.import_module(module_prefix + '.' + module_name)
                UpLoader.__process_module(modules_module, modules_list, module_filter, load_strategy)

    @staticmethod
    def __process_module(modules_module, up_modules, module_filter, load_strategy):
        """
        Processes the classes specified in the module. Only subclasses of the BaseModule are added to the
        up_modules list
        :param modules_module: module to load classes from
        :param up_modules: array of up modules, where instances of all relevant modules should be appended
        :return: None
        :rtype: None
        """
        # noinspection SpellCheckingInspection
        for name, klass in inspect.getmembers(modules_module):
            if module_filter(name, klass):
                UpLoader.__process_up_module(klass, name, up_modules, load_strategy)

    # noinspection SpellCheckingInspection
    @staticmethod
    def __process_up_module(klass, name, up_modules, load_strategy):
        """
        Adds the klass to the globals() under the 'name' key. Instantiates the up module and adds the instance to
        the 'up_modules' list if the load flag is set. Flag is checked via invocating the load() on the module
        instance.
        :param klass: class of the up module
        :param name: string name of the up module
        :param up_modules: list of up module instances, which has the load flag set
        :return: None
        :rtype: None
        """
        globals()[name] = klass
        try:
            if klass not in tuple(x.__class__ for x in up_modules):
                module = klass()
                if load_strategy.load(module):
                    up_modules.append(module)
        except TypeError as e:
            pass

    def __get_modules_folder(self):
        """
        :return: string path to the modules folder, or None if the folder was newly created
        :rtype: str
        """
        modules_path = os.path.join(os.path.dirname(__file__), self.__modules_path)
        modules_path = os.path.abspath(modules_path)
        self.__logger.debug('Looking for modules in {}'.format(modules_path))
        if not os.path.exists(modules_path):
            self.__logger.error(
                "Modules dir not found. Dir %s created, please place your modules there and start up again" % modules_path)
            os.makedirs(modules_path)
            return None
        return modules_path

    def __get_recorders_folder(self):
        """
        :return: string path to the modules folder, or None if the folder was newly created
        :rtype: str
        """
        modules_path = os.path.join(os.path.dirname(__file__), self.__recorders_path)
        modules_path = os.path.abspath(modules_path)
        self.__logger.debug('Looking for recorders in {}'.format(modules_path))
        if not os.path.exists(modules_path):
            self.__logger.error(
                "Recorders dir not found. Dir was created, please place your modules there and start up again")
            os.makedirs(modules_path)
            return None
        return modules_path

    def __get_flight_controller_folder(self):
        """
        :return: string path to the modules folder, or None if the folder was newly created
        :rtype: str
        """
        modules_path = os.path.join(os.path.dirname(__file__), self.__flight_controller_path)
        modules_path = os.path.abspath(modules_path)
        self.__logger.debug('Looking for flight controller in {}'.format(modules_path))
        if not os.path.exists(modules_path):
            self.__logger.error(
                "Flight Controller dir not found. Dir was created, please place your modules there and start up "
                "again")
            os.makedirs(modules_path)
            return None
        return modules_path
