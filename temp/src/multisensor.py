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


def is_zwave_network_awake(network_obj):
    """Check if state of network is Awake

    :param network_obj: initialized network object
    :type network_obj: ZWaveNetwork Object
    :return: True or False
    :rtype: bool
    """
    print("Waiting for Z-Stick Network to be awake")
    time_elapsed = 0
    for i in range(0, 60):
        if network_obj.state >= network_obj.STATE_AWAKED:
            print("\nSuccess: Z-Stick Network is Awake")
            return True
        else:
            time_elapsed += 1
            time.sleep(1.0)

            # Write to display to indicate that network is still sleeping
            if i % 2 == 0:
                sys.stdout.write("zz")
            else:
                sys.stdout.write("Z")
            sys.stdout.flush()

    if network_obj.state < network_obj.STATE_AWAKED:
        print("\nError: Network could not wake up!")
        return False


def zwave_network_scan(network_obj):
    """ Performs a complete scan for network nodes
        and print all information.
        Primarily for Debug and Test use
    """
    network = network_obj
    print("Network home id : {}".format(network.home_id_str))
    print("Controller node id : {}".format(
        network.controller.node.node_id))
    print("Controller node version : {}".format(
        network.controller.node.version))
    print("Nodes in network : {}".format(network.nodes_count))
    for node in network.nodes:
        print("---------------------------------------")
        print(
            "{} - Name : {}".format(network.nodes[node].node_id,
                                    network.nodes[node].name))
        print("{} - Manufacturer name / id : {} / {}".format(
            network.nodes[node].node_id,
            network.nodes[node].manufacturer_name,
            network.nodes[node].manufacturer_id))
        print("{} - Product name / id / type : {} / {} / {}".format(
            network.nodes[node].node_id,
            network.nodes[node].product_name,
            network.nodes[node].product_id,
            network.nodes[node].product_type))
        print(
            "{} - Version : {}".format(network.nodes[node].node_id,
                                       network.nodes[node].version))
        print("{} - Command classes : {}".format(
            network.nodes[node].node_id,
            network.nodes[node].command_classes_as_string))
        print("{} - Capabilities : {}".format(
            network.nodes[node].node_id, network.nodes[node].capabilities))
        print(
            "{} - Neigbors : {}".format(network.nodes[node].node_id,
                                        network.nodes[node].neighbors))
        print(
            "{} - Can sleep : {}".format(network.nodes[node].node_id,
                                         network.nodes[node].can_wake_up()))


def get_multisensors_node_ids(network_obj):
    """Look for multisensor(s) in the ZWave network
        to retrieve the node id of all "multisensor 6" that is found
        If no multisensor is found, the returned value is -1

    :param network_obj: initialized network object
    :type network_obj: ZWaveNetwork Object
    :return: Array of Sensors IDs (node id) or
             -1 if no Multisensors are found
    :rtype: [int]
    """
    sensor_id = []

    for node in network_obj.nodes:
        if "MultiSensor 6" in network_obj.nodes[node].product_name:
            sensor_id.append(network_obj.nodes[node].node_id)
    if len(sensor_id) > 0:
        return sensor_id
    else:
        return -1


def is_multisensor_awake(sensor_id, network_obj):
    """Checks if a multisensor 6 is awake (True) or
    sleeping (False)

    :param sensor_id: network.nodes.node_id
    :type sensor_id: int
    :param network_obj: network object
    :type network_obj: OpenZWave Network object
    :return: True or False
    :rtype: Bool
    """
    multisensor = ZWaveNode(sensor_id, network_obj)
    if multisensor.is_awake:
        return True, sensor_id
    else:
        return False, sensor_id


def get_all_data(sensor_id, network_obj):
    multisensor = network_obj.nodes[sensor_id]

    values = {}
    for cmd in multisensor.command_classes:
        print("Command: ", cmd)
        for val in multisensor.get_values_for_command_class(cmd):
            values = {}
            values[multisensor.values[val].object_id] = {
                'label': multisensor.values[val].label,
                'help': multisensor.values[val].help,
                'max': multisensor.values[val].max,
                'min': multisensor.values[val].min,
                'units': multisensor.values[val].units,
                'data': multisensor.values[val].data,
                'data_str': multisensor.values[val].data_as_string,
                'genre': multisensor.values[val].genre,
                'type': multisensor.values[val].type,
                'ispolled': multisensor.values[val].is_polled,
                'readonly': multisensor.values[val].is_read_only,
                'writeonly': multisensor.values[val].is_write_only,
            }
            # if values is not None:
            # print(values)


def get_temperature(sensor_id, network_obj):
    multisensor = network_obj.nodes[sensor_id]
    multisensor.get_values()
    values = {}

    for value in multisensor.values:
        if multisensor.values[value].label == 'Temperature':
            values = {'Temperature': multisensor.values[value].data}
    return values


def get_values(sensor_id, network_obj):
    multisensor = network_obj.nodes[sensor_id]
    multisensor.get_values()

    # Iterate through values and keep only the Readings from CMD CLASS 49
    values = {}
    new_label_data = {}
    for val in multisensor.values:
        if multisensor.values[val].command_class == 49:
            new_label_data = {
                multisensor.values[val].label: multisensor.values[val].data}
            values.update(new_label_data)

    if len(values) > 0:
        return json.dumps(values)


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