
from typing import NamedTuple

import config
import geocoder
from exceptions import CantGetCoordinates


class Coordinates(NamedTuple):
    latitude: float
    longitude: float
    address: str
    city: str


def get_current_gps_coordinates() -> Coordinates:
    """Returns current coordinates using IP Add"""
    coordinates = _get_geocoder_coordinates()
    return _round_coordinates(coordinates)


def _get_geocoder_coordinates() -> Coordinates:
    g = geocoder.ip('me')
    latlng = g.latlng
    if not latlng:
        raise CantGetCoordinates
    lat, lng = g.latlng
    return Coordinates(latitude=lat, longitude=lng, address=g.address, city=g.city)


def _round_coordinates(coordinates: Coordinates):
    if not config.USE_ROUNDED_COORDS:
        return coordinates
    return Coordinates(*map(
        lambda c: round(c, 1),
        [coordinates.latitude, coordinates.longitude]
    ), address=coordinates.address, city=coordinates.city)


if __name__ == "__main__":
    coordinates = get_current_gps_coordinates()
    try:
        print("Your current GPS coordinates are:")
        print(f"Latitude: {coordinates.latitude}")
        print(f"Longitude: {coordinates.longitude}")
    except CantGetCoordinates:
        print("Unable to retrieve your GPS coordinates.")
