import pytest
import sys
import os
from flask import Flask
current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir + "\..")
from run import create_app
from models.interactive_devices import InteractiveDevice

@pytest.fixture()
def app():
  app = create_app()
  app.config.update({
    "TESTING": True,
  })


  yield app

  # clean up / reset resources here


@pytest.fixture()
def client(app):
  return app.test_client()


@pytest.fixture()
def runner(app):
  return app.test_cli_runner()

def test_new_device():
  device = InteractiveDevice('cam_1', 'Camera')
  assert device.id == 'cam_1'

# 'http://localhost:5001'
# def test_request_example(client):
#   response = client.get()
#   assert b"Hello, World!" in response.data


# def test_json_data(client):
#   response = client.post("/", json={
#     "id": "cam_1",
#     "type": "Camera"
#   })
#   assert b"cam_1" in response.data
