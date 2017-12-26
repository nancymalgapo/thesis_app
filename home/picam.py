import time, os
import RPi.GPIO as GPIO
from picamera import PiCamera

def capture_images(path, page_no, process):

    camera = PiCamera()
    number = int(page_no)
    ctr = 1
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT) #FEEDER
    GPIO.setup(23,GPIO.OUT) #GLASS
    GPIO.setup(25,GPIO.OUT) #GLASS REVERSE
    GPIO.setup(12,GPIO.OUT) #CAMERA
    GPIO.setup(21,GPIO.OUT) #CAMERA REVERSE
    
    if process == 'feeder':        
        for i in range(1, number*2+1):
            image_name = 'image{0:02d}.jpg'.format(i)
            os.chdir(path)
            if(i%2==0):
                camera.start_preview()
                camera.capture(image_name)
                GPIO.output(21,GPIO.HIGH)
                GPIO.output(25,GPIO.HIGH)
                time.sleep(2)
                GPIO.output(21,GPIO.LOW)
                GPIO.output(23,GPIO.HIGH)
                time.sleep(1)
                GPIO.output(23,GPIO.HIGH)
                time.sleep(1)
                GPIO.output(21,GPIO.LOW)
                GPIO.output(23,GPIO.LOW)
                time.sleep(1)
                GPIO.cleanup()
                camera.close()            
            else:
                GPIO.output(18,GPIO.HIGH)
                camera.start_preview()
                time.sleep(10)
                GPIO.output(18,GPIO.LOW)
                camera.capture(image_name)
                GPIO.output(12,GPIO.HIGH)
                time.sleep(2) 
                GPIO.output(12,GPIO.LOW)

    elif process == 'flatbed':
        camera.start_preview()
        while number==1:
            image_name = 'image{0:02d}.jpg'.format(ctr)
            os.chdir(path)        
            time.sleep(1)                                
            camera.capture(image_name)
            GPIO.output(12,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(12,GPIO.LOW)
            ctr+=1
            image_name = 'image{0:02d}.jpg'.format(ctr)
            camera.capture(image_name)
            GPIO.output(21,GPIO.HIGH)
            time.sleep(2)
            GPIO.output(21,GPIO.LOW)
            GPIO.cleanup()
            camera.close()
            number=0
        ctr += 1                                                                                      