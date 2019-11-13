from gpiozero import LED
import time
lamp=LED(20)

lamp.off()

time.sleep(3)

lamp.on()
