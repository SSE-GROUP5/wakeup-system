from flask import Blueprint, request, jsonify
from models.target_devices import TargetDevice
from sqlalchemy.exc import IntegrityError
from requests.exceptions import ConnectionError

target_devices_blueprint = Blueprint('target_devices', __name__)

@target_devices_blueprint.route('/target_devices', methods=['POST'])
def create_device():
  data = request.get_json()
  
  # Extract the necessary information from the data
  matter_id = data.get('matter_id')
  device_name = data.get('name')
  device_type = data.get('type')

  # Perform any necessary validation on the data
  if device_name is None:
    return "No device name provided", 400
  if device_type is None:
    return "No device type provided", 400
  
  try:
    device = TargetDevice(matter_id, device_name, device_type)
    device.create()
    return jsonify(device.json()), 201
      
  except IntegrityError:
      return "Device already exists", 400
  except ConnectionError:
      return "Connection error with Home Assistant", 400
  except Exception as e:
      return str(e), 400

  
@target_devices_blueprint.route('/target_devices', methods=['GET'])
def get_devices():
  all_devices = TargetDevice.find_all()
  return jsonify([device.json() for device in all_devices]), 200

@target_devices_blueprint.route('/target_devices/<string:id>', methods=['GET'])
def get_device(id):
  device = TargetDevice.find_by_id(id)
  if device is None:
    return "Device not found", 404
  return jsonify(device.json()), 200