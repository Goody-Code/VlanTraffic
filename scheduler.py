import schedule
import time
from app import send_telegram_report

BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
CHAT_ID = 'YOUR_CHAT_ID_HERE'

def daily_report():
    send_telegram_report('daily', BOT_TOKEN, CHAT_ID)

def weekly_report():
    send_telegram_report('weekly', BOT_TOKEN, CHAT_ID)

def monthly_report():
    send_telegram_report('monthly', BOT_TOKEN, CHAT_ID)

schedule.every().day.at("08:00").do(daily_report)
schedule.every().monday.at("08:00").do(weekly_report)
schedule.every(1).month.do(monthly_report)

while True:
    schedule.run_pending()
    time.sleep(1)
