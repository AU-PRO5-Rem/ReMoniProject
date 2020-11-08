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


from abstract_classes import ISensor
from abstract_classes import IOZWNetwork


class Multisensor(ISensor, IOZWNetwork):

    def __init__(self, ISensor, IOZWNetwork, node_id):

        self.__multisensor = ISensor
        self.__network = IOZWNetwork

        self.__node_id = node_id

        self.__temperature = 0
        self.__humidity = 0
        self.__luminous = 0

    def is_awake(self):
        return self.__network.is_awake()
