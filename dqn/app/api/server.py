import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import state, schemas
from app.models.qlearning.model_predict import predict
from app.models.qlearning.model_validate import validate, validate_baseline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ACTION_NAMES = {
    0: 'charge',
    1: 'discharge',
    2: 'do nothing',
    3: 'defer aircon',
    4: 'run deferred aircon',
}

app = FastAPI(
    title="Energy Management API",
    description="DQN-based home energy scheduling",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


@app.on_event("startup")
def startup():
    """Runs once when the server starts."""
    state.initialize()
    


@app.get("/health")
def health():
    """Quick check that the server and model are up."""
    try:
        state.get_dqn()
        state.get_env()
        return {"status": "ok", "model_loaded": True}
    except RuntimeError:
        return {"status": "ok", "model_loaded": False}
    
@app.post("/predict", response_model=schemas.PredictResponse)
def predict_endpoint(request: schemas.PredictRequest):
    """
    Run the trained DQN for one day and return the 24-hour schedule.
    """
    dqn = state.get_dqn()
    env = state.get_env()

    schedule = predict(dqn, env, date=request.date)

    # Aggregate daily totals from the hourly schedule
    daily_grid = sum(h['grid_import_kwh'] for h in schedule)
    daily_solar = sum(h['solar_kwh'] for h in schedule)
    daily_demand = sum(h['demand_kwh'] for h in schedule)
    daily_ref = (daily_demand - daily_grid) / daily_demand if daily_demand > 0 else 0.0

    return schemas.PredictResponse(
        date_index=env.current_date,
        schedule=schedule,
        daily_grid_import_kwh=round(daily_grid, 3),
        daily_solar_kwh=round(daily_solar, 3),
        daily_demand_kwh=round(daily_demand, 3),
        daily_ref=round(daily_ref, 4),
    )
    
@app.post("/validate", response_model=schemas.ValidateResponse)
def validate_endpoint(request: schemas.ValidateRequest):
    """
    Run baseline and DQN on the same seeded days, return comparison metrics.
    """
    dqn = state.get_dqn()
    env = state.get_env()

    baseline = validate_baseline(env, episodes=request.episodes, seed=request.seed)
    trained = validate(dqn, env, episodes=request.episodes, seed=request.seed)

    n = request.episodes

    def avg(d, key):
        return sum(d[key]) / n

    def pct(new, old):
        return ((new - old) / abs(old) * 100) if old != 0 else 0.0

    DIRECTIONS = {
    "Reward": "higher_better",
    "Grid Import (kWh)": "lower_better",
    "REF": "higher_better",
    "CO2": "lower_better",
    }

    metrics = []
    for label, key in [
        ("Reward", "total_reward"),
        ("Grid Import (kWh)", "grid_import"),
        ("REF", "ref"),
        ("CO2", "co2"),
    ]:
        b = avg(baseline, key)
        d = avg(trained, key)
        raw_pct = pct(d, b)
        direction = DIRECTIONS[label]
        improvement = raw_pct if direction == "higher_better" else -raw_pct
        metrics.append(schemas.MetricRow(
            metric=label,
            baseline=round(b, 4),
            dqn=round(d, 4),
            improvement_pct=round(improvement, 2),
        ))

    return schemas.ValidateResponse(
        episodes=request.episodes,
        seed=request.seed,
        comparison=metrics,
    )
    
@app.post("/forecast", response_model=schemas.ForecastResponse)
def forecast_endpoint(request: schemas.ForecastRequest):
    """
    Given a current date and hour, return the next N hours of recommended actions.
    """
    dqn = state.get_dqn()
    env = state.get_env()

    # Reset to the requested starting point
    env.reset()
    env.current_date = request.date
    env.current_step = request.current_hour
    env.current_battery_capacity = request.battery_soc
    state_vec = env._get_state()

    horizon = []
    for offset in range(request.hours_ahead):
        action = dqn.best_action(state_vec)
        next_state, reward, done, _, info = env.step(action)
        horizon.append({
            'hour_offset': offset,
            'absolute_hour': (request.current_hour + offset) % 24,
            'action_id': action,
            'action_name': ACTION_NAMES[action],
            'predicted_solar_kwh': round(info['solar_kwh'], 3),
            'predicted_demand_kwh': round(info['effective_demand'], 3),
            'expected_grid_import_kwh': round(info['grid_import'], 3),
            'battery_soc_after': round(env.current_battery_capacity, 3),
        })
        state_vec = next_state
        if done:
            break

    return schemas.ForecastResponse(
        from_date=request.date,
        from_hour=request.current_hour,
        horizon=horizon,
    )