import sys
import logging
import calendar
from pprint import pprint
from gcalendar import gCalendar
from eventDate import eventDate
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

group_id = -390942838
#cal = gCalendar(timezone='Asia/Kolkata')

updater = Updater(token='735017680:AAESxPqvkT0UIv5pXrBmxG4QFyY-OyxroxM', use_context=True)
dispatcher = updater.dispatcher

def monthEvents(update,context):    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="These are the dates for {}.\nPick a date for which you would like to see the events of.".format(eventDate.getMonthName()),
        reply_markup=eventDate.generateCalendar())

def callback(update, context):
    query = update.callback_query
    args = query.data.split('_')
    handle = args[0]
    if handle == 'dayevent':
        sendDayEvent(update,context)


def sendDayEvent(update, context):
    query = update.callback_query 
    args = query.data.split('_')
    date, month, year = [ args[i] for i in (1,2,3) ]
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text="{} {} {}".format(date,month,year)
    )

dispatcher.add_handler(CommandHandler('monthEvents',monthEvents))
dispatcher.add_handler(CallbackQueryHandler(sendDayEvent,pattern="^dayevent"))

updater.start_polling()
updater.idle()