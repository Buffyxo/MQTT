import requests

DQN_URL = "http://localhost:8000"


def send_to_dqn(state):

    payload = {
        "state": state
    }

    response = requests.post(
        f"{DQN_URL}/predict",
        json=payload
    )

    return response.json()
