from flask import Blueprint, request, jsonify
from pymongo.errors import DuplicateKeyError
from db import mongo

interactive_devices_blueprint = Blueprint('interactive_devices', __name__)

@interactive_devices_blueprint.route('/interactive_devices', methods=['POST'])
def create_interactive_device():
  data = request.get_json()
  
  # Extract the necessary information from the data
  device_name = data.get('name')
  device_type = data.get('type')

  # Perform any necessary validation on the data
  if device_name is None:
    return "No device name provided", 400
  if device_type is None:
    return "No device type provided", 400

  # check if collection exists
  if "devices" not in mongo.db.list_collection_names():
      interactive_devices = mongo.db.create_collection("interactive_devices")
      interactive_devices.create_index([("id", 1)], unique=True)
  
  # Insert the data into the database
  device = {
    'id': device_name,
    'type': device_type
  }
  try: 
      mongo.db.interactive_devices.insert_one(device)
      
      return jsonify({
          "name": device_name,
          "type": device_type
      }), 201
      
  except DuplicateKeyError:
      return "Device already exists", 400
    
  except Exception as e:
      return "Unknown error", 400


