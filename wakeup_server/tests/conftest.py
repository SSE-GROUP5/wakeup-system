import pytest
import sys 
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/..")
from run import create_app
from db import db
dir_path = os.path.dirname(os.path.realpath(__file__))
@pytest.fixture()
def app():
    if os.path.exists(f"{dir_path}/../instance/test.sqlite"):
        os.remove(f"{dir_path}/../instance/test.sqlite")
    app = create_app("sqlite:///test.sqlite")

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()