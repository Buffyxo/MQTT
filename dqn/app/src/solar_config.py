from dataclasses import dataclass

@dataclass
class SolarConfig:
    p_peak: float = 0.4
    a_sp: float = 2.1
    eta_global: float = 0.637
    n_pannels: int = 10
    eta_conv: float = 0.95