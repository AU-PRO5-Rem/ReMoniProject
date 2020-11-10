from abc import ABC, abstractmethod


class Ijsonhandler(ABC):

    @abstractmethod
    def convertfromjson(self):
        pass

    @abstractmethod
    def converttojson(self):
        pass
