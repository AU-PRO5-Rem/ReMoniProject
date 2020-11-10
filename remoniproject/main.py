from .startup.start_up_functions import setup


def main():
    setup()


def increment(x):
    return x + 1


def decrement(x):
    return x - 1


if __name__ == "__main__":
    main()
