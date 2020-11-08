#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Fakes to use for unit testing
"""

from abstract_classes import IOZWNetwork


class fake_network(IOZWNetwork):

    def __init__(self):
        self.status_is_awake = False

    def is_network_ready(self):
        raise NotImplementedError

    def is_awake(self):
        """
        Check if 
        """
        return self.status_is_awake