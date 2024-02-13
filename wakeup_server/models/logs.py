import datetime
from db import db
from sqlalchemy import Column, DateTime, Uuid
import uuid

class SignalLogs(db.Model):
  __tablename__ = 'signal_logs'
  
  id = Column(Uuid, primary_key=True)
  signal_id = Column(Uuid)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  
  def __init__(self, signal_id):
    self.id = uuid.uuid4()
    self.signal_id = signal_id
    self.created_at = datetime.datetime.utcnow()

    
  @staticmethod
  def info(signal_id):
    new_log = SignalLogs(signal_id)
    try:
      db.session.add(new_log)
      db.session.commit()
      return True
    except Exception as e:
      print(e)
      db.session.rollback()
      raise e