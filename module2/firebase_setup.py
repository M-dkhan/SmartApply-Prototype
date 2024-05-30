import os
import firebase_admin
from firebase_admin import credentials, firestore

class FirestoreManager:
    # Get the parent directory path
    parent_dir = os.path.dirname(os.getcwd())
    
    # Construct the path to the JSON file in the parent directory
    json_file_path = os.path.join(parent_dir, "SmartApply-Prototype/testproject.json")
    print(parent_dir)

    # Initialize Firebase Admin SDK and Firestore client
    cred = credentials.Certificate(json_file_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
