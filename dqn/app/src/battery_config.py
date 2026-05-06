from dataclasses import dataclass

@dataclass
class BatteryConfig:
    depth_of_discharge: float = 0.90
    soc_max: float = 1.0
    soc_min: float = 0.10
    battery_initial_capacity: float = 0.5
    eta_ch: float = 0.90 # Charge efficiency
    eta_dch: float = 0.90 # Discharge efficiency
    eta_conv: float = 0.95 # Convert efficiency