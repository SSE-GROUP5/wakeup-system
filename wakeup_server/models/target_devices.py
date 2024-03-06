from homeassistant_client import homeassistant_client
from scheduler.alert_scheduler import alert_scheduler
from homeassistant.fake_matter_device import FAKE_MATTER_DEVICE
from constants import HOMEASSISTANT_OFFLINE_MODE
from sqlalchemy import Column, String, JSON
from models.triggers_target_map import trigger_target_association
from db import db
from models.target_device_logs import TargetDeviceLogs
from sqlalchemy.exc import IntegrityError

class TargetDevice(db.Model):
  __tablename__ = 'target_devices'
  
  matter_id = db.Column(db.String(50), primary_key=True)
  name = Column(String)
  type = Column(String)
  possible_actions = Column(JSON, nullable=True)
  triggers = db.relationship("Trigger", secondary=trigger_target_association, back_populates="target_devices")
  
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
    if self.type.lower() == "telegram":
      return [{"action": "send_alert", "description": "Send an alert to the medical staff"}]
    
    
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
    
    except IntegrityError as e:
      db.session.rollback()
      print("Already exists")
      print(e)
      raise e
    except Exception as e:
      print(e)
      db.session.rollback()
      raise e
    
  def do_action(self, action, picture_path=None):
    
    target_type = self.type.lower()
    if target_type == "telegram":
      channel_id = self.matter_id.split(".")[1]
      message = "Alert ! Patient needs help ! \n To stop the alert, type /stop"
      alert_scheduler.start_alert(channel_id, message, picture_path)
      print("Action: " + action)
      return True
    
 
    if HOMEASSISTANT_OFFLINE_MODE:
      print("HOMEASSISTANT_OFFLINE_MODE IS ENABLED")
      print("Action: " + action)
      return True
    
    try:
      device = homeassistant_client.find_entity_by_id(self.matter_id)
      if device == None:
        return False
      device.set_state(action)
      return True
    except Exception as e:
      raise e
    
  def log_device_data(self):
    yesterday_date, number_of_toggles, total_on_time, total_off_time, total_unavailable_time = homeassistant_client.get_logs_per_entity(self.matter_id)
    TargetDeviceLogs.info(self.matter_id, yesterday_date, number_of_toggles, total_on_time, total_off_time, total_unavailable_time)
    
  @staticmethod
  def find_by_id(matter_id):
    return TargetDevice.query.get(matter_id)
  
  @staticmethod
  def update_new_triggers_from_ha():
    all_ha_triggers = homeassistant_client.get_switch_media_player_targets_from_ha()
    current_triggers = db.session.query(TargetDevice.matter_id).all()
    current_triggers_ids = [t.matter_id for t in current_triggers]
    
    for trigger in all_ha_triggers:
      if trigger["entity_id"] not in current_triggers_ids:
        _type = trigger["entity_id"].split(".")[0]
        name = trigger["entity_id"]
        try:
          new_trigger = TargetDevice(matter_id=trigger["entity_id"], name=name, type=_type)
          new_trigger.create()
          print("New trigger added: " + trigger["entity_id"])
        except Exception as e:
          print(e)
          continue



  @staticmethod
  def find_all():
    (TargetDevice.update_new_triggers_from_ha() 
     if not HOMEASSISTANT_OFFLINE_MODE 
     else print("HOMEASSISTANT_OFFLINE_MODE IS ENABLED"))
    
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
