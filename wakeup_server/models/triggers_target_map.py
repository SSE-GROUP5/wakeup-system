from sqlalchemy import Table, Column, String, ForeignKey, Uuid, UniqueConstraint, Integer
from db import db

# Define the junction table
trigger_target_association = Table('trigger_target_association', db.Model.metadata,
  Column('id', Uuid, primary_key=True),
  Column('trigger_id', String, ForeignKey('triggers.id')),
  Column('trigger_action', String),
  Column('trigger_num_actions', Integer),
  Column('target_device_id', String, ForeignKey('target_devices.matter_id')),
  Column('target_action', String),
  Column('user_id', String, ForeignKey('users.id'), nullable=True),
  UniqueConstraint('trigger_id', 'trigger_action', 'trigger_num_actions', 'target_device_id', 'target_action', 'user_id', name='unique_constraint')
)

def signal_to_json(signal):
  from models.triggers import Trigger
  trigger = db.session.query(Trigger).filter_by(id=signal.trigger_id).first()
  return {
    'id': signal.id,
    'trigger_id': signal.trigger_id,
    'trigger_action': signal.trigger_action,
    'trigger_name': trigger.name,
    'trigger_num_actions': signal.trigger_num_actions,
    'target_id': signal.target_device_id,
    'target_action': signal.target_action,
    'user_id': signal.user_id if signal.user_id is not None else None
  }

def delete_signal_from_map(signal_to_be_deleted):
    signal = db.session.query(trigger_target_association).filter_by(id=signal_to_be_deleted)
    if signal.first() is None:
      return False
    try:
      signal.delete()
      db.session.commit()
      return True
    except Exception as e:
      db.session.rollback()
      print(e)
      return False
    