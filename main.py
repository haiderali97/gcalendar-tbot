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
timezone = 'Asia/Kolkata'
ed = eventDate(timezone)
gCal = gCalendar(timezone='Asia/Kolkata')

updater = Updater(token='735017680:AAESxPqvkT0UIv5pXrBmxG4QFyY-OyxroxM', use_context=True)
dispatcher = updater.dispatcher

#Generates a calendar for the current month
def dayEvents(update,context):    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="These are the dates for {}.\nPick a date for which you would like to see the events of.".format(eventDate.getMonthName()),
        reply_markup=ed.generateDayCalendar())

#Gets the events of a particular day and sends it
def sendDayEvent(update, context):
    query = update.callback_query 
    date = query.data.split('_')
    events = gCal.getEvents(date[1],date[2])
    pprint(events)
    

dispatcher.add_handler(CommandHandler('dayEvents',dayEvents))
dispatcher.add_handler(CallbackQueryHandler(sendDayEvent,pattern="^dayevent"))

updater.start_polling()
updater.idle()