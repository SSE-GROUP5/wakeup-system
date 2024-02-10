from flask import Blueprint, request, jsonify
from models.triggers import Trigger
from sqlalchemy.exc import IntegrityError
from zmq_client import zmq_client
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
    return {"message": f"Device name already used by {name_already_exists.id}"}, 402 
  
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

@triggers_blueprint.route('/triggers/confirm', methods=['POST'])
def confirm_trigger():
    data = request.get_json()
    device_id = data.get('id')
    if device_id is None:
        return "No name provided", 400
    device = Trigger.find_by_id(device_id)
    if device is None:
        return "Device not found", 404
    device.confirm()
    return "Device confirmed", 200




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


@triggers_blueprint.route('/triggers/<string:id>', methods=['PUT'])
def update_trigger(id):
    device = Trigger.find_by_id(id)
    if device is None:
        device = Trigger.find_by_name(id)
        
    if device is None:
        return "Device not found", 404
    
    data = request.get_json()
    try:
      print("Warning: ZMQ Server needs to be started to proceed.")
      zmq_body = {}
      for key, value in data.items():
        zmq_body[key.upper()] = value
      
      zmq_client.send_data(device.id, zmq_body)
      zmq_client.receive_reply()
    except Exception as e:
      print(e)
      return f"Failed to send ZMQ message to trigger: {device.id}", 400
    
    return jsonify(device.json()), 200