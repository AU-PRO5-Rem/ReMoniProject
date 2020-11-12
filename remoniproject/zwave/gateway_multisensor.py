#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Concrete Multisensor Gateway Object (Raspian OS/Debian OS)
    Dependencies:   Raspberry 3b (or eq) with Raspian OS (or eq)

"""

from interfaces.interface_gatewayfs import IGatewayFS


class GatewayFS(IGatewayFS):
    def write_values_to_file(self):

        pass

    def read_configuration_from_file(self):

        pass
