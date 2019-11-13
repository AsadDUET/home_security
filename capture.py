from picamera import PiCamera
import time

with PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    camera.capture('raw/arjun/'+str(int(time.time()))+'.jpg')
    camera.stop_preview()
