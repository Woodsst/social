import requests  # type: ignore
from pytest import fixture
from requests import Session

from config import get_settings

sett = get_settings()

pytest_plugins = ("fixtures.postgres",)


@fixture(scope="function")
def http_session() -> Session:
    """Fixture for getting http session."""
    session = requests.Session()
    yield session
    session.close()
