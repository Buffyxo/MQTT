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

def insert_data(payload):
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

# MQTT callback
def on_message(client, userdata, msg):
    print("Received:", msg.payload.decode())

    data = json.loads(msg.payload.decode())
    insert_data(data)

# MQTT setup
client = mqtt.Client()
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.subscribe("co2/data")

client.loop_forever()

