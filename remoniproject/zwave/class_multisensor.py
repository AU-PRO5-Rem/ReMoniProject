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

from datetime import datetime


class Multisensor(object):

    def __init__(self, IOZWNetwork, IGatewayFS):

        self.__network = IOZWNetwork
        self.__gateway = IGatewayFS
        self.sensor_values = '''
{
    "Temperature": 00.00,
    "Luminance": 00.00,
    "Relative Humidity": 00.00,
    "Ultraviolet": 00.00
}
            '''

    def is_awake(self):
        """
        Check if Sensor is awake
        This can take some time before Z-Stick is ready
        :return: True: Awake or False: Sleeping
        :rtype: bool
        """
        return self.__network.is_awake()

    def get_values(self):
        """
        Retrieve values from sensor using Open-ZWave lib
        values are stored in field 'sensor_values'
        """
        self.sensor_values = self.__network.get_values()
        self.__add_timestamp()

    def update_configuration(self):
        pass

    def write_values_to_file(self):
        self.__gateway.write_values_to_file()

    def read_configuration_from_file(self):
        self.__gateway.read_configuration_from_file()

    def __add_timestamp(self):
        new_val = {}
        try:
            timestamp = timestamp(datetime.now(timezone.utc))
            new_val = {"Timestamp": timestamp}
            self.sensor_values.update(new_val)
            return True
        except Exception as emsg:
            syslog(syslog.LOG_ERR, 'Unable to add timestamp to file!\n %s', emsg)
            return False
