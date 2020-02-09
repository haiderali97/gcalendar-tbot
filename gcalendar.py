import pickle
import os
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from eventHelper import eventHelper


class gCalendar:
    def __init__(self,secretFile='client_secret.json',timezone = None):              
        if not os.path.exists('token.pkl'):
            scopes = ['https://www.googleapis.com/auth/calendar']
            flow = InstalledAppFlow.from_client_secrets_file(secretFile, scopes=scopes)
            credentials = flow.run_console()
            pickle.dump(credentials, open("token.pkl", "wb"))
    
        credentials = pickle.load(open("token.pkl", "rb"))
        self.service = build("calendar", "v3", credentials=credentials)
        self.timezone = timezone
        self.eHelper = eventHelper(timezone)
        self.calendarID = 'primary'

    # By default the primary calendar is used, use this method to change to whatever calendar is required
    def setCalendarID(self,id):
        self.calendarID = id

    # Get all events for today - the results are sorted by startTime   
    def getEvents(self,startDate,endDate):        
        return self.service.events().list(
            calendarId=self.calendarID, 
            timeZone=self.timezone, 
            timeMin=startDate, 
            timeMax=endDate,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
    def getEventsTomorrow(self):
        return self.service.events().list(
            calendarId=self.calendarID, 
            timeZone=self.timezone, 
            timeMin=self.ed.getDate('add',1), 
            timeMax=self.ed.getDate('add',2),
            singleEvents=True,
            orderBy="startTime"
        ).execute()

    def getEventsYesterday(self):
        return self.service.events().list(
            calendarId=self.calendarID, 
            timeZone=self.timezone, 
            timeMin=self.ed.getDate('sub',2), 
            timeMax=self.ed.getDate(),
            singleEvents=True,
            orderBy="startTime"
        ).execute()        


