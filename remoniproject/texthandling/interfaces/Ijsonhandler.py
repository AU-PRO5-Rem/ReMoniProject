"""
    Description:    Interface to jsonhandler
"""


from abc import ABC, abstractmethod


class Ijsonhandler(ABC):

    @abstractmethod
    def convertfromjson(self, json_data):
        pass

    @abstractmethod
    def converttojson(self, string_data):
        pass
