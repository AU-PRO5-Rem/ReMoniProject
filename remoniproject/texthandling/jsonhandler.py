from remoniproject.texthandling.interfaces import Ijsonhandler


import json


class jsonhandler(Ijsonhandler):
    def __init__(self):
        self.__jsonhandler = Ijsonhandler

    def convertfromjson(self):
        return NotImplementedError

    def converttojson(self):
        return NotImplementedError
