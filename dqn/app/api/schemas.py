from pydantic import BaseModel, Field
from typing import Optional


class PredictRequest(BaseModel):
    """Body sent to POST /predict."""
    date: Optional[int] = Field(
        default=None,
        ge=0, le=364,
        description="Day index 0-364. Random if omitted.",
    )


class HourlyResult(BaseModel):
    """One row of the 24-hour schedule."""
    hour: int
    action_id: int
    action_name: str
    battery_soc: float
    solar_kwh: float
    demand_kwh: float
    grid_import_kwh: float
    queue_size: int
    reward: float


class PredictResponse(BaseModel):
    """Body returned from POST /predict."""
    date_index: int
    schedule: list[HourlyResult]
    daily_grid_import_kwh: float
    daily_solar_kwh: float
    daily_demand_kwh: float
    daily_ref: float


class ValidateRequest(BaseModel):
    """Body sent to POST /validate."""
    episodes: int = Field(default=100, ge=1, le=1000)
    seed: int = Field(default=42)


class MetricRow(BaseModel):
    """One metric in the comparison table."""
    metric: str
    baseline: float
    dqn: float
    improvement_pct: float


class ValidateResponse(BaseModel):
    """Body returned from POST /validate."""
    episodes: int
    seed: int
    comparison: list[MetricRow]
    
class ForecastRequest(BaseModel):
    """Body sent to POST /forcast."""
    date: int = Field(ge=0, le=364)
    current_hour: int = Field(ge=0, le=23)
    battery_soc: float = Field(ge=0.0, le=1.0, default=0.5)
    hours_ahead: int = Field(default=3, ge=1, le=12)


class HorizonStep(BaseModel):
    """Hour breakdown."""
    hour_offset: int
    absolute_hour: int
    action_id: int
    action_name: str
    predicted_solar_kwh: float
    predicted_demand_kwh: float
    expected_grid_import_kwh: float
    battery_soc_after: float


class ForecastResponse(BaseModel):
    """Body retured from post /forecast."""
    from_date: int
    from_hour: int
    horizon: list[HorizonStep]