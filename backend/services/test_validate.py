import requests
import pandas as pd

payload = {
    "episodes": 10,
    "seed": 42
}

response = requests.post(
    "http://localhost:8000/validate",
    json=payload
)

result = response.json()

df = pd.DataFrame(result["comparison"])

print(df.head())
