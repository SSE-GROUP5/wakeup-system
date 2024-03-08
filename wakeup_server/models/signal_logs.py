import datetime
from db import db
from sqlalchemy import Column, DateTime, Uuid, String
import uuid
from models.users import User

class SignalLogs(db.Model):
  __tablename__ = 'signal_logs'
  
  id = Column(Uuid, primary_key=True)
  signal_id = Column(Uuid)
  created_at = Column(DateTime, default=datetime.datetime.utcnow)
  signal_type = Column(String)
  patient_id = Column(String)
  
  def __init__(self, signal_id, patient_id, signal_type):
    self.id = uuid.uuid4()
    self.signal_id = signal_id
    self.created_at = datetime.datetime.utcnow()
    self.signal_type = signal_type
    self.patient_id = patient_id
   
  @staticmethod
  def info(signal_id, patient_id, signal_type):
    new_log = SignalLogs(signal_id, patient_id, signal_type)
    try:
      db.session.add(new_log)
      db.session.commit()
      return True
    except Exception as e:
      print(e)
      db.session.rollback()
      raise e
    
  @staticmethod
  def aggregate_signal_logs_by_day():
    query_result = (
        db.session.query(
          SignalLogs.signal_id,
          db.func.date(SignalLogs.created_at).label('day'),
          SignalLogs.signal_type,
          db.func.count().label('number_of_times_signalled')
        ).group_by(db.func.date(SignalLogs.created_at), SignalLogs.signal_type).all()
    )

    aggregated_info = []
    for result in query_result:
      aggregated_info.append({
        "signal_id" : result.signal_id,
        "day": result.day,
        "signal_type": result.signal_type,
        "number_of_times_signalled": result.number_of_times_signalled
      })
        
    return aggregated_info
  
  @staticmethod
  def aggregate_signal_logs_by_patient():
    query_result = (
     db.session.query(
        SignalLogs.patient_id,
        db.func.date(SignalLogs.created_at).label('day'),
        db.func.group_concat(SignalLogs.signal_type).label('patient_signals')
     ).group_by(SignalLogs.patient_id, db.func.date(SignalLogs.created_at)).all()
    )
    
    aggregated_result = []

    for result in query_result:
      patient = User.find_by_id(result.patient_id)
      signal_type_list = result.patient_signals.split(',')

      output_row = {
        "day": result.day,
        "patientFirstName": patient.first_name,
        "patientLastName": patient.last_name,
        "patient_gosh_id": patient.gosh_id,
      }

      signal_type_counts = {}
      for signal_type in signal_type_list:
        signal_type_counts[signal_type] = signal_type_counts.get(signal_type,0) + 1

      combined_signals = []
      for signal_type, count in signal_type_counts.items():
        combined_signals.append(f"{signal_type}:{count}")

      output_row["patient_signals"] = ",".join(combined_signals)
      aggregated_result.append(output_row)

    return aggregated_result


     
    