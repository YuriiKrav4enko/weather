from weather_api_service import Weather
from coordinates import Coordinates


def format_weather(weather: Weather) -> str:
    """Returns wather data in string"""
    return (f"Weather at {weather.coordinates.address}\n"
            f"Temperature: {weather.temperature} °C, "
            f"{weather.weather_type.value}\n"
            f"Sunrise time: {weather.sunrise.strftime('%H:%M')}\n"
            f"Sunset time: {weather.sunset.strftime('%H:%M')}")


if __name__ == "__main__":
    from datetime import datetime
    from weather_api_service import WeatherType

    print(format_weather(
        Weather(
            coordinates=Coordinates(50.3, 30.4, 'Kyiv, UA', 'Kyiv'),
            temperature=25,
            weather_type=WeatherType.CLEAR,
            sunrise=datetime(2024, 8, 9, 5, 0),
            sunset=datetime(2024, 8, 9, 20, 15)
        )
    ))
