from abc import ABC, abstractmethod


class Itexthandler(ABC):

    @abstractmethod
    def loadfilter(self):
        pass

    @abstractmethod
    def converttext(self):
        pass

    @abstractmethod
    def __stringtodict(self):
        pass

    @abstractmethod
    def __getdatafromjson(self):
        pass

    @abstractmethod
    def __savedatatojson(self):
        pass

    @abstractmethod
    def __filterdata(self):
        pass
