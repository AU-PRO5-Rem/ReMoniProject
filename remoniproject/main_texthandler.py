from texthandling.texthandler import texthandler as TH
from texthandling.interfaces.Ijsonhandler import jsonhandler as JH
from texthandling.filehandler import filehandler as FH


ID = [1,2,3,4]

data = {}

filter = {
    "Temperature": 1,
    "Time": 30,
    "Luminance": 1,
    "Ultraviolet": 1,
    "Relative Humidity": 1
}

data = {
    "Temperature": 71.0,
    "Luminance": 55.0,
    "Relative Humidity": 51.0,
    "Ultraviolet": 0.0,
    "Timestamp": "2020-11-18 11:37:39.727683"
}


def main():
    TH(JH, FH)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
