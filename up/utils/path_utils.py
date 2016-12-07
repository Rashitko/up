import os


class PathUtils:
    @staticmethod
    def expand_user(path):
        if '~' in path:
            return os.path.join(os.path.expanduser(path[path.index('~'):]))
        return path