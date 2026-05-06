import torch
import torch.nn as nn
import datetime
import logging
import os
from models.qlearning.model_type import ModelType
from models.qlearning.dqn import DQN

logger = logging.getLogger(__name__)

def load(file_path:str, model_type:ModelType=None) -> nn.Module:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    if model_type == ModelType.DQN:
        model = DQN(input_size=18, output_size=5).to(device)
        
        model.load_state_dict(torch.load(file_path, map_location=device))
        model.eval()
        logger.info(f"Model {model_type} loaded from {file_path}")
    else:
        logger.warning(f"Incorrect Model Type: {model_type}")
        return None
    return model