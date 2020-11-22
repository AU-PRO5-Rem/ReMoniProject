"""
    Description:    Converts to and from json format and return data
    Dependencies:   json lib

    Functions:      :convertfromjson - Converts passed string to dict
                    :converttojson - Converts passed dict to string

"""

from remoniproject.texthandling.interfaces.Ijsonhandler import Ijsonhandler
import json


class jsonhandler(Ijsonhandler):

    def convertfromjson(self, json_data):
        """
        Converts to dict from string
        :param json_data: data in string format
        :return: data in dict format
        """

        # Converts data with json.loads function
        string_data = json.loads(json_data)

        # Returns converted data
        return string_data

    def converttojson(self, string_data):
        """
        Converts to string from dict
        :param string_data: data in dict format
        :return: data in string format
        """

        # Converts data with json.dumps funtion
        json_data = json.dumps(string_data)

        # Returns converted data
        return json_data
