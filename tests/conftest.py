import os
import shutil
import pytest

# Set test DB before importing app/models
TEST_DB_PATH = os.path.join(os.path.dirname(__file__), 'test_db.sqlite')
os.environ['DATABASE_URL'] = f'sqlite:///{TEST_DB_PATH}'

from app import app as flask_app
from models import init_db, get_db, Shelf

import utils.serial_ctrl as serial_mod

class MockSerial:
    def __init__(self):
        self.sent = []
    def connect(self):
        return True
    def send(self, msg):
        self.sent.append(msg)
        return True
    def close(self):
        pass

@pytest.fixture(scope='session')
def app():
    # ensure clean test db
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    init_db()
    # create 8 shelves
    db = get_db()
    if db.query(Shelf).count() == 0:
        for i in range(1,9):
            s = Shelf(slot=i, status='EMPTY')
            db.add(s)
        db.commit()
    flask_app.testing = True
    yield flask_app
    # teardown
    try:
        os.remove(TEST_DB_PATH)
    except Exception:
        pass

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def mock_serial():
    m = MockSerial()
    # replace module instance
    serial_mod.serial_ctrl = m
    yield m
