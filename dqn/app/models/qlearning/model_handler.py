import torch
from models.qlearning.dqn import DQN

class ModelHandler:
    def __init__(self, model_type, model_path, device):
        self.model = None
        if model_type == "dqn":
            self.model = DQN(input_size=18, output_size=3).to(device)
            self.model.load_state_dict(torch.load(model_path, map_location=device))
            self.model.eval()