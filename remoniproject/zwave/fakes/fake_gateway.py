#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Fake Gateway object to use for unit testing
"""

from remoniproject.zwave.interfaces.interface_gatewayfs import IGatewayFS


class FakeGatewayFS(IGatewayFS):

    def __init__(self):
        self.write_values_called = 0
        self.read_configurations_called = 0

    def write_values_to_file(self):
        self.write_values_called += 1

    def read_configuration_from_file(self):
        self.read_configuration_from_file += 1
