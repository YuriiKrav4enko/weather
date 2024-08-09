
from typing import NamedTuple

import geocoder


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


def get_current_gps_coordinates() -> Coordinates:
    """Returns current coordinates using IP Add"""
    g = geocoder.ip('me')
    if g.latlng is not None:  # g.latlng tells if the coordiates are found or not
        return Coordinates(latitude=g.latlng[0], longitude=g.latlon[1])
    else:
        raise Exception()


if __name__ == "__main__":
    coordinates = get_current_gps_coordinates()
    if coordinates is not None:
        print("Your current GPS coordinates are:")
        print(f"Latitude: {coordinates.latitude}")
        print(f"Longitude: {coordinates.longitude}")
    else:
        print("Unable to retrieve your GPS coordinates.")
