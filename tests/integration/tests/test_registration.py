from psycopg import Cursor
from requests import Session


def test_registration(postgres_cur: Cursor, http_session: Session):
    """Test - correctly working registration endpoint."""
