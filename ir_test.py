import lgpio as GPIO
import time

# Set the GPIO to use
ir_gpio = 15
h = GPIO.gpiochip_open(0)
GPIO.gpio_claim_input(h, ir_gpio)

while True:
    print(GPIO.gpio_read(h, ir_gpio))
    time.sleep(1)
