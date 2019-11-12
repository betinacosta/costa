import logging
import pandas as pd

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

    def format_dataframe_columns(self, df):
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace(':', '')
        df.columns = df.columns.str.replace('?', '')
        df.columns = df.columns.str.lower()

        return df

    def get_kindle_information(self, dataframe):
        df = self.format_dataframe_columns(dataframe)
        information = []
        delimiter = "---------"

        for index, row in df.iterrows():
            if delimiter in row["your_kindle_notes_for"]:
                kindle_information = pd.DataFrame(information, columns=["your_kindle_notes_for"])
                kindle_information.dropna()
                return kindle_information
            information.append(row["your_kindle_notes_for"])

        logging.error(f"File delimiter: {delimiter} not found")
        return df

    def get_highlights_information(self, dataframe):
        df = self.format_dataframe_columns(dataframe)
        delimiter = "Annotation"

        pattern = df.your_kindle_notes_for.str.contains(delimiter).cumsum()

        groupby = {f'df': g for i, g in df.groupby(pattern)}
        new_dataframe = groupby["df"]

        new_header = new_dataframe.iloc[0]

        highlights_information = new_dataframe[1:]
        highlights_information.columns = new_header
        highlights_information.reset_index(drop=True, inplace=True)

        return self.format_dataframe_columns(highlights_information)

    def get_title(self, kindle_information):
        uppercase_title = kindle_information.your_kindle_notes_for.iloc[0]
        title = uppercase_title.lower()

        return title

    def get_authors(self, kindle_information):
        raw_authors = kindle_information.your_kindle_notes_for.iloc[1]
        delimiter = "by "

        raw_authors = raw_authors.split(delimiter)
        authors = raw_authors[1]

        return authors

    def get_kindle_preview(self, kindle_information):
        kindle_preview = kindle_information.your_kindle_notes_for.iloc[3]
        return kindle_preview

    def get_notes_and_highlights(self):
        pass

    def get_cover(self):
        pass

    def get_isbn_by_title(self):
        pass
