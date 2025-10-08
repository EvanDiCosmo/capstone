import gpiozero as gp
import time as t

led = gp.PWMLED(18)

while True:
    led.value = 0  # off
    t.sleep(10)
    led.value = 0.5  # half brightness
    t.sleep(10)
    led.value = 1  # full brightness
    t.sleep(10)
