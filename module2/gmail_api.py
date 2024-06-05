import os
import pickle
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CLIENT_SECRETS_FILE = 'credentials.json'
TOKEN_PICKLE_FILE = 'token.pickle'

def create_message(sender, to, subject, message_text):
    """Create a message for an email."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}

def send_message(service, user_id, message):
    """Send an email message."""
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def automate_authorization(auth_url, driver):
    """Automate the OAuth authorization using Selenium with headless Chrome."""
    driver.get(auth_url)
    
    # Wait for the authorization page to load and simulate user actions
    try:
        
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "identifier"))
        ).send_keys('khan.mohd.zaid.ca@gmail.com')  # Replace with your email


        # Add a delay to allow the password page to load fully
        sleep(5)  # Adjust the delay as needed

        # Print a message to confirm that the button was clicked
        print("Clicked the button with ID 'identifierNext'")

        with open("hello.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
            
            
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID,"identifierNext"))
        ).click()

        # Add a delay to allow the password page to load fully
        sleep(5)  # Adjust the delay as needed

        # Print a message to confirm that the button was clicked
        print("Clicked the button with ID 'identifierNext'")

        with open("hello.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "Passwd"))
        ).send_keys('MoZaKh{2002#')  

        

        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
        ).click()

        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
        ).click()

        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
        ).click()


        WebDriverWait(driver, 30).until(
            EC.url_contains('http://localhost:8080')
        )

    finally:
        pass  # Do not quit the driver, as it is managed elsewhere

def authorize_and_send_email(driver):
    creds = None

    # Load credentials from the token.pickle file if it exists
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)

    # If there are no valid credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Create the flow using the client secrets file
            flow = Flow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                scopes=SCOPES,
                redirect_uri='http://localhost:8080')

            # Run the local server for user authorization
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f'Please go to this URL to authorize the application: {auth_url}')
            
            # Automate the authorization process
            automate_authorization(auth_url, driver)
            
            # Capture the authorization code from the redirect
            from http.server import BaseHTTPRequestHandler, HTTPServer

            class OAuthHandler(BaseHTTPRequestHandler):
                def do_GET(self):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'Authorization complete. You can close this window.')

                    # Extract the authorization code from the URL
                    code = self.path.split('code=')[1]
                    flow.fetch_token(code=code)
                    creds = flow.credentials
                    # Save the credentials for the next run
                    with open(TOKEN_PICKLE_FILE, 'wb') as token:
                        pickle.dump(creds, token)
                    # Shutdown the server once the token is received
                    self.server.shutdown()

            server_address = ('', 8080)
            httpd = HTTPServer(server_address, OAuthHandler)
            print('Waiting for authorization...')
            httpd.handle_request()

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # Create and send an email
        message = create_message('khan.mohd.zaid.ca@gmail.com', 'khan.mohd.zaid@protonmail.com', 'Subject', 'Email body text')
        send_message(service, 'me', message)

    except HttpError as error:
        print(f'An error occurred: {error}')
