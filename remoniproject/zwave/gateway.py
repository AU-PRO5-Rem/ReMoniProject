#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Concrete Multisensor Gateway Object (Raspian OS/Debian OS)
    Dependencies:   Raspberry 3b (or eq) with Raspian OS (or eq)

"""

import json
from pathlib import Path

from .interfaces.i_gateway import IGateway


class Gateway(IGateway):

    def __init__(self, node_id):

        # Configuration filehandling
        self.conf_filename = ''
        self.conf_params = ''

        # Values filehandling
        self.__val_filepath = ''
        self.__vals_filename = 'sensor_vals_'+str(node_id)+'.txt'

    def __set_path_to_data(self):
        abs_path = str(Path(__file__).parent.absolute())
        path = abs_path.split("remoniproject/")[0]
        self.__val_filepath = path+'/data/'

    def write_values_to_file(self, vals):
        self.__set_path_to_data()
        filename = self.__val_filepath+self.__vals_filename
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
                self.conf_params = ifile.read()
            return True

        except Exception as emsg:
            print('Unable to read configuration! %s', emsg)
            return False
