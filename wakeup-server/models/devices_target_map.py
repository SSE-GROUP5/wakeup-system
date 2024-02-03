from sqlalchemy import Table, Column, String, ForeignKey, Uuid, UniqueConstraint, Integer
from db import db

# Define the junction table
interactive_target_association = Table('interactive_target_association', db.Model.metadata,
  Column('id', Uuid, primary_key=True),
  Column('interactive_device_id', String, ForeignKey('interactive_devices.id')),
  Column('interactive_action', String),
  Column('interactive_device_num_actions', Integer),
  Column('target_device_id', String, ForeignKey('target_devices.matter_id')),
  Column('target_action', String),
  Column('user_id', String, ForeignKey('users.id'), nullable=True),
  UniqueConstraint('interactive_device_id', 'interactive_action', 'interactive_device_num_actions', 'target_device_id', 'target_action', 'user_id', name='unique_constraint')
)

def signal_to_json(signal):
  return {
    'id': signal.id,
    'interactive_id': signal.interactive_device_id,
    'interactive_action': signal.interactive_action,
    'interactive_device_num_actions': signal.interactive_device_num_actions,
    'target_id': signal.target_device_id,
    'target_action': signal.target_action,
    'user_id': signal.user_id if signal.user_id is not None else None
  }
