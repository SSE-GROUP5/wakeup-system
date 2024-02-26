from apscheduler.schedulers.background import BackgroundScheduler
from models.target_devices import TargetDevice

class LogScheduler:
    def __init__(self, app):
        self.scheduler = BackgroundScheduler()
        self.app = app

    def add_target_device_logs_to_db(self):
        with self.app.app_context():
            devices = TargetDevice.find_all()
            for device in devices:
                device.log_device_data()

    def start_logging(self):
        self.scheduler.add_job(self.add_target_device_logs_to_db, 'cron', hour=0, minute=0)

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()
        else:
            print("Scheduler is already running")

