from fastapi import FastAPI
from backend.subscriber.subscriber import run_mqtt
from backend.services.redis_client import redis_client

import json

app = FastAPI(title="Digital Twin API")


@app.on_event("startup")
def start_mqtt():
    import threading
    thread = threading.Thread(target=run_mqtt)
    thread.daemon = True
    thread.start()


# 1. Live system state (from MQTT pipeline)


@app.get("/state/live")
def get_live_state():
    state = redis_client.get(

        "state:latest"

    )

    if not state:

        return {}

    return json.loads(state)


# 2. Live DQN output

@app.get("/output/live")
def get_live_output():
    output = redis_client.get(

        "output:dqn"

    )

    if not output:

        return {}

    return json.loads(output)


# 3. Full system snapshot

@app.get("/system")
def system_snapshot():
    state = redis_client.get(

        "state:latest"

    )

    output = redis_client.get(

        "output:dqn"

    )

    return {

        "state":

            json.loads(state)

            if state else {},

        "output":

            json.loads(output)

            if output else {}

    }


# 4. Optional: trigger run
@app.post("/run")
def trigger_run():
    return {
        "status": "ok",
        "message": "Run is event-driven via MQTT (no manual compute needed)"
    }
