import requests
import pandas as pd
from db import get_latest_weather
from state_builder import build_state

weather = get_latest_weather()
state = build_state(weather)

response = requests.post(
    "http://localhost:8000/predict",
    json=state
)

result = response.json()

df = pd.DataFrame(result["schedule"])

print(df.head())
