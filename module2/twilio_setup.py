from twilio.rest import Client
import os 
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


 

class TwilioManager:

    account_sid = os.getenv("ACCOUNT_SID")
    auth_token = os.getenv("AUTH_TOKEN")
    fromPhoneNumber = os.getenv("TWILO_PHONE_NUMBER")
    toPhoneNumber = os.getenv('TO_PHONE_NUMBER') 


    client = Client(account_sid, auth_token)

    def sendSMSMessage(self, fromPhoneNumber, toPhoneNumber, body):

        message = self.client.messages.create(
                        from_=fromPhoneNumber,
                        body=body,
                        to=toPhoneNumber
                    )
        print(message)
        return message
    
    def sendWhatsappMessage(self, fromPhoneNumber, toPhoneNumber, body):

        message = self.client.messages.create(
            from_='whatsapp:' + fromPhoneNumber,
            body=body,
            to='whatsapp:' + toPhoneNumber
        )
        print(message)
        return message