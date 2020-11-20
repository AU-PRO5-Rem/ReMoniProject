from remoniproject.texthandling.interfaces import Ijsonhandler, Ifilehandler


class texthandler(Ijsonhandler, Ifilehandler):
    def __init__(self, Ijsonhandler, Ifilehandler):
        self.__jsonhandler = Ijsonhandler
        self.__filehandler = Ifilehandler

        self.__filter = {}
        self.__id = {}
        self.__result = {}

    def filterdata(self, sensordata_dict, sensor_id):

        filepath = 'Remoni_Project/data/'    # File path
        filename = 'Send_sensor'+str(sensor_id)+'.txt'   # File name with ID
        writepath = filepath + filename     # Complete path to file

        for key1, value1 in filter.items():
            for key2, value2 in sensordata_dict.items():
                if key1 == key2:
                    if value1 == 1:
                        self.__result[key2] = value2

        self.__result["Timestamp"] = sensordata_dict.get("Timestamp")

        temp = self.__jsonhandler.converttojson(self.__result)

        self.__filehandler.writefile(writepath, temp)

    def Getconfig(self, config_dict):
        self.__filter = config_dict

    def get_id(self, id_dict):
        self.__id = id_dict



























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
