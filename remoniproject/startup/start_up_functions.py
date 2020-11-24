# Imports
import subprocess
import urllib.request
import urllib.error

# Variables
z_stick = b"Z-Stick Gen5"


# Checks if the USB is connected to the RP, by running shell commands
def find_usb():
    try:
        p = subprocess.Popen("lsusb", stdout=subprocess.PIPE, shell=True)
        (usb_list, err) = p.communicate()
        if z_stick in usb_list:
            return 1
        else:
            return -1
    except subprocess.SubprocessError:
        return -1


# Initiate logging for program
def logger():
    return True


# Checks if RP is connected to the internet
def check_internet_connection():
    try:
        urllib.request.urlopen('http://google.com')  # Python 3.x
        return True
    except urllib.error.URLError:
        return False


def mqtt_setup():
    try:
        subprocess.Popen("python3 MQTT_program.py",
                         stdout=subprocess.PIPE, shell=True)
        return 1
    except subprocess.SubprocessError:
        return -1


def setup():
    # Setup logger
    if logger():
        # Change to logging function
        print("Logger initiated!")
    else:
        # Change to logging function
        print("Logger initiate failed!")
        return -1

    # Checks the internet connection
    if check_internet_connection():
        # Change to logging function
        print("RP is connected to the web!")
    else:
        # Change to logging function
        print("RP is not connected to the web!")
        return -1

    # Checks MQTT
    if mqtt_setup():
        # Change to logging function
        print("MQTT connection is established!")
    else:
        # Change to logging function
        print("MQTT connection is not established!")
        return -1

    # Checks USB list for Z-Stick Gen 5
    if find_usb():
        # Change to logging function
        print("Z-Stick Gen 5 is connected!")
    else:
        # Change to logging function
        print("Z-Stick Gen 5 is not connected!")
        return -1

    return 1
