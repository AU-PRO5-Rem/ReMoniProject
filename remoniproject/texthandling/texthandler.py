from remoniproject.texthandling.interfaces import Ijsonhandler, Ifilehandler


class texthandler(Ijsonhandler, Ifilehandler):
    def __init__(self, Ijsonhandler, Ifilehandler):
        self.__jsonhandler = Ijsonhandler
        self.__filehandler = Ifilehandler

        self.__filter = {}

        self.__data_string = ""
        self.__data_json = '''{}'''
        self.__data_dict = {}

    def loadfilter(self):
        localid = {}        # Sensor ID

        for id in localid:  # Gets all sensor configs and saves them with ID
            self.__filter = {id, self.__filehandler.readconffile(id)}

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
