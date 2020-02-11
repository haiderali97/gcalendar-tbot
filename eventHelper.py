# Helper methods to generate keyboard, prettify responses

import pytz
from datetime import datetime, date, time, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import calendar 

class eventHelper:
    def __init__(self,tz):        
        self.tz = pytz.timezone(tz)              
    
    ##Create a human readable time format for messages 
    def __humanizeForMessage(self,date):
        date = date[:19]
        date = datetime.strptime(date,"%Y-%m-%dT%H:%M:%S")
        return date.strftime("%b %d at %I:%M%p")

    #Creates current timestamp for use with google calendar api
    #This function is used to create a timestamp for recurring events
    def createTime(self,minutes = None):
        now = datetime.now()
        now = now.replace(microsecond=0)
        if minutes is not None: 
            now += timedelta(minutes=minutes)
        return self.tz.localize(now).isoformat()

    #Creates a datetime string with time set to midnight for use with the google calendar api 
    def createDate(self,year=None,month=None,day=None,opt=None,days=None):
        now = datetime.now()

        if month is None:
            month = now.month
        if year is None:
            year = now.year 
        if day is None:
            day = now.day
        dt = self.tz.localize(datetime(year,month,day)) 
        if opt == "add":
            dt += timedelta(days = days)
        if opt == "sub":
            dt += timedelta(days = days)        
        return dt.isoformat()

    # stuff
    @staticmethod
    def getMonthName(month=None):
        if month is None:
            month = datetime.now().month 
        return calendar.month_name[month]

    def prepareEventsMessage(self,events): 
        msg = "-------EVENTS------\n\n"     
        for x in events:
            description = x['description'] if "description" in x else None 
            msg += (                
                f"Event Name: {x['summary']}\n\n"
                f"Event Description: {description}\n\n"
                f"Starts at: {self.__humanizeForMessage(x['start']['dateTime'])}\n\n"
                f"Ends at: {self.__humanizeForMessage(x['end']['dateTime'])}\n\n"
                "-------------------------\n\n"
            )            
        return msg

    # Returns an inline keyboard with dates for a specified month and year 
    # The month attribute is used to calculate whether February is a leap year    
    def generateDayCalendar(self,month=None,year=None):
        if month is None:
            month = datetime.now().month
        if year is None:
            year = datetime.now().year 
        
        if month in [4,6,9,11]:
            end = 31
        elif month in [1,3,5,7,8,10,12]:
            end = 32
        else:
            #check if leap year 
            if (year % 4 == 0):
                end = 30
            else:
                end = 29        
        dates = [InlineKeyboardButton(str(x).zfill(2), callback_data = "dayevent_{}_{}".format(self.createDate(year,month,x),self.createDate(year,month,x,opt='add',days=1)) ) for x in range(1,end)]
        n = 6 
        dates = [dates[i * n:(i + 1) * n] for i in range((len(dates) + n - 1) // n )] 
        return InlineKeyboardMarkup(dates)



