import time

from requests import post, exceptions  # type: ignore

from config import get_settings
from logging import getLogger

logger = getLogger(__name__)


def wait() -> None:
    while True:
        try:
            post(f"{get_settings().url}registration/", json={"": ""})
        except exceptions.ConnectionError:
            logger.warning("Failed connect")
            time.sleep(1)
            continue
        break


if __name__ == "__main__":
    wait()
