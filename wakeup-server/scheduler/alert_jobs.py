import requests
from constants import TELEGRAM_BOT_TOKEN as token

def send_alert(channel_id: str, message: str, picture_path: str = None):
  picture = open(picture_path, "rb") if picture_path else None
  data = {
    "chat_id": channel_id,
    "text": message,
  }
  requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=data)
  if picture:
      requests.post(f"https://api.telegram.org/bot{token}/sendPhoto", data={"chat_id": channel_id}, files={"photo": picture})
