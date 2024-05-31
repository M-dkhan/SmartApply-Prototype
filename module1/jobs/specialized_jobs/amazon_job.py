from .base_job import BaseJob
import firebase_admin
from firebase_admin import credentials, firestore
from twilio.rest import Client

class AmazonJob(BaseJob):
    
    def __init__(self, title, url, role_type, description, location, job_id, collectionName,due_date=None):
        
        super().__init__(title, url, role_type, description, location, due_date, collectionName)
        self.job_id = job_id
        
        # before creating the database object first checkif the job already exisits 
        if not self.check_document_existence('job_id', job_id):
            self.add_document({
                'title': title,
                'url': url,
                'description': description,
                'location': location,
                'job_id': job_id,
                'due_date': due_date,
                'timestamp': self.createdOn
            })

            # send a message whenever there is a new job posting
            job_message_template = f"""
                                    Title: {title}
                                    URL: {url}
                                    Description: {description}
                                    Location: {location}
                                    Job ID: {job_id}
                                    Due Date: {due_date}
                                    """
            
            # send a sms message for a latest job post 
            sentMessage = self.twilioClient.sendSMSMessage(self.twilioClient.fromPhoneNumber,self.twilioClient.toPhoneNumber, job_message_template)
            
            
            # send a sms on whatsapp for the latest job post 
            # sentwhatsappMessage = self.twilioClient.sendWhatsappMessage(self.twilioClient.fromPhoneNumber,self.twilioClient.toPhoneNumber, job_message_template)
            
            print(sentMessage) 

    def display(self):
        base_info = super().display()
        return f"{base_info}"
    
    
