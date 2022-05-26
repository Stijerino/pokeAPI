import statistics
import collections
import typing
import mpld3
import matplotlib.pyplot as plt

from src.api import utils
from src.models import models

BASE_ENDPOINT: str = "https://pokeapi.co/api/v2"
BERRY_ENDPOINT: str = "berry"


def all_berry_stats() -> typing.Dict[str, typing.Any]:
    """Resolver used for the endpoint allBerryStats"""

    all_berries = utils.get_all_summarized_objects(f"{BASE_ENDPOINT}/{BERRY_ENDPOINT}")
    berries_names, berries_urls = utils.extract_summarized_objects_info(all_berries)
    berries_growth_times = _get_berries_growth_times(berries_urls)
    berries_growth_stats = _get_berries_growth_stats(berries_growth_times)

    return {
        "berries_names": berries_names,
        "min_growth_time": berries_growth_stats["min_growth_time"],
        "median_growth_time": berries_growth_stats["median_growth_time"],
        "max_growth_time": berries_growth_stats["max_growth_time"],
        "variance_growth_time": berries_growth_stats["variance_growth_time"],
        "mean_growth_time": berries_growth_stats["mean_growth_time"],
        "frequency_growth_time": berries_growth_stats["frequency_growth_time"],
    }


def _get_berries_growth_times(
    all_urls: typing.Tuple[str, ...]
) -> typing.Tuple[int, ...]:
    """Fetch for each url, the growth_time of the berry."""
    return tuple(
        [
            int(
                models.BerryResponse.from_dict(
                    utils.get_response_as_json(url)
                ).growth_time
            )
            for url in all_urls
        ]
    )


def _get_berries_growth_stats(
    berries_growth_values: typing.Tuple[int, ...],
) -> typing.Dict[str, typing.Union[int, float]]:
    """Return a dictionary with the growth stats values of the berries."""
    min_growth_time: int = min(berries_growth_values)
    median_growth_time: float = float(statistics.median(berries_growth_values))
    max_growth_time: int = max(berries_growth_values)
    variance_growth_time: float = float(statistics.variance(berries_growth_values))
    mean_growth_time: float = float(statistics.mean(berries_growth_values))
    frequency_growth_time: typing.Dict[int, int] = dict(
        collections.Counter(berries_growth_values)
    )
    return {
        "min_growth_time": min_growth_time,
        "median_growth_time": median_growth_time,
        "max_growth_time": max_growth_time,
        "variance_growth_time": variance_growth_time,
        "mean_growth_time": mean_growth_time,
        "frequency_growth_time": frequency_growth_time,
    }


def _create_berries_growth_time_histogram(  # pragma: no cover
    berries_growth_times: typing.Tuple[int, ...]
) -> typing.Optional[str]:
    """
    Create a histogram based on the growth time of the berries and return it as HTML.

    This function is supposed to show and return the HTML of the Histogram,
    Since it blocks flow of the program once it opens the browser, it's not being used,
    and it stays here as proof of concept

    """
    fig = plt.figure()  # pragma: no cover
    hist = fig.gca()  # pragma: no cover
    hist.hist(berries_growth_times, bins=20)  # pragma: no cover
    plt.title("Berry Growth Histogram")  # pragma: no cover
    plt.xlabel("Growth value")  # pragma: no cover
    plt.ylabel("Frequency")  # pragma: no cover
    mpld3.show()  # pragma: no cover
    data = f"<html>{mpld3.fig_to_html(fig)}</html>"  # pragma: no cover
    return data  # pragma: no cover
