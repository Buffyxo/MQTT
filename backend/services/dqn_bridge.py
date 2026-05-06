from services.state_builder import build_state
from sources.db import get_latest_weather
import requests


def send_to_dqn():
    latest_weather = get_latest_weather()

    state = build_state(latest_weather)

    response = requests.post("http://dqn-api/predict", json=state)

    return response.json()
