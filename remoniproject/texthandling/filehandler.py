from remoniproject.texthandling.interfaces import Ifilehandler


class filehandler(Ifilehandler):
    def __init__(self, Ifilehandler):
        self.__filehandler = Ifilehandler

    def readfile(self, path):
        f = open(path, 'r')     # Opens file on path
        data = f.read()     # Reads file content
        f.close()       # Closes files
        return data


    def writefile(self, path, data):

        return NotImplementedError





    def writetojsonfile(self, data, ID):
        filepath = 'remoniproject/data/'    # File path
        filename = 'Send_sensor'+str(ID)+'.json'   # File name with ID
        writepath = filepath + filename     # Complete path to file
        # Open file if file doesn't exist create the file
        f = open(writepath, 'w+')
        f.write(data)       # Write json data in the file
        f.close()       # Close the file

    def readfromfile(self):
        return NotImplementedError

    def readconffile(self, ID):
        filepath = 'remoniproject/data/'  # File path
        # File name with ID
        filename = 'conf_pnZW100_MultiSensor_6_ni'+str(ID)+'.txt'
        writepath = filepath + filename     # Complete path to file
        f = open(writepath, 'r')        # open file in read mode
        data = f.read()             # Read content of file
        f.close()           # Close file

        return data     # return data
