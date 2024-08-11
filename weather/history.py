from weather_api_service import Weather
from pathlib import Path
from datetime import datetime
from weather_formatter import format_weather
from coordinates import Coordinates
from typing import TypedDict
import json


class WeatherStorage:
    """Interface for any storage saving weather"""
    def save(self, coordinates: Coordinates, weather: Weather) -> None:
        raise NotImplementedError


class PlainFileWeatherStorage(WeatherStorage):
    """Store weather in plain text file"""
    def __init__(self, file: Path) -> None:
        self._file = file

    def save(self, coordinates: Coordinates, weather: Weather) -> None:
        now = datetime.now()
        formatted_weather = format_weather(coordinates, weather)
        with open(self._file, "a") as f:
            f. write(f"{now}\n{formatted_weather}\n\n")


class HistoryRecord(TypedDict):
    date: str
    weather: str


class JSONFileWeatherStorage(WeatherStorage):
    """Store weathre in JSON file"""
    def __init__(self, jsonfile: Path) -> None:
        self._jsonfile = jsonfile
        self._init_storage()

    def save(self, coordinates: Coordinates, weather: Weather) -> None:
        history = self._read_history()
        history.append({
            "date": str(datetime.now()),
            "weather": format_weather(coordinates, weather)
        })
        self._write(history)

    def _init_storage(self) -> None:
        if not self._jsonfile.exists():
            self._jsonfile.write_text("[]")

    def _read_history(self) -> list[HistoryRecord]:
        with open(self._jsonfile, "r") as f:
            return json.load(f)
        
    def _write(self, history: list[HistoryRecord]) -> None:
        with open(self._jsonfile, "w") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
        

def save_weather(coordinates: Coordinates, weather: Weather, storage: WeatherStorage) -> None:
    """Saves weathre in the storage"""
    storage.save(coordinates, weather)
