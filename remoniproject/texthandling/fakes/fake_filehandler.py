from remoniproject.texthandling.interfaces import Ifilehandler


class fake_filehandler(Ifilehandler):

    def __init__(self):
        pass

    def writetojsonfile(self):
        return NotImplementedError

    def readfromfile(self):
        return NotImplementedError
