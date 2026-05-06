from models.qlearning.energy_environment import EnergyEnvironment
from models.qlearning.dqn import DQN
import logging

logger = logging.getLogger(__name__)

def predict(dqn:DQN, env:EnergyEnvironment, date:int = None):
    """Run the trained DQN on a single day and return the hourly schedule."""
    state, _ = env.reset()
    
    if date is not None:
        env.current_date = date
        state = env._get_state()
        
    action_names = {
        0: 'charge',
        1: 'discharge',
        2: 'do nothing',
        3: 'defer aircon',
        4: 'run deferred aircon'
    }
    
    results = []
    
    for hour in range(24):
        action = dqn.best_action(state)
        
        next_state, reward, done, _, info = env.step(action)
        
        results.append({
            'hour': hour,
            'action_id': action,
            'action_name': action_names[action],
            'battery_soc': round(env.current_battery_capacity, 3),
            'solar_kwh': round(info['solar_kwh'], 3),
            'demand_kwh': round(info['effective_demand'], 3),
            'grid_import_kwh': round(info['grid_import'], 3),
            'queue_size': info['queue_size'],
            'reward': round(reward, 3),        
        })
        
        state = next_state
        if done:
            break
        
    return results