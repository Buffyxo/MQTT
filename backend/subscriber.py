import json
import psycopg2
import paho.mqtt.client as mqtt
from datetime import datetime

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="digitaltwin",
    user="zara",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

# CSV for hourly data


def insert_co2(payload):
    cursor.execute(
        """
        INSERT INTO co2_data (timestamp, co2_g_per_kwh, co2_kg_per_kwh)
        VALUES (%s, %s, %s)
        """,
        (
            datetime.utcnow(),
            payload["co2_g_per_kwh"],
            payload["co2_kg_per_kwh"]
        )
    )
    conn.commit()

# Nasa data


def insert_weather(payload):
    cursor.execute(
        """
        INSERT INTO weather_data (timestamp, temperature, humidity, wind_speed)
        VALUES (%s, %s, %s, %s)
        """,
        (
            payload["timestamp"],
            payload["temperature"],
            payload["humidity"],
            payload["wind_speed"]
        )
    )
    conn.commit()

# Message routing according to topic


def on_message(client, userdata, msg):
    print("Received:", msg.topic, msg.payload.decode())

    data = json.loads(msg.payload.decode())

    if msg.topic == "co2/data":
        insert_co2(data)

    elif msg.topic == "weather/data":
        insert_weather(data)


# MQTT setup
client = mqtt.Client()
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.subscribe("co2/data")
client.subscribe("weather/data")

client.loop_forever()
