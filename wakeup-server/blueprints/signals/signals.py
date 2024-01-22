from flask import Blueprint, request
from db import mongo
from homeassistant_client import homeassistant_client
from models.interactive_devices import InteractiveDevice

signals_blueprint = Blueprint('signals', __name__)

@signals_blueprint.route('/signals', methods=['POST'])
def receive_signal():
  data = request.get_json()
  interactive_device_id = data.get('id')
  interactive_device_action = data.get('action')
  
  if interactive_device_id is None:
      return "No interactive device ID provided", 400
  if interactive_device_action is None:
      return "No interactive device action provided", 400
    
  interactive_device = InteractiveDevice.find_by_id(interactive_device_id)
  
  if interactive_device is None:
      return "Interactive device not found", 400
    
  target_object = interactive_device.get_target(interactive_device_action)
  
  target_device_id = target_object.get('id')
  action = target_object.get('action')
  
  if target_device_id is None:
      return "No target device ID set", 400
  if action is None:
      return "No action set", 400
    
  target_device_mongo = mongo.db.target_devices.find_one({'matter_id': target_device_id})
  if target_device_mongo is None:
      return "Target Matter device not found", 400
    
  device = homeassistant_client.find_entity_by_id(target_device_id)
  device.set_state(action)
  
  return f"Signal received for device {target_device_id} to perform action {action}", 200


@signals_blueprint.route('/signals/set', methods=['POST'])
def set_signal():
  interactive_device_id = request.json.get('interactive_device_id')
  interactive_device_action = request.json.get('interactive_device_action')
  target_device_id = request.json.get('target_device_id')
  target_action = request.json.get('target_action')
  
  if interactive_device_id is None:
      return "No interactive device ID provided", 400
  if target_device_id is None:
      return "No target device ID provided", 400
  if target_action is None:
      return "No target action provided", 400
  if interactive_device_action is None:
      return "No interactive device action provided", 400
  
  interactive_device = mongo.db.interactive_devices.find_one({'id': interactive_device_id})
  interactive_device = InteractiveDevice.find_by_id(interactive_device_id)

  if interactive_device is None:
      return "Interactive device not found", 400

  target_device = mongo.db.target_devices.find_one({'matter_id': target_device_id})
  if target_device is None:
      return "Target Matter device not found", 400
  
  actions = target_device.get('possible_actions')
  if actions is None:
      return "Target device has no actions", 400
    
  actions_ids = [action['action'] for action in actions]
  if target_action not in actions_ids:
      return "Target device does not have this action", 400
  
  interactive_device.add_target(interactive_device_action, target_device_id, target_action)
  
  return "Signal set", 200

