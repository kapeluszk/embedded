# import RPi.GPIO as GPIO
# import time
# import w1thermsensor
#
# # GPIO setup
# sensor = w1thermsensor.W1ThermSensor()
# # water_level_sensor = 5
# # GPIO.setmode(GPIO.BCM)
# # GPIO.setup(water_level_sensor, GPIO.IN)
#
# # Main loop
# while True:
#     temperature = sensor.get_temperature()
#     print(temperature)
#     # print(GPIO.input(water_level_sensor))
#     time.sleep(1)

import smbus
import time

# Ustawienia I2C
I2C_BUS = 1  # Numer magistrali I2C (zazwyczaj 1 dla Raspberry Pi)
I2C_ADDR = 0x10  # Adres HAT-u na magistrali I2C

# Rejestry ADC
REG_ADC_CTRL = 0x0E
REG_ADC_VAL1 = 0x0F
REG_ADC_VAL2 = 0x11
REG_ADC_CHANNELS = {
    "A0": REG_ADC_VAL1,
    "A1": REG_ADC_VAL2,
    # Można dodać inne kanały tutaj
}


def enable_adc(bus):
    """Włącza funkcję ADC na płytce."""
    bus.write_byte_data(I2C_ADDR, REG_ADC_CTRL, 0x01)


def read_adc(bus, channel):
    """Odczytuje wartość ADC z wybranego kanału."""
    if channel not in REG_ADC_CHANNELS:
        raise ValueError("Nieznany kanał ADC: {}".format(channel))

    reg = REG_ADC_CHANNELS[channel]
    data = bus.read_i2c_block_data(I2C_ADDR, reg, 2)
    return (data[0] << 8) | data[1]


if __name__ == "__main__":
    # Inicjalizacja magistrali I2C
    bus = smbus.SMBus(I2C_BUS)

    try:
        # Włącz ADC
        enable_adc(bus)
        print("ADC włączony.")

        # Odczytuj dane z ADC co 1 sekundę
        while True:
            value = read_adc(bus, "A0")
            print(f"Wartość ADC z kanału A0: {value}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Zatrzymano przez użytkownika.")
    except Exception as e:
        print(f"Błąd: {e}")
    finally:
        bus.close()
