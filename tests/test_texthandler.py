from remoniproject.texthandling.fakes.fake_filehandler import fake_filehandler
from remoniproject.texthandling.fakes.fake_jsonhandler import fake_jsonhandler
from remoniproject.texthandling.texthandler import texthandler

import unittest


class Testtexthandler(unittest.TestCase):
    def setUp(self):
        filterdata = '''{
            "Temperature": 1,
            "Time": 30,
            "Luminance": 0,
            "Ultraviolet": 0,
            "Relative Humidity": 1
        }'''

        self.__uut = texthandler(fake_jsonhandler, fake_filehandler)
        self.__uut.get_id(1)
        self.__uut.Getconfig(filterdata)

    def test_filterdata_correctid(self):
        data = {
            "Temperature": 71.0,
            "Luminance": 55.0,
            "Relative Humidity": 51.0,
            "Ultraviolet": 0.0,
            "Timestamp": "2020-11-18 11:37:39.727683"
        }
        value = self.__uut.filterdata(data, 1)
        self.assertEqual(value, 1)

    def test_filterdata_wrongid(self):
        data = {
            "Temperature": 71.0,
            "Luminance": 55.0,
            "Relative Humidity": 51.0,
            "Ultraviolet": 0.0,
            "Timestamp": "2020-11-18 11:37:39.727683"
        }
        value = self.__uut.filterdata(data, 2)
        self.assertNotEqual(value, 1)

    def test_filterdata_correctfiltering(self):
        data = '''{
            "Temperature": 71.0,
            "Luminance": 55.0,
            "Relative Humidity": 51.0,
            "Ultraviolet": 0.0,
            "Timestamp": "2020-11-18 11:37:39.727683"
        }'''
        expected = {'Temperature': 71.0, 'Relative Humidity': 51.0,
                    'Timestamp': '2020-11-18 11:37:39.727683'}
        self.__uut.filterdata(data, 1)
        self.assertEqual(self.__uut.result, expected)

    def test_getconfig_changeconfig(self):
        currentfilter = {"Temperature": 1, "Time": 30, "Luminance": 0,
                         "Ultraviolet": 0, "Relative Humidity": 1}
        self.assertEqual(self.__uut.datafilter, currentfilter)
        newfilter = {"Temperature": 1, "Time": 30, "Luminance": 1,
                     "Ultraviolet": 1, "Relative Humidity": 1}
        self.__uut.Getconfig(newfilter)
        self.assertEqual(self.__uut.datafilter, newfilter)

    def test_get_id(self):
        self.assertEqual(self.__uut.id, 1)
