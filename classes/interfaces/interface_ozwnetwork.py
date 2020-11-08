#!/usr/bin/python3
# -*- coding: utf-8 -*-


class IOZWNetwork():
    """
    Interface Python Open-ZWave Network
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
