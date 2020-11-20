from abc import ABC, abstractmethod


class Ifilehandler(ABC):

    @abstractmethod
    def readfile(self, path):
        pass

    @abstractmethod
    def writefile(self, path, data):
        pass
