from flask import Blueprint, request, jsonify
from models.interactive_devices import InteractiveDevice
from models.target_devices import TargetDevice
from models.devices_target_map import signal_to_json
from models.users import User
from sqlalchemy.exc import IntegrityError, NoResultFound

signals_blueprint = Blueprint('signals', __name__)

@signals_blueprint.route('/signals', methods=['GET'])
def get_signals():
  devices = InteractiveDevice.find_all()
  all_signals = []
  try:
    for device in devices:
        device_signals = device.get_signals()
        for signal in device_signals:
            all_signals.append(signal)
            
    return {'signals': all_signals}, 200
  except Exception as e:
    print(e)
    return "Internal server error in getting signals", 500


@signals_blueprint.route('/signals/users/<string:user_id>', methods=['GET'])
def get_signals_for_user(user_id):
  user = User.find_by_id(user_id)
  if user is None:
      return "User not found", 400
  try:
    user_signals = user.get_signals()
    return {'signals': user_signals}, 200
  except Exception as e:
    print(e)
    return "Internal server error in getting signals", 500
  

@signals_blueprint.route('/signals', methods=['POST'])
def receive_signal():
  data = request.get_json()
  interactive_device_id = data.get('id')
  interactive_device_action = data.get('action')
  interactive_device_num_actions = data.get('num_actions')
  interactive_device_with_user_id = data.get('user_id')
  
  if interactive_device_id is None:
      return "id not provided", 400
  if interactive_device_action is None:
      return "action not provided", 400
  if interactive_device_num_actions is None:
      return "num_actions not provided", 400
    
  interactive_device = InteractiveDevice.find_by_id(interactive_device_id)
  
  if interactive_device is None:
      return "Interactive device not found", 400
    
  targets_objects = interactive_device.get_targets_per_device(interactive_device_action, interactive_device_with_user_id, interactive_device_num_actions)
  
  if len(targets_objects) == 0:
      return f"No targets set for {interactive_device_id} with action: {interactive_device_action}", 400
  
  output_message = []
  for target_objects in targets_objects:
      target_device_id = target_objects.get('matter_id')
      target_action = target_objects.get('action')
      user_id = target_objects.get('user_id') if target_objects.get('user_id') is not None else None
  
      target_device = TargetDevice.find_by_id(target_device_id)
      if target_device is None:
          return "Target device not found", 400
      
      possible_action_names = [action['action'] for action in target_device.possible_actions]
      
      if target_action not in possible_action_names:
          return "Target device does not have this action", 400
        
      target_device.do_action(target_action)
      output_message.append({
          'target_device_id': target_device_id,
          'target_action': target_action,
          'num_actions': interactive_device_num_actions,
          'user_id': user_id,
          'status': 'sent',
      })
  
    
  return {'signals': output_message}, 200


@signals_blueprint.route('/signals/set', methods=['POST'])
def set_signal():
  interactive_device_id = request.json.get('interactive_device_id')
  interactive_device_action = request.json.get('interactive_device_action')
  interactive_device_num_actions = request.json.get('interactive_device_num_actions')
  target_device_id = request.json.get('target_device_id')
  target_action = request.json.get('target_action')
  user_id = request.json.get('user_id')
  
  if interactive_device_id is None:
      return "No interactive device ID provided", 400
  if target_device_id is None:
      return "No target device ID provided", 400
  if target_action is None:
      return "No target action provided", 400
  if interactive_device_action is None:
      return "No interactive device action provided", 400
  if interactive_device_num_actions is None:
      return "No interactive device num actions provided", 400
  
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
      new_signal = interactive_device.add_target(interactive_device_action, interactive_device_num_actions, target_device_id, target_action, user_id)
      return jsonify({
        'message': 'Signal set',
        'signal': new_signal
      })
  except IntegrityError as e:
      return "Signal already set", 400
  except NoResultFound as e:
      return jsonify({"error": str(e)}), 400
  except Exception as e:
      print(e)
      return jsonify({"error": str(e)}), 500
