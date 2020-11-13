
import time

from openzwave.node import ZWaveNode
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption

from startup.start_up_functions import setup
from zwave.ozw_network_scan import OZWNetworkScanner
from zwave.class_multisensor import Multisensor
from zwave.ozw_multisensor import OZWMultisensor
from zwave.gateway_multisensor import GatewayFS

Z_STICK = "/dev/ttyACM0"
options = ZWaveOption(Z_STICK)
options.set_console_output(False)
options.set_logging(False)
options.lock()

network_obj = ZWaveNetwork(options)

sensor_list = []
sensor_list_changed = []
# Sensor lists:
#             Sensor I Node ID:       [0][0]
#             Sensor I Product Name:  [0][1]
#             Sensor II Node ID:      [1][0]
#             Sensor II Product Name: [1][1]    etc..

# Contains Node ID's for multisensors
multisensor_id = []

ozw_scanner = OZWNetworkScanner(network_obj)


def main():
    # Start-up checks
    setup()

    try:
        # Scan the ZWave network for sensors
        sensor_list = ozw_scanner.scan_ozwnetwork_for_nodes(initial=True)

        # Create Sensor objects
        multisensor_id = ozw_scanner.get_multisensor_node_ids(sensor_list)
        multisensor = [0]*(len(multisensor_id))

        for idx, node_id in enumerate(multisensor_id):
            multisensor[idx] = Multisensor(
                OZWMultisensor(node_id, network_obj), GatewayFS(node_id))

    except Exception as emsg:
        print(emsg)

        # Main Loop
    for i in range(0, 5):
        time.sleep(10.0)
        sensor_list_changed = ozw_scanner.scan_ozwnetwork_for_nodes()

        if sensor_list_changed == 0:
            print("Failed to scan Open-ZWave network!")
            continue

        # Check if sensors is added or removed from the network
        if len(sensor_list_changed) != len(sensor_list):

            print("Sensor list changed")
            # Do something
            # (eg. create or demolish multisensor object per multisensor 6)
            sensor_list = sensor_list_changed

        # TO-DO: Implement routines to:

        for idx, _ in enumerate(multisensor):
            # Get data-points from Multisensor
            if multisensor[idx].is_awake() is True:
                multisensor[idx].get_values()
                # Write Timestamped Data-points to File in /data/
                multisensor[idx].write_values_to_file()
            else:
                print("Sensor %s is sleeping" % multisensor[idx])

        # Filter Data
        # Push to MQTT


def increment(x):
    return x + 1


def decrement(x):
    return x - 1


if __name__ == "__main__":
    main()
