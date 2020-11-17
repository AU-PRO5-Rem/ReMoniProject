#!/usr/bin/python3

import thread

from main import main
from mqtt_process import MQTT_process

# Create Main and MQTT Process
try:
    thread.start_new_thread(main, ())
    thread.start_new_thread(MQTT_process, ())
except Exception as emsg:
    print(emsg)

while True:
    # Just let the threads run
    pass
