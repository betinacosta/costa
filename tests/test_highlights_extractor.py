import pytest
import os
from unittest import mock
import json

from app.highlights_extractor import HighlightsExtractor


@pytest.fixture
def message_detail():
    path = os.path.join("tests/stubs/message_detail.json")
    f = open(path, 'r')

    return json.load(f)


@pytest.fixture
def highlights_extractor():
    highlights = HighlightsExtractor()

    return highlights


@pytest.fixture
def message_list():
    message_list = {"messages": [{"id": "16e8395", "threadId": "16e8395"}], "resultSizeEstimate": 7}
    return message_list


@mock.patch("app.gmail_client.GmailClient.get_message_details")
@mock.patch("app.gmail_client.GmailClient.get_messages_matching_query")
def test_should_return_dict_list_with_message_id_and_attachment_id(mock_messages, mock_detail, message_list,
                                                                   message_detail, highlights_extractor):
    expected_result = [{"message_id": "16e8395", "attachment_id": "ANGjdJ9gYQLvWOK_Qi"}]

    mock_messages.return_value = message_list
    mock_detail.return_value = message_detail

    result = highlights_extractor.get_attachment_ids_list()

    assert result == expected_result


def test_should_return_attachment_id(message_detail, highlights_extractor):
    expected_result = "ANGjdJ9gYQLvWOK_Qi"
    result = highlights_extractor.get_attachment_id(message_detail=message_detail)

    assert expected_result == result


@mock.patch("app.gmail_client.GmailClient.download_attachment")
@mock.patch("app.highlights_extractor.HighlightsExtractor.get_attachment_ids_list")
def test_should_call_functions_to_download_highlights(mock_attachments_list, mock_download, highlights_extractor):
    mock_attachments_list.return_value = [{"message_id": "16e8395", "attachment_id": "ANGjdJ9gYQLvWOK_Qi"}]
    highlights_extractor.download_highlights()

    mock_attachments_list.assert_called()
    mock_download.assert_called()
