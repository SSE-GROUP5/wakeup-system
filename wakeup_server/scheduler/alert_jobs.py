import requests
from constants import TELEGRAM_BOT_TOKEN as token

def send_alert(channel_id: str, message: str):
  data = {
    "chat_id": channel_id,
    "text": message,
  }
  requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data=data)
