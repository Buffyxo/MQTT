from dataclasses import dataclass

@dataclass
class EngeryConfig:
    battery_discharge_rate: float = 0.1
    battery_charge_rate: float = 0.1
    solar_capacity: float = 5.0
    solar_efficiency: float = 0.2
