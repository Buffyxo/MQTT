import argparse
import logging
import os
import pandas
import torch
from src.data_container import DataContainer
from src.battery_config import BatteryConfig
from utilities.data_reader import read_csv
from models.qlearning.energy_environment import EnergyEnvironment
from models.qlearning.dqn import DQN
from models.qlearning.replay_buffer import ReplayBuffer
from models.qlearning.model_type import ModelType
from models.qlearning.model_load import load
from models.qlearning.model_save import save
from models.qlearning.model_train import train
from models.qlearning.model_predict import predict
from models.qlearning.model_validate import validate, validate_baseline, print_results_table

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def setup_parser():
    """Setup of arguments parser"""
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--read_file", help="Directory to data files")
    parser.add_argument("--qlearn_train", action='store_true', help="Train the model using the app/data/ files")
    parser.add_argument("--qlearn_predict", action='store_true', help="Predict a 24-hour schedule for one day using a saved model")
    parser.add_argument("--predict_date", type=int, default=None, help="Day index 0-364 (default: random)")
    parser.add_argument("--model_path", help="Path to model")
    
    args = parser.parse_args()

    return args

def main(args, **kwarg):
    if args.qlearn_predict:
        if not args.model_path:
            logger.error("--model_path is required for --qlearn_predict")
            return

        # Load and merge data
        data = []
        if args.read_file:
            data.append(read_csv(args.read_file))
        else:
            for file in os.scandir('app/data/'):
                data.append(read_csv(file.path))

        data_frames = []
        for d in data:
            df = pandas.DataFrame(d)
            df['Date/Time'] = pandas.to_datetime(df['Date/Time'], dayfirst=True)
            df = df.set_index('Date/Time')
            data_frames.append(df)

        data_container = DataContainer(
            0, "Date Environment",
            pandas.concat(data_frames, axis=1, join='inner')
        )

        # Build env and load model
        energy_env = EnergyEnvironment(date_container=data_container)
        dqn = load(args.model_path, ModelType.DQN)

        # Run prediction
        schedule = predict(dqn, energy_env, date=args.predict_date)

        # Pretty-print the schedule
        logger.info(f"\n{'='*90}")
        logger.info(f"24-HOUR SCHEDULE [Day index {energy_env.current_date}]")
        logger.info(f"{'='*90}")
        logger.info(
            f"{'Hour':<6}{'Action':<22}{'Battery':<10}{'Solar':<10}"
            f"{'Demand':<10}{'Grid Imp':<10}{'Queue':<8}{'Reward':<10}"
        )
        logger.info('-' * 90)
        for row in schedule:
            logger.info(
                f"{row['hour']:<6}{row['action_name']:<22}"
                f"{row['battery_soc']:<10.3f}{row['solar_kwh']:<10.3f}"
                f"{row['demand_kwh']:<10.3f}{row['grid_import_kwh']:<10.3f}"
                f"{row['queue_size']:<8}{row['reward']:<10.3f}"
            )
        logger.info('=' * 90)
    if args.qlearn_train:
        data = []

        if args.read_file:
            data.append(read_csv(args.read_file))
        else:
            files = os.scandir('app/data/')
            for file in files:
                data.append(read_csv(file.path))

        data_frames = []
        for d in data:
            data_frame = pandas.DataFrame(d)
            data_frame['Date/Time'] = pandas.to_datetime(data_frame['Date/Time'], dayfirst=True)
            data_frame = data_frame.set_index('Date/Time')
            
            data_frames.append(data_frame)

        data_container = DataContainer(0, "Date Environment", pandas.concat([frame for frame in data_frames], axis=1, join='inner'))

        energy_env = EnergyEnvironment(date_container=data_container)
        state, _ = energy_env.reset()

        for _ in range(24):
            action = energy_env.action_space.sample()  # random actions
            next_state, reward, done, _, _ = energy_env.step(action)
            logger.debug(f"Reward: {reward:.3f}, Battery: {energy_env.current_battery_capacity:.2f}, Done: {done}")
            if done:
                break
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        dqn = DQN(input_size=18, output_size=5).to(device)
        logger.debug(dqn)
        replay_buffer = ReplayBuffer()
        
        for step in range(24):
            raw_row = energy_env.raw_data.iloc[(energy_env.current_date * 24) + step]
            g_i = float(raw_row['Predicted_Gb(i)']) / 1000
            e_panel = g_i * energy_env.solar_config.p_peak * energy_env.solar_config.eta_global * energy_env.solar_config.a_sp
            solar = e_panel * energy_env.solar_config.n_pannels
            logger.debug(f"Hour {step:02d} | Solar: {solar:.4f} | Demand: {float(raw_row['Total_Demand_kWh']):.4f} | Gb(i): {float(raw_row['Predicted_Gb(i)']):.2f}")
        
        TRAINING_EPISODE_AMOUNT = 5000
        train(dqn, energy_env, replay_buffer, TRAINING_EPISODE_AMOUNT)
        save(dqn, f'dqn_{TRAINING_EPISODE_AMOUNT}_episodes')
        
        VALIDATION_EPISODE_AMOUNT = 100
        baseline_results = validate_baseline(energy_env, VALIDATION_EPISODE_AMOUNT)
        trained_results = validate(dqn, energy_env, VALIDATION_EPISODE_AMOUNT)
        print_results_table(baseline_results, trained_results, VALIDATION_EPISODE_AMOUNT)
       
if __name__ == "__main__":
    args = setup_parser()
    main(args)