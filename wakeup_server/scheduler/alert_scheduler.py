from apscheduler.schedulers.background import BackgroundScheduler
from scheduler.alert_jobs import send_alert
import requests
from constants import TELEGRAM_BOT_TOKEN as token

class AlertScheduler:
  def __init__(self):
    self.scheduler = BackgroundScheduler()
  
  def start_alert(self, channel_id, message, picture_path: str=None):
    picture = open(picture_path, "rb") if picture_path else None
    if picture:
      requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={"chat_id": channel_id}, files={"photo": picture})

    self.add_job(lambda: send_alert(channel_id, message), 'interval', 5, channel_id)
    
  def stop_alert(self, channel_id):
    self.remove_job(channel_id)

  def add_job(self, func, trigger: str, second: int, id: str):
    self.scheduler.add_job(func, trigger, seconds=second, id=id)

  def remove_job(self, id):
    self.scheduler.remove_job(id)
    
  def get_jobs(self):
    return self.scheduler.get_jobs()

  def start(self):
    if not self.scheduler.running:
        self.scheduler.start()
    else:
        print("Scheduler is already running")

  def stop(self):
    self.scheduler.shutdown()
    


alert_scheduler = AlertScheduler()
alert_scheduler.start()