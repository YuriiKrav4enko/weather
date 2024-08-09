from typing import NamedTuple
from datetime import datetime
from enum import Enum

from coordinates import Coordinates


Cilsius = int


class WeatherType(Enum):
    THUNDERSTORM = "Гроза"
    DRIZZLE = "Мряка"
    RAIN = "Дощ"
    SNOW = "Сніг"
    CLEAR = "Чисто"
    FOG = "Туман"
    CLOUDS = "Пасмурно"


class Weather(NamedTuple):
    temperature: Cilsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str


def get_weather(coordinates: Coordinates) -> Weather:
    """Request weather in OpenWeather API and returns it"""
    return Weather(
        temperature=20, weather_type=WeatherType.CLEAR,
        sunrise=datetime(2024, 8, 9, 5, 15),
        sunset=datetime(2024, 8, 9, 20, 15),
        city="Kyiv"
    )
