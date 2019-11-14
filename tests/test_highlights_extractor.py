import pytest
import os
from unittest import mock
import json
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal

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


@pytest.fixture
def highlights():
    highlights_sample = os.path.join("tests/stubs/correnteza-notebook.csv")
    data = pd.read_csv(highlights_sample)
    return data


@pytest.fixture
def kindle_information():
    information = pd.DataFrame({"your_kindle_notes_for": ["SEGUINDO A CORRENTEZA",
                                                              "by Agatha Christie, Lúcia Brito",
                                                              "Free Kindle instant preview:",
                                                              "http://a.co/9O6l4am"]})
    return information


@pytest.fixture
def highlights_information():
    data = [["Highlight (Yellow)", "Location 3750", "5", "A senhorita está errada – disse Poirot."],
            ["Note", "Location 3751", "5", "Real"],
            ["Highlight (Yellow)", "Location 4263", "5", "(a esposa de Underhay não era católica)"]]

    information = pd.DataFrame(data, columns=["annotation_type", "location", "starred", "annotation"])

    return information


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


def test_should_return_dataset_with_kindle_information(highlights_extractor, highlights, kindle_information):
    expected_result = kindle_information
    result = highlights_extractor.get_kindle_information(dataframe=highlights)

    assert_frame_equal(expected_result, result)


def test_should_return_dataset_with_highlights_information(highlights_extractor, highlights, highlights_information):
    expected_result = highlights_information
    result = highlights_extractor.get_highlights_information(dataframe=highlights)

    assert_frame_equal(expected_result, result, check_names=False)


def test_should_return_book_title(highlights_extractor, kindle_information):
    expected_result = "seguindo a correnteza"
    result = highlights_extractor.get_title(kindle_information=kindle_information)

    assert expected_result == result


def test_should_return_book_authors(highlights_extractor, kindle_information):
    expected_result = "Agatha Christie, Lúcia Brito"
    result = highlights_extractor.get_authors(kindle_information=kindle_information)

    assert expected_result == result


def test_should_return_kinlde_preview_link(highlights_extractor, kindle_information):
    expected_result = "http://a.co/9O6l4am"
    result = highlights_extractor.get_kindle_preview(kindle_information=kindle_information)

    assert expected_result == result


def test_should_return_highlights_and_notes(highlights_extractor, highlights_information):
    expected_result = [{"highlight": "A senhorita está errada – disse Poirot.", "note": "Real"},
                       {"highlight": "(a esposa de Underhay não era católica)", "note": ""}]
    result = highlights_extractor.get_notes_and_highlights(highlights_information=highlights_information)

    assert expected_result == result

