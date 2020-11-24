#!/usr/bin/python3
# -*- coding: utf-8 -*-


class ISensor():
    """
    Interface Python Open-ZWave Network
    """

    def is_network_ready(self, parameter_list):
        """
        Check if Z-Stick network is awake'n'ready
        """
        raise NotImplementedError  # pragma: no cover

    def is_awake(self, parameter_list):
        """
        Check if sensor is awake
        """
        raise NotImplementedError  # pragma: no cover

    def get_values(self, parameter_list):
        """
        Get Values from Sensor(s)
        """
        raise NotImplementedError  # pragma: no cover
