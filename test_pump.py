import lgpio as GPIO
import time

h = GPIO.gpiochip_open(0)
GPIO.gpio_claim_output(h,12)

def main():
    GPIO.gpio_write(h,12,0)
    time.sleep(15)
    GPIO.gpio_write(h,12,1)

if __name__ == '__main__':
    main()