import requests
import pandas as pd
from db import get_latest_weather
from state_builder import build_state

weather = get_latest_weather()
state = build_state(weather)

payload = {
    "date": state["date"],
    "current_hour": 12,
    "battery_soc": state["battery_soc"],
    "hours_ahead": 5
}

response = requests.post(
    "http://localhost:8000/forecast",
    json=payload
)

result = response.json()

df = pd.DataFrame(result["horizon"])

print(df.head())
