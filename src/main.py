import paho.mqtt.client as mqtt


def main():
    print("Hello World")


def increment(x):
    return x + 1


def decrement(x):
    return x - 1


if __name__ == "__main__":
    mqtt.client()
    main()
    y = 1
    increment(y)
    decrement(y)
    print("Goodbye World")
