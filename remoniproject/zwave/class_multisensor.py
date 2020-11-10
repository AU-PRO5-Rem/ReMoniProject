#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Use Open-ZWave with Aeotec Z-Stick Gen. 5 and Multisensor 6
    Dependencies:   Open-ZWave, TBD

    Hardware setup: 1.  Z-Stick Gen. 5 is plugged into an USB port
                        and Z-Stick is registered as "/dev/ttyACM0"
                        (as per default).
                    2.  Multisensor should be wired to a power source,
                        i.e. plug it into an USB port to power it,
                        or it will probably be sleeping most of the time.

"""


class Multisensor(object):

    def __init__(self, _IOZWNetwork):

        self.__network = _IOZWNetwork
        self.sensor_values = '''
{
    "Temperature": 00.00,
    "Luminance": 00.00,
    "Relative Humidity": 00.00,
    "Ultraviolet": 00.00
}
            '''

    def is_awake(self):
        return self.__network.is_awake()

    def get_values(self):
        self.sensor_values = self.__network.get_values()
