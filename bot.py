import requests

class Bot:

    def __init__(self,token):        
        self.uri = "https://api.telegram.org/bot"+token+"/" 
        

    def sendMessage(self,msg):
        payload = {'chat_id' : -390942838,'text':msg,'parse_mode':'Markdown'}
        uri = self.uri+"sendMessage"        
        res = requests.get(uri,params=payload)
        