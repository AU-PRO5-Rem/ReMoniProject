#!/usr/bin/python3
# -*- coding: utf-8 -*-


class IZStick():
    """
    Interface Python Open-ZWave Network
    """

    def network_is_awake(self, parameter_list):
        """
        Check if Z-Stick network is awake'n'ready
        """
        raise NotImplementedError

    def scan_for_nodes(self, parameter_list):
        """
        Search for any sensor and get its node id
        """
        raise NotImplementedError
