import sys
import logging
import calendar
import schedule 
import time
from configparser import ConfigParser
from pprint import pprint
from gcalendar import gCalendar
from eventHelper import eventHelper
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
config = ConfigParser()
config.read('config.ini')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
 
# Initialize the classes We're going to be using 
eHelper = eventHelper(config['DEFAULT']['Timezone'])
gCal = gCalendar(timezone=config['DEFAULT']['Timezone'])
updater = Updater(token=config['DEFAULT']['BotToken'], use_context=True)
dispatcher = updater.dispatcher


#This function is called with a scheduler and sends all of todays events
def sendTodaysEvents():
    print("Doing today's events")
    events = gCal.getEvents(
        startDate=eHelper.createDate(),
        endDate=eHelper.createDate(opt='add',days=1)
        )['items']
    if(len(events)):
        msg = eHelper.prepareEventsMessage(events) 
    else:
        msg = "There are no events scheduled for today."
    updater.bot.sendMessage(chat_id=group_id,text=msg)

#This function is called with a scheduler reccuringly to send events of today within a timespan
def sendRecurringEvents(): 
    startDate = eHelper.createTime()
    endDate = eHelper.createTime(config.getint('EVENTS','RecurringTimespan'))    
    events = gCal.getEvents(startDate=startDate,endDate=endDate)['items']    
    if len(events) >= 1:
        print('running send')
        msg = eHelper.prepareEventsMessage(events)
        updater.bot.sendMessage(chat_id=config['DEFAULT']['GroupID'],text=msg)

#Generates a calendar for the current month
def dayEvents(update,context):    
    context.bot.send_message(
        chat_id=config['DEFAULT']['GroupID'],
        text="These are the dates for {}.\nPick a date for which you would like to see the events of.".format(eHelper.getMonthName()),
        reply_markup=eHelper.generateDayCalendar())

#Gets the events of a particular day and sends it
def sendDayEvent(update, context):
    query = update.callback_query 
    date = query.data.split('_')
    events = gCal.getEvents(date[1],date[2])['items']  
    pprint(events)  
    if(len(events)):
        msg = eHelper.prepareEventsMessage(events) 
    else:
        msg = "There are no events scheduled for this date."    
    query.edit_message_text(text=msg,reply_markup=eHelper.generateDayCalendar())

    
    

dispatcher.add_handler(CommandHandler('dayEvents',dayEvents))
dispatcher.add_handler(CallbackQueryHandler(sendDayEvent,pattern="^dayevent"))

if(config['EVENTS']['SendDaily'] == '1'):
    schedule.every().day.at(config['EVENTS']['SendDailyTime']).do(sendTodaysEvents)

if(config['EVENTS']['SendRecurring'] == '1'):
    schedule.every(config.getint('EVENTS','RecurringInterval')).minutes.do(sendRecurringEvents)


""" TESTING """
def mock_run_pending():
    sendRecurringEvents()

def mock_time_sleep(num):
    exit()

schedule.run_pending = mock_run_pending
time.sleep = mock_time_sleep

updater.start_polling()
while True:
    schedule.run_pending()
    time.sleep(1)







