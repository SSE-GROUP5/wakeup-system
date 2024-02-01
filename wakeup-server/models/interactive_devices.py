from sqlalchemy import Column, String, insert
from models.devices_target_map import signal_to_json, interactive_target_association
from models.users import User
from db import db
from zmq_client import zmq_client
from constants import DEV_MODE
from sqlalchemy.exc import NoResultFound
import uuid

class InteractiveDevice(db.Model):
  __tablename__ = 'interactive_devices'
  
  id = Column(String, primary_key=True)
  type = Column(String)
  target_devices = db.relationship("TargetDevice", secondary=interactive_target_association, back_populates="interactive_devices")
  
  def __init__(self, device_id, device_type):
    self.id = device_id
    self.type = device_type
    self.targets = self.get_targets()
    
  def create(self):
    try:
        stmt = insert(InteractiveDevice).values(id=self.id, type=self.type)
        db.session.execute(stmt)
        db.session.commit()
    except Exception as e:
        print(e)
        raise e
  
  
  def json(self):
    return {
      "id": self.id,
      "type": self.type,
      "targets": self.get_targets()
    }
  
  @staticmethod
  def find_by_id(device_id):
    return db.session.query(InteractiveDevice).filter_by(id=device_id).first()
  
  @staticmethod
  def find_all():
    return db.session.query(InteractiveDevice).all()
  
  @staticmethod
  def delete_by_id(device_id):
    device = db.session.query(InteractiveDevice).filter_by(id=device_id).first()
    if device:
      db.session.delete(device)
      db.session.commit()
      return True
    return False
  
  @staticmethod
  def update_by_id(device_id, device_type):
    device = db.session.query(InteractiveDevice).filter_by(id=device_id).first()
    if device:
      device.type = device_type
      db.session.commit()
      return True
    return False
  
  def get_targets(self):
    targets = db.session.query(interactive_target_association).filter_by(interactive_device_id=self.id).all()
    return {target.interactive_action: {'id': target.target_device_id, 'action': target.target_action, 'user_id': target.user_id} for target in targets}
  
  def get_targets_per_device(self, action, user_id=None):
    targets = db.session.query(interactive_target_association).filter_by(interactive_device_id=self.id, interactive_action=action, user_id=user_id).all()
    return [{'matter_id': target.target_device_id, 'action': target.target_action, 'user_id': target.user_id} for target in targets]
  
  def get_signals(self):
    signals = db.session.query(interactive_target_association).filter_by(interactive_device_id=self.id).all()
    return [signal_to_json(signal) for signal in signals]
  
  def add_target(self, action, target_device_id, target_action, user_id=None):
    
    if user_id is not None:
      user = db.session.query(User).filter_by(id=user_id).first()
      if user is None:
        raise NoResultFound("User not found")
    
    if(DEV_MODE == False):
      try:
        zmq_client.send_data(self.type, {"action": action})
        print("Warning: ZMQ Server needs to be started to proceed.")
        zmq_client.receive_reply()
      except Exception as e:
        print(e)
        raise e
    else:
      print("Warning: ZMQ Client inactive in Dev Mode")
      
    is_already_set = db.session.query(interactive_target_association).filter_by(
          interactive_device_id=self.id, 
          interactive_action=action,
          target_device_id=target_device_id,
          user_id=user_id,
    ).first()
    
    if is_already_set:
        update_signal = interactive_target_association.update().where(interactive_target_association.c.interactive_device_id == self.id).where(interactive_target_association.c.interactive_action == action).values(target_device_id=target_device_id, target_action=target_action)
        db.session.execute(update_signal)
    else:
        new_signal = interactive_target_association.insert().values(
            id=uuid.uuid4(),
            interactive_device_id=self.id,
            interactive_action=action,
            target_device_id=target_device_id,
            target_action=target_action,
            user_id=user_id
          )
        db.session.execute(new_signal)
        
    db.session.commit()
    
    new_signal = db.session.query(interactive_target_association).filter_by(interactive_device_id=self.id, interactive_action=action, target_device_id=target_device_id, user_id=user_id).first()
    return signal_to_json(new_signal)
  
  def remove_target(self, action):
    delete_target = interactive_target_association.delete().where(interactive_target_association.c.interactive_device_id == self.id).where(interactive_target_association.c.interactive_action == action)
    db.session.execute(delete_target)
    db.session.commit()


