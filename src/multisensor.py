#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
    Description:    Use Open-ZWave with Aeotec Z-Stick Gen. 5 and Multisensor 6
    Dependencies:   Open-ZWave, TBD

    Hardware setup: 1.  Z-Stick Gen. 5 is plugged into an USB port
                        and Z-Stick is registered as "/dev/ttyACM0"
                        (as per default).
                    2.  Multisensor should be wired to a power source,
                        i.e. plug it into an USB port to power it,
                        or it will probably be sleeping most of the time.

'''
import sys

from openzwave.node import ZWaveNode
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption

import time

# Aotec Gen.5 Stick should be known as USB ACM Device (ttyACM0) by default
# Note: Earlier model of Z-Stick would be known as ttyUSB0 but USE ttyACM0
# Test: dmesg | grep ttyACM0
Z_STICK = "/dev/ttyACM0"

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

print("Waiting for Z-Stick Network to be awake")

time_elapsed = 0
for i in range(0, 300):
    if network.state >= network.STATE_AWAKED:
        print("Success: Z-Stick Network is Awake")
        break
    else:
        time_elapsed += 1
        time.sleep(1.0)

        # Write to display to indicate that network is still sleeping
        if (i % 2 == 0):
            sys.stdout.write("zz")
        else:
            sys.stdout.write("Z")
        sys.stdout.flush()

if network.state < network.STATE_AWAKED:
    print(":-(")
    print("Network is not awake but continue anyway")


def zwave_network_scan():
    """Performs a complete scan for network nodes
        and print all information
    """
    print("Network home id : {}".format(network.home_id_str))
    print("Controller node id : {}".format(
        network.controller.node.node_id))
    print("Controller node version : {}".format(
        network.controller.node.version))
    print("Nodes in network : {}".format(network.nodes_count))
    for node in network.nodes:
        print("------------------------------------------------------------")
        print(
            "{} - Name : {}".format(network.nodes[node].node_id, network.nodes[node].name))
        print("{} - Manufacturer name / id : {} / {}".format(
            network.nodes[node].node_id, network.nodes[node].manufacturer_name, network.nodes[node].manufacturer_id))
        print("{} - Product name / id / type : {} / {} / {}".format(
            network.nodes[node].node_id, network.nodes[node].product_name, network.nodes[node].product_id, network.nodes[node].product_type))
        print(
            "{} - Version : {}".format(network.nodes[node].node_id, network.nodes[node].version))
        print("{} - Command classes : {}".format(
            network.nodes[node].node_id, network.nodes[node].command_classes_as_string))
        print("{} - Capabilities : {}".format(
            network.nodes[node].node_id, network.nodes[node].capabilities))
        print(
            "{} - Neigbors : {}".format(network.nodes[node].node_id, network.nodes[node].neighbors))
        print(
            "{} - Can sleep : {}".format(network.nodes[node].node_id, network.nodes[node].can_wake_up()))


def get_all_multisensors_node_ids(network):
    """Look for multisensor(s) in the ZWave network
        to retrieve the node id of all "multisensor 6" that is found
        If no multisensor is found, the returned value is -1

    :param network: initialized network object
    :type network: ZWaveNetwork Object
    :return: Array of Sensors IDs
    :rtype: [int]
    """
    sensor_id = []

    for node in network.nodes:
        if "MultiSensor 6" in network.nodes[node].product_name:
            sensor_id.append(network.nodes[node].node_id)
    if len(sensor_id) > 0:
        return sensor_id
    else:
        return -1


def is_multisensor_awake(sensor_id, network):
    """Checks if a multisensor 6 is awake (True) or
    sleeping (False)

    :param sensor_id: network.nodes.node_id
    :type sensor_id: netowrk object
    :param network: node id
    :type network: OpenZWave Network object
    :return: Bool, Node_id
    :rtype: Bool, Int
    """
    multisensor = ZWaveNode(sensor_id, network)
    if multisensor.is_awake:
        return True, sensor_id
    else:
        return False, sensor_id


if __name__ == "__main__":

    # zwave_network_scan()

    multisensors_node_ids = get_all_multisensors_node_ids(network)

    for idx, nodeid in enumerate(multisensors_node_ids):
        multisensor_is_awake = is_multisensor_awake(nodeid, network)

        if multisensor_is_awake:
            print("Multisensor with node ID %d is Awake" % nodeid)
        else:
            print("Multisensor with node ID %d is Sleeping" % nodeid)
    pass
