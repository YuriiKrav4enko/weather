import json
import ssl
import urllib
import urllib.request
from datetime import datetime, timezone
from enum import Enum
from typing import Literal, NamedTuple, TypeAlias
from urllib.error import URLError

import config
from coordinates import Coordinates
from exceptions import ApiServiceError

Celsius: TypeAlias = int


class WeatherType(Enum):
    CLEAR = "Чисто"
    MAINLY_CLEAR = "Переважно ясно"
    PARTLY_CLOUDY = "Мінлива хмарність"
    OVERCAST = "Похмуро"
    FOG = "Туман"
    DEPOSITING_RIME_FOG = "Відкладення інею"
    LIGHT_DRIZZLE = "Мряка: легка"
    MODERATE_DRIZZLE = "Мряка: помірна"
    DENSE_INTENSITY_DRIZZLE = "Мряка: густа інтенсивність"
    LIGHT_FREEZING_DRIZZLE = "Крижана мряка: легкий"
    DENSE_INTENSITY_FREEZING_DRIZZLE = "Крижана мряка: сильна інтенсивність"
    SLIGHT_RAIN = "Слабкий дощ"
    MODERATE_RAIN = "Помірний дощ"
    HEAVY_INTENSITY_RAIN = "Інтенсивний дощ"
    LIGHT_FREEZING_RAIN = "Крижаний дощ: легкий"
    HEAVY_INTENSITY_FREEZING_RAIN = "Крижаний дощ: сильна інтенсивність"
    SLIGHT_SNOW_FALL = "Слабкий снігопад"
    MODERATE_SNOW_FALL = "Помірний снігопад"
    HEAVY_INTENSITY_SNOW_FALL = "Інтенсивний снігопад"
    SNOW_GRAINS = "Снігові крупинки"
    SLIGHT_RAIN_SHOWERS = "Слабкий зливний дощ"
    MODERATE_RAIN_SHOWERS = "Помірний зливний дощ"
    VIOLENT_RAIN_SHOWERS = "Сильний снігопад"
    SLIGHT_SNOW_SHOWERS = "Легка хуртовина"
    HEAVY_SNOW_SHOWERS = "Сильна хуртовина"
    THUNDERSTORM = "Гроза"
    THUNDERSTORM_WITH_SLIGHT = "Гроза з невеликим і сильним градом"


class Weather(NamedTuple):
    temperature: Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime


def get_weather(coordinates: Coordinates) -> Weather:
    """Request weather in OpenWeather API and returns it"""
    openweather_response = _get_openmeteo_response(
        latitude=coordinates.latitude, longitude=coordinates.longitude
    )
    weather = _parse_openmeteo_response(openweather_response)
    return weather


def _get_openmeteo_response(latitude: float, longitude: float) -> str:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPENMETEO_URL.format(
        latitude=latitude, longitude=longitude
    )
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError


def _parse_openmeteo_response(openweather_response: str) -> Weather:
    try:
        openmeteo_dict = json.loads(openweather_response)
    except json.JSONDecodeError:
        raise ApiServiceError
    return Weather(
        temperature=_parse_temperature(openmeteo_dict),
        weather_type=_parse_weather_code(openmeteo_dict),
        sunrise=_parse_sun_time(openmeteo_dict, 'sunrise'),
        sunset=_parse_sun_time(openmeteo_dict, 'sunset')    )


def _parse_temperature(openmeteo_dict: dict) -> Celsius:
    return round(openmeteo_dict['current']['temperature_2m'])


def _parse_weather_code(openmeteo_dict: dict) -> WeatherType:
    try:
        weather_type_code = openmeteo_dict['current']['weather_code']
    except (IndexError, KeyError):
        raise ApiServiceError
    
    weather_types = {
        0: WeatherType.CLEAR,
        1: WeatherType.MAINLY_CLEAR,
        2: WeatherType.PARTLY_CLOUDY,
        3: WeatherType.OVERCAST,
        45: WeatherType.FOG,
        48: WeatherType.DEPOSITING_RIME_FOG,
        51: WeatherType.LIGHT_DRIZZLE,
        53: WeatherType.MODERATE_DRIZZLE,
        55: WeatherType.DENSE_INTENSITY_DRIZZLE,
        56: WeatherType.LIGHT_FREEZING_DRIZZLE,
        57: WeatherType.DENSE_INTENSITY_FREEZING_DRIZZLE,
        61: WeatherType.SLIGHT_RAIN,
        63: WeatherType.MODERATE_RAIN,
        65: WeatherType.HEAVY_INTENSITY_RAIN,
        66: WeatherType.LIGHT_FREEZING_RAIN,
        67: WeatherType.HEAVY_INTENSITY_FREEZING_RAIN,
        71: WeatherType.SLIGHT_SNOW_FALL,
        73: WeatherType.MODERATE_SNOW_FALL,
        75: WeatherType.HEAVY_INTENSITY_SNOW_FALL,
        77: WeatherType.SNOW_GRAINS,
        80: WeatherType.SLIGHT_RAIN_SHOWERS,
        81: WeatherType.MODERATE_RAIN_SHOWERS,
        82: WeatherType.VIOLENT_RAIN_SHOWERS,
        85: WeatherType.SLIGHT_SNOW_SHOWERS,
        86: WeatherType.HEAVY_SNOW_SHOWERS,
        95: WeatherType.THUNDERSTORM,
        96: WeatherType.THUNDERSTORM_WITH_SLIGHT,
        99: WeatherType.THUNDERSTORM_WITH_SLIGHT
    }
    try:
        return weather_types[weather_type_code]
    except (IndexError, KeyError):
        raise ApiServiceError
    

def _parse_sun_time(
        openmeteo_dict: dict,
        time: Literal["sunrise"] | Literal["sunset"]) -> datetime:
    localtzinfo = datetime.now(timezone.utc).astimezone().tzinfo
    return datetime.strptime(openmeteo_dict['daily'][time][0], "%Y-%m-%dT%H:%M").replace(
        tzinfo=timezone.utc).astimezone(localtzinfo)


if __name__ == "__main__":
    print(get_weather(Coordinates(50.3, 30.4)))
