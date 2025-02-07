#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Concrete Multisensor Open-ZWave Object
    Dependencies:   Python Open-ZWave, Aeotec Z-Stick gen.5 and Multisensor 6

    Hardware setup: 1.  Z-Stick Gen. 5 is plugged into an USB port
                        and Z-Stick is registered as "/dev/ttyACM0"
                        (as per default).
                    2.  Multisensor should be wired to a power source,
                        i.e. plug it into an USB port to power it,
                        or it will probably be sleeping most of the time.

"""

import time
from datetime import datetime

from .interfaces.i_sensor import ISensor
from openzwave.node import ZWaveNode


class OZWMultisensor(ISensor):

    def __init__(self, node_id, OZWNetwork_obj):

        # The concrete Node ID
        self.__node_id = node_id

        # Open-ZWave Network object injection
        self.__network = OZWNetwork_obj

        # Node Object
        self.__zwnode = ZWaveNode(self.__node_id, self.__network)

    def get_values(self):
        """
        Retrieve values from the ZWave network node associated with this
        Multisensor object. It will Perform af Refresh_info() to ensure
        that the values are the latest registered by the sensor.
        If OK, then values are returned, else if it fails
        to retrieve the values an error code is returned:

        -1 : network is not ready
         0 : no values was returned by the sensor

        :return: dict or int errorcode

        :rtype: dict or int
        """
        if self.network_is_ready() is True:
            multisensor = self.__network.nodes[self.__node_id]
            multisensor.refresh_info()
            multisensor.get_values()

            # Iterate through values and keep the Readings from CMD CLASS 49
            stored_vals = {}
            new_val = {}

            for val in multisensor.values:
                if multisensor.values[val].command_class == 49:
                    new_val = {
                        multisensor.values[val].label:
                        multisensor.values[val].data}
                    stored_vals.update(new_val)

            if len(stored_vals) > 0:
                stored_vals = self.__add_timestamp(stored_vals)
                return stored_vals
            else:
                # No values gathered. Possibly due to an unknown error
                return 0

        # Network is not ready return -1
        else:
            return -1

    def network_is_ready(self):
        """
        Check if Z-Stick network is awake'n'ready
        Can take up to 60s

        :return: True (Awake) / False (Sleeping)

        :rtype: bool
        """
        time_elapsed = 0
        for i in range(0, 60):
            if self.__network.state >= self.__network.STATE_AWAKED:
                return True
            else:
                time_elapsed += 1
                time.sleep(1.0)

        if self.__network.state < self.__network.STATE_AWAKED:
            return False

    def is_awake(self):
        """
        Check if Sensor is awake

        :return: True (Awake) / False (Sleeping)

        :rtype: bool
        """
        if self.network_is_ready():
            if self.__zwnode.is_awake:
                return True
        else:
            return False

    # Support functions

    def __make_timestamp(self):
        """
        Make ISO8601 Timestamp

        :return: ISO 8601 Timestamp
        :rtype: String
        """
        timestamp = datetime.now()
        timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        return str(timestamp)

    def __add_timestamp(self, vals_dict):
        """
        Append timestamp to dictionary with sensor values

        :param vals_dict: sensor_values
        :type vals_dict: dict
        :return: sensor_values with timestamp entry
        :rtype: dict
        """
        timestamp = self.__make_timestamp()
        try:
            new_timestamp = {"Timestamp": timestamp}
            # Apply timestamp to sensor_values
            vals_dict.update(new_timestamp)
            return vals_dict

        except Exception as emsg:
            print('Unable to add timestamp!', emsg)
            return False
