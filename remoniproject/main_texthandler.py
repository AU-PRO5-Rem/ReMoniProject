from .texthandling.texthandler import texthandler as TH
from .texthandling.jsonhandler import jsonhandler as JH
from .texthandling.filehandler import filehandler as FH


ID = [1,2,3,4]

filterdata = '''{
    "Temperature": 0,
    "Time": 30,
    "Luminance": 0,
    "Ultraviolet": 0,
    "Relative Humidity": 0
}'''

data = {
    "Temperature": 71.0,
    "Luminance": 55.0,
    "Relative Humidity": 51.0,
    "Ultraviolet": 0.0,
    "Timestamp": "2020-11-18 11:37:39.727683"
}


def main():
    text = TH(JH, FH)

    text.get_id(1)
    text.Getconfig(filterdata)
    if text.filterdata(data, 1) == -1:
        print("wrong id!");


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/