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

from remoniproject.zwave.class_multisensor import Multisensor
from remoniproject.zwave.ozw_multisensor import OZWMultisensor


def application():

    menu_text = """
Select:
Is Sensor 1 Awake? (1a)
Is Sensor 2 Awake? (2a)
Show Values from Sensor 1 (1v)
Show Values from Sensor 2 (2v)
Write values to file, Sensor 1 (1w)
Write values to file, Sensor 2 (2w)
Exit (e)
"""

    multisensor_one = Multisensor(OZWMultisensor(7), dummy_fs())
    multisensor_two = Multisensor(OZWMultisensor(8), dummy_fs())

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
            print("TBD...")
            pass

        elif choice == "2w":
            # Write values from sensor 2 to file
            print("TBD...")
            pass

        else:
            print("Bad input!\n")


if __name__ == "__main__":
    application()
