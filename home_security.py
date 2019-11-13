#! /usr/bin python3
from picamera import PiCamera
import Adafruit_CharLCD as LCD
lcd_rs        = 26  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 11
lcd_columns = 16
lcd_rows    = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)
lcd.clear()
lcd.message('importing')
import time
time.sleep(5)
try:
    lcd.clear()
    lcd.message('loading Im.P')
    import label_image

    import Adafruit_CharLCD as LCD
    import snowboydecoder
    import os
    import os.path
    import sys
    import signal
    import RPi.GPIO as GPIO
    import threading
    from gpiozero import LED
    lcd.clear()
    lcd.message('chrome')
    import VoiceUsingChrome
except:
    lcd.clear()
    lcd.message('error')
    raise
GPIO.setmode(GPIO.BCM)

wait_limit=10
interrupted = False
door_p = LED(10)
door_n = LED(9)
light = LED(21)
fan=LED(20)
light.on() # off
fan.on() # off
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd.clear()
lcd.message('Press')
model = "/home/pi/home_security/resources/models/jarvis.pmdl"
command={('লাইট অন','লাইট টা দাও','লাইট অন করো','লাইট চালু করো'):'light_on',
        ('লাইট অফ','লাইটটা অফ করো','লাইট অফ করো','লাইট অফ কর','লাইট বন্ধ কর','লাইট বন্ধ করো'):'light_off',
        ('ফ্যান অন','ফ্যান টা দাও','ফ্যান চালু করো','ফ্যান টা চালু করো','ফোনটা চালু কর','ফ্যান চালু কর'):'fan_on',
        ('ফ্যান অফ',''):'fan_off'}
def door_open():
    door_p.on()
    door_n.off()
def door_close():
    door_p.off()
    door_n.on()
def door_stop():
    door_p.off()
    door_n.off()
class door_in(threading.Thread):
    def run(self):
        lcd.clear()
        lcd.message('Press')
        with PiCamera() as camera:
            camera.start_preview()
            time.sleep(3)
            camera.capture('/home/pi/home_security/img.jpg')
            camera.stop_preview()
        person=label_image.detect('/home/pi/home_security/img.jpg')

        if person=='unknown':
            lcd.clear()
            lcd.message('Unauthorized')
            print('Unauthorized try')
            time.sleep(2)
            lcd.clear()
            lcd.message('Press')
        else:
            lcd.clear()
            lcd.message('Hi '+str(person))
            print('Name: ',person)

            door_open()
            time.sleep(2)
            door_stop()

            time.sleep(5)

            door_close()
            time.sleep(2)
            door_stop()

            lcd.clear()
            lcd.message('Press')

class door_out(threading.Thread):
    def run(self):
        door_open()
        lcd.clear()
        lcd.message('out')
        time.sleep(2)
        door_stop()

        time.sleep(5)

        door_close()
        lcd.clear()
        time.sleep(2)
        door_stop()
        lcd.message('press')

def call_door_in(x):
    entry=door_in()
    entry.start()
def call_door_out(x):
    entry=door_out()
    entry.start()
def signal_handler(signal, frame):
    global interrupted
    interrupted = True
def interrupt_callback():
    global interrupted
    return interrupted

def conversation():
    detector.terminate()
    VoiceUsingChrome.on_mic()
    snowboydecoder.play_audio_file()
    count=0
    while True:
        try:
            user_said=None
            while (user_said==None):
                print('now say...')
                lcd.clear()
                lcd.message('Speak')
                user_said, talking=VoiceUsingChrome.chrome_detect()
                if talking:
                    count=1
                if(user_said==None and count>0 and not talking):
                    count=count+1
                    print('Terminate listening: ',wait_limit-count)
                    if (count==wait_limit):
                        break
                if(user_said==None and count<=0 and not talking):
                    count=count-1
                    print('Terminate listening: ',wait_limit+count)
                    if (count==-wait_limit*2):
                        break
            lcd.clear()
            lcd.message('press')
            if (count==wait_limit):
                break
            if (count==-wait_limit*2):
                break
            print('user_said')
            if (('লাইট' in user_said) or ('লাইটটা'in user_said) or ('লাইটটি'in user_said)):
                if (('অন' in user_said) or ('চালু' in user_said) or ('জ্বালাও' in user_said) or ('জ্বালিয়ে' in user_said)):
                    light.off()
                if (('বন্ধু' in user_said) or ('বন্ধ' in user_said) or ('অফ' in user_said)):
                    light.on()
            if ('ফ্যান' in user_said):
                if (('অন' in user_said) or ('চালু' in user_said) or ('চালিয়ে' in user_said) or ('চালায়' in user_said)):
                    fan.off()
                if (('বন্ধু' in user_said) or ('বন্ধ' in user_said) or ('অফ' in user_said)):
                    fan.on()
        except KeyboardInterrupt:
            GPIO.cleanup()
            raise


''' End of Conversation'''


# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
if __name__=='__main__' :
    try:
        GPIO.add_event_detect(17, GPIO.RISING, callback=call_door_in, bouncetime=300)
        GPIO.add_event_detect(27, GPIO.RISING, callback=call_door_out, bouncetime=300)
        while True:
            door_stop()
            lcd.clear()
            lcd.message('Press')
            print('Listening... Press Ctrl+C to exit')
            VoiceUsingChrome.off_mic()
            detector.start(detected_callback=conversation,
                        interrupt_check=interrupt_callback)
    except KeyboardInterrupt:
        GPIO.cleanup()
        raise
