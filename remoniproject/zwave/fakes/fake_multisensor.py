#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Fake open-zwave object to use for unit testing
"""

from remoniproject.zwave.interfaces.i_sensor import ISensor


class FakeMultisensor(ISensor):

    def __init__(self):
        self.status_is_awake = False

    def is_network_ready(self):
        raise NotImplementedError  # pragma no cover

    def is_awake(self):
        """
        Check if sensor is awake
        """
        return self.status_is_awake

    def get_values(self):
        """
        Get Values from Sensor(s)
        """
        fake_values_dict = '''{
            "Temperature": 12.34,
            "Luminance": 12.34,
            "Relative Humidity": 12.34,
            "Ultraviolet": 12.34,
            "Timestamp":"2020-11-12 23:25:05.684056"
            }'''
        return fake_values_dict

    def update_configuration(self):
        """
        Send configurations to sensor
        """
        raise NotImplementedError  # pragma: no cover
