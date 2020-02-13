import sys
import logging
import calendar
import schedule 
import time
import config as cfg
from pprint import pprint
from gcalendar import gCalendar
from eventHelper import eventHelper
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
 
eHelper = eventHelper(cfg.timeZone)
gCal = gCalendar(timezone=cfg.timeZone)
updater = Updater(token=cfg.botToken, use_context=True)
dispatcher = updater.dispatcher

#Checks for events at XX:YY Every day and fetches the events for the entire day
def sendTodaysEvents():    
    events = gCal.getEvents(
        startDate=eHelper.createDate(),
        endDate=eHelper.createDate(opt='add',days=1)
        )['items']
    msg = eHelper.prepareEventsMessage(events) if len(events) >= 1 else "There are no events scheduled for today"
    updater.bot.sendMessage(chat_id=group_id,text=msg)

#Checks for events every X minutes within Y timespan
def sendRecurringEvents(): 
    #Stop execution if time is same as the time to run sendTodaysEvents
    #I should probably add a check to see if SendDaily is enabled, otherwise this check doesn't really 
    #Matter does it?
    if(eHelper.getCurrentTime() == config['EVENTS']['SendDailyTime']):
        return     
    startDate = eHelper.createTime()
    endDate = eHelper.createTime(cfg.sendRecurringTimespan)    
    events = gCal.getEvents(startDate=startDate,endDate=endDate)['items']    
    if len(events) >= 1:        
        msg = eHelper.prepareEventsMessage(events)
        updater.bot.sendMessage(chat_id=config['DEFAULT']['GroupID'],text=msg)

#dayCalendar command handler. Generates a keyboard of dates for specified month(or current month)
def dayCalendar(update,context): 
    try:
        month = (int(update.callback_query.data.split('_')[1]))
        replyMarkup = eHelper.generateDayCalendar(month)
        month = eHelper.getMonthName(month)
    except AttributeError:
        replyMarkup = eHelper.generateDayCalendar()
        month = eHelper.getMonthName()
    msg=f"These are the dates for {month}.\nPick a date for which you would like to see the events of."
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg,
        reply_markup=replyMarkup)

#monthCalendar command handler. Generates a keyboard of months
def monthCalendar(update,context):    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Pick a month!",
        reply_markup=eHelper.generateMonthCalendar())        

#setCalendar command handler . Generates a keyboard of available calendars in the google account
def setCalendar(update, context):
    calendars = gCal.getCalendars()    
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Pick a calendar", 
        reply_markup=eHelper.generateCalendarOptions(calendars)     
    )

# Changes the calendar ID in gCal instance
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

if(cfg.sendDaily == 1):
    schedule.every().day.at(cfg.sendDailyTime).do(sendTodaysEvents)

if(cfg.sendRecurring == 1):
    schedule.every(cfg.sendRecurringInterval).minutes.do(sendRecurringEvents)

print(schedule.jobs)
updater.start_polling()
while True:
    schedule.run_pending()
    time.sleep(1)







