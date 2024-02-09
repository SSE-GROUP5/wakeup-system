import pytest
import sys 
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
from run import create_app
from db import db

@pytest.fixture()
def app():
    app = create_app("sqlite://")

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()