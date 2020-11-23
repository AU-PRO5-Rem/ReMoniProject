"""
The "main" MQTT program.

This client program will run in the background,
to enable a constant MQTT connection, to an MQTT broker.
In this program it will be connected to our own rented MQTT broker (beebotte),
so it's possible to do extended test's,
where in reality it will be changed to Remonis own MQTT client and broker.
"""
# Enable full folder struct to becoma available
import os
import json
import paho.mqtt.client as mqtt
import logging
import sys
from pathlib import Path
sys.path.append("../")

# Rest of imports
# and can be done in other ways)


class MQTT_Client():

    def __init__(self):

        logging.basicConfig(
            filename='MQTT.log',
            format=('%(asctime)s %(levelname)s:%(message)s'),
            level=logging.INFO
        )

        # Setup Client
        self.__client = mqtt.Client(client_id="zwave_sensors",
                                    clean_session=False)
        self.__client.on_connect = self.on_connect
        self.__client.on_disconnect = self.on_disconnect
        self.__client.on_message = self.on_message
        self.__client.username_pw_set('token:'+str(os.environ['MQTTTOKEN']))
        self.__client.loop_start()

        # Start Client
        self.host = "mqtt.beebotte.com"
        self.port = 1883
        self.timer = 60

        # Files with Sensor Values
        self.__path = ''

        self.is_running = False

    def on_connect(self, client, userdata, flags, rc):
        logging.info("MQTT: Connection established")
        self.__client.subscribe("mqtt_test/Filter", 0)
        self.is_running = True
        # Jan?

    def on_disconnect(self, client, userdata, rc):
        logging.info("MQTT: Connection lost")
        self.is_running = False

    def on_message(self, client, userdata, msg):
        logging.info("MQTT: Message Received")
        # Jan?

    def start_client(self):
        """
        This function will start the MQTT client.

        :param host:
        :param port:
        :param timer:
        :return:
        """
        self.__client.connect(self.host, self.port, self.timer)

    def set_path_to_data(self):
        abs_path = str(Path(__file__).parent.absolute())
        path = abs_path.split("remoniproject/")[0]
        self.__path = path+'/data/'

    def publish_values(self, node_ids):
        self.set_path_to_data()
        try:
            for node_id in node_ids:
                vals_file = 'sensor_vals_'+str(node_id)+'.txt'
                filename = self.__path+vals_file

                with open(filename, 'r') as sensor_vals:
                    vals = json.load(sensor_vals)

                for val in vals:
                    sens_string = str(vals[val])
                    val = val.replace(" ", "_")
                    pub_string = '{"data":' + sens_string + ',"write":true}'
                    self.__client.publish(
                        "mqtt_test/" + val + str(node_id), pub_string, 1)
                    logging.info('Published to channel %s',
                                 "mqtt_test/" + val + str(node_id))
                    logging.info('resource: %s', pub_string)
        except Exception as emsg:
            logging.info('Unable to publish values! %s', emsg)