import typing
import dataclasses


@dataclasses.dataclass(frozen=True)
class SummarizedObject:
    """Represents a summarized view of an item after a top level call."""

    # Name of the object under the endpoint
    name: str
    # URL used to fetch the data of the given object
    url: str

    @classmethod
    def from_dict(cls, data: typing.Dict[str, str]) -> "SummarizedObject":
        return SummarizedObject(name=data.get("name", ""), url=data.get("url", ""))


@dataclasses.dataclass(frozen=True)
class TopLevelResponse:
    """Response of https://pokeapi.co/api/v2/{name}."""

    # Amount of items under the current endpoint
    count: int
    # Next URL cursor of data
    next: typing.Optional[str]
    # Previous URL cursor of data
    previous: typing.Optional[str]
    # Array of SummarizedObjects under the current endpoint
    results: typing.List[SummarizedObject]

    @classmethod
    def from_dict(cls, data: typing.Dict[str, str]) -> "TopLevelResponse":
        return TopLevelResponse(
            count=data.get("count", 0),
            next=data.get("next"),
            previous=data.get("previous"),
            results=[
                SummarizedObject.from_dict(result_data)
                for result_data in data.get("results")
            ],
        )


@dataclasses.dataclass(frozen=True)
class BerryResponse:
    """Response of https://pokeapi.co/api/v2/berry/{name or id}."""

    # Numeric id associated to the berry
    id: int
    # Name of the berry
    name: str
    # Growth time for a given berry
    growth_time: int

    @classmethod
    def from_dict(cls, data: typing.Dict[str, typing.Any]) -> "BerryResponse":
        return BerryResponse(
            id=data.get("id", 0),
            name=data.get("name", ""),
            growth_time=data.get("growth_time", 0),
        )
