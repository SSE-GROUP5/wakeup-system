from sqlalchemy import Column, String, insert
from models.triggers_target_map import signal_to_json, trigger_target_association
from models.users import User
from db import db
from zmq_client import zmq_client
from constants import DEV_MODE
from sqlalchemy.exc import NoResultFound
import uuid

class Trigger(db.Model):
  __tablename__ = 'triggers'
  
  id = Column(String, primary_key=True)
  name = Column(String)
  type = Column(String)
  confirmed = Column(db.Boolean, default=False)
  target_devices = db.relationship("TargetDevice", secondary=trigger_target_association, back_populates="triggers")
  
  def __init__(self, device_id, name, device_type):
    self.id = device_id
    self.name = name
    self.type = device_type
    self.targets = self.get_targets()
    
  def create(self):
    try:
        stmt = insert(Trigger).values(id=self.id, name=self.name, type=self.type)
        db.session.execute(stmt)
        db.session.commit()
    except Exception as e:
        print(e)
        raise e
  
  def confirm(self):
    self.confirmed = True
    db.session.commit()
  
  def json(self):
    return {
      "id": self.id,
      "name": self.name,
      "type": self.type,
      "confirmed": self.confirmed,
      "targets": self.get_targets()
    }
  
  @staticmethod
  def find_by_id(device_id):
    return db.session.query(Trigger).filter_by(id=device_id).first()
  
  @staticmethod
  def find_by_name(device_name):
    return db.session.query(Trigger).filter_by(name=device_name).first()
  
  @staticmethod
  def find_all():
    return db.session.query(Trigger).all()
  
  @staticmethod
  def delete_by_id(device_id):
    device = db.session.query(Trigger).filter_by(id=device_id).first()
    if device:
      db.session.delete(device)
      db.session.commit()
      return True
    return False
  
  @staticmethod
  def update_by_id(device_id, device_name, device_type):
    device = db.session.query(Trigger).filter_by(id=device_id).first()
    if device:
      device.type = device_type
      device.name = device_name
      db.session.commit()
      return True
    return False
  
  def get_targets(self):
    targets = db.session.query(trigger_target_association).filter_by(trigger_id=self.id).all()
    return {target.trigger_action: {'id': target.target_device_id, 'action': target.target_action, 'user_id': target.user_id} for target in targets}
  
  def get_targets_per_device(self, action, num_actions, user_id=None):
    targets = db.session.query(trigger_target_association).filter_by(trigger_id=self.id, trigger_action=action, trigger_num_actions=num_actions, user_id=user_id).all()
    return [{'matter_id': target.target_device_id, 'action': target.target_action, 'user_id': target.user_id} for target in targets]
  
  def get_signals(self):
    signals = db.session.query(trigger_target_association).filter_by(trigger_id=self.id).all()
    return [signal_to_json(signal) for signal in signals]
  
  def get_signal(self, action, num_actions, target_device_id, user_id=None):
    signal = db.session.query(trigger_target_association).filter_by(trigger_id=self.id, trigger_action=action, trigger_num_actions=num_actions, target_device_id=target_device_id, user_id=user_id).first()
    return signal_to_json(signal)
  
  def add_target(self, action, num_actions, target_device_id, target_action, user_id=None):
    
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
    else:
      print("Warning: ZMQ Client inactive in Dev Mode")
      
    is_already_set = db.session.query(trigger_target_association).filter_by(
          trigger_id=self.id, 
          trigger_action=action,
          trigger_num_actions=num_actions,
          target_device_id=target_device_id,
          user_id=user_id,
    ).first()
    
    if is_already_set:
        update_signal = trigger_target_association.update(
        ).where(
          trigger_target_association.c.id == is_already_set.id
        ).values(
          trigger_id=self.id,
          trigger_action=action,
          trigger_num_actions=num_actions,
          target_device_id=target_device_id,
          target_action=target_action,
          user_id=user_id
        )
        db.session.execute(update_signal)
    else:
        new_signal = trigger_target_association.insert().values(
            id=uuid.uuid4(),
            trigger_id=self.id,
            trigger_action=action,
            trigger_num_actions=num_actions,
            target_device_id=target_device_id,
            target_action=target_action,
            user_id=user_id
          )
        db.session.execute(new_signal)
        
    db.session.commit()
    
    new_signal = db.session.query(trigger_target_association).filter_by(
        trigger_id=self.id, 
        trigger_action=action, 
        target_device_id=target_device_id, 
        trigger_num_actions=num_actions, 
        user_id=user_id
      ).first()
    return signal_to_json(new_signal)
  
  def remove_target(self, action):
    delete_target = trigger_target_association.delete().where(trigger_target_association.c.trigger_id == self.id).where(trigger_target_association.c.trigger_action == action)
    db.session.execute(delete_target)
    db.session.commit()


