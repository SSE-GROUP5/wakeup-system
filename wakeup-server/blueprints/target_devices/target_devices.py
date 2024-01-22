from flask import Blueprint, request, jsonify
from pymongo.errors import DuplicateKeyError
from db import mongo
from homeassistant_client import homeassistant_client

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

  # check if collection exists
  if "target_devices" not in mongo.db.list_collection_names():
      target_devices = mongo.db.create_collection("target_devices")
      target_devices.create_index([("matter_id", 1)], unique=True)
  
  # Insert the data into the database
  possible_actions = homeassistant_client.get_possible_actions(matter_id)
  
  if possible_actions is None:
      return "No possible actions found", 400
    
  device = {
    'matter_id': matter_id,
    'name': device_name,
    'type': device_type,
    'possible_actions': possible_actions
  }
  
  try: 
      mongo.db.target_devices.insert_one(device)
      
      return jsonify({
          "matter_id": matter_id,
          "name": device_name,
          "type": device_type,
          "possible_actions": possible_actions
      }), 201
      
  except DuplicateKeyError:
      return "Device already exists", 400
    
  except Exception as e:
      return "Unknown error", 400


@target_devices_blueprint.route('/target_devices/refresh', methods=['GET'])
def refresh_devices():
    devices = homeassistant_client.find_entity_by_attributes()
    switches = devices['switches']
  
    for switch in switches:
        json_data = switch.json()
        
        device = {
            'matter_id': json_data['id'],
            'possible_actions': json_data['possible_actions'],
            'type': 'switch'
        }
        
        try:
              # check if collection exists
            if "target_devices" not in mongo.db.list_collection_names():
                target_devices = mongo.db.create_collection("target_devices")
                target_devices.create_index([("matter_id", 1)], unique=True)
            
            mongo.db.target_devices.insert_one(device)
        except DuplicateKeyError:
            pass
        except Exception as e:
            print(e)
            return "Unknown error", 400
          
        
    return jsonify("OK"), 200