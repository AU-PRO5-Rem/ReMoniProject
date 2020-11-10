from remoniproject.texthandling.interfaces import Ijsonhandler


class fake_jsonhandler(Ijsonhandler):
    def __init__(self):
        pass

    def convertfromjson(self):
        return NotImplementedError

    def converttojson(self):
        return NotImplementedError
