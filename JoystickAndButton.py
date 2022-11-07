import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.IN)



def loop(onButton,validate):
    while validate():
        if GPIO.input(3) == 0:
            onButton()
            time.sleep(0.200)
            
        
