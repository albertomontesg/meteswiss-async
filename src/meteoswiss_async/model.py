"""Module to define the data models from the API."""

from __future__ import annotations

__all__ = [
    "Weather",
]

import abc
import dataclasses
import enum
import typing
from typing import TypeAlias

from dataclasses_json import (
    DataClassJsonMixin,
    LetterCase,
    config,
    dataclass_json,
)

TimestampMs: TypeAlias = int


@typing.dataclass_transform(kw_only_default=True)
class Model(DataClassJsonMixin, abc.ABC):
    """Base class for any data model.

    This class makes sure that every subclass is registered as a dataclass as
    well as implements methods to convert/parse them from Json data."""

    def __init_subclass__(cls):
        dataclasses.dataclass(frozen=True, kw_only=True)(cls)
        dataclass_json(cls, letter_case=LetterCase.CAMEL)
        return cls


class Condition(enum.StrEnum):
    UNKNOWN = "unknown"
    CLEAR_NIGHT = "clear-night"
    CLOUDY = "cloudy"
    FOG = "fog"
    HAIL = "hail"
    LIGHTNING = "lightning"
    LIGHTNING_RAINY = "lightning-rainy"
    PARTLY_CLOUDY = "partlycloudy"
    POURING = "pouring"
    RAINY = "rainy"
    SNOWY = "snowy"
    SNOWY_RAINY = "snowy-rainy"
    SUNNY = "sunny"
    WINDY = "windy"
    WINDY_VARIANT = "windy-variant"
    EXCEPTIONAL = "exceptional"

    @classmethod
    def from_icon(cls, icon: int) -> "Condition":
        if icon in (101,):
            return Condition.CLEAR_NIGHT
        elif icon in (5, 35, 105, 135):
            return Condition.CLOUDY
        elif icon in (27, 28, 127, 128):
            return Condition.FOG
        elif icon in (12, 112):
            return Condition.LIGHTNING
        elif icon in (13, 23, 24, 25, 32, 113, 123, 124, 125, 132):
            return Condition.LIGHTNING_RAINY
        elif icon in (2, 3, 4, 102, 103, 104):
            return Condition.PARTLY_CLOUDY
        elif icon in (20, 120):
            return Condition.POURING
        elif icon in (6, 9, 14, 17, 29, 33, 106, 109, 114, 117, 129, 133):
            return Condition.RAINY
        elif icon in (
            8,
            11,
            16,
            19,
            22,
            30,
            34,
            108,
            111,
            116,
            119,
            122,
            130,
            134,
        ):
            return Condition.SNOWY
        elif icon in (7, 10, 15, 18, 21, 31, 107, 110, 115, 118, 121, 131):
            return Condition.SNOWY_RAINY
        elif icon in (1, 26, 126):
            return Condition.SUNNY
        else:
            return Condition.UNKNOWN


class CurrentWeather(Model):
    time: TimestampMs
    icon: int
    icon_v2: int
    temperature: int

    @property
    def condition(self) -> Condition:
        return Condition.from_icon(self.icon)


class DayForecast(Model):
    day_date: str
    icon_day: int
    icon_day_v2: int
    temperature_max: int
    temperature_min: int
    precipitation: float

    @property
    def condition(self) -> Condition:
        return Condition.from_icon(self.icon_day)


class WarnType(enum.IntEnum):
    THUNDERSTORM = 1
    RAIN = 2
    FROST = 5
    FORECAST_FIRE = 10
    FLOOD = 11
    # WIND = XX
    # SLIPPERY_ROADS = XX
    # HEAT_WAVE = XX


class WarningOverview(Model):
    warn_type: WarnType
    warn_level: int


class WarningDetail(WarningOverview):
    text: str
    html_text: str
    valid_from: TimestampMs
    valid_to: TimestampMs
    ordering: str
    outlook: bool


{
    "N": [0, 11.25],
    "NNE": [11.25, 33.75],
    "NE": [33.75, 56.25],
    "ENE": [56.25, 78.75],
    "E": [78.75, 101.25],
    "ESE": [101.25, 123.75],
    "SE": [123.75, 146.25],
    "SSE": [146.25, 168.75],
    "S": [168.75, 191.25],
    "SSW": [191.25, 213.75],
    "SW": [213.75, 236.25],
    "WSW": [236.25, 258.75],
    "W": [258.75, 281.25],
    "WNW": [281.25, 303.75],
    "NW": [303.75, 326.25],
    "NNW": [326.25, 348.75],
}


