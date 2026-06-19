import json
import psycopg2
import paho.mqtt.client as mqtt
from datetime import datetime, timezone

from ..services.state_builder import build_state
from ..services.dqn_bridge import send_to_dqn
from backend.api.state_cache import latest_state, latest_output
from backend.services.redis_client import redis_client


# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="digitaltwin",
    user="zara",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


# MQTT CACHE
latest_state_cache = {
    "weather": None,
    "co2": None,
    "demand": None,
    "solar": None
}


# Helpers
def parse_timestamp(ts: str):
    """
    Supports:
    - ISO format: 2024-01-01T00:00:00
    - Backup format: 2024010100
    """
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        return datetime.strptime(ts, "%Y%m%d%H")


# DB INSERT: CO2
def insert_co2(payload):
    cursor.execute(
        """
        INSERT INTO co2_data (
            timestamp,
            co2_g_per_kwh,
            co2_kg_per_kwh
        )
        VALUES (%s, %s, %s)
        """,
        (
            datetime.now(timezone.utc),
            payload.get("co2_g_per_kwh", 0),
            payload.get("co2_kg_per_kwh", 0)
        )
    )
    conn.commit()


# DB INSERT: WEATHER

def insert_weather(payload):
    try:
        ts = parse_timestamp(payload["timestamp"])

        cursor.execute(
            """
            INSERT INTO weather_data (
                timestamp,
                temperature,
                humidity,
                wind_speed,
                solar_radiation
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                ts,
                payload.get("temperature", 0),
                payload.get("humidity", 0),
                payload.get("wind_speed", 0),
                payload.get("solar_radiation", 0)
            )
        )

        conn.commit()

    except Exception as e:
        print("WEATHER INSERT ERROR:", e)
        print("BAD PAYLOAD:", payload)


# DQN PIPELINE

def try_run_ml(client):

    # ensure all streams exist
    if not all(latest_state_cache.values()):
        return

    try:
        state = build_state(
            latest_state_cache["weather"],
            latest_state_cache["co2"],
            latest_state_cache["demand"],
            latest_state_cache["solar"]
        )

        print("\n===== DQN STATE =====")
        print(state)

        result = send_to_dqn(state)

        print("\n===== DQN RESULT =====")
        print(result)

        # Update FastAPI shared cache

        # REDIS

        redis_client.set(
            "state:latest",
            json.dumps(state)
        )

        redis_client.set(
            "output:dqn",
            json.dumps(result)
        )

        # Publish to MQTT
        client.publish(
            "dt/output",
            json.dumps(result)
        )

        print("Published -> dt/output")

    except Exception as e:
        print("DQN ERROR:", e)


# MQTT MESSAGE HANDLER
def on_message(client, userdata, msg):

    print(f"Received [{msg.topic}]")

    data = json.loads(msg.payload.decode())

    if msg.topic == "dt/weather":
        insert_weather(data)
        latest_state_cache["weather"] = data
        print("Weather updated")

    elif msg.topic == "dt/co2":
        insert_co2(data)
        latest_state_cache["co2"] = data
        print("CO2 updated")

    elif msg.topic == "dt/demand/predicted":
        latest_state_cache["demand"] = data
        print("Demand updated")

    elif msg.topic == "dt/solar/predicted":
        latest_state_cache["solar"] = data
        print("Solar updated")

    # run ML after every update
    try_run_ml(client)


# MQTT SETUP
def run_mqtt():
    client = mqtt.Client()
    client.on_message = on_message

    client.connect("localhost", 1883, 60)

    client.subscribe("dt/weather")
    client.subscribe("dt/co2")
    client.subscribe("dt/demand/predicted")
    client.subscribe("dt/solar/predicted")

    print("MQTT Subscriber Running...")
    client.loop_forever()


if __name__ == "__main__":
    run_mqtt()
