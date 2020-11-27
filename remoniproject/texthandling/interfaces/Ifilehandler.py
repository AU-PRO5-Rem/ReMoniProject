"""
    Description:    Interface to filehandler
"""

from abc import ABC, abstractmethod


class Ifilehandler(ABC):

    @abstractmethod
    def readfile(self, path):
        pass    # pragma: no cover

    @abstractmethod
    def writefile(self, path, data):
        pass    # pragma: no cover