class CardinalDirection(enum.Enum):
    N = enum.auto()
    NNE = enum.auto()
    NE = enum.auto()
    ENE = enum.auto()
    E = enum.auto()
    ESE = enum.auto()
    SE = enum.auto()
    SSE = enum.auto()
    S = enum.auto()
    SSW = enum.auto()
    SW = enum.auto()
    WSW = enum.auto()
    W = enum.auto()
    WNW = enum.auto()
    NW = enum.auto()
    NNW = enum.auto()

    @classmethod
    def from_degrees(cls, degrees: int) -> "CardinalDirection":
        if degrees >= 0 and degrees < 11.25:
            return CardinalDirection.N
        elif degrees < 33.75:
            return CardinalDirection.NNE
        elif degrees < 56.25:
            return CardinalDirection.NE
        elif degrees < 78.75:
            return CardinalDirection.ENE
        elif degrees < 101.25:
            return CardinalDirection.E
        elif degrees < 123.75:
            return CardinalDirection.ESE
        elif degrees < 146.25:
            return CardinalDirection.SE
        elif degrees < 168.75:
            return CardinalDirection.SSE
        elif degrees < 191.25:
            return CardinalDirection.S
        elif degrees < 213.75:
            return CardinalDirection.SSW
        elif degrees < 236.25:
            return CardinalDirection.SW
        elif degrees < 258.75:
            return CardinalDirection.WSW
        elif degrees < 281.25:
            return CardinalDirection.W
        elif degrees < 303.75:
            return CardinalDirection.WNW
        elif degrees < 326.25:
            return CardinalDirection.NW
        elif degrees < 348.75:
            return CardinalDirection.NNW
        else:
            return CardinalDirection.N


class GraphLite(Model):
    start: TimestampMs
    precipitation_mean_10m: list[float] = dataclasses.field(
        metadata=config(field_name="precipitation10m")
    )
    precipitation_min_10m: list[float]
    precipitation_max_10m: list[float]
    temperature_min_1h: list[float]
    temperature_max_1h: list[float]
    temperature_mean_1h: list[float]
    precipitation_mean_1h: list[float]
    precipitation_min_1h: list[float]
    precipitation_max_1h: list[float]


class Graph(GraphLite):
    start_low_resolution: TimestampMs
    weather_icon_3h: list[int]
    weather_icon_3h_v2: list[int]
    wind_direction_3h: list[int]
    wind_speed_3h: list[float]
    sunrise: list[TimestampMs]
    sunset: list[TimestampMs]

    # Overwrite the field name that return this whole message as the field name
    # is slightly different from the lite version.
    precipitation_mean_1h: list[float] = dataclasses.field(
        metadata=config(field_name="precipitation1h")
    )

    @property
    def weather_condition_3h(self) -> list[Condition]:
        return [Condition.from_icon(icon) for icon in self.weather_icon_3h]

    @property
    def wind_cardinal_direction_3h(self) -> list[CardinalDirection]:
        return [
            CardinalDirection.from_degrees(degrees)
            for degrees in self.wind_direction_3h
        ]


class Forecast(Model):
    forecast: list[DayForecast]


class Weather(Forecast):
    current_weather: CurrentWeather
    warnings_overview: list[WarningOverview]
    warnings: list[WarningDetail]
    graph: Graph


class StationInformation(Model):
    station_id: str
    time: TimestampMs
    temperature: float
    wind_speed: float
    wind_direction: int
    wind_gust: float
    precipitation: float
    humidity: int
    pressure_standard: float
    pressure_station: float
    pressure_sea: float
    sunshine: int
    dew_point: float
    snow_new: int
    snow_total: int

    @property
    def wind_cardinal_direction(self) -> CardinalDirection:
        return CardinalDirection.from_degrees(self.wind_direction)


class FullOverview(Model):
    forecast: dict[str, Forecast]
    graph: dict[str, GraphLite]
    warnings: dict[str, list[WarningDetail]]
    current_weather: dict[str, StationInformation]


class StationType(enum.StrEnum):
    WEATHER_STATION = "Weather station"
    PRECIPITATION_STATION = "Precipitation station"


class Station(Model):
    name: str = dataclasses.field(metadata=config(field_name="Station"))
    code: str = dataclasses.field(metadata=config(field_name="Abbr."))
    wigos_id: str = dataclasses.field(metadata=config(field_name="WIGOS-ID"))
    station_type: StationType = dataclasses.field(
        metadata=config(field_name="Station type")
    )
    data_owner: str = dataclasses.field(
        metadata=config(field_name="Data Owner")
    )
    data_since: str = dataclasses.field(
        metadata=config(field_name="Data since")
    )
    station_height: int = dataclasses.field(
        metadata=config(field_name="Station height m a. sea level")
    )
    barometric_altitude: int | None = dataclasses.field(
        metadata=config(field_name="Barometric altitude m a. ground")
    )
    coordinates_east: int = dataclasses.field(
        metadata=config(field_name="CoordinatesE")
    )
    coordinates_north: int = dataclasses.field(
        metadata=config(field_name="CoordinatesN")
    )
    latitude: float = dataclasses.field(metadata=config(field_name="Latitude"))
    longitude: float = dataclasses.field(
        metadata=config(field_name="Longitude")
    )
    exposition: str = dataclasses.field(
        metadata=config(field_name="Exposition")
    )
    canton: str = dataclasses.field(metadata=config(field_name="Canton"))
    measurements: list[str] = dataclasses.field(
        metadata=config(field_name="Measurements")
    )
    link: str = dataclasses.field(metadata=config(field_name="Link"))
