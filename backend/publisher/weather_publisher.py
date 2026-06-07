from ..sources.nasa_source import get_data
import json
import time
import paho.mqtt.client as mqtt
from datetime import datetime

client = mqtt.Client()
client.connect("localhost", 1883, 60)

for row in get_data():
    client.publish("dt/weather", json.dumps(row))
    print("Published weather:", row)
    time.sleep(1)

client.disconnect()
