from dataclasses import dataclass
import pandas as pd
@dataclass
class DataContainer:
    id: int
    name: str
    data: pd.DataFrame 