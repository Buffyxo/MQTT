import requests
import pandas as pd


def get_data():

    url = "https://power.larc.nasa.gov/api/temporal/hourly/point"

    params = {

        "parameters": "T2M,RH2M,WS2M,ALLSKY_SFC_SW_DWN",

        "community": "RE",

        "latitude": -37.8136,

        "longitude": 144.9631,

        "start": "20240101",

        "end": "20240102",

        "format": "JSON"

    }

    response = requests.get(url, params=params)

    data = response.json()

    params_data = data["properties"]["parameter"]

    t2m = params_data["T2M"]

    rh2m = params_data["RH2M"]

    ws2m = params_data["WS2M"]

    solar = params_data["ALLSKY_SFC_SW_DWN"]

    for timestamp in t2m:

        yield {

            "timestamp": timestamp,

            "temperature": t2m[timestamp],

            "humidity": rh2m[timestamp],

            "wind_speed": ws2m[timestamp],

            "solar_radiation": solar[timestamp]

        }
