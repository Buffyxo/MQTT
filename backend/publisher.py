import pandas as pd
import json
import time
import paho.mqtt.client as mqtt

df = pd.read_csv("./data/cdeii_vic_hourly_2024.csv")

client = mqtt.Client()
client.connect("localhost", 1883, 60)

topic = "co2/data"

for _, row in df.iterrows():

    payload = {
        "timestamp": str(row["Date/Time"]),
        "co2_g_per_kwh": row["CDEII_gCO2_per_kWh"],
        "co2_kg_per_kwh": row["CDEII_kgCO2_per_kWh"]
    }

    client.publish(topic, json.dumps(payload))
    print("Published:", payload)

    time.sleep(1)  

client.disconnect()
