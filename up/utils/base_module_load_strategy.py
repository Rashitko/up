class BaseModuleLoadStrategy:
    @staticmethod
    def load(module):
        return module.load()
