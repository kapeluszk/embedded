import time
import lgpio as GPIO
import sqlite3
from db_handler import fetch_target_moisture, fetch_current_moisture

# Define the GPIO pin for the water pump
h = GPIO.gpiochip_open(0)

# Release the GPIO pin if it is already claimed
try:
    GPIO.gpio_claim_output(h, 12)
except GPIO.Error as e:
    GPIO.gpio_free(h, 12)
    GPIO.gpio_claim_output(h, 12)


def water_plant(db_lock):
    while True:
        with db_lock:
            # Fetch the target moisture level from the database
            with sqlite3.connect('measurements.db') as conn:
                cur = conn.cursor()
                target_moisture = fetch_target_moisture(cur)
                current_moisture = fetch_current_moisture(cur)

        print("Current moisture level: ", current_moisture)
        print("Target moisture level: ", target_moisture)

        if target_moisture is None:
            target_moisture = 0

        if current_moisture < target_moisture:
            # gpio to 0 because the relay is active low
            GPIO.gpio_write(h, 12, 0)
            print("Watering the plant")
            time.sleep(10)

            GPIO.gpio_write(h, 12, 1)
            print("Plant watered")

        # Wait for 15 minutes before checking the moisture level again
        time.sleep(9000)

