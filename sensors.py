import RPi.GPIO as GPIO
import time
import w1thermsensor
import math
from db_handler import add_measurement
from adc_handler import read_adc

# GPIO setup
thermometer = w1thermsensor.W1ThermSensor()

def calculate_avg(tab):
    if len(tab) < 2:
        return sum(tab) / len(tab) if tab else 0
    tab = sorted(tab)[1:-1]
    return sum(tab)/len(tab)

def moisture_normalization(moisture):
    air_dry = 3100 # Read from sensor when is exposed to air
    water = 1350 # Read from sensor when is in water

    return round((moisture - air_dry) / (water - air_dry) * 100,2)

def illuminance_normalization(ilu):
    direct_flashlight = 3100  # Read from sensor when is exposed to direct flashlight

    if ilu <= 0:
        return 0

    # Using logarithm because the sensor is not linear
    normalized_ilu = math.log(ilu)
    max_log_value = math.log(direct_flashlight)

    return round((normalized_ilu / max_log_value) * 100, 2)


def measure(bus):
    total_temp = []
    total_ilu = []
    total_moist = []
    print("Measuring...")
    for _ in range(8):
        total_temp.append(thermometer.get_temperature())
        total_ilu.append(read_adc(bus,"A0"))
        total_moist.append(read_adc(bus,"A1"))
        time.sleep(1)

    sanitized_moist = moisture_normalization(calculate_avg(total_moist))
    normalized_ilu = illuminance_normalization(calculate_avg(total_ilu))

    return round(calculate_avg(total_temp),2),normalized_ilu,sanitized_moist
