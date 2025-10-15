import gpiozero as gp
import time as t

led = gp.PWMLED(18)

while(True):
    led.value = 1 if led.value == 0 else 0 
    t.sleep(.05)