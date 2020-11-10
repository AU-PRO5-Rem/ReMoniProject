# Imports
import subprocess

# Variables
z_stick = b"Z-Stick Gen5"


# Checks if the USB is connected to the RP, by running shell commands
def find_usb():
    p = subprocess.Popen("lsusb", stdout=subprocess.PIPE, shell=True)
    (usb_list, err) = p.communicate()
    if z_stick in usb_list:
        return True
    else:
        return False


# Initiate logging for program
def logger():
    return True


# Checks if RP is connected to the internet
def check_internet_connection():
    return True


def mqtt_setup():
    return True


def setup():
    # Setup logger
    if logger():
        # Change to logging function
        print("Logger initiated!")
    else:
        # Change to logging function
        print("Logger initiate failed!")
        exit(-1)

    # Checks the internet connection
    if check_internet_connection():
        # Change to logging function
        print("RP is connected to the web!")
    else:
        # Change to logging function
        print("RP is not connected to the web!")
        exit(-1)

    # Checks MQTT
    if mqtt_setup():
        # Change to logging function
        print("MQTT connection is established!")
    else:
        # Change to logging function
        print("MQTT connection is not established!")
        exit(-1)

    # Checks USB list for Z-Stick Gen 5
    if find_usb():
        # Change to logging function
        print("Z-Stick Gen 5 is connected!")
    else:
        # Change to logging function
        print("Z-Stick Gen 5 is not connected!")
        exit(-1)