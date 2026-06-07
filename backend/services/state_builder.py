def build_state(weather, co2, demand, solar):

    return {
        "temperature": weather.get("temperature"),
        "solar_radiation": weather.get("solar_radiation"),

        "co2_intensity": co2.get("co2_g_per_kwh"),

        "demand_forecast": demand.get("total_demand_kwh"),
        "solar_forecast": solar.get("solar_generation_kw"),

        "net_energy": solar.get("solar_generation_kw", 0) - demand.get("total_demand_kwh", 0)
    }


def get_battery_soc():
    return 0.5  # temp value


def convert(solar_radiation):
    return solar_radiation / 1000  # kWh approx


def estimate_demand(latest_weather):
    return 1.0  # temp value
