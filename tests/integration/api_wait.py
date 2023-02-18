import time

from requests import post, exceptions

from config import get_settings


def wait():
    while True:
        try:
            post(f"{get_settings().url}registration/", json={"": ""})
        except exceptions.ConnectionError:
            print("Failed connect")
            time.sleep(1)
            continue
        break


if __name__ == "__main__":
    wait()
