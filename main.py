import threading
import smbus
import sqlite3
from data_collector import data_collection
from data_displayer import data_display
from db_handler import init_db
from adc_handler import enable_adc
from plant_water import water_plant

# I2C settings
I2C_BUS = 1  # I2C bus number
I2C_ADDR = 0x10  # HAT I2C address

if __name__ == "__main__":
    # DB initialization
    with sqlite3.connect('measurements.db') as conn:
        cur = conn.cursor()
        init_db(conn,cur)

    # I2C bus initialization
    bus = smbus.SMBus(I2C_BUS)

    try:
        # Enable ADC
        enable_adc(bus)
        print("ADC enabled.")

        # Create mutex
        db_lock = threading.Lock()

        # Create threads
        collector_thread = threading.Thread(target=data_collection, args=(bus,db_lock))
        water_thread = threading.Thread(target=water_plant, args=(db_lock,))

        # Start threads
        collector_thread.start()
        water_thread.start()

        data_display()

        # Wait for threads to finish
        collector_thread.join()
        water_thread.join()
    except KeyboardInterrupt:
        print("Stopped by user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        bus.close()
        print("I2C bus closed.")
        print("Exiting program.")
