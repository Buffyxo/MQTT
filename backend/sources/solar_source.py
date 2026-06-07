import pandas as pd


def get_data():

    df = pd.read_csv(
        "./data/predicted_solar_2024_XGB.csv"
    )

    for _, row in df.iterrows():

        yield {

            "timestamp": str(row["Date/Time"]),

            "solar_generation_kw":
                float(row["Predicted_Gb(i)"])
        }
