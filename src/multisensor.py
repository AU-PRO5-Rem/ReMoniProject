#!/bin/env python
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
options.set_console_output(True)
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

if __name__ == "__main__":
    print("This should be called from main.py")
    pass
