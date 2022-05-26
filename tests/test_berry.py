import pytest

from src.api import berry
from src.api import utils
from src.models import models


def test_all_berry_stats(monkeypatch: pytest.MonkeyPatch):
    def mock_all_summarized_objects(_: str):
        mock_summarized_data = [
            {"name": "pinba", "url": "pinba.com"},
            {"name": "chesto", "url": "chesto.com"},
            {"name": "test", "url": "test.com"},
        ]
        return [
            models.SummarizedObject.from_dict(mock_summarized_data[0]),
            models.SummarizedObject.from_dict(mock_summarized_data[1]),
            models.SummarizedObject.from_dict(mock_summarized_data[2]),
        ]

    def mock_get_response_as_json(url: str):
        if url == "pinba.com":
            return {"growth_time": 5}
        elif url == "chesto.com":
            return {"growth_time": 10}
        elif url == "test.com":
            return {"growth_time": 30}

    monkeypatch.setattr(
        utils, "get_all_summarized_objects", mock_all_summarized_objects
    )
    monkeypatch.setattr(utils, "get_response_as_json", mock_get_response_as_json)

    expected = {
        "berries_names": ("pinba", "chesto", "test"),
        "min_growth_time": 5,
        "median_growth_time": 10.0,
        "max_growth_time": 30,
        "variance_growth_time": 175.0,
        "mean_growth_time": 15.0,
        "frequency_growth_time": {5: 1, 10: 1, 30: 1},
    }
    assert berry.all_berry_stats() == expected


def test_get_berries_growth_times(monkeypatch: pytest.MonkeyPatch):
    mock_all_urls = (
        "https://url1.com",
        "https://url2.com",
        "https://url3.com",
    )

    def mock_get_response_as_json(url: str):
        if url == "https://url1.com":
            return {"growth_time": "10"}
        elif url == "https://url2.com":
            return {"growth_time": 20}
        elif url == "https://url3.com":
            return {"growth_time": "30"}

    monkeypatch.setattr(utils, "get_response_as_json", mock_get_response_as_json)

    expected = (10, 20, 30)
    assert berry._get_berries_growth_times(mock_all_urls) == expected


def test_get_berries_growth_stats():
    mock_growth_values = (1, 5, 6, 7, 8, 9, 8, 6, 5, 1, 6, 5)
    assert berry._get_berries_growth_stats(mock_growth_values) == {
        "min_growth_time": 1,
        "median_growth_time": 6.0,
        "max_growth_time": 9,
        "variance_growth_time": 6.265151515151516,
        "mean_growth_time": 5.583333333333333,
        "frequency_growth_time": {1: 2, 5: 3, 6: 3, 7: 1, 8: 2, 9: 1},
    }
