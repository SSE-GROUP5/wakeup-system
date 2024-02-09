from models.triggers_target_map import trigger_target_association
from models.triggers_target_map import signal_to_json
from db import db
import uuid

class User(db.Model):
  __tablename__ = 'users'
  
  id = db.Column(db.String(100), primary_key=True)
  gosh_id = db.Column(db.String(100), unique=True, nullable=True)
  first_name = db.Column(db.String(100), nullable=False)
  last_name = db.Column(db.String(100), nullable=True)

  def __repr__(self):
    return f"<User {self.first_name}>"

  def __init__(self, first_name, last_name, gosh_id):
    if first_name is None or first_name == "" or " " in first_name:
      raise Exception("Invalid user first_name, cannot be null, empty or contain spaces")
    if last_name is None or last_name == "" or " " in last_name:
      raise Exception("Invalid user last_name, cannot be null, empty or contain spaces")
    
    self.id = str(uuid.uuid4())
    self.first_name = first_name.strip()
    self.last_name = last_name.strip() 
    self.gosh_id = gosh_id
    
  def json(self):
    return {
      "id": self.id,
      "first_name": self.first_name,
      "last_name": self.last_name,
      "gosh_id": self.gosh_id
    }
    
  def create(self):
    try:
      db.session.add(self)
      db.session.commit()
      return True
    except Exception as e:
      print(e)
      db.session.rollback()
      raise e
    
  @staticmethod
  def find_by_id(user_id):
    return User.query.get(user_id)
  
  @staticmethod
  def find_by_gosh_id(gosh_id):
    return User.query.filter_by(gosh_id=gosh_id).first()
  
  @staticmethod
  def find_all():
    return User.query.all()
  
  @staticmethod
  def delete_by_id(user_id):
    user = User.query.get(user_id)
    if user:
      db.session.delete(user)
      db.session.commit()
      return True
    return False
  
  @staticmethod
  def update_by_id(user_id, obj):
    user = User.query.get(user_id)
    if user:
      for key, value in obj.items():
        setattr(user, key, value)
      db.session.commit()
      return True
    return False
  
  def get_signals(self):
    signals = db.session.query(trigger_target_association).filter_by(user_id=self.id).all()
    return [signal_to_json(signal) for signal in signals]