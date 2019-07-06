from picamera import PiCamera
import label_image

while True:
    with PiCamera() as camera:
        camera.start_preview()
        time.sleep(3)
        camera.capture('/home/pi/examples/foo.jpg')
        camera.stop_preview()
    person=label_image.detect('/home/pi/examples/foo.jpg')

    if person=='unknown':
        print('Unauthorized try')
    else:
        top_design()
        print('Name: ',person)
