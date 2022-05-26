import dataclasses

from src.models import models


def test_summarized_object_from_dict():
    mock_data = {"name": "example_berry", "url": "https://example_berry.com"}

    assert dataclasses.asdict(models.SummarizedObject.from_dict(mock_data)) == mock_data


def test_top_level_response_from_dict():
    mock_data = {
        "count": 24,
        "next": "next.com",
        "previous": None,
        "results": [
            dataclasses.asdict(
                models.SummarizedObject.from_dict(
                    {"id": 1, "name": "testBerry", "growth_time": "14"}
                )
            )
        ],
    }

    assert dataclasses.asdict(models.TopLevelResponse.from_dict(mock_data)) == mock_data


def test_berry_response_from_dict():
    mock_data = {
        "id": 50,
        "name": "passio",
        "growth_time": 8,
    }

    assert dataclasses.asdict(models.BerryResponse.from_dict(mock_data)) == mock_data
