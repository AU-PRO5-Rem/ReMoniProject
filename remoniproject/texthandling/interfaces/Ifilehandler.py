from abc import ABC, abstractmethod


class Ifilehandler(ABC):

    @abstractmethod
    def writetojsonfile(self):
        pass

    @abstractmethod
    def readfromfile(self):
        pass
