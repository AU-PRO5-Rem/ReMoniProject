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

from remoniproject.zwave.interfaces.interface_sensor import ISensor
from remoniproject.zwave.interfaces.interface_ozwnetwork import IOZWNetwork


class Multisensor(object):

    def __init__(self, _ISensor, _IOZWNetwork, node_id):

        self.__multisensor = _ISensor
        self.__network = _IOZWNetwork

        self.__node_id = node_id

        self.__temperature = 0.0
        self.__rel_humidity = 0.0
        self.__luminance = 0.0
        self.__ultraviolet = 0.0
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
