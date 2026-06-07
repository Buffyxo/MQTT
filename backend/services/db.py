import psycopg2


def get_latest_weather():

    conn = psycopg2.connect(

        dbname="digitaltwin",

        user="zara",

        host="localhost",

        port="5432"

    )

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT timestamp, temperature, humidity, wind_speed, solar_radiation
            FROM weather_data
            ORDER BY timestamp DESC
            LIMIT 1
        """)

        row = cursor.fetchone()

        if not row:
            return None

        timestamp = row[0]

        if hasattr(timestamp, "isoformat"):
            timestamp = timestamp.isoformat()

        return {
            "timestamp": timestamp,
            "temperature": row[1],
            "humidity": row[2],
            "wind_speed": row[3],
            "solar_radiation": row[4]
        }

    finally:
        conn.close()
