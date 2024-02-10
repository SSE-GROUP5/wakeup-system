from flask import Blueprint, request, jsonify
from models.triggers import Trigger
from sqlalchemy.exc import IntegrityError
import uuid

triggers_blueprint = Blueprint('triggers', __name__)

@triggers_blueprint.route('/triggers', methods=['POST'])
def create_trigger():
  data = request.get_json()
  # Extract the necessary information from the data
  device_type = data.get('type')
  device_name = data.get('name')

  # Perform any necessary validation on the data
  if device_type is None:
    return "No type provided", 400
  if device_name is None:
    return "No name provided", 400
  if " " in device_name:
    return {"message": "Device name cannot contain spaces"}, 400

  device_name = device_name.strip()
  name_already_exists = Trigger.find_by_name(device_name)
  if name_already_exists is not None:
    return {"message": "Device name already used"}, 409
  
  try: 
      device_id = str(uuid.uuid4())
      new_device = Trigger(device_id, device_name, device_type)
      new_device.create()
      new_device = Trigger.find_by_id(device_id)
      return new_device.json(), 201
  
  except IntegrityError:
      return "Device already exists", 400
  except ConnectionError:
      return "Connection error", 400
  except Exception as e:
      print(e)
      return "Unknown error", 400

@triggers_blueprint.route('/triggers', methods=['GET'])
def get_triggers():
    all_devices = Trigger.find_all()
    return jsonify([device.json() for device in all_devices]), 200
    
@triggers_blueprint.route('/triggers/<string:id>', methods=['GET'])
def get_trigger(id):
    device = Trigger.find_by_id(id)
    if device is None:
        return "Device not found", 404
    return jsonify(device.json()), 200
