import pytest
import requests

from src.api import utils
from src.models import models


def test_get_all_summarized_objects(monkeypatch: pytest.MonkeyPatch):
    mock_results = [
        {"name": "cherry", "url": "cherry.com"},
        {"name": "oran", "url": "oran.com"},
    ]

    def mock_get_response_as_json(url: str):
        if url == "https://mock_url.com":
            return {
                "count": 1,
                "next": "https://mock.url.com?offset=1",
                "results": [mock_results[0]],
            }

        elif url == "https://mock.url.com?offset=1":
            return {"count": 1, "results": [mock_results[1]]}

    base_url = "https://mock_url.com"
    monkeypatch.setattr(utils, "get_response_as_json", mock_get_response_as_json)

    expected_results = [
        models.SummarizedObject.from_dict(mock_results[0]),
        models.SummarizedObject.from_dict(mock_results[1]),
    ]
    results = utils.get_all_summarized_objects(base_url)
    assert results == expected_results


def test_extract_summarized_objects_info():
    mock_data = [
        {"name": "name1", "url": "url1"},
        {"name": "name2", "url": "url2"},
        {"name": "name3", "url": "url3"},
    ]
    summarized_items = [
        models.SummarizedObject.from_dict(single_object) for single_object in mock_data
    ]
    names, urls = utils.extract_summarized_objects_info(summarized_items)
    assert names == ("name1", "name2", "name3")
    assert urls == ("url1", "url2", "url3")


def test_get_response_as_json(monkeypatch: pytest.MonkeyPatch):
    def mocked_requests_get(url: str):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        if url == "https://mock_url.com":
            return MockResponse(
                {
                    "count": "123",
                    "results": [{"key": "value", "another_key": "another_value"}],
                },
                200,
            )

    monkeypatch.setattr(requests, "get", mocked_requests_get)
    mock_url = "https://mock_url.com"
    response = utils.get_response_as_json(mock_url)
    assert response == {
        "count": "123",
        "results": [{"key": "value", "another_key": "another_value"}],
    }
