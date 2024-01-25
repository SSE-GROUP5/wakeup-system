from flask import Blueprint, request
from models.interactive_devices import InteractiveDevice
from models.target_devices import TargetDevice
from sqlalchemy.exc import IntegrityError

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
  
  if target_object is None:
      return f"No target device set for action {interactive_device_action}", 400
  
  target_device_id = target_object.get('matter_id')
  target_action = target_object.get('action')
  
  if target_device_id is None:
      return "No target device ID set", 400
  if target_action is None:
      return "No action set", 400
    
  target_device = TargetDevice.find_by_id(target_device_id)
  if target_device is None:
      return "Target device not found", 400
    
  action_names = [action['action'] for action in target_device.possible_actions]
  if target_action not in action_names:
      return "Target device does not have this action", 400
    
  target_device.do_action(target_action)
  
  return f"Signal received for device {target_device_id} to perform action {target_action}", 200


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
  
  interactive_device = InteractiveDevice.find_by_id(interactive_device_id)

  if interactive_device is None:
      return "Interactive device not found", 400

  target_device = TargetDevice.find_by_id(target_device_id)
  if target_device is None:
      return "Target Matter device not found", 400
  
  actions = target_device.possible_actions
  if actions is None:
      return "Target device has no actions", 400
    
  actions_ids = [action['action'] for action in actions]
  if target_action not in actions_ids:
      return "Target device does not have this action", 400
  try:
      interactive_device.add_target(interactive_device_action, target_device_id, target_action)
      return "Signal set", 200
  except IntegrityError as e:
      return "Signal already set", 400
