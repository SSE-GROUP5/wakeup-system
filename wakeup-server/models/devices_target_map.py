from sqlalchemy import Table, Column, String, ForeignKey
from db import db

# Define the junction table
interactive_target_association = Table('interactive_target_association', db.Model.metadata,
  Column('interactive_device_id', String, ForeignKey('interactive_devices.id')),
  Column('interactive_action', String),
  Column('target_device_id', String, ForeignKey('target_devices.matter_id')),
  Column('target_action', String)
)

