
import time

from remoniproject.startup.start_up_functions import setup
from remoniproject.zwave.ozw_network_scan import scan_ozwnetwork_for_nodes

# Options for ZWave Network
Z_STICK = "/dev/ttyACM0"
options = ZWaveOption(self.__Z_STICK)
options.set_console_output(False)
options.set_logging(False)
options.lock()

# Network object
ozw_network = ZWaveNetwork(options)

sensor_list = [][]


def main():
    # Start-up
    setup()
    sensor_list = scan_ozwnetwork_for_nodes(ozw_network)

    # Main Loop
    while(1):
        time.sleep(10.0)
        sensor_list_changed = scan_ozwnetwork_for_nodes(ozw_network)
        print(sensor_list, sensor_list_changed)
        # Check if sensors is added or removed from the network
        if len(sensor_list_changed) != len(sensor_list):
            print("Sensor list changed")
            # Do something
            # (eg. create or demolish multisensor object per multisensor 6)
            sensor_list = sensor_list_changed

        # TO-DO: Implement routines to:
        # Get data
        # Write Data
        # Filter Data
        # Push to MQTT


def increment(x):
    return x + 1


def decrement(x):
    return x - 1


if __name__ == "__main__":
    main()
