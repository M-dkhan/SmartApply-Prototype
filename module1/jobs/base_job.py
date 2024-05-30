from module2.firebase_setup import FirestoreManager
from module2.twilio_setup import TwilioManager
from datetime import datetime

class BaseJob:
    def __init__(self, title, url, role_type, description, location, due_date, collectionName):
        self.title = title
        self.url = url
        self.role_type = role_type
        self.descrption = description
        self.location = location
        self.due_date = due_date
        self.db = FirestoreManager.db
        self.twilioClient = TwilioManager()
        self.collectionName = collectionName
        self.createdOn = datetime.now()


    def display(self):
        print(f"{self.title} at {self.location} is due by {self.due_date}")
        return f"{self.title} at {self.location} is due by {self.due_date}"
    
    def check_document_existence(self, key, value):
        """
        Check if a document with the specified key-value pair exists in the collection.
        """
        query = self.db.collection(self.collectionName).where(key, "==", value)
        result = query.limit(1).get()
        return bool(result)



    
    def add_document(self, data):
        """
        Add a document with specified data to the collection.
        """
        self.db.collection(self.collectionName).add(data)
