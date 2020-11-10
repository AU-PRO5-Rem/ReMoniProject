from remoniproject.texthandling.interfaces import Ifilehandler


class filehandler(Ifilehandler):
    def __init__(self, Ifilehandler):
        self.__filehandler = Ifilehandler

    def writetojsonfile(self):
        return NotImplementedError

    def readfromfile(self):
        return NotImplementedError