from abc import ABC, abstractmethod


class Ifilehandler(ABC):

    @abstractmethod
    def writetojsonfile(self, data, ID):
        pass

    @abstractmethod
    def readfromfile(self):
        pass

    @abstractmethod
    def readconffile(self, ID):
        pass
