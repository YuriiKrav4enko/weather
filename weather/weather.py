#!/usr/bin/env python3.11
from coordinates import get_current_gps_coordinates
from weather_api_service import get_weather
from weather_formatter import format_weather
from exceptions import ApiServiceError, CantGetCoordinates


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

    print(format_weather(coordinates, weather))


if __name__ == "__main__":
    main()
