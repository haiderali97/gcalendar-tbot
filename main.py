import sys
import logging
import calendar
import schedule 
import time
from configparser import ConfigParser
from pprint import pprint
from gcalendar import gCalendar
from eventHelper import eventHelper
from telegram import ParseMode
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
    #Stop execution if time is same as the time to run sendTodaysEvents
    if(eHelper.getCurrentTime() == config['EVENTS']['SendDailyTime']):
        return 

    print("Running event scan")    
    startDate = eHelper.createTime()
    endDate = eHelper.createTime(config.getint('EVENTS','RecurringTimespan'))    
    events = gCal.getEvents(startDate=startDate,endDate=endDate)['items']    
    if len(events) >= 1:
        print('running send')
        msg = eHelper.prepareEventsMessage(events)
        updater.bot.sendMessage(chat_id=config['DEFAULT']['GroupID'],text=msg)

#Generates a calendar for the current month
def dayCalendar(update,context): 
    try:
        month = (int(update.callback_query.data.split('_')[1]))
        replyMarkup = eHelper.generateDayCalendar(month)
        month = eHelper.getMonthName(month)
    except AttributeError:
        replyMarkup = eHelper.generateDayCalendar()
        month = eHelper.getMonthName()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"These are the dates for {month}.\nPick a date for which you would like to see the events of.",
        reply_markup=replyMarkup)

def monthCalendar(update,context):    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Pick a month!",
        reply_markup=eHelper.generateMonthCalendar())        

def setCalendar(update, context):
    calendars = gCal.getCalendars()    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Pick a calendar", 
        reply_markup=eHelper.generateCalendarOptions(calendars)     
    )

def setCalendarID(update, context):
    query = update.callback_query 
    data = query.data.split('_')
    gCal.setCalendarID(data[1])
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Your calendar has changed to {data[1]}."        
    )

#Gets the events of a particular day and sends it
def sendDayEvent(update, context):
    query = update.callback_query     
    month,date = [int(x) for x in query.data.split('_')[1:3]]
    startDate = eHelper.createDate(month=month,day=date)
    endDate = eHelper.createDate(month=month,day=date,opt='add',days=1)    
    events = gCal.getEvents(startDate,endDate)['items']
    msg = eHelper.prepareEventsMessage(events) if len(events) >= 1 else "There are no events for this date"
    query.edit_message_text(text=msg,reply_markup=eHelper.generateDayCalendar(month=month),parse_mode='Markdown')



    

dispatcher.add_handler(CommandHandler('dayCalendar',dayCalendar))
dispatcher.add_handler(CommandHandler('monthCalendar',monthCalendar))
dispatcher.add_handler(CommandHandler('setCalendar',setCalendar))
dispatcher.add_handler(CallbackQueryHandler(dayCalendar,pattern="^monthCalendar"))
dispatcher.add_handler(CallbackQueryHandler(setCalendarID,pattern="^sc"))
dispatcher.add_handler(CallbackQueryHandler(sendDayEvent,pattern="^dayevent"))

if(config['EVENTS']['SendDaily'] == '1'):
    schedule.every().day.at(config['EVENTS']['SendDailyTime']).do(sendTodaysEvents)

if(config['EVENTS']['SendRecurring'] == '1'):
    schedule.every(config.getint('EVENTS','RecurringInterval')).minutes.do(sendRecurringEvents)


""" TESTING """
# def mock_run_pending():
#     sendRecurringEvents()

# def mock_time_sleep(num):
#     exit()

# schedule.run_pending = mock_run_pending
# time.sleep = mock_time_sleep

updater.start_polling()
while True:
    schedule.run_pending()
    time.sleep(1)







