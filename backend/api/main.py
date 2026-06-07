from fastapi import FastAPI
from backend.api.state_cache import latest_state, latest_output, system_config
from backend.subscriber.subscriber import run_mqtt

app = FastAPI(title="Digital Twin API")


@app.on_event("startup")
def start_mqtt():
    import threading
    thread = threading.Thread(target=run_mqtt)
    thread.daemon = True
    thread.start()

# ---------------------------
# 1. Live system state (from MQTT pipeline)
# ---------------------------


@app.get("/state/live")
def get_live_state():
    return latest_state


# ---------------------------
# 2. Live DQN output
# ---------------------------
@app.get("/output/live")
def get_live_output():
    return latest_output


# ---------------------------
# 3. Full system snapshot
# ---------------------------
@app.get("/system")
def system_snapshot():
    return {
        "config": system_config,
        "state": latest_state,
        "output": latest_output
    }


# ---------------------------
# 4. Optional: trigger run (if you still want manual control)
# ---------------------------
@app.post("/run")
def trigger_run():
    return {
        "status": "ok",
        "message": "Run is event-driven via MQTT (no manual compute needed)"
    }
