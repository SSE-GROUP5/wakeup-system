from db import mongo

class InteractiveDevice:
  def __init__(self, device_id, device_type):
    self.collection_name = "interactive_devices"
    self.id = device_id
    self.type = device_type
    self.targets = self.get_targets()
    
    self.create_collection()
  
  
  def create_collection(self):
    if self.collection_name not in mongo.db.list_collection_names():
      interactive_devices = mongo.db.create_collection(self.collection_name)
      interactive_devices.create_index([("id", 1)], unique=True)
  
  def create(self):
    device = {
      'id': self.id,
      'type': self.type,
      'targets': self.targets
    }
    try: 
        mongo.db.interactive_devices.insert_one(device) 
        return True
        
    except Exception as e:
        raise e

  @staticmethod
  def find_by_id(device_id):
    device = mongo.db.interactive_devices.find_one({"id": device_id})
    if device is None:
      return None
    return InteractiveDevice(device['id'], device['type'])
    
  @staticmethod
  def find_all():
    devices = mongo.db.interactive_devices.find()
    if devices is None:
      return None
    return devices
    
  @staticmethod
  def delete_by_id(device_id):
    try:
      mongo.db.interactive_devices.delete_one({"id": device_id})
      return True
    except Exception as e:
      return False
  
  @staticmethod
  def update_by_id(device_id, device_type):
    try:
      mongo.db.interactive_devices.update_one({"id": device_id}, {"$set": {"type": device_type}})
      return True
    except Exception as e:
      return False
  
  
  def get_targets(self):
    try:
      device = mongo.db.interactive_devices.find_one({"id": self.id})
      return device['targets']
    except Exception as e:
      return None
    
  def get_target(self, action):
    try:
      device = mongo.db.interactive_devices.find_one({"id": self.id})
      return device['targets'][action]
    except Exception as e:
      return None
  
  
  def add_target(self, action, target_device_id, target_action):
    try:
      interactive_device = mongo.db.interactive_devices.find_one({"id": self.id})
      interactive_device['targets'][action] = {
        'id': target_device_id,
        'action': target_action
      }
      mongo.db.interactive_devices.update_one({"id": self.id}, {"$set": interactive_device})
      return True
    except Exception as e:
      return False
      
      
  
  def remove_target(self, action):
    try:
      interactive_device = mongo.db.interactive_devices.find_one({"id": self.id})
      del interactive_device['targets'][action]
      mongo.db.interactive_devices.update_one({"id": self.id}, {"$set": interactive_device})
      return True
    except Exception as e:
      return False
    