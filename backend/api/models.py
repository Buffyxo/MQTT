from pydantic import BaseModel


class BatteryConfig(BaseModel):
    battery_capacity_kwh: float
    max_charge_rate_kw: float
    max_discharge_rate_kw: float
    max_soc: float
    solar_panels: int


class RunRequest(BaseModel):
    forecast_horizon_hours: int
