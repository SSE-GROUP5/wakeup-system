from sqlalchemy import Column, String, insert
from models.devices_target_map import interactive_target_association
from db import db
from zmq_client import zmq_client

devMode = False #Set to developer mode as necessary

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
    return {target.interactive_action: {'id': target.target_device_id, 'action': target.target_action} for target in targets}
  
  def get_target(self, action):
    target = db.session.query(interactive_target_association).filter_by(interactive_device_id=self.id, interactive_action=action).first()
    return {'matter_id': target.target_device_id, 'action': target.target_action}
  
  def get_signals(self):
    signals = db.session.query(interactive_target_association).filter_by(interactive_device_id=self.id).all()
    return [{'interactive_id': signal.interactive_device_id, 'interactive_action': signal.interactive_action, 'target_id': signal.target_device_id, 'target_action': signal.target_action} for signal in signals]
  
  def add_target(self, action, target_device_id, target_action):
    if(devMode == False):
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
    ).first()
    
    if is_already_set:
        update_target = interactive_target_association.update().where(interactive_target_association.c.interactive_device_id == self.id).where(interactive_target_association.c.interactive_action == action).values(target_device_id=target_device_id, target_action=target_action)
        db.session.execute(update_target)
    else:
        new_target = interactive_target_association.insert().values(interactive_device_id=self.id, interactive_action=action, target_device_id=target_device_id, target_action=target_action)
        db.session.execute(new_target)
    db.session.commit()
  
  def remove_target(self, action):
    delete_target = interactive_target_association.delete().where(interactive_target_association.c.interactive_device_id == self.id).where(interactive_target_association.c.interactive_action == action)
    db.session.execute(delete_target)
    db.session.commit()


