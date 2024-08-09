from weather_api_service import Weather


def format_weather(weather: Weather) -> str:
    """Returns wather data in string"""
    return (f"Температура: {weather.temperature} °C, "
            f"{weather.weather_type.value}\n"
            f"Схід: {weather.sunrise.strftime('%H:%M')}\n"
            f"Захід: {weather.sunset.strftime('%H:%M')}")


if __name__ == "__main__":
    from datetime import datetime
    from weather_api_service import WeatherType

    print(format_weather(Weather(
        temperature=25,
        weather_type=WeatherType.CLEAR,
        sunrise=datetime(2024, 8, 9, 5, 0),
        sunset=datetime(2024, 8, 9, 20, 15)
    )))
