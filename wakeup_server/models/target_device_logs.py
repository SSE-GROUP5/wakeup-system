from db import db
from sqlalchemy import Column, Uuid, Integer, Date, String
import uuid

class TargetDeviceLogs(db.Model):
  __tablename__ = 'target_device_logs'
  
  id = Column(Uuid, primary_key=True)
  target_device = Column(String)
  day = Column(Date)
  number_of_toggles = Column(Integer)
  on_time = Column(String)
  off_time = Column(String)
  unavailable_time = Column(String)
  
  def __init__(self, target_device, day, number_of_toggles, on_time, off_time, unavailable_time):
    self.id = uuid.uuid4()
    self.target_device = target_device
    self.day = day
    self.number_of_toggles = number_of_toggles
    self.on_time = on_time
    self.off_time = off_time
    self.unavailable_time = unavailable_time

  @staticmethod
  def info(target_device, day, number_of_toggles, on_time, off_time, unavailable_time):
    new_log = TargetDeviceLogs(target_device, day, number_of_toggles, on_time, off_time, unavailable_time)
    try:
      db.session.add(new_log)
      db.session.commit()
      return True
    except Exception as e:
      print(e)
      db.session.rollback()
      raise e