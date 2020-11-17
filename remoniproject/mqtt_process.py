#!/usr/bin/python3

import time

from mqtt.mqtt_beebotte import MQTT_Client


def MQTT_process():
    print("Starting MQTT Process!")
    mqtt = MQTT_Client()
    multisensor_ids = [7, 8]  # This should not be hardcoded
    while True:
        if mqtt.is_running is False:
            try:
                mqtt.start_client()
                mqtt.is_running = True
                print("MQTT Client is Running!)

            except Exception as emsg:
                print(emesg)
                mqtt.is_running = False
                time.sleep(60)
                pass

        # Send Values to MQTT Broker
        try:
            mqtt.publish_values(multisensor_ids)
        except Exception as emsg:
            print(emsg)
            mqtt.is_running = False
            print("Retries to start client")

        # Wait 2 minutes
        time.sleep(120)


if __name__ == "__main__":

    MQTT_process()
