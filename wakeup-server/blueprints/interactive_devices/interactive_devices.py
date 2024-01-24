from flask import Blueprint, request, jsonify
from models.interactive_devices import InteractiveDevice
from sqlalchemy.exc import IntegrityError

interactive_devices_blueprint = Blueprint('interactive_devices', __name__)

@interactive_devices_blueprint.route('/interactive_devices', methods=['POST'])
def create_interactive_device():
  data = request.get_json()
  # Extract the necessary information from the data
  device_id = data.get('id')
  device_type = data.get('type')

  # Perform any necessary validation on the data
  if device_id is None:
    return "No device id provided", 400
  if device_type is None:
    return "No device type provided", 400

  try: 
      new_device = InteractiveDevice(device_id, device_type)
      new_device.create()
      
      return jsonify({
          "id": device_id,
          "type": device_type
      }), 201
  
  except IntegrityError:
      return "Device already exists", 400
    
  except Exception as e:
      print(e)
      return "Unknown error", 400


