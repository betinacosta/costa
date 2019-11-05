from httplib2 import Http
from googleapiclient.discovery import build

from app.gmail_client import GmailClient


class HighlightsExtractor:

    def get_service(self):
        gmail_client = GmailClient()
        credentials = gmail_client.get_credentials()
        service = build("gmail", "v1", http=credentials.authorize(Http()))

        return service

