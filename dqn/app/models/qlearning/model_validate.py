from models.qlearning.energy_environment import EnergyEnvironment
from models.qlearning.dqn import DQN
import logging
import random
import numpy as np

logger = logging.getLogger(__name__)

ACTION_NAMES = {
    0: 'charge',
    1: 'discharge',
    2: 'do nothing',
    3: 'defer aircon',
    4: 'run deferred',
}


def validate(dqn: DQN, env: EnergyEnvironment, episodes: int = 100, seed: int = 42):
    """Run the trained DQN on a set of seeded days and report metrics."""
    random.seed(seed)
    np.random.seed(seed)

    results = {
        'total_reward': [], 'grid_import': [], 'ref': [], 'co2': [],
        'total_demand': [], 'aircon': [], 'plugs': [], 'lighting': [], 'other': [],
        'solar': [], 'predicted_demand': [], 'singlehouse_demand': [], 'actions': [],
    }

    for episode in range(episodes):
        state, _ = env.reset()
        ep_reward = ep_grid = ep_solar = ep_demand = ep_co2 = 0
        ep_aircon = ep_plugs = ep_lighting = ep_other = 0
        ep_pred_demand = ep_single_demand = 0
        ep_actions = []

        for step in range(24):
            action = dqn.best_action(state)
            next_state, reward, done, _, info = env.step(action)
            ep_reward += reward
            ep_actions.append(action)

            # Trust the environment for physics
            ep_grid += info['grid_import']
            ep_solar += info['solar_kwh']
            ep_demand += info['effective_demand']

            # Pull contextual columns from raw data
            row_index = (env.current_date * 24) + step
            raw_row = env.raw_data.iloc[row_index]
            norm_row = env.date_container.data.iloc[row_index]

            ep_co2 += info['grid_import'] * float(norm_row['CDEII_gCO2_per_kWh'])
            ep_aircon += float(raw_row['Aircon_kWh'])
            ep_plugs += float(raw_row['Plugs_kWh'])
            ep_lighting += float(raw_row['Lighting_kWh'])
            ep_other += float(raw_row['Other_kWh'])
            ep_pred_demand += float(raw_row['Predicted Demand (kWh)'])
            ep_single_demand += float(raw_row['Singlehouse Demand (kWh)'])

            state = next_state
            if done:
                break

        ref = (ep_demand - ep_grid) / ep_demand if ep_demand > 0 else 0
        results['total_reward'].append(ep_reward)
        results['grid_import'].append(ep_grid)
        results['ref'].append(ref)
        results['co2'].append(ep_co2)
        results['total_demand'].append(ep_demand)
        results['solar'].append(ep_solar)
        results['aircon'].append(ep_aircon)
        results['plugs'].append(ep_plugs)
        results['lighting'].append(ep_lighting)
        results['other'].append(ep_other)
        results['predicted_demand'].append(ep_pred_demand)
        results['singlehouse_demand'].append(ep_single_demand)
        results['actions'].append(ep_actions)

    _print_dqn_results(results, episodes)
    return results


def validate_baseline(env: EnergyEnvironment, episodes: int = 100, seed: int = 42):
    """Run a do-nothing baseline (action 2 every step) on the same seeded days."""
    random.seed(seed)
    np.random.seed(seed)

    results = {'total_reward': [], 'grid_import': [], 'ref': [], 'co2': []}

    for episode in range(episodes):
        state, _ = env.reset()
        ep_reward = ep_grid = ep_demand = ep_co2 = 0

        for step in range(24):
            next_state, reward, done, _, info = env.step(2)  # always do nothing
            ep_reward += reward

            row_index = (env.current_date * 24) + step
            norm_row = env.date_container.data.iloc[row_index]

            ep_grid += info['grid_import']
            ep_demand += info['effective_demand']
            ep_co2 += info['grid_import'] * float(norm_row['CDEII_gCO2_per_kWh'])

            state = next_state
            if done:
                break

        ref = (ep_demand - ep_grid) / ep_demand if ep_demand > 0 else 0
        results['total_reward'].append(ep_reward)
        results['grid_import'].append(ep_grid)
        results['ref'].append(ref)
        results['co2'].append(ep_co2)

    n = episodes
    logger.info(f"Baseline Avg Reward:      {sum(results['total_reward'])/n:.3f}")
    logger.info(f"Baseline Avg Grid Import: {sum(results['grid_import'])/n:.3f}")
    logger.info(f"Baseline Avg REF:         {(sum(results['ref'])/n)*100:.3f}%")
    logger.info(f"Baseline Avg CO2:         {sum(results['co2'])/n:.3f}")

    return results


