#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Abstract classes for ReMoni 3rd-part Sensors Project
"""


#
class ISensor():
    """

    """

    def is_awake(self, parameter_list):
        """
        Probe if sensor is awake
        """
        raise NotImplementedError

    def get_sensor_values(self, parameter_list):
        """
        Retrive all values and store them as dict or string
        """
        raise NotImplementedError

    def configure_sensor(self, parameter_list):
        """
        send configurations to sensor. Return int error_code
        error_codes: see Documentation
        """
        raise NotImplementedError


class IOZWNetwork():
    """
    Interface for Aeotec Multisensor 6
    """

    def is_network_ready(self, parameter_list):
        """
        Check if Z-Stick network is awake'n'ready
        """
        raise NotImplementedError

    def is_awake(self, parameter_list):
        """
        Check if 
        """
        raise NotImplementedError