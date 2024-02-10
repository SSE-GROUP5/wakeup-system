#!/usr/bin/env python
# pylint: disable=unused-argument

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
load_dotenv()
import os

class TelegramBot:
  def __init__(self, token, wakeup_server_url):
    self.token = token
    self.wakeup_server_url = wakeup_server_url
    
  async def get_channel_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_message.chat_id, text="telegram."+str(update.effective_message.chat_id))

  async def remove_job(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Remove alert job."""
    channel_id = update.effective_message.chat_id
    requests.post(f"{self.wakeup_server_url}/signals/stop_alert/{channel_id}")
    await context.bot.send_message(chat_id=update.effective_message.chat_id, text="Alert stopped")

  def start(self):
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(self.token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("stop", self.remove_job))
    application.add_handler(CommandHandler("id", self.get_channel_id))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
  token = os.getenv("TELEGRAM_BOT_TOKEN")
  wakeup_server_url = os.getenv("WAKEUP_SERVER_URL")
  if not token:
    print("Please set the TELEGRAM_BOT_TOKEN environment variable")
    exit(1)
    
  if not wakeup_server_url:
    print("Please set the WAKEUP_SERVER_URL environment variable")
    exit(1)
  bot = TelegramBot(token, wakeup_server_url)
  print("Bot started")
  bot.start()