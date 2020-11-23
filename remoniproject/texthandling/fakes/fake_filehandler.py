from remoniproject.texthandling.interfaces.Ifilehandler import Ifilehandler


class fake_filehandler(Ifilehandler):

    def readfile(self, path):
        data = {
            "Temperature": 71.0,
            "Luminance": 55.0,
            "Relative Humidity": 51.0,
            "Ultraviolet": 0.0,
            "Timestamp": "2020-11-18 11:37:39.727683"
        }
        return data

    def writefile(self, file, data):
        return
