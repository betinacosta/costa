import logging

from app.gmail_client import GmailClient

ATTACHMENT_FILENAME = "Kindle-Notebook.csv"


class HighlightsExtractor:

    def download_highlights(self):
        client = GmailClient()
        attachments_list = self.get_attachment_ids_list()

        for attachment in attachments_list:
            client.download_attachment(message_id=attachment["message_id"],
                                       attachment_id=attachment["attachment_id"])

    def get_attachment_ids_list(self):
        attachments_list = []
        client = GmailClient()
        messages = client.get_messages_matching_query(query="from:no-reply@amazon.com, has:attachment")

        for message in messages["messages"]:
            message_detail = client.get_message_details(message_id=message["id"])
            attachment_id = self.get_attachment_id(message_detail=message_detail)

            if attachment_id:
                attachments_list.append({"message_id": message["id"], "attachment_id": attachment_id})
            else:
                logging.info(f"Message: {message['id']} has no Kinlde highlights attachments")

        return attachments_list

    def get_attachment_id(self, message_detail):
        for part in message_detail['payload']['parts']:
            if part['filename'] == ATTACHMENT_FILENAME:
                return part["body"]["attachmentId"]

        return ""
