#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Fakes to use for unit testing
"""

from remoniproject.zwave.interfaces.interface_ozwnetwork import IOZWNetwork


class fake_ozwnetwork(IOZWNetwork):

    def __init__(self):
        self.status_is_awake = False

    def is_network_ready(self):
        raise NotImplementedError

    def is_awake(self):
        """
        Check if sensor is awake
        """
        return self.status_is_awake

    def get_values(self):
        """
        Get Values from Sensor(s)
        """
        fake_values_dict = '''
{
    "Temperature": 12.34,
    "Luminance": 12.34,
    "Relative Humidity": 12.34,
    "Ultraviolet": 12.34
}
'''
        return fake_values_dict

    def update_configuration(self):
        """
        Send configurations to sensor
        """
        raise NotImplementedError
