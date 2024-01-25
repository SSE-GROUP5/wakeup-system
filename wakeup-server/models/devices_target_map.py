from sqlalchemy import Table, Column, String, ForeignKey
from db import db

# Define the junction table
interactive_target_association = Table('interactive_target_association', db.Model.metadata,
  Column('interactive_device_id', String, ForeignKey('interactive_devices.id'), primary_key=True),
  Column('interactive_action', String, primary_key=True),
  Column('target_device_id', String, ForeignKey('target_devices.matter_id'), primary_key=True),
  Column('target_action', String)
)

