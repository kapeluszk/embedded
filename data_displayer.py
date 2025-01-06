from db_handler import fetch_measurements
import sqlite3
import time

def data_display(db_lock):
    with sqlite3.connect('measurements.db') as conn:
        cur = conn.cursor()
        while True:
            with db_lock:
                measurements = fetch_measurements(cur, 7)
            for measurement in measurements:
                print(measurement)
            time.sleep(300)