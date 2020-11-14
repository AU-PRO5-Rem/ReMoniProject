#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
    Description:    Use Open-ZWave with Aeotec Z-Stick Gen. 5 and Multisensor 6
    Dependencies:   Open-ZWave, TBD

    Hardware setup: 1.  Z-Stick Gen. 5 is plugged into an USB port
                        and Z-Stick is registered as "/dev/ttyACM0"
                        (as per default).
                    2.  Multisensor should be wired to a power source,
                        i.e. plug it into an USB port to power it,
                        or it will probably be sleeping most of the time.

"""

import time
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption

def setup_open_zwave_network(z_stick="/dev/ttyACM0"):
    options = ZWaveOption(z_stick)
    options.set_console_output(False)
    options.set_logging(False)
    options.lock()

    network_obj = ZWaveNetwork(options)
    return network_obj

class OZWNetworkScanner():

    def __init__(self, OZWNetwork_obj):

        # Options for ZWave Network

        # Open-ZWave Network object injection
        self.__network = OZWNetwork_obj

    def zwave_network_is_awake(self):
        """Check if state of network is Awake

        :param self.__network: initialized network object
        :type self.__network: ZWaveNetwork Object
        :return: True or False
        :rtype: bool
        """

        time_elapsed = 0
        print("Waiting for ZWave Network")
        for i in range(0, 60):
            if self.__network.state >= self.__network.STATE_AWAKED:
                return True
            else:
                if i % 2 == 0:
                    print('/', end="\r")
                else:
                    print('\\', end="\r")
                time_elapsed += 1
                time.sleep(1.0)

        if self.__network.state < self.__network.STATE_AWAKED:
            return False

    def scan_ozwnetwork_for_nodes(self, initial=False):
        """get_multisensors_node_ids [summary]

        :param self.__network: [description]
        :type self.__network: [type]
        :return: [description]
        :rtype: [type]
        """
        sensor_list = []
        sensor_node_id = 0
        sensor_type = ''

        try:
            if self.zwave_network_is_awake() is True:

                for node in self.__network.nodes:
                    sensor_node_id = self.__network.nodes[node].node_id
                    sensor_type = self.__network.nodes[node].product_name
                    # Ignore the USB Z-Stick
                    if 'Z-Stick' not in sensor_type:
                        sensor_list.append([sensor_node_id, sensor_type])
                        if initial is True:
                            print("Found Sensor with node id: %s of type: %s" %
                                  (sensor_node_id, sensor_type))
        except Exception as emsg:
            print(emsg)
            sensor_list = 0
        finally:
            return sensor_list

    def get_multisensor_node_ids(self, sensor_list):

        multisensor_node_ids = []

        for col1, _ in enumerate(sensor_list):
            for col2, _ in enumerate(sensor_list):
                if sensor_list[col1][col2] == 'ZW100 MultiSensor 6':
                    multisensor_node_ids.append(sensor_list[col1][0])
        return multisensor_node_ids
