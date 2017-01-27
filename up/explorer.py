import abc
import importlib
import os

from up.base_module import BaseModule
from up.base_system_state_recorder import BaseSystemStateRecorder


class Explorer:
    def __init__(self):
        pass

    def explore_modules(self):
        path = os.path.join(os.getcwd(), 'modules')
        return self.__explore_dir(path, BaseModule)

    def explore_recorders(self):
        path = os.path.join(os.getcwd(), 'recorders')
        return self.__explore_dir(path, BaseSystemStateRecorder)

    def __explore_dir(self, path: str, required_super_class: abc.ABCMeta):
        discovered = []
        if not os.path.isdir(path):
            return discovered
        root_module_name = path.split('/')[-2]
        type_name = path.split('/')[-1]
        for f in os.listdir(path):
            if self.__is_relevant(f):
                prefix = '%s.%s.%s' % (root_module_name, type_name, f.replace('.py', ''))
                mod = importlib.import_module(prefix)
                md = mod.__dict__
                defined_classes = [
                    md[c] for c in md if (
                        isinstance(md[c], type) and md[c].__module__ == mod.__name__ and issubclass(md[c],
                                                                                                    required_super_class)
                    )
                    ]
                for cls in defined_classes:
                    discovered.append({
                        'class_name': cls.__name__,
                        'prefix': cls.__module__
                    })
        return discovered

    @staticmethod
    def __is_relevant(file):
        return not file.startswith('__')
