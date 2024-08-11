#!/usr/bin/env python3.11
from pathlib import Path

from coordinates import get_current_gps_coordinates
from exceptions import ApiServiceError, CantGetCoordinates
from history import JSONFileWeatherStorage, save_weather
from weather_api_service import get_weather
from weather_formatter import format_weather


def main():
    try:
        coordinates = get_current_gps_coordinates()
    except CantGetCoordinates:
        print("Can't get gps coordinates")
        exit(1)

    try:
        weather = get_weather(coordinates)
    except ApiServiceError:
        print(f"Can't get weathger for {coordinates.latitude}, "
              f"{coordinates.longitude} coordinates")
        exit(1)

    print(format_weather(weather))

    save_weather(
        weather,
        JSONFileWeatherStorage(Path.cwd() / "history.json")
    )


if __name__ == "__main__":
    main()
