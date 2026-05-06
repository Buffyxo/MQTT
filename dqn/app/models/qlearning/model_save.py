import torch
import torch.nn as nn
import datetime
import logging
import os
logger = logging.getLogger(__name__)

def save(model:nn.Module, model_name:str) -> str:
    file_path = f'{os.getcwd()}/app/models/saves/{model_name}_model_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.pth'
    torch.save(model.state_dict(), file_path)
    logger.info(f'Completed training and saved to {file_path}')
    return file_path