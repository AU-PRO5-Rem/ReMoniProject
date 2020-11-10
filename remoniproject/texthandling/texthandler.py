from remoniproject.texthandling.interfaces import Itexthandler, Ijsonhandler, Ifilehandler


class texthandler(Itexthandler, Ijsonhandler, Ifilehandler):
    def __init__(self, Itexthandler, Ijsonhandler, Ifilehandler):
        self.__texthandler = Itexthandler
        self.__jsonhandler = Ijsonhandler
        self.__filehandler = Ifilehandler

        self.__filter = {}

        self.__data_string = ""
        self.__data_json = '''{}'''
        self.__data_dict = {}

    def loadfilter(self):
        return NotImplementedError

    def converttext(self):
        return NotImplementedError

    def __stringtodict(self):
        return NotImplementedError

    def __getdatafromjson(self):
        return NotImplementedError

    def __savedatatojson(self):
        return NotImplementedError

    def __filterdata(self):
        return NotImplementedError
