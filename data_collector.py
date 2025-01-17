import sensors
import time
import sqlite3
from db_handler import add_measurement

def data_collection(bus, db_lock):
    while True:
        print("im alive")
        try:
            temperature, illuminance, moisture = sensors.measure(bus)
            with db_lock:
                with sqlite3.connect('measurements.db') as conn:
                    cur = conn.cursor()
                    add_measurement(conn, cur, temperature, illuminance, moisture)
        except Exception as e:
            print(f"Error during data collection or insertion: {e}")
        time.sleep(300)