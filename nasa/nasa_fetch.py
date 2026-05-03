import requests
import pandas as pd
import time

# T2M = temp, RH2M = humidity, WS2M = wind speed
url = "https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=T2M,RH2M,WS2M&community=RE&latitude=-37.8136&longitude=144.9631&start=20240101&end=20240102&format=JSON"

response = requests.get(url)
data = response.json()

params = data["properties"]["parameter"]

t2m = params["T2M"]
rh2m = params["RH2M"]
ws2m = params["WS2M"]

rows = []

for timestamp in t2m:
    row = {
        "timestamp": timestamp,
        "temperature": t2m[timestamp],
        "humidity": rh2m[timestamp],
        "wind_speed": ws2m[timestamp]
    }
    rows.append(row)

# print(rows[:5])


df = pd.DataFrame(rows)
# print(df.head())

for _, row in df.iterrows():

    print(row.to_dict())

    time.sleep(1)

# print(data)
