def build_state(latest_weather):

    return {

        "date": latest_weather.get("date", 364),

        "battery_soc": get_battery_soc(),

        "solar_kwh": convert(latest_weather["solar_radiation"]),

        "demand_kwh": estimate_demand(latest_weather),

        "grid_import_kwh": 0

    }


def get_battery_soc():
    return 0.5  # temp value


def convert(solar_radiation):
    return solar_radiation / 1000  # kWh approx


def estimate_demand(latest_weather):
    return 1.0  # temp value
