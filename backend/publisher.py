import json
import time
import paho.mqtt.client as mqtt


from sources.nasa_source import get_data
# from sources.csv_source import get_data

client = mqtt.Client()
client.connect("localhost", 1883, 60)


topic = "weather/data"
# topic = "co2/data"

for row in get_data():
    client.publish(topic, json.dumps(row))
    print("Published:", row)
    time.sleep(1)

client.disconnect()
