import os
import firebase_admin
from firebase_admin import credentials, firestore

class FirestoreManager:
    # Get the directory path of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(current_dir)
    
    # Construct the path to the JSON file in the parent directory
    json_file_path = os.path.join(current_dir, "../testproject.json")
    print(json_file_path)
    # Initialize Firebase Admin SDK and Firestore client
    cred = credentials.Certificate(json_file_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
