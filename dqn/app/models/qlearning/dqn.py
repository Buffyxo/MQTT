import torch
import torch.nn as nn
import logging

logger = logging.getLogger(__name__)

class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.debug(f"Torch Settings\nUsing Cuda: {torch.cuda.is_available()}\nCuda Verison: {torch.version.cuda}\nDevice: {self.device}")

        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, output_size)
        )
        
    def forward(self, x):
        return self.network(x)
    
    def best_action(self, state):
        state_t = torch.FloatTensor(state).unsqueeze(0).to(self.device)
        with torch.no_grad():
            q_values = self.forward(state_t)
        
        noise = torch.randn_like(q_values) * 0.01
        return (q_values + noise).argmax().item()