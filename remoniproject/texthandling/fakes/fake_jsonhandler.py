from texthandling.interfaces.Ijsonhandler import Ijsonhandler


class fake_jsonhandler(Ijsonhandler):

    def convertfromjson(self, json_data):
        data = {
            "Temperature": 71.0,
            "Luminance": 55.0,
            "Relative Humidity": 51.0,
            "Ultraviolet": 0.0,
            "Timestamp": "2020-11-18 11:37:39.727683"
        }
        return data

    def converttojson(self, string_data):
        data = '''{
            "Temperature": 71.0,
            "Luminance": 55.0,
            "Relative Humidity": 51.0,
            "Ultraviolet": 0.0,
            "Timestamp": "2020-11-18 11:37:39.727683"
        }'''
        return data
