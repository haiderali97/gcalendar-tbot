import pytz
from datetime import datetime, date, time, timedelta
tz = pytz.timezone("Australia/Melbourne")

x = '2020-02-05T00:00:00+05:30'
x = x[:19]

x = datetime.strptime(x,"%Y-%m-%dT%H:%M:%S")
x = x.strftime("%I:%M")
print(x)