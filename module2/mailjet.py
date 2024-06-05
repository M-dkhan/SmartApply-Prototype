from mailjet_rest import Client
import os
import dotenv

dotenv.load_dotenv()

mailjet_apikey = os.getenv('MAILJET_APIKEY')
mailjet_secretkey = os.getenv('MAILJET_SECRETKEY')


def sendmail(api_key=mailjet_apikey, api_secret=mailjet_secretkey, senderEmail:str ="khan.mohd.zaid.ca@gmail.com", reciptient:list =[], message: str = ''):

    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    # Construct the list of recipient dictionaries
    recipients_list = [{'Email': email} for email in reciptient]

    data = {
    'Messages': [
        {
        "From": {
            "Email": senderEmail,
            "Name": "MD"
        },
        "To": recipients_list,
        "Subject": "!!! New Amazon Job Update !!!",
        "TextPart": "",
        "HTMLPart": message,
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())