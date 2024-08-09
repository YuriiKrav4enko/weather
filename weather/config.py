USE_ROUNDED_COORDS = True

OPENMETEO_URL = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude={latitude}&longitude={longitude}&"
    "current=temperature_2m,apparent_temperature,weather_code&"
    "daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,daylight_duration&"
    "timezone=GMT&forecast_days=1"
)
