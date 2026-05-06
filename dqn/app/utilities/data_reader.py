import csv
import logging
import pandas as pd
from src.data_container import DataContainer
logger = logging.getLogger(__name__)

def read_csv(filepath:str):
    """
    Reads csv file
        Returns: Dict
    """
    if not filepath.endswith('.csv'):
        logging.warning(f"{filepath} isn't a csv.")

    data = {}
    with open(filepath, newline='') as file:
        csv_data = csv.reader(file, delimiter=',')
        for i, row in enumerate(csv_data):
            if i == 0:
                for column in row:
                    data[column] = []
            else:
                for i, column in enumerate(row):
                    data[list(data.keys())[i]].append(column)
    logger.info(f"Successfully loaded {filepath}")
    return data

def create_data_container(id:int, container_name:str, dates_column:list, data_columns:list[list]):
    """
    Create a data container.
    Arguments:
        id: identifier
        container_name: name of the data
        x: prediction data
        y: date/time
    Returns:
        DataContainer
    """
    date_name = dates_column.pop(0)
    data = {date_name: dates_column}
    for column in data_columns:
        data[column.pop(0)] = column

    logger.info(f"Creating new data container {container_name}")
    
    dataFrame = pd.DataFrame(data)
    dataFrame[date_name] = pd.to_datetime(dataFrame[date_name], dayfirst=True)
    dataFrame.set_index(date_name)
    return DataContainer(id=id, name=container_name, data=dataFrame)