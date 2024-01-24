from sqlalchemy import Column, String, insert
from models.devices_target_map import interactive_target_association
from db import db


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
  
  def add_target(self, action, target_device_id, target_action):
    new_target = interactive_target_association.insert().values(interactive_device_id=self.id, interactive_action=action, target_device_id=target_device_id, target_action=target_action)
    db.session.execute(new_target)
    db.session.commit()
  
  def remove_target(self, action):
    delete_target = interactive_target_association.delete().where(interactive_target_association.c.interactive_device_id == self.id).where(interactive_target_association.c.interactive_action == action)
    db.session.execute(delete_target)
    db.session.commit()


