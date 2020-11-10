#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Concrete Object
    Dependencies:   Open-ZWave, TBD

    Hardware setup: 1.  Z-Stick Gen. 5 is plugged into an USB port
                        and Z-Stick is registered as "/dev/ttyACM0"
                        (as per default).
                    2.  Multisensor should be wired to a power source,
                        i.e. plug it into an USB port to power it,
                        or it will probably be sleeping most of the time.

"""

import time

from remoniproject.zwave.interfaces.interface_ozwnetwork import IOZWNetwork


class OZWMultisensor(IOZWNetwork):

    def __init__(self, node_id):

        # The concrete Node ID
        self.__node_id = node_id

        # Options for ZWave Network
        self.__Z_STICK = "/dev/ttyACM0"
        self.__options = ZWaveOption(self.__Z_STICK)
        self.__options.set_console_output(False)
        self.__options.set_logging(False)
        self.__options.lock()

        # Network object
        self.__network = ZWaveNetwork(self.__options)

        # Node Object
        self.__zwnode = ZWaveNode(self.__node_id, self.__network)


def get_values(self):
    if self.network_is_ready is True:
        multisensor = self.__network.nodes[self.__node_id]
        multisensor.get_values()

        # Iterate through values and keep only the Readings from CMD CLASS 49
        values = {}
        new_label_data = {}
        for val in multisensor.values:
            if multisensor.values[val].command_class == 49:
                new_label_data = {
                    multisensor.values[val].label:
                    multisensor.values[val].data}
                values.update(new_label_data)

        if len(values) > 0:
            return values
        else:
            return 0
    else:
        return -1

    def network_is_ready(self):
        """
        Check if Z-Stick network is awake'n'ready
        """
        time_elapsed = 0
        for i in range(0, 60):
            if self.__network.state >= self.__network.STATE_AWAKED:
                print("\nSuccess: Z-Stick Network is Awake")
                return True
            else:
                time_elapsed += 1
                time.sleep(1.0)

        if network_obj.state < network_obj.STATE_AWAKED:
            return False

    def is_awake(self):
        """
        Check if sensor is awake
        """
        if self.__zwnode.is_awake:
            return True
        else:
            return False

    def update_configuration(self):
        """
        Send configurations to sensor
        """
        raise NotImplementedError
