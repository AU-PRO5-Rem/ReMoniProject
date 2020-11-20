# TODO: insert open() file locks with fcntl, to avoid race conditions

import os
import json
import logging
import fcntl


class ConfClass:
    """"
    This class is meant for methods to handle the configuration file/files.
    The purpose of the configuration file is to store, and select, which sensor data a customer would be interrested in.
    By storing these "customer data preferrals", it's possible to use them as a filter on the recieved sensor data.

    there will be 7 methods which will:
    *Get sensor id's
    *Create + setup configuration files log file
    *Create a configuration file
    *Update configuration file
    *Read configuration file
    *Clean of possible junk files (used when testing this file's functions)
    *Delete conf log file (for clean up purposes)
    """

    def get_multisensors_node_ids(self, network_obj):
        """Look for multisensor(s) in the ZWave network
            to retrieve the node id of all "multisensor 6" that is found
            If no multisensor is found, the returned value is -1
        :param network_obj: initialized network object
        :type network_obj: ZWaveNetwork Object
        :return: Array of Sensors IDs (node id) or
                 -1 if no Multisensors are found
        :rtype: [int]
        """
        sensor_id = []

        for node in network_obj.nodes:
            if "MultiSensor 6" in network_obj.nodes[node].product_name:
                sensor_id.append(network_obj.nodes[node].node_id)
        if len(sensor_id) > 0:
            return sensor_id
        else:
            return -1

    def conf_logging_setup(self):
        """
        File for logging

        :return:
        """
        logging.basicConfig(
            filename='confs.log',
            format=('%(asctime)s %(levelname)s:%(message)s'),
            level=logging.INFO
        )

    def create_confs(self, network_obj, path="", conf_log=0):
        """
        This function will create configuration files for nodes, as long as the node exist, and there's a init configuration
        file named after the product name (fx. ZW100_MultiSensor_6), containing sensor parameters (fx. Temperature, lum,
        ...).

        This function also has a minimum of logging, regarding basic errors and succesful configuration file creation.

        It is neccessary to pass a network object to the function as an argument, and will return 1 on error free run
        through.

        :param obj network_obj:
        :param str path:
        :param int conf_log:
        :return:
        """
        # Setting up logging file
        if conf_log == 1:
            self.conf_logging_setup()

        # Collect node ID's
        multisensors_node_ids = self.get_multisensors_node_ids(network_obj)

        # Go through the node's, to collect sensor data
        for IDs in multisensors_node_ids:
            multisensor = network_obj.nodes[IDs]
            multisensor.get_values()
            sens_dict = multisensor.to_dict()

            # Extract product_name and node_id
            for name, value in sens_dict.items():
                if name == "product_name":
                    pn = value
                    pn = pn.replace(" ", "_")
                if name == "node_id":
                    ni = str(value)

                # Create conf file if there's a product_name and a node_id
                if "pn" in locals() and "ni" in locals():
                    conf_fn = "conf_pn" + pn + "_ni" + ni

                    # Create conf file
                    try:
                        conf_vars = open(pn, "r")
                    except:
                        z = " "
                        logging.error("conf: missing init configuration file called " + pn)
                        logging.info("conf: There should be an init configuration file, "
                                     "named after the product_name of a sensor, \n" + 29 * z +
                                     "containing the names of the sensor vals listed on new lines fx:\n" + 29 * z +
                                     "Temperature\n" + 29 * z +
                                     "Burglar\n" + 29 * z +
                                     "Luminance")
                        return -1

                    # Path corrections
                    o_path = os.getcwd()  # old path
                    if path != "":
                        os.chdir(path)

                    nlines = conf_vars.readlines()
                    json_dict = {}
                    for i in nlines:
                        i = i.replace("\n", "")
                        json_dict[i] = 1
                        json_dict["Time"] = 10
                    with open(conf_fn + ".txt", "w+") as outfile_fd:
                        lock = 0
                        while lock != 1:
                            try:
                                fcntl.flock(outfile_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                                lock = 1
                            except:
                                lock = 0
                        json.dump(json_dict, outfile_fd, indent=4)
                        fcntl.flock(outfile_fd, fcntl.LOCK_UN)

                    conf_vars.close()

                    # Delete var's to ensure there's no replicas
                    del ni
                    del pn

                    logging.info("conf: configuration file " + conf_fn + ".txt created")

                    # Reset path
                    os.chdir(o_path)

        return 1

    def update_conf(self, product_name, node_id, update_json, path="", conf_log=0):
        """
        Updates a configuration file, from a new given json string, containing the name of a parameter fx:
        json_update_string = {"Temperature": 0}
        This example will turn the value "off",, where a "1"w ill indicate the value is turned "on"


        :param str product_name:
        :param int node_id:
        :param str path:
        :param int conf_log:
        :param json update_json:
        :return:
        """
        # Setting up log file
        if conf_log == 1:
            self.conf_logging_setup()

        # Path corrections
        o_path = os.getcwd()  # old path
        if path != "":
            os.chdir(path)

        conf_fn = "conf_pn" + product_name + "_ni" + str(node_id)

        # Try to open corresponding configuration file
        try:
            with open(conf_fn + ".txt", "r") as og_conf_fd:
                lock = 0
                while lock != 1:
                    try:
                        fcntl.flock(og_conf_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        lock = 1
                    except:
                        lock = 0
                og_data = json.load(og_conf_fd)
                fcntl.flock(og_conf_fd, fcntl.LOCK_UN)
        except:
            logging.warning("conf: Couldn't find '" + str(conf_fn) + ".txt'")
            os.chdir(o_path)
            return -1

        # Try to find the corresponding name, and if found then change the old configuration value,
        # to the updated configuration value
        for og_name in og_data:
            og_val = og_data[og_name]
            for new_name in update_json:
                if new_name == og_name:
                    og_data[new_name] = update_json[new_name]
                    logging.info("Node " + str(node_id) + " changes: " +
                                 new_name + ":" + str(og_val) +
                                 " has been changed to "
                                 + new_name + ":" + str(update_json[new_name]))

        # Overwrite old configuration file, with the new updated params
        with open(conf_fn + ".txt", "w+") as outfile_fd:
            lock = 0
            while lock != 1:
                try:
                    fcntl.flock(outfile_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    lock = 1
                except:
                    lock = 0
            json.dump(og_data, outfile_fd, indent=4)
            fcntl.flock(outfile_fd, fcntl.LOCK_UN)

        os.chdir(o_path)

    def read_conf(self, product_name, node_id, path="", conf_log=0):
        """
        Returns a configuration file as a json dict, so it's parameters can be used as filter parameters

        :param str product_name:
        :param int node_id:
        :param str path:
        :param int conf_log:
        :return json dict:
        """
        # Setting up log file
        if conf_log == 1:
            self.conf_logging_setup()

        # Path corrections
        o_path = os.getcwd()  # old path
        if path != "":
            os.chdir(path)

        conf_fn = "conf_pn" + product_name + "_ni" + str(node_id)

        # Try to open corresponding configuration file
        try:
            with open(conf_fn + ".txt", "r") as og_conf_fd:
                lock = 0
                while lock != 1:
                    try:
                        fcntl.flock(og_conf_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        lock = 1
                    except:
                        lock = 0
                conf_data = json.load(og_conf_fd)
                fcntl.flock(og_conf_fd, fcntl.LOCK_UN)
        except:
            logging.warning("Couldn't find '" + str(conf_fn) + ".txt'")
            os.chdir(o_path)
            return -1

        os.chdir(o_path)
        return conf_data

    def clean_up_junk(self):
        """
        Cleans up junk files, generated when testing configuration files functions

        :return:
        """
        os.remove("options.xml")
        os.remove("OZW_Log.txt")
        os.remove("pyozw.sqlite")
        print("junk removed")

    def reset_conf_log(self):
        """
        Used for removing the conf log file, in case of a clean up

        :return:
        """
        open("confs.log", 'w').close()
