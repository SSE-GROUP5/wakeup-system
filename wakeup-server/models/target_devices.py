from db import mongo
from homeassistant_client import homeassistant_client

class TargetDevice:
  def __init__(self, matter_id, name, type):
    self.matter_id = matter_id
    self.name = name
    self.type = type
    self.possible_actions = self.get_possible_actions()
    
    self.collection_name = "target_devices"
    self.create_collection()
    
  def create_collection(self):
    if self.collection_name not in mongo.db.list_collection_names():
      target_devices = mongo.db.create_collection(self.collection_name)
      target_devices.create_index([("matter_id", 1)], unique=True)
      
  def get_possible_actions(self):
    return homeassistant_client.get_possible_actions(self.matter_id)
    
  def create(self):
    device = {
      'matter_id': self.matter_id,
      'name': self.name,
      'type': self.type,
      'possible_actions': self.possible_actions
    }
    try: 
        mongo.db.target_devices.insert_one(device) 
        return True
        
    except Exception as e:
        raise e
      
  def do_action(self, action):
    try:
       device = homeassistant_client.find_entity_by_id(self.matter_id)
       device.set_state(action)
       return True
    except Exception as e:
      raise e
      
  @staticmethod
  def find_by_id(matter_id):
    device = mongo.db.target_devices.find_one({"matter_id": matter_id})
    if device is None:
      return None
    return TargetDevice(device['matter_id'], device['name'], device['type'])
  
  @staticmethod
  def find_all():
    devices = mongo.db.target_devices.find()
    if devices is None:
      return None
    return devices
  
  @staticmethod
  def delete_by_id(matter_id):
    try:
      mongo.db.target_devices.delete_one({"matter_id": matter_id})
      return True
    except Exception as e:
      return False
    
  @staticmethod
  def update_by_id(matter_id, name, type):
    try:
      mongo.db.target_devices.update_one({"matter_id": matter_id}, {"$set": {"name": name, "type": type}})
      return True
    except Exception as e:
      return False
    