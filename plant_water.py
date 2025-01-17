import time
import gpiozero as gpio
import sqlite3
from db_handler import fetch_target_moisture, fetch_current_moisture

# Define the GPIO pin for the water pump
# water_pump = gpio.OutputDevice(27)

def water_plant(db_lock):
    while True:
        with db_lock:
            # Fetch the target moisture level from the database
            with sqlite3.connect('measurements.db') as conn:
                cur = conn.cursor()
                target_moisture = fetch_target_moisture(cur)
                current_moisture = fetch_current_moisture(cur)

        if current_moisture < target_moisture:

            # water_pump.on()
            print("Watering the plant")
            time.sleep(10)

            # water_pump.off()
            print("Plant watered")

        # Wait for 15 minutes before checking the moisture level again
        time.sleep(9000)

