from homeassistant_client import homeassistant_client
from homeassistant.fake_matter_device import FAKE_MATTER_DEVICE
from constants import HOMEASSISTANT_OFFLINE_MODE
from sqlalchemy import Column, String, JSON
from models.devices_target_map import interactive_target_association
from db import db

class TargetDevice(db.Model):
  __tablename__ = 'target_devices'
  
  matter_id = db.Column(db.String(50), primary_key=True)
  name = Column(String)
  type = Column(String)
  possible_actions = Column(JSON, nullable=True)
  interactive_devices = db.relationship("InteractiveDevice", secondary=interactive_target_association, back_populates="target_devices")
  
  def __init__(self, matter_id, name, type):
    self.matter_id = matter_id
    self.name = name
    self.type = type
    self.possible_actions = self.get_possible_actions()
    
    
  def json(self):
    return {
      "matter_id": self.matter_id,
      "name": self.name,
      "type": self.type,
      "possible_actions": self.possible_actions
    }
    
  def get_possible_actions(self):
    if HOMEASSISTANT_OFFLINE_MODE:
      print("HOMEASSISTANT_OFFLINE_MODE IS ENABLED")
      return FAKE_MATTER_DEVICE.get("possible_actions")
    
    return homeassistant_client.get_possible_actions(self.matter_id)
    
  def create(self):
    device = TargetDevice(matter_id=self.matter_id, name=self.name, type=self.type)
    try:
      db.session.add(device)
      db.session.commit()
      return True
    except Exception as e:
      print(e)
      db.session.rollback()
      raise e
    
  def do_action(self, action):
    if HOMEASSISTANT_OFFLINE_MODE:
      print("HOMEASSISTANT_OFFLINE_MODE IS ENABLED")
      print("Action: " + action)
      return True
    
    try:
      device = homeassistant_client.find_entity_by_id(self.matter_id)
      device.set_state(action)
      return True
    except Exception as e:
      raise e
    
  @staticmethod
  def find_by_id(matter_id):
    return TargetDevice.query.get(matter_id)
  
  @staticmethod
  def find_all():
    return TargetDevice.query.all()
  
  @staticmethod
  def delete_by_id(matter_id):
    device = TargetDevice.query.get(matter_id)
    if device:
      try:
        db.session.delete(device)
        db.session.commit()
        return True
      except Exception as e:
        db.session.rollback()
        return False
    return False
  
  @staticmethod
  def update_by_id(matter_id, name, type):
    device = TargetDevice.query.get(matter_id)
    if device:
      try:
        device.name = name
        device.type = type
        db.session.commit()
        return True
      except Exception as e:
        db.session.rollback()
        return False
    return False
    