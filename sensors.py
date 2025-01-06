import RPi.GPIO as GPIO
import time
import w1thermsensor
from db_handler import add_measurement
from adc_handler import read_adc

# GPIO setup
thermometer = w1thermsensor.W1ThermSensor()

def calculate_avg(tab):
    if len(tab) < 2:
        return sum(tab) / len(tab) if tab else 0
    tab = sorted(tab)[1:-1]
    return sum(tab)/len(tab)

def measure(bus):
    total_temp = []
    total_ilu = []
    total_moist = []
    for _ in range(8):
        total_temp.append(thermometer.get_temperature())
        total_ilu.append(read_adc(bus,"A0"))
        total_moist.append(read_adc(bus,"A1"))
        time.sleep(1)

    return calculate_avg(total_temp),calculate_avg(total_ilu),calculate_avg(total_moist)
