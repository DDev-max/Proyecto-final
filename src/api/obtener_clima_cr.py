import requests

def obtener_clima_cr():
    url = "https://archive-api.open-meteo.com/v1/era5"

    params = {
        "latitude": 9.9281,
        "longitude": 84.0907,
        "start_date": "2023-01-01",
        "end_date": "2024-12-31",
        "hourly": ["cloud_cover", "precipitation", "apparent_temperature", "wind_speed_10m", "sunshine_duration"]
    }

    try:
        respuesta = requests.get(url, params=params)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.RequestException as e:
        print(f"Error consultando la API: {e}")