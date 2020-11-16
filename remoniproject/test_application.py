#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Description:    Test integration with Open-ZWave
    Dependencies:   Open-ZWave, TBD

    Hardware setup: 1.  Z-Stick Gen. 5 is plugged into an USB port
                        and Z-Stick is registered as "/dev/ttyACM0"
                        (as per default).
                    2.  Multisensor should be wired to a power source,
                        i.e. plug it into an USB port to power it,
                        or it will probably be sleeping most of the time.

"""

from zwave.multisensor import Multisensor
from zwave.ozw_multisensor import OZWMultisensor
from zwave.gateway import Gateway
from zwave.ozw_zstick import ZStick
from mqtt.mqtt_beebotte import MQTT_Client


def application():

    menu_text = """
Enter : Choice
--------------------------------------------------|
1a    : Is Sensor 1 Awake? 
2a    : Is Sensor 2 Awake? 
1v    : Show Values from Sensor 1
2v    : Show Values from Sensor 2
1w    : Write values to file, Sensor 1
2w    : Write values to file, Sensor 2
1p    : Publish values to beebotte from Sensor 1
2p    : Publish values to beebotte from Sensor 2
e     : Exit
--------------------------------------------------|
"""

    sensor_list = []

    ozw_network = ZStick()

    try:
        # Scan the ZWave network for sensors
        sensor_list = ozw_network.scan_for_nodes(initial=True)

        # Create 'Multisensor 6' objects
        multisensor_ids = ozw_network.get_multisensor_node_ids(sensor_list)

        # Add other types of Sensors here..
        # <SENSORTYPE_id> = ozw_network.get_<SENSORTPYE>_node_ids(sensor_list)

    except Exception as emsg:
        print(emsg)

    # Multisensors:
    multisensor_one = Multisensor(OZWMultisensor(7, ozw_network), Gateway(7))
    multisensor_two = Multisensor(OZWMultisensor(8, ozw_network), Gateway(8))

    # MQTT Client
    mqtt = MQTT_Client()

    mqtt.start_client()

    print("Welcome to the Demonstration of 'how to get data from two "
          "Aeotec Multisensor 6'")

    choice = 0
    while choice != "e":
        choice = input(menu_text)

        if choice == "e":
            print("Farewell")
            break

        elif choice == "1a":

            if multisensor_one.is_awake() is True:
                print("Multisensor 1 is Awake!")
            else:
                print("Multisensor 1 is Sleeping!")

        elif choice == "2a":
            if multisensor_two.is_awake() is True:
                print("Multisensor 2 is Awake!")
            else:
                print("Multisensor 2 is Sleeping!")

        elif choice == "1v":
            multisensor_one.get_values()
            print(multisensor_one.sensor_values)

        elif choice == "2v":
            multisensor_two.get_values()
            print(multisensor_two.sensor_values)

        elif choice == "1w":
            # Write values from sensor 1 to file
            multisensor_one.write_values_to_file()

        elif choice == "2w":
            # Write values from sensor 2 to file
            multisensor_two.write_values_to_file()

        elif choice == "1p":
            # Publish Values from sensor 1 to beebotte mqtt
            mqtt.publish_values(multisensor_ids)
        elif choice == "2p":
            # Publish Values from sensor 2 to beebotte mqtt
            mqtt.publish_values(multisensor_ids)

        else:
            print("Bad input!\n")


if __name__ == "__main__":
    application()
