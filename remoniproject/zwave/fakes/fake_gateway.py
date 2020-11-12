#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Fake Gateway object to use for unit testing
"""

from remoniproject.zwave.interfaces.interface_gatewayfs import IGatewayFS


class FakeGatewayFS(IGatewayFS):
    def write_values_to_file(self):

        pass

    def read_configuration_from_file(self):

        pass
