#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Concrete Multisensor Gateway Object (Raspian OS/Debian OS)
    Dependencies:   Raspberry 3b (or eq) with Raspian OS (or eq)

"""

import json
from pathlib import Path

from .interfaces.interface_gatewayfs import IGatewayFS


class GatewayFS(IGatewayFS):

    def __init__(self, node_id):
        self.__node_id = node_id

        # Configuration filehandling
        self.conf_filename = ''
        self.conf_params_from_file = ''

        # Values filehandling
        self.__path = ''
        self.__vals_file = 'sensor_vals_'+str(node_id)+'.txt'

    def set_path_to_data(self):
        abs_path = str(Path(__file__).parent.absolute())
        path = abs_path.split("remoniproject/")[0]
        self.__path = path+'/data/'

    def write_values_to_file(self, vals):
        self.set_path_to_data()
        filename = self.__path+self.__vals_file
        try:
            with open(filename, 'w') as outfile:
                json.dump(vals, outfile, indent=4)
            return True

        except Exception as emsg:
            print('Unable to write values! %s', emsg)
            pass
            return False

    def read_configuration_from_file(self):
        try:
            with open(self.__conf_filename, 'r') as ifile:
                self.conf_params_from_file = ifile.read()
            return True

        except Exception as emsg:
            print('Unable to read configuration! %s', emsg)
            return False
