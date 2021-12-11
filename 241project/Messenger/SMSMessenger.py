from twilio.rest import Client

class SMSMessenger:
    def __init__(self):
       account_sid = "AC91b510c8bac23819b49e3edf5f535423" # Your Account SID from www.twilio.com/console
       auth_token  = "e838ea682649c1eb4539facc5368c90d"  # Your Auth Token from www.twilio.com/console
       self.client = Client(account_sid, auth_token)
       self.phone_number = '+15099564805'

    def send_message(self, body, to, media_url=[]):
        message = self.client.messages.create(body=body, to=to, from_=self.phone_number, media_url=media_url)
