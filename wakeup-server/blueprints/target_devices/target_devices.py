from flask import Blueprint, request
from models.target_devices import TargetDevice
from sqlalchemy.exc import IntegrityError

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
  
  try:
    device = TargetDevice(matter_id, device_name, device_type)
    device.create()
    return "Device created successfully", 200
      
  except IntegrityError:
      return "Device already exists", 400
    
  except Exception as e:
      print(e)
      return "Unknown error", 400

  
