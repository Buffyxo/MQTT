import pandas as pd


def get_data():

    df = pd.read_csv(
        "./data/predicted_demand_2024_XGB_full.csv"
    )

    for _, row in df.iterrows():

        yield {

            "timestamp": str(row["Date/Time"]),

            "demand_forecast_kwh":
                float(row["Predicted Demand (kWh)"]),

            "demand_actual_kwh":
                float(row["Singlehouse Demand (kWh)"]),

            "aircon_kwh": 0,
            "plugs_kwh": 0,
            "lighting_kwh": 0,
            "other_kwh": 0
        }
