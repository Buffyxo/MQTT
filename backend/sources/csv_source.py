import pandas as pd


def get_data():

    df = pd.read_csv("./data/cdeii_vic_hourly_2024.csv")

    for _, row in df.iterrows():

        yield {

            "timestamp": str(row["Date/Time"]),

            "co2_g_per_kwh": row["CDEII_gCO2_per_kWh"],

            "co2_kg_per_kwh": row["CDEII_kgCO2_per_kWh"]

        }
