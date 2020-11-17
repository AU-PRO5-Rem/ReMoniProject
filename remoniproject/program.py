#!/usr/bin/python3

from threading import Thread

from main import main
from mqtt_process import MQTT_process

mp = Thread(None, main)
mq = Thread(None, MQTT_process)
# Create Main and MQTT Process
try:
    print("Starting threads")
    mp.start()
    mq.start()

except Exception as emsg:
    print(emsg)

while True:
    # Just let the threads run
    pass
