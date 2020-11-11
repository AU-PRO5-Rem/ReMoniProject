from remoniproject.texthandling.interfaces import Ijsonhandler


import json


class jsonhandler(Ijsonhandler):
    def __init__(self):
        self.__jsonhandler = Ijsonhandler

    def convertfromjson(self, json_data):
        string_data = json.loads(json_data)

        return string_data

    def converttojson(self, string_data):
        json_data = json.dumps(string_data)

        return json_data
