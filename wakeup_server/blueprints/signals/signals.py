from flask import Blueprint, request, jsonify
from models.triggers import Trigger
from models.target_devices import TargetDevice
from models.triggers_target_map import delete_signal_from_map
from models.users import User
from models.signal_logs import SignalLogs as signal_logs
from sqlalchemy.exc import IntegrityError, NoResultFound
from scheduler.alert_scheduler import alert_scheduler
import uuid
from constants import DATA_FOLDER_PATH, TRIGGERS_TYPES
import base64

signals_blueprint = Blueprint('signals', __name__)

@signals_blueprint.route('/signals', methods=['GET'])
def get_signals():
  devices = Trigger.find_all()
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


@signals_blueprint.route('/signals/stop_alert/<string:channel_id>', methods=['POST'])
def stop_alert(channel_id):
  alert_scheduler.stop_alert(channel_id)
  return "Alert stopped", 200

@signals_blueprint.route('/signals', methods=['POST'])
def receive_signal():
  data = request.get_json()
  trigger_id = data.get('id')
  trigger_name = data.get('name')
  trigger_action = data.get('action')
  trigger_num_actions = data.get('num_actions')
  trigger_with_user_id = data.get('user_id')
  trigger_picture = data.get('picture')
  
  if trigger_id is None and trigger_name is None:
      return "No trigger id or name provided", 400
  if trigger_action is None:
      return "action not provided", 400
  if trigger_num_actions is None:
      return "num_actions not provided", 400
    
  trigger = Trigger.find_by_id(trigger_id) if trigger_id is not None else Trigger.find_by_name(trigger_name)
  if trigger is None:
      return "trigger not found", 400

  trigger_num_actions = trigger_num_actions.lower() if isinstance(trigger_num_actions, str) else trigger_num_actions
  targets_objects = trigger.get_targets_per_device(trigger_action, trigger_num_actions, trigger_with_user_id)
  
  if len(targets_objects) == 0:
      return f"No targets set for {trigger.name} with action: {trigger_action} and value: {trigger_num_actions}", 400
  
  # if there is a picture in the request, save it
  picutre_path = None
  try:
    if trigger_picture:
        picture = base64.b64decode(trigger_picture)
        picutre_path = f'{DATA_FOLDER_PATH}/{trigger_name}.png'
        with open(picutre_path, 'wb') as img:
            img.write(picture)
            
  except Exception as e:
    print(e)
    
      
  
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
        
      target_device.do_action(target_action, picutre_path)
      signal = trigger.get_signal(trigger_action, trigger_num_actions, target_device_id, user_id)
      signal_logs.info(signal_id=signal['id'], patient_id=user_id, signal_type=str(trigger_action) + '_' + str(trigger.name), target_device=str(target_device.matter_id))
      output_message.append({
          'target_device_id': target_device_id,
          'target_action': target_action,
          'num_actions': trigger_num_actions,
          'user_id': user_id,
          'status': 'sent',
      })
  
    
  return {'signals': output_message}, 200


@signals_blueprint.route('/signals/set', methods=['POST'])
def set_signal():
  trigger_id = request.json.get('trigger_id')
  trigger_name = request.json.get('trigger_name')
  trigger_action = request.json.get('trigger_action')
  trigger_num_actions = request.json.get('trigger_num_actions')
  target_device_id = request.json.get('target_device_id')
  target_action = request.json.get('target_action')
  user_id = request.json.get('user_id')
  
  if trigger_id is None and trigger_name is None:
      return "No trigger ID or name provided", 400
  if target_device_id is None:
      return "No target device ID provided", 400
  if target_action is None:
      return "No target action provided", 400
  if trigger_action is None:
      return "No trigger action provided", 400
  if trigger_num_actions is None:
      return "No trigger num actions provided", 400
    
  if trigger_action not in TRIGGERS_TYPES:
      return {"message": f"Trigger action not supported. Supported types are {TRIGGERS_TYPES}"}, 400
  
  trigger = Trigger.find_by_id(trigger_id) if trigger_id is not None else Trigger.find_by_name(trigger_name)

  if trigger is None:
      return "trigger not found", 400

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
      new_signal = trigger.add_target(trigger_action, trigger_num_actions, target_device_id, target_action, user_id)
      return jsonify({
        'message': 'Signal set',
        'signal': new_signal
      }), 201
  except IntegrityError as e:
      return "Signal already set", 400
  except NoResultFound as e:
      return jsonify({"error": str(e)}), 400
  except Exception as e:
      print(e)
      return jsonify({"error": str(e)}), 500
  
@signals_blueprint.route('/signals/<string:signal_id>', methods=['DELETE'])
def delete_signal(signal_id):
  try:
    signal_as_uuid = uuid.UUID(signal_id)
  except Exception as e:
     print(e)
     return "Signal ID not in correct format", 400
  success = delete_signal_from_map(signal_as_uuid)
  if(success):
     return "Deleted successfully", 200
  else:
     return "Signal Not Found", 400





