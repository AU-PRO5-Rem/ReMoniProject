"""
    Description:    writes to and reads from file
    Dependencies:   fcntl

    Functions:      :readfile - reads data from file
                    :writefile - Writes data to file

"""

from texthandling.interfaces.Ifilehandler import Ifilehandler
import fcntl    # package with file lock function
import os


class filehandler(Ifilehandler):

    def readfile(self, path):
        """
        Reads from file
        :param path: path to where file is located
        :return: returns file data
        """

        cwd = os.getcwd()   # get current working directory
        os.chdir(('../data'))   # Changes cwd to /data

        # Opens file
        with open(path, "r") as filepointer:
            # Local lock variable
            lock = 0
            # while loop to wait for lock to be available
            while lock != 1:
                # Tries to lock file so other process can't use it
                try:
                    # Lock function, throws exception if file is already locked
                    fcntl.flock(filepointer, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    lock = 1
                # Catch thrown error
                except IOError:
                    lock = 0
            # Reads data from file
            data = filepointer.read()
            # Releases lock
            fcntl.flock(filepointer, fcntl.LOCK_UN)
        os.chdir(cwd)   # Switch back to original working directory
        #returns data
        return data

    def writefile(self, file, data):
        """
        Write to file
        :param path: path including filename
        :param data: data going to be written to file
        :return: None
        """
        cwd = os.getcwd()   # get current working directory
        os.chdir(('../data'))   # Changes cwd to /data

        # Opens file
        with open(file, "w") as filepointer:
            lock = 0
            # Tries to get lock for the file
            while lock != 1:
                try:
                    fcntl.flock(filepointer, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    lock = 1
                except IOError:
                    lock = 0
            # Writes to file
            filepointer.write(data)
            # Releases lock
            fcntl.flock(filepointer, fcntl.LOCK_UN)

        os.chdir(cwd)   # Switch back to original working directory
