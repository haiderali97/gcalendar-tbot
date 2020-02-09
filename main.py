import sys
import logging
import calendar
import telegram.ext
import schedule
import time
import threading
from pprint import pprint
from gcalendar import gCalendar
from eventHelper import eventHelper
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler


""" CONFIGURE SOME STUFF """
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
group_id = -390942838
timezone = 'Asia/Kolkata'

""" Initialize all the things we need """ 
eHelper = eventHelper(timezone)
gCal = gCalendar(timezone='Asia/Kolkata')
updater = Updater(token='735017680:AAESxPqvkT0UIv5pXrBmxG4QFyY-OyxroxM', use_context=True)
dispatcher = updater.dispatcher


#This function is called with a scheduler and sends todays events
def sendTodaysEvents():
    events = gCal.getEvents(
        startDate=eHelper.createDate(),
        endDate=eHelper.createDate(opt='add',days=1)
        )['items']
    if(len(events)):
        msg = eHelper.prepareEventsMessage(events) 
    else:
        msg = "There are no events scheduled for today."
    updater.bot.sendMessage(chat_id=group_id,text=msg)

#Generates a calendar for the current month
def dayEvents(update,context):    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="These are the dates for {}.\nPick a date for which you would like to see the events of.".format(eHelper.getMonthName()),
        reply_markup=eHelper.generateDayCalendar())

#Gets the events of a particular day and sends it
def sendDayEvent(update, context):
    query = update.callback_query 
    date = query.data.split('_')
    events = gCal.getEvents(date[1],date[2])['items']    
    if(len(events)):
        msg = eHelper.prepareEventsMessage(events) 
    else:
        msg = "There are no events scheduled for this date."

    #context.bot.send_message(chat_id=update.effective_chat.id,text=msg,reply_markup=eHelper.generateDayCalendar(month=1))
    query.edit_message_text(text=msg,reply_markup=eHelper.generateDayCalendar())

    
    

dispatcher.add_handler(CommandHandler('dayEvents',dayEvents))
dispatcher.add_handler(CallbackQueryHandler(sendDayEvent,pattern="^dayevent"))
schedule.every(5).seconds.do(sendTodaysEvents)


updater.start_polling()
while True:
    schedule.run_pending()
    time.sleep(1)







