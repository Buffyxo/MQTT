import gymnasium as gym
import numpy as np
import random
from src.battery_config import BatteryConfig
from src.solar_config import SolarConfig
from src.engery_config import EngeryConfig
from src.data_container import DataContainer
from sklearn.preprocessing import MinMaxScaler
import logging

logger = logging.getLogger(__name__)


class EnergyEnvironment(gym.Env):
    """
    Action space (5 actions):
      0 = charge battery
      1 = discharge battery
      2 = do nothing (passive — solar fills battery if surplus)
      3 = defer aircon (queue this hour's aircon for later)
      4 = run deferred aircon (pull oldest from queue, add to demand)

    State (12 features, all 0–1):
      hour, solar, total_demand, co2, battery_soc, month,
      aircon, plugs, lighting, other,
      queued_kwh, queue_size
    """

    AIRCON_DEFER_WINDOW = 4  # hours — must run within this many hours

    def __init__(self,
                 date_container: DataContainer,
                 battery_config: BatteryConfig = BatteryConfig(),
                 energy_config: EngeryConfig = EngeryConfig(),
                 solar_config: SolarConfig = SolarConfig()):
        super().__init__()
        self.date_container = date_container
        self.raw_data = date_container.data.copy()
        self._normalize_data()

        self.battery_config = battery_config
        self.default_battery_config = battery_config
        self.solar_config = solar_config
        self.energy_config = energy_config

        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(18,), dtype=np.float32
        )
        self.action_space = gym.spaces.Discrete(5)

        # Live episode state
        self.current_step = 0
        self.current_date = 0
        self.current_battery_capacity = battery_config.battery_initial_capacity
        self.aircon_queue = []  # list of (kwh, deadline_hour) tuples

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.battery_config = self.default_battery_config
        self.current_battery_capacity = self.battery_config.battery_initial_capacity
        max_start_date = (len(self.date_container.data) - 24) // 24
        self.current_date = random.randint(0, max_start_date)
        self.current_step = 0
        self.aircon_queue = []

        return self._get_state(), {}

    def step(self, action: int):
        row_index = (self.current_date * 24) + self.current_step
        raw_row = self.raw_data.iloc[row_index]
        norm_row = self.date_container.data.iloc[row_index]

        # ── Solar generation (paper equations) ───────────────
        g_i = float(raw_row['Predicted_Gb(i)']) / 1000
        energy_per_panel = (g_i * self.solar_config.p_peak
                            * self.solar_config.eta_global * self.solar_config.a_sp)
        solar_kwh = energy_per_panel * self.solar_config.n_pannels

        # ── Build effective demand from sub-loads ────────────
        # NOTE: sum the parts directly, do NOT use Total_Demand_kWh
        # (otherwise aircon gets double-counted when we also add it).
        base_demand = (
            float(raw_row['Plugs_kWh'])
            + float(raw_row['Lighting_kWh'])
            + float(raw_row['Other_kWh'])
        )
        aircon_now = float(raw_row['Aircon_kWh'])

        # Handle aircon shifting actions
        if action == 3:  # defer this hour's aircon
            if aircon_now > 0:
                deadline = self.current_step + self.AIRCON_DEFER_WINDOW
                self.aircon_queue.append((aircon_now, deadline))
            aircon_demand = 0.0
        elif action == 4 and self.aircon_queue:  # run oldest deferred
            deferred_kwh, _ = self.aircon_queue.pop(0)
            aircon_demand = aircon_now + deferred_kwh
        else:
            aircon_demand = aircon_now

        # Force-run anything past its deadline (user comfort constraint)
        expired = [(k, d) for k, d in self.aircon_queue if d <= self.current_step]
        self.aircon_queue = [(k, d) for k, d in self.aircon_queue if d > self.current_step]
        forced_run = sum(k for k, _ in expired)

        effective_demand = base_demand + aircon_demand + forced_run

        # ── SOC limits ───────────────────────────────────────
        soc_min = self.battery_config.soc_max * (1 - self.battery_config.depth_of_discharge)
        soc_max = self.battery_config.soc_max

        # ── Battery action — determine flow ──────────────────
        # Convention: battery_flow > 0 = charging, < 0 = discharging
        battery_flow = 0.0

        if action == 0:  # CHARGE
            room = soc_max - self.current_battery_capacity
            battery_flow = min(self.energy_config.battery_charge_rate, room)

        elif action == 1:  # DISCHARGE
            available = self.current_battery_capacity - soc_min
            battery_flow = -min(self.energy_config.battery_discharge_rate, available)

        elif action == 2:  # DO NOTHING — passively absorb surplus solar
            net_solar = solar_kwh - effective_demand
            if net_solar > 0:
                room = soc_max - self.current_battery_capacity
                battery_flow = min(net_solar, room)

        # Actions 3 & 4 don't directly touch the battery — same passive
        # behaviour as "do nothing" for any leftover solar
        if action in (3, 4):
            net_solar = solar_kwh - effective_demand
            if net_solar > 0:
                room = soc_max - self.current_battery_capacity
                battery_flow = min(net_solar, room)

        # ── Update SOC (apply efficiency) ────────────────────
        if battery_flow > 0:
            self.current_battery_capacity += battery_flow * self.battery_config.eta_ch
        elif battery_flow < 0:
            self.current_battery_capacity += battery_flow / self.battery_config.eta_dch
        self.current_battery_capacity = float(np.clip(
            self.current_battery_capacity, soc_min, soc_max
        ))

        # ── Grid import = supply shortfall ───────────────────
        load = effective_demand + max(0, battery_flow)     # demand + any charging
        supply = solar_kwh + max(0, -battery_flow)         # solar + any discharging
        grid_import = max(0.0, load - supply)

        # ── Reward — pure physics, no shaping ────────────────
        co2_normalised = float(norm_row['CDEII_gCO2_per_kWh'])
        reward = -grid_import - 0.3 * grid_import * co2_normalised

        # ── Advance ──────────────────────────────────────────
        self.current_step += 1
        done = self.current_step >= 24

        # End-of-day: any leftover queued aircon must be flushed as grid load
        if done and self.aircon_queue:
            leftover = sum(k for k, _ in self.aircon_queue)
            reward -= leftover * (1 + 0.3 * co2_normalised)
            self.aircon_queue = []

        next_state = self._get_state() if not done else np.zeros(18, dtype=np.float32)

        return next_state, reward, done, False, {
            'grid_import': grid_import,
            'solar_kwh': solar_kwh,
            'effective_demand': effective_demand,
            'battery_flow': battery_flow,
            'queue_size': len(self.aircon_queue),
        }

    def _get_state(self):
        row_index = (self.current_date * 24) + self.current_step
        row = self.date_container.data.iloc[row_index]

        queued_kwh = sum(k for k, _ in self.aircon_queue)
        
        future_solar = []
        future_demand = []
        
        for i in range(1, 4):
            future_idx = min(row_index + i, len(self.date_container.data) - 1)
            future_row = self.date_container.data.iloc[future_idx]
            future_solar.append(future_row['Predicted_Gb(i)'])
            future_demand.append(float(future_row['Total_Demand_kWh']))

        # Normalise queue features
        queued_norm = min(queued_kwh / max(self.AIRCON_DEFER_WINDOW, 1), 1.0)
        queue_size_norm = len(self.aircon_queue) / max(self.AIRCON_DEFER_WINDOW, 1)

        state = np.array([
            self.current_step / 23.0,
            row['Predicted_Gb(i)'],
            row['Total_Demand_kWh'],
            row['CDEII_gCO2_per_kWh'],
            self.current_battery_capacity,
            row.name.month / 12.0,
            row['Aircon_kWh'],
            row['Plugs_kWh'],
            row['Lighting_kWh'],
            row['Other_kWh'],
            queued_norm,
            queue_size_norm,
            *future_solar,
            *future_demand,
        ], dtype=np.float32)

        return state

    def _normalize_data(self):
        scaler = MinMaxScaler()
        for col in self.date_container.data:
            self.date_container.data[col] = scaler.fit_transform(self.date_container.data[[col]])

        logger.debug(self.date_container.data['CDEII_gCO2_per_kWh'].describe())
        logger.debug(self.date_container.data['Total_Demand_kWh'].describe())