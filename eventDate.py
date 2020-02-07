import pytz
from datetime import datetime, date, time, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import calendar 
class eventDate:
    def __init__(self,tz = None):        
        if tz is not None:
            self.tz = pytz.timezone(tz) 
        else:
            self.tz = None               

        
    def humanize(self,d,format):        
        x = datetime.strptime(string[:19],"%Y-%m-%dT%H:%M:%S")
        return x.strftime(format)
    
    def getDate(self,op=None,num=None):
        if op is not None:
            if op == 'add':
                cdate = datetime.combine(date.today(),time()).astimezone(self.tz) + timedelta(days = num)
            if op == 'sub':
                cdate = datetime.combine(date.today(),time()).astimezone(self.tz) - timedelta(days = num)
        else:
            cdate = cdate = datetime.combine(date.today(),time()).astimezone(self.tz)
        return cdate.isoformat()

    @staticmethod
    def getMonthName(month=None):
        if month is None:
            month = datetime.now().month 
        return calendar.month_name[month]

    # Returns an inline keyboard with dates for a specified month and year 
    # The month attribute is used to calculate whether February is a leap year
    @staticmethod
    def generateCalendar(month=None,year=None):
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
        dates = [InlineKeyboardButton(str(x).zfill(2),callback_data=str('dayevent_{}-{}-{}').format(year,month,x)) for x in range(1,end)]
        n = 6 
        dates = [dates[i * n:(i + 1) * n] for i in range((len(dates) + n - 1) // n )] 
        return InlineKeyboardMarkup(dates)



