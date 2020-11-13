#!/usr/bin/python3
# -*- coding: utf-8 -*-


class IGatewayFS():
    """
    Interface File System
    """

    def write_values_to_file(self, parameter_list):
        """
        Write sensor values to a file
        """
        raise NotImplementedError

    def read_configuration_from_file(self, parameter_list):
        """
        Read sensor configurations from a file
        """
        raise NotImplementedError
