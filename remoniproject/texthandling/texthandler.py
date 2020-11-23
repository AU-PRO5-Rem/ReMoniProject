"""
    Description:    This class is for text handling / filtering / formatting
                    sensor data. This class readies the data before it is to be
                    send with MQTT to server.
    Dependencies:   JsonHandler & FileHandler

    Functions:      :filterdata - Takes sensor data and sensor ID and formats
                                 it to a file
                    :getconfig - Gets filter for a particular sensor
                    :get_id - Gets id for a particular sensor

"""


class texthandler(object):

    def __init__(self, Ijsonhandler, Ifilehandler):
        self.__jsonhandler = Ijsonhandler()  # Inherit interface
        self.__filehandler = Ifilehandler()  # Inherit interface

        self.datafilter = {}  # Variable to store filter
        self.id = []  # Variable to store sensor ID in
        self.result = {}  # Variable to store filtered data

    def filterdata(self, sensordata_dict, sensor_id):

        """
        Filters sensor data.

        :param sensordata_dict: Sensor data for a particular sensor ID
        :param sensor_id:   Sensor ID
        :return: 1 - If success, -1 - If Error
        """

        if sensor_id != self.id:  # Checks for correct sensor ID
            return -1

        # Checks if sensor data is formatted correct
        if isinstance(sensordata_dict, str):
            sensordata_dict = \
                self.__jsonhandler.convertfromjson(sensordata_dict)

        filename = 'sensor_filtered_val_' + str(sensor_id) + '.txt'  # File name with ID

        # Filters through sensor data ands saves to result variable
        for key1, value1 in self.datafilter.items():
            for key2, value2 in sensordata_dict.items():
                if key1 == key2:
                    if value1 == 1:
                        self.result[key2] = value2

        # Adds timestamp to result variable
        self.result["Timestamp"] = sensordata_dict.get("Timestamp")

        # Converts to JSON format and saves data in temp variable
        temp = self.__jsonhandler.converttojson(self.result)

        # Writes to file.
        self.__filehandler.writefile(filename, temp)
        return 1

    def Getconfig(self, data):
        """
        Saves filter config for sensor with ID to local variable
        :param data: filter configuration
        :return: None
        """

        # Checks formatting of data, if data is str convert to dict
        if isinstance(data, str):
            data = self.__jsonhandler.convertfromjson(data)
        # Saves data to local variable
        self.datafilter = data

    def get_id(self, sensor_id):
        """
        Saves sensor ID to local variable
        :param sensor_id: sensor id
        :return: None
        """
        self.id = sensor_id
