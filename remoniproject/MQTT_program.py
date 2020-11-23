"""
The "main" MQTT program.

This client program will run in the background, to enable a constant MQTT
connection, to an MQTT broker.
In this program it will be connected to our own rented MQTT broker (beebotte),
so it's possible to do extended test's,
where in reality it will be changed to Remonis own MQTT client and broker.
"""
# Rest of imports
import logging
import paho.mqtt.client as mqtt
# Used for sleeping function (although it's kinda irrelevant,
# and can be done in other ways)
import time
import json
import os
import fcntl
from conf.conf_class import ConfClass


# Path settings (is gonna change in the final setup)
path_to_val = ""  # path to sensor and ID value's txt's
path_to_conf = "../conf_tests"  # path to conf class file


# ------------------------- Logging setup ----------------------------------- #
def MQTT_logging_setup():
    # File for logging
    logging.basicConfig(
        filename='MQTT.log',
        format='%(asctime)s %(levelname)s:%(message)s',
        level=logging.INFO
    )


# --------------------------------------------------------------------------- #
# Callback definitions
# it's possible to create a callback function,
# so when a certain function is done or "accomplished", it will call these
# functions, and execute the definition code.
def on_connect(client, userdata, flags, rc):
    logging.info("MQTT: Connection establed and returned with result code:"
                 + str(rc))
    mqtt_client.subscribe("mqtt_test/Filter", 0)
    mqtt_client.subscribe("mqtt_test/SensorPair", 0)
    # mqtt_client.subscribe("mqtt_test/FIFO", 0)  # used for debugging

    # Read values from FIFO file, if there's any content
    if os.path.isfile("FIFO.txt"):
        if os.stat("FIFO.txt").st_size != 0:
            with open("FIFO.txt", "r") as FIFO_fd:
                lock = 0
                while lock != 1:
                    try:
                        fcntl.flock(FIFO_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        lock = 1
                    except IOError:
                        lock = 0
                # Load old FIFO values
                FIFO_dict = json.load(FIFO_fd)
                fcntl.flock(FIFO_fd, fcntl.LOCK_UN)

            FIFO_dict = str(FIFO_dict).replace("'", '"')
            publish_string = '{"data":' + str(FIFO_dict) + ',"write":true}'
            mqtt_client.publish("mqtt_test/FIFO", publish_string, 1)
            logging.info("MQTT: FIFO content sent to broker")
            # os.remove("FIFO.txt")


def on_disconnect(client, userdata, rc):
    logging.info("MQTT: Disconnection returned result:" + str(rc) + " ")

    # FIFO in case of connection loss
    # Read current sensor vals from sensor_filtered_val_x files
    sensor_vals_list = read_sensor_vals()

    FIFO_dict = {}

    # Read values from FIFO file, or create one if not existing
    if os.path.isfile("FIFO.txt"):
        if os.stat("FIFO.txt").st_size != 0:
            e_check = 1
        else:
            e_check = 0
    else:
        e_check = 0

    if e_check == 1:
        with open("FIFO.txt", "r") as FIFO_fd:
            lock = 0
            while lock != 1:
                try:
                    fcntl.flock(FIFO_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    lock = 1
                except IOError:
                    lock = 0
            # Load old FIFO values
            FIFO_dict = json.load(FIFO_fd)
            fcntl.flock(FIFO_fd, fcntl.LOCK_UN)

    with open("FIFO.txt", "w") as FIFO_fd:
        lock = 0
        while lock != 1:
            try:
                fcntl.flock(FIFO_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                lock = 1
            except IOError:
                lock = 0
        # Update FIFO
        FIFO_dict[time.ctime()] = sensor_vals_list
        # Insert updated FIFO
        json.dump(FIFO_dict, FIFO_fd, indent=4)
        fcntl.flock(FIFO_fd, fcntl.LOCK_UN)

    time.sleep(Timer)


def on_filter_message(client, userdata, msg):
    """
    If necessary it's possible to have individual callbacks for topics,
    instead of 1 collective.
    could be necessary whit multiple sensors,
    function for this is "message_callback_add()"

    example of a recieved JSON string:
    {"Time":30,"7":{ "Temperature":1},"8":{"Temperature":1}}

    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    # Path correction
    o_path = os.getcwd()  # old path
    if path_to_val != "":
        os.chdir(path_to_val)  # new path
    with open("sensor_ids.txt", "r") as sensor_ids_fd:
        lock = 0
        while lock != 1:
            try:
                fcntl.flock(sensor_ids_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                lock = 1
            except IOError:
                lock = 0
        sensor_ids = json.load(sensor_ids_fd)
        fcntl.flock(sensor_ids_fd, fcntl.LOCK_UN)
    os.chdir(o_path)  # Return to old path

    # Load and decode filter message (std. paho msg format is binary)
    msg.payload = msg.payload.decode("utf-8")
    filter_msg = str(msg.payload)  # to avoid pyton int format errors
    filter_msg = json.loads(filter_msg)

    # Dict for new configuration values
    new_vals = {}  # place holder?
    time_val = {}  # place holder?

    # Create conf class, so conf functions can be used
    conf = ConfClass()

    # Looping through the recieved message
    for msg_objects in filter_msg:
        if msg_objects == "data":
            for data_objects in filter_msg[msg_objects]:
                # "Time" values
                if data_objects == "Time":
                    time_val[data_objects] = \
                        filter_msg[msg_objects][data_objects]
                    for ids in sensor_ids:
                        conf.update_conf(sensor_ids[ids], ids, time_val,
                                         path_to_conf)
                # Sensor values
                else:
                    new_vals = filter_msg[msg_objects][data_objects]
                    conf.update_conf(sensor_ids[data_objects], data_objects,
                                     new_vals, path_to_conf)

    # Log recieved info
    logging.info("MQTT: recieved " + str(msg.topic) +
                 " message" + " : " + str(filter_msg["data"]))


def on_SensorPair_message(client, userdata, msg):
    """
    callback used to set dongle into pairing mode,
    although it's not implemented, it's been set up for possible future
    function implementation.

    example of a recieved JSON string: {"Pair_sensor":1}

    :param client:
    :param userdata:
    :param msg:
    :return:
    """

    # Load and decode filter message (std. paho msg format is binary)
    msg.payload = msg.payload.decode("utf-8")
    filter_msg = str(msg.payload)  # to avoid pyton int format errors
    filter_msg = json.loads(filter_msg)
    filter_msg = filter_msg["data"]

    logging.info("MQTT: Call recieved to set dongle into pairing mode | "
                 "msg recieved: " + str(filter_msg))


def on_FIFO_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    # to avoid pyton int format errors
    filter_msg = str(msg.payload).replace("'", '"')
    filter_msg = json.loads(filter_msg)
    filter_msg = filter_msg["data"]
    logging.info("MQTT_debugging: FIFO recieved: " + str(filter_msg))


# --------------------------------------------------------------------------- #
# Non callback functions
def read_sensor_vals():
    vals_dict = {}

    # Path correction
    o_path = os.getcwd()  # old path
    if path_to_val != "":
        os.chdir(path_to_val)  # new path

    # First check if Sensor node id's txt file
    while os.path.isfile("sensor_ids.txt") != 1:
        logging.warning("MQTT: missing sensor_ids.txt file "
                        "(file listing sensor node id's)")
        time.sleep(5)

    # Read possible/connected sensor ID's from txt file
    with open("sensor_ids.txt", "r") as sensor_ids_fd:
        lock = 0
        while lock != 1:
            try:
                fcntl.flock(sensor_ids_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                lock = 1
            except IOError:
                lock = 0
        sensor_ids = json.load(sensor_ids_fd)
        fcntl.flock(sensor_ids_fd, fcntl.LOCK_UN)

    # Load/read values: sensor reading + time values/value from txt file
    for ids in sensor_ids:

        # First check if sensor value files exist
        while os.path.isfile("sensor_filtered_val_" + str(ids) + ".txt") != 1:
            logging.warning("MQTT: missing sensor values txt file")
            time.sleep(5)

        # Load file
        with open("sensor_filtered_val_" + str(ids) + ".txt", "r") \
                as sensor_vals:
            lock = 0
            while lock != 1:
                try:
                    fcntl.flock(sensor_vals, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    lock = 1
                except IOError:
                    lock = 0
            sensor_value = json.load(sensor_vals)
            fcntl.flock(sensor_vals, fcntl.LOCK_UN)

        vals_dict[ids] = sensor_value
        os.chdir(o_path)  # Return to old path

    return vals_dict


def client_setup():
    """
    This function will set up the client and its properties,
    as well as directing the callback's to their functions

    :return:
    """
    client = mqtt.Client(client_id="zwave_sensors", clean_session=False)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.message_callback_add("mqtt_test/Filter", on_filter_message)
    client.message_callback_add("mqtt_test/SensorPair", on_SensorPair_message)
    # used for debugging
    # client.message_callback_add("mqtt_test/FIFO", on_FIFO_message)

    # Password/token for beebotte
    client.username_pw_set('token:token_mWOdtefqeUm0mlDo')
    client.loop_start()
    return client


def start_client(host, port, timer):
    """
    This function will start the MQTT client.

    :param host:
    :param port:
    :param timer:
    :return:
    """
    client = client_setup()
    client.connect(host, port, timer)
    return client


# ------------------------ "Main part" -------------------------------------- #

# Create log
MQTT_logging_setup()

# MQTT client start function
mqtt_client = start_client("mqtt.beebotte.com", 1883, 60)

# default Timer value (incase no timer value is defined in txt files)
Timer = 600

# Endless loop
# client.loop_forever(timeout=5, retry_first_connection=False)
while 1:
    sensor_vals_list = read_sensor_vals()

    for sensor_val in sensor_vals_list:
        for names in sensor_vals_list[sensor_val]:
            if names == "Time":
                Timer = sensor_vals_list[sensor_val][names]
            # This part is for publishing to beebotte mqtt broker
            else:
                sens_string = str(sensor_vals_list[sensor_val][names])
                names = names.replace(" ", "_")
                pub_string = '{"data":' + sens_string + ',"write":true}'
                mqtt_client.publish("mqtt_test/" + names +
                                    str(sensor_val), pub_string, 1)

    time.sleep(Timer)
