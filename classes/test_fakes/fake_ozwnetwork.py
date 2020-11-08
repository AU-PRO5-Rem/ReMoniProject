#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Fakes to use for unit testing
"""

from classes.interfaces.interface_ozwnetwork import IOZWNetwork
from classes.test_fakes.fake_sensordata import fake_sensor_dict


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
        return fake_sensor_dict

    def update_configuration(self):
        """
        Send configurations to sensor
        """
        raise NotImplementedError
