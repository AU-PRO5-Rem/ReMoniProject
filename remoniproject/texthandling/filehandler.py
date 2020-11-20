from remoniproject.texthandling.interfaces import Ifilehandler
import fcntl


class filehandler(Ifilehandler):
    def __init__(self, Ifilehandler):
        self.__filehandler = Ifilehandler

    def readfile(self, path):

        with open(path, "r") as filepointer:
            lock = 0
            while lock != 1:
                try:
                    fcntl.flock(filepointer, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    lock = 1
                except IOError:
                    lock = 0
            data = filepointer
            fcntl.flock(filepointer, fcntl.LOCK_UN)

        return data

    def writefile(self, path, data):

        with open(path, "w") as filepointer:
            lock = 0
            while lock != 1:
                try:
                    fcntl.flock(filepointer, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    lock = 1
                except IOError:
                    lock = 0
            filepointer.write(data)
            fcntl.flock(filepointer, fcntl.LOCK_UN)
