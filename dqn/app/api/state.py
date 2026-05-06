import logging
import os
import pandas
from src.data_container import DataContainer
from utilities.data_reader import read_csv
from models.qlearning.energy_environment import EnergyEnvironment
from models.qlearning.model_load import load
from models.qlearning.model_type import ModelType

logger = logging.getLogger(__name__)

MODEL_PATH = "app/models/saves/dqn_5000_episodes_model_20260502234251.pth"
DATA_DIR = "app/data/"

_dqn = None
_env = None


def initialize():
    """Load model and environment. Called once on server startup."""
    global _dqn, _env

    if _dqn is not None:
        logger.info("Already initialized, skipping")
        return

    logger.info("Loading data files...")
    data = []
    for file in os.scandir(DATA_DIR):
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

    logger.info("Building environment...")
    _env = EnergyEnvironment(date_container=data_container)

    logger.info(f"Loading model from {MODEL_PATH}")
    _dqn = load(MODEL_PATH, ModelType.DQN)

    logger.info("Initialization complete")


def get_dqn():
    if _dqn is None:
        raise RuntimeError("Call initialize() first")
    return _dqn


def get_env():
    if _env is None:
        raise RuntimeError("Call initialize() first")
    return _env