def _print_dqn_results(results, episodes):
    n = episodes
    logger.info(f"\n{'='*65}")
    logger.info(f"{'DQN VALIDATION RESULTS':^65}")
    logger.info(f"{'='*65}")
    logger.info(f"{'Metric':<30} {'Avg per Day':>15}")
    logger.info(f"{'-'*65}")
    logger.info(f"{'Reward':<30} {sum(results['total_reward'])/n:>15.3f}")
    logger.info(f"{'Grid Import (kWh)':<30} {sum(results['grid_import'])/n:>15.3f}")
    logger.info(f"{'REF':<30} {(sum(results['ref'])/n)*100:>14.3f}%")
    logger.info(f"{'CO2 (normalised)':<30} {sum(results['co2'])/n:>15.3f}")
    logger.info(f"{'Solar Generated (kWh)':<30} {sum(results['solar'])/n:>15.4f}")
    logger.info(f"{'Effective Demand (kWh)':<30} {sum(results['total_demand'])/n:>15.4f}")
    logger.info(f"{'Predicted Demand (kWh)':<30} {sum(results['predicted_demand'])/n:>15.4f}")
    logger.info(f"{'Singlehouse Demand (kWh)':<30} {sum(results['singlehouse_demand'])/n:>15.4f}")
    logger.info(f"{'Aircon (kWh)':<30} {sum(results['aircon'])/n:>15.4f}")
    logger.info(f"{'Plugs (kWh)':<30} {sum(results['plugs'])/n:>15.4f}")
    logger.info(f"{'Lighting (kWh)':<30} {sum(results['lighting'])/n:>15.4f}")
    logger.info(f"{'Other (kWh)':<30} {sum(results['other'])/n:>15.4f}")
    logger.info(f"{'='*65}")

    # Action distribution
    all_actions = [a for ep in results['actions'] for a in ep]
    logger.info(f"\n{'ACTION DISTRIBUTION':^65}")
    logger.info(f"{'-'*65}")
    for action_id, name in ACTION_NAMES.items():
        count = all_actions.count(action_id)
        pct = count / len(all_actions) * 100 if all_actions else 0
        logger.info(f"  {name:<15} {count:>6}  {pct:>5.1f}%")
    logger.info(f"{'='*65}\n")


def print_results_table(baseline_results, dqn_results, episodes):
    b = {k: sum(v) / episodes for k, v in baseline_results.items()}
    d = {k: sum(dqn_results[k]) / episodes for k in baseline_results.keys()}

    def pct(new, old):
        return ((new - old) / abs(old) * 100) if old != 0 else 0

    logger.info(f"\n{'Metric':<15} {'Baseline':>10} {'DQN':>10} {'Improvement':>13}")
    logger.info("-" * 54)
    logger.info(f"{'Reward':<15} {b['total_reward']:>10.3f} {d['total_reward']:>10.3f} {pct(d['total_reward'], b['total_reward']):>+12.1f}%")
    logger.info(f"{'Grid Import':<15} {b['grid_import']:>10.3f} {d['grid_import']:>10.3f} {pct(d['grid_import'], b['grid_import']):>+12.1f}%")
    logger.info(f"{'REF':<15} {b['ref']:>10.3f} {d['ref']:>10.3f} {pct(d['ref'], b['ref']):>+12.1f}%")
    logger.info(f"{'CO2':<15} {b['co2']:>10.3f} {d['co2']:>10.3f} {pct(d['co2'], b['co2']):>+12.1f}%\n")