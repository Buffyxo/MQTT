from ..sources.solar_source import get_data

import json
import time
import paho.mqtt.client as mqtt

client = mqtt.Client()

client.connect(
    "localhost",
    1883,
    60
)

for row in get_data():

    client.publish(
        "dt/solar/predicted",
        json.dumps(row)
    )

    print(row)

    time.sleep(1)

client.disconnect()
