import pytest
import sys
import os

# Add project root to the Python path for all tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db
from _pytest.monkeypatch import MonkeyPatch

@pytest.fixture(scope='session')
def db_connection():
    """Session-scoped fixture to set up a single, persistent in-memory database."""
    mpatch = MonkeyPatch()
    mpatch.setattr(db, 'DATABASE_FILE', 'file:memdb1?mode=memory&cache=shared')
    conn = db.get_db_connection()
    db.init_db()
    yield conn
    conn.close()
    mpatch.undo()

@pytest.fixture(autouse=True)
def clean_db(db_connection):
    """Function-scoped fixture to clean the database before each test."""
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM agents")
    db_connection.commit()
    yield
