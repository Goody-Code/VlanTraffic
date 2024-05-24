import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import requests

API_URL = 'https://your-flask-api.onrender.com/vlan_note'
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
CHAT_ID = 'YOUR_CHAT_ID_HERE'

# تعيين سجل تسجيل الدخول
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# دالة لبدء البوت
def start(update, context):
    keyboard = [
        [telegram.InlineKeyboardButton("تسمية الفيلانات", callback_data='name_vlans')],
        [telegram.InlineKeyboardButton("تحديد وقت الإرسال", callback_data='set_time')]
    ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    update.message.reply_text('اختر الإجراء:', reply_markup=reply_markup)

# دالة لتنفيذ الإجراءات
def button(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'name_vlans':
        vlans = requests.get(API_URL).json()
        for vlan in vlans:
            query.message.reply_text(f"VLAN: {vlan['name']}")
    elif query.data == 'set_time':
        keyboard = [
            [telegram.InlineKeyboardButton("يوميًا", callback_data='daily')],
            [telegram.InlineKeyboardButton("أسبوعيًا", callback_data='weekly')],
            [telegram.InlineKeyboardButton("شهريًا", callback_data='monthly')],
            [telegram.InlineKeyboardButton("تحديد الكل", callback_data='all')]
        ]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        query.message.reply_text('اختر وقت الإرسال:', reply_markup=reply_markup)

def add_note(update, context):
    try:
        vlan_name = context.args[0]
        note = ' '.join(context.args[1:])
        response = requests.post(API_URL, json={'vlan_name': vlan_name, 'note': note})
        if response.status_code == 200:
            update.message.reply_text(f"Note added for VLAN {vlan_name}")
        else:
            update.message.reply_text("Failed to add note.")
    except IndexError:
        update.message.reply_text("Usage: /note <VLAN_Name> <Note>")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("note", add_note))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
