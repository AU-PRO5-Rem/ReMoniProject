from remoniproject.texthandling.interfaces import Ifilehandler
from

class filehandler(Ifilehandler):
    def __init__(self, Ifilehandler):
        self.__filehandler = Ifilehandler

    def writetojsonfile(self, data, ID):
        filepath = 'remoniproject/data/'    # File path
        filename = 'Send_sensor'+str(ID)+'.json'   # File name with ID
        writepath = filepath + filename     # Complete path to file
        f = open(writepath, 'w+')       # Open file if file doesn't exist create the file
        f.write(data)       # Write json data in the file
        f.close()       # Close the file

    def readfromfile(self, ID):
        filepath = 'remoniproject/data/'  # File path
        filename = 'conf_pnZW100_MultiSensor_6_ni'+str(ID)+'.txt'   # File name with ID
        writepath = filepath + filename     # Complete path to file
        f = open(writepath, 'r')        # open file in read mode
        data = f.read()             # Read content of file
        f.close()           # Close file

        return data     # return data
