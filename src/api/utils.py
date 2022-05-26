import typing
import requests

from src.models import models


def get_all_summarized_objects(url: str) -> typing.List[models.SummarizedObject]:
    """Get all the Summarized objects over a top url endpoint."""

    all_objects: typing.List[models.SummarizedObject] = []

    response: models.TopLevelResponse = models.TopLevelResponse.from_dict(
        get_response_as_json(url)
    )
    all_objects.extend(response.results)

    while response.next:
        response = models.TopLevelResponse.from_dict(
            get_response_as_json(response.next)
        )
        all_objects.extend(response.results)

    return all_objects


def extract_summarized_objects_info(
    summarized_objects: typing.List[models.SummarizedObject],
) -> typing.Tuple[typing.Tuple[str], typing.Tuple[str]]:
    """Extrac the name and url from a list of Summarized Objects."""
    return tuple(
        zip(
            *[
                (summarized_object.name, summarized_object.url)
                for summarized_object in summarized_objects
            ]
        )
    )


def get_response_as_json(url: str) -> typing.Dict[str, typing.Any]:
    """Wrapper used to parse a GET Response as JSON object."""
    return requests.get(url).json()
