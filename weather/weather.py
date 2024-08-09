#!/usr/bin/env python3.11
from coordinates import get_current_gps_coordinates
from weather_api_service import get_weather
from wheather_formatter import format_weather


def main():
    coordinates = get_current_gps_coordinates()
    weather = get_weather(coordinates)
    print(format_weather(weather))


if __name__ == "__main__":
    main()
