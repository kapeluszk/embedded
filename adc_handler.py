import smbus
import time

# I2C settings
I2C_BUS = 1  # I2C bus number
I2C_ADDR = 0x10  # HAT I2C address

# ADC registers according to the HAT datasheet
REG_ADC_CTRL = 0x0E
REG_ADC_VAL1 = 0x0F
REG_ADC_VAL2 = 0x11
REG_ADC_VAL3 = 0x13
REG_ADC_VAL4 = 0x15
REG_ADC_CHANNELS = {
    "A0": REG_ADC_VAL1,
    "A1": REG_ADC_VAL2,
    "A2": REG_ADC_VAL3,
    "A3": REG_ADC_VAL4,
}


def enable_adc(bus):
    bus.write_byte_data(I2C_ADDR, REG_ADC_CTRL, 0x01)


def read_adc(bus, channel):
    if channel not in REG_ADC_CHANNELS:
        raise ValueError("Unknown ADC channel: {}".format(channel))

    reg = REG_ADC_CHANNELS[channel]
    data = bus.read_i2c_block_data(I2C_ADDR, reg, 2)

    """
    since we are reading 2 bytes of data from the i2c bus, we need to combine them into one value.
    we are returning data[0] shifted to the left so it won't be overridden by data[1]
    because we are using the OR operator to combine the two values it will look like this:
    
    data[0] = 0x0000 to 0xFF00 (after moving 8 bits to the left)
    data[1] = 0x0000 to 0x00FF (no change)
    
    so we will return the whole i2c data as one value
    """
    return (data[0] << 8) | data[1]