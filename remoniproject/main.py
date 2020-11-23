#!/usr/bin/python3
import time

from startup.start_up_functions import setup
# Aeotec Z-Stick Gen. 5 using Open-ZWave lib
from zwave.ozw_zstick import ZStick
# Aeotec Multisensor 6 using Open-ZWave lib
from zwave.multisensor import Multisensor
from zwave.ozw_multisensor import OZWMultisensor
from zwave.gateway import Gateway
from conf.conf_class import ConfClass
from texthandling.texthandler import texthandler
from texthandling.filehandler import filehandler
from texthandling.jsonhandler import jsonhandler

# Set how often it will re-scan ZWave network for nodes and execute main()
main_loop_time = 60.0


def main():
    # Start-up checks
    setup()

    # Create the Z-Stick object conaining the OZW network obj
    # Default constructs "/dev/ttyACM0" as zstick
    zstick = ZStick()

    # Create conf object
    conf = ConfClass()

    # Scan ZWave network for nodes and
    # save node ids to zstick.sensor_list
    # set initial=False to turn off print to std.out
    zstick.scan_for_nodes(initial=True)

    # Get node ids for all multisensors in the network
    multisensors_node_ids = zstick.get_multisensor_node_ids()

    # Initialize an empty list that can contain all Multisensors, texthandlers
    # and confs
    multisensors = [0] * (len(multisensors_node_ids))
    texthandlers = [0] * (len(multisensors_node_ids))
    confs = [0] * (len(multisensors_node_ids))

    # create/update conf files
    conf.create_confs(zstick.network, "../data")

    # Save confs in list
    for idx, node_id in enumerate(multisensors_node_ids):
        confs[idx] = conf.read_conf("ZW100_MultiSensor_6", node_id, "../data")

    # Create Multisensor object per multisensors_node_ids
    # Create a texthandler object per sensor id + id and corresponding config
    for idx, node_id in enumerate(multisensors_node_ids):
        multisensors[idx] = Multisensor(
            OZWMultisensor(node_id, zstick.network),
            Gateway(node_id))
        texthandlers[idx] = texthandler(jsonhandler, filehandler)
        texthandlers[idx].get_id(node_id)
        texthandlers[idx].Getconfig(confs[idx])

    # Implement other types of Sensors as needed:
    # 1. Implement method in 'ozw_zstick' to return
    #    node ids for a given sensor type
    #   ( like 'get_multisensor_node_ids()' )
    #    <SENSORTYPE_id> = zstick.get_<SENSORTPYE>_node_ids()
    #
    # 2. Implement Sensor class that inherites from the ISensor and,
    #    IGateway class and implement specific funtionality.
    #    All functionality is probably equivalent to functionality
    #    in ozw_multisensor.py
    #
    #  3. Implement loop that creates the needed sensor objects

    # Main Loop
    while True:

        # Get Values from each Multisensor and Write values to file
        # in ./data
        for idx, node_id in enumerate(multisensors_node_ids):
            # Get data-points from Multisensor if it is awake
            if multisensors[idx].is_awake() is True:
                # Retrive all values from the Multisensor
                multisensors[idx].get_values()
                # filter retrieved data.
                texthandlers[idx].filterdata(multisensors[idx].sensor_values,
                                             node_id)
                # Write values to sensor_vals_<node_id>.txt
                # ISO8601 Timestamp is appended as 'Timestamp: "<timestamp>"'
                multisensors[idx].write_values_to_file()
            else:
                print("Sensor %s is sleeping" % multisensors[idx])

        # Wait for main_loop_time
        time.sleep(main_loop_time)

        # Re-scan ZWave network for changes
        zstick.scan_for_nodes()

        # Create updated list of Multisensors in the network
        updated_sensor_list = zstick.get_multisensor_node_ids()

        # Compare and handle changes
        if multisensors_node_ids != updated_sensor_list:
            print("Sensor list changed!")
            # Create or pop sensor object in multisensor[]

            multisensors_node_ids = updated_sensor_list

        # create/update conf files
        conf.create_confs(zstick.network, "../data")


if __name__ == "__main__":
    main()
