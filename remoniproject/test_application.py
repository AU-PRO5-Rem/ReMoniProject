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

from remoniproject.zwave.ozw_multisensor import OZWMultisensor
from temp.classes import Multisensor
from remoniproject.zwave.interfaces.interface_sensor import ISensor


def application():
    multisensor_one = OZWMultisensor(7)
    multisensor_two = OZWMultisensor(8)
    dummy_sensor = ISensor()

    multisensor_one_c = Multisensor(dummy_sensor, multisensor_one, 7)
    multisensor_two_c = Multisensor(dummy_sensor, multisensor_two, 8)

    if multisensor_one.is_awake:
        print("Multisensor One is Awake")
    else:
        print("Multisensor One is not Awake")

    if multisensor_two.is_awake:
        print("Multisensor Two is Awake")
    else:
        print("Multisensor Two is not Awake")
