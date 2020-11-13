#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Concrete Multisensor Gateway Object (Raspian OS/Debian OS)
    Dependencies:   Raspberry 3b (or eq) with Raspian OS (or eq)

"""

import json
import syslog

from .interfaces.interface_gatewayfs import IGatewayFS


class GatewayFS(IGatewayFS):

    def __init__(self, node_id):
        self.__node_id = node_id

        # Configuration filehandling
        self.conf_filename = ''
        self.conf_params_from_file = ''

        # Values filehandling
        self.__path = './data/sensor_transactions/'
        self.__vals_file = self.__path+'sensor_vals_'+str(node_id)+'.txt'

    def write_values_to_file(self, vals):
        try:
            with open(self.__vals_file, 'w') as outfile:
                json.dump(vals, outfile, indent=4)
            return True

        except Exception as emsg:
            syslog(syslog.LOG_ERR, 'Unable to write values to file!', emsg)
            return False

    def read_configuration_from_file(self):
        try:
            with open(self.__conf_filename, 'r') as ifile:
                self.conf_params_from_file = ifile.read()
            return True

        except Exception as emsg:
            syslog(syslog.LOG_ERR, 'Unable to write values!\n %s', emsg)
            return False
