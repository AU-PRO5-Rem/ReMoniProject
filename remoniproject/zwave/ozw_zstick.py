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
import logging

from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
from .interfaces.i_zstick import IZStick


class ZStick(IZStick):

    def __init__(self, z_stick="/dev/ttyACM0"):
        logging.basicConfig(
            filename='zstick.log',
            format=('%(asctime)s %(levelname)s:%(message)s'),
            level=logging.INFO
        )
        # Options for ZWave Network
        options = ZWaveOption(z_stick)
        options.set_console_output(False)
        options.set_logging(False)
        options.lock()

        # Open-ZWave Network object
        self.network = ZWaveNetwork(options)
        self.sensor_list = 0

    def network_is_awake(self, timeout=60):
        """Check if state of network is Awake

        :param self.network: initialized network object
        :param timeout: set max time to wait for awake state
        :type self.network: ZWaveNetwork Object
        :return: True or False
        :rtype: bool
        """

        time_elapsed = 0
        print("Waiting for ZWave Network")
        logging.INFO("ZStick: Waiting for ZWave Network Awake State")
        for i in range(0, timeout):
            if self.network.state >= self.network.STATE_AWAKED:
                logging.INFO("ZStick: Awake after %d seconds" % i)
                return True
            else:
                if i % 2 == 0:
                    print('/', end="\r")
                else:
                    print('\\', end="\r")
                time_elapsed += 1
                time.sleep(1.0)

        if self.network.state < self.network.STATE_AWAKED:
            logging.INFO("ZStick: Timeout waiton for Awake State, Time set %d"
                         timeout % )
            return False

    def scan_for_nodes(self, initial=False):
        """get node ids for any sensors [summary]

        :param self.network: [description]
        :type self.network: [type]
        :return: [description]
        :rtype: [type]
        """
        sensor_list = []
        sensor_node_id = 0
        sensor_type = ''

        try:
            if self.zwave_network_is_awake() is True:

                for node in self.network.nodes:
                    sensor_node_id = self.network.nodes[node].node_id
                    sensor_type = self.network.nodes[node].product_name
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
            self.sensor_list = sensor_list

    def get_multisensor_node_ids(self, sensor_list):

        multisensor_node_ids = []

        for col1, _ in enumerate(self.sensor_list):
            for col2, _ in enumerate(self.sensor_list):
                if self.sensor_list[col1][col2] == 'ZW100 MultiSensor 6':
                    multisensor_node_ids.append(self.sensor_list[col1][0])
        if multisensor_node_ids is not None:
            return multisensor_node_ids
        else:
            return -1
