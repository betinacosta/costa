import base64
import os
from httplib2 import Http
from googleapiclient.discovery import build
from googleapiclient import errors
from oauth2client import file, client, tools
import logging

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CREDENTIALS_PATH = "credentials.json"
CLIENT_SECRET_PATH = "client_secret.json"
USER_ID = "me"
ATTACHMENT_FILENAME = "Kindle-Notebook.csv"
STORAGE_RAW_PATH = os.path.join("app/storage/raw")


class GmailClient:

    def __init__(self):
        self.user_id = USER_ID

    def get_credentials(self):
        store = file.Storage(CREDENTIALS_PATH)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_PATH, SCOPES)
            credentials = tools.run_flow(flow, store)

        return credentials

    def authenticate(self):
        credentials = self.get_credentials()
        service = build("gmail", "v1", http=credentials.authorize(Http()))

        return service

    def get_messages_matching_query(self, service, query=""):
        try:
            response = service.users().messages().list(userId=self.user_id,
                                                       q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId=self.user_id, q=query,
                                                           pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError as error:
            logging.error(f"An Error occurred while executing list messages request: {error}")

    def get_message_details(self, service, message_id):
        try:
            message = service.users().messages().get(userId=self.user_id, id=message_id).execute()
            return message

        except errors.HttpError as error:
            logging.error(f"An Error occurred while getting message {message_id}: {error}")

    def download_attachment(self, service, message_id, attachment_id):
        try:
            attachment = service.users().messages().attachments().get(userId=self.user_id,
                                                                      messageId=message_id,
                                                                      id=attachment_id).execute()

            file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
            path = f"{STORAGE_RAW_PATH}/{message_id}.csv"

            if not os.path.exists(path):
                f = open(path, 'wb')
                f.write(file_data)
                f.close()

        except errors.HttpError as error:
            logging.error(f"An Error occurred while downloading attachment for message: {message_id}: {error}")
