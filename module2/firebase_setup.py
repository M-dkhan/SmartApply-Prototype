import firebase_admin
from firebase_admin import credentials, firestore

class FirestoreManager:
    # Initialize Firebase Admin SDK and Firestore client
    cred = credentials.Certificate("/home/zaid/SmartApply-Prototype/testproject.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()