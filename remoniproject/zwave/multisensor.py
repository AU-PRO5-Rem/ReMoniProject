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

    def __init__(self, ISensor, IGateway):

        self.__sensor = ISensor
        self.__gateway = IGateway
        self.sensor_values = '''
{
    "Temperature": 00.00,
    "Luminance": 00.00,
    "Relative Humidity": 00.00,
    "Ultraviolet": 00.00
}
            '''
        self.configurations = ''

    def is_awake(self):
        """
        Check if Sensor is awake
        This can take some time before Z-Stick is ready
        :return: True: Awake or False: Sleeping
        :rtype: bool
        """
        return self.__sensor.is_awake()

    def get_values(self):
        """
        Retrieve values from sensor using Open-ZWave lib
        values are stored in field 'sensor_values'
        """
        self.sensor_values = self.__sensor.get_values()

    def update_configuration(self):
        pass

    def write_values_to_file(self):
        self.__gateway.write_values_to_file(self.sensor_values)

    def read_configuration(self):
        self.__gateway.read_configuration()
