from typing import Generator

import psycopg
from psycopg import Cursor
from psycopg.rows import dict_row

from config import get_settings
from pytest import fixture

from tests_utils.generate_test_data import add_test_data, delete_data

sett = get_settings()


@fixture(scope="session")
def postgres_cur() -> Generator:
    """Fixture for getting postgres cursor."""
    con = psycopg.connect(sett.postgres_test_dsn, row_factory=dict_row)
    cursor = con.cursor()
    yield cursor
    con.close()


@fixture(scope="function")
def clear_postgres(postgres_cur: Cursor) -> Generator:
    """Fixture for clear all data in postgres after test worked."""
    yield
    delete_data(postgres_cur)


@fixture(scope="function")
def add_test_data_in_postgres(postgres_cur: Cursor) -> Generator:
    """Fixture for add and delete data in postgres."""
    add_test_data(postgres_cur)
    yield
    delete_data(postgres_cur)
