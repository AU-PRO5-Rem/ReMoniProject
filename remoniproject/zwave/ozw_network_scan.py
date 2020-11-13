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
import sys
import json
import time

from openzwave.node import ZWaveNode
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption


# Aotec Gen.5 Stick should be known as USB ACM Device (ttyACM0) by default
# Note: Earlier model of Z-Stick would be known as ttyUSB0 but USE ttyACM0
# Test: dmesg | grep ttyACM0
Z_STICK = "/dev/ttyACM0"


def zwave_network_is_awake(network_obj):
    """Check if state of network is Awake

    :param network_obj: initialized network object
    :type network_obj: ZWaveNetwork Object
    :return: True or False
    :rtype: bool
    """
    time_elapsed = 0
    for i in range(0, 60):
        if network_obj.state >= network_obj.STATE_AWAKED:
            return True
        else:
            time_elapsed += 1
            time.sleep(1.0)

    if network_obj.state < network_obj.STATE_AWAKED:
        return False


def scan_ozwnetwork_for_nodes(network_obj):
    """get_multisensors_node_ids [summary]

    :param network_obj: [description]
    :type network_obj: [type]
    :return: [description]
    :rtype: [type]
    """
    sensor_list = [][]
    sensor_node_id = 0
    sensor_type = ''

    if zwave_network_is_awake() is True:

        for node in network_obj.nodes:
            sensor_node_id = network_obj.nodes[node].node_id
            sensor_type = network_obj.nodes[node].product_name
            sensor_list.append([sensor_node_id, sensor_type])
            return sensor_list
    else:
        return false


if __name__ == "__main__":
    ''' Running this script as main will perform the following:
        1. Set logging options
        2. Initialize a Network object with options
        3. Check if Z-Stick ZWave network is awake
        4. Collect node ids for all Multisensors in network
        5. Check if multisensors are Awake or Sleeping '''
    # Set some options for ZWave, logging to file etc.
    options = ZWaveOption(Z_STICK)
    options.set_log_file("OpenZWave_Log.log")
    options.set_append_log_file(False)
    options.set_save_log_level("Debug")
    options.set_console_output(False)
    options.set_logging(True)
    options.lock()

    # Create network object
    network = ZWaveNetwork(options)

    # Check is Z-Stick ZWave Network Awake
    is_zwave_network_awake(network)
    print("Do you want to perform a Z-Wave network scan? y/n")
    if (input == "y"):
        zwave_network_scan(network)

    # Collect node IDs for alle Multisensors in the Network
    # (Any other sensor type is ignored)
    multisensors_node_ids = get_multisensors_node_ids(network)

    # Check each Multisensor if it is awake (Show case)
    for idx, nodeid in enumerate(multisensors_node_ids):
        multisensor_is_awake = is_multisensor_awake(nodeid, network)

        # Multisensor_is_awake [State, nodeid]
        if multisensor_is_awake[0]:
            print("Multisensor with node ID %d is Awake" %
                  multisensor_is_awake[1])
            try:
                temp = get_temperature(nodeid, network)
                print(temp)
            except Exception as e:
                print("Failed to get data from Sensor")
                print(e)

        else:
            print("Multisensor with node ID %d is Sleeping" %
                  multisensor_is_awake[1])
