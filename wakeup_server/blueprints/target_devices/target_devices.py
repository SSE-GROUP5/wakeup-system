from flask import Blueprint, request, jsonify
from models.target_devices import TargetDevice
from sqlalchemy.exc import IntegrityError
from requests.exceptions import ConnectionError
from constants import TARGETS_TYPES
from wake_on_lan.wake_on_lan_cllient import validate_mac_address

target_devices_blueprint = Blueprint('target_devices', __name__)

@target_devices_blueprint.route('/target_devices', methods=['POST'])
def create_device():
  data = request.get_json()
  
  # Extract the necessary information from the data
  matter_id = data.get('matter_id') or data.get('id')
  device_name = data.get('name')
  device_type = data.get('type')
  ip_address = data.get('ip') or data.get('ip_address')
  mac_address = data.get('mac') or data.get('mac_address')

  # Perform any necessary validation on the data
  if matter_id is None:
    return "No id provided", 400
  if device_name is None:
    return "No device name provided", 400
  if device_type is None:
    return "No device type provided", 400
  
  if device_type not in TARGETS_TYPES:
    return "Invalid device type, must be one of: " + str(TARGETS_TYPES), 400
  
  if device_type == "wake_on_lan":
    if mac_address is None:
      return "No mac address provided", 400
    if ip_address is None:
      return "No ip address provided", 400
    
    try:
      validate_mac_address(mac_address)
    except ValueError:
      return "Invalid mac address", 400
  
  try:
    device = TargetDevice(matter_id, device_name, device_type, mac_address, ip_address)
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