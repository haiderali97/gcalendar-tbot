import pickle
import os
import sys
from pprint import pprint
from bot import Bot
from eventDate import eventDate
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


scopes = ['https://www.googleapis.com/auth/calendar']
tz = "Asia/Kolkata"
ed = eventDate(tz)
bot = Bot('735017680:AAESxPqvkT0UIv5pXrBmxG4QFyY-OyxroxM')

def prettify(event):
    msg = "----EVENT ALERT----\n\nEvent name: *{}*\n\nEvent Description : {}\n\nStart Time: *{}*\n\nEnd Time: *{}*\n\n[View More Info]({})"
    if "description" not in event:
        description = ''
    else:
        description = "*{}*".format(event['description'])
    return msg.format(
        event['summary'],
        description,
        ed.humanize(event['start']['dateTime']),
        ed.humanize(event['end']['dateTime']),
        event['htmlLink']
    )

###
###  If token doesnt already exist, authenticate and save token
###
if not os.path.exists('token.pkl'):
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
    credentials = flow.run_console()
    pickle.dump(credentials, open("token.pkl", "wb"))

credentials = pickle.load(open("token.pkl", "rb"))
service = build("calendar", "v3", credentials=credentials)

result = service.calendarList().list().execute()
cal_id = result['items'][0]['id']

###
### GET EVENTS OF TODAY
###
result = service.events().list(calendarId=cal_id, timeZone=tz, timeMin=ed.today(), timeMax=ed.tomorrow(),singleEvents=True,orderBy="startTime").execute()


for event in result['items']:            
    bot.sendMessage(prettify(event))

sys.exit()




