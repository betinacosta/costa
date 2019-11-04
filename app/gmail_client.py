from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


class GmailClient:

    def __init__(self):
        credentials = self.get_credentials()
        self.service = build("gmail", "v1", http=credentials.authorize(Http()))

    def get_credentials(self):
        store = file.Storage("credentials.json")
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets("client_secret.json", SCOPES)
            credentials = tools.run_flow(flow, store)

        return credentials

    def get_emails_by_sender(self):
        pass

    def get_attachments(self, email_body):
        pass