'''
Filename: Sonar.py
Author: Taylor Witherell
Description: Contains sonar class for initializing sonar sensor and
receiving data.
'''

#Libraries
import RPi.GPIO as GPIO
import time

class Sonar():

    def __init__(self, trigger_pin, echo_pin):
        #GPIO Mode (BOARD / BCM)
#         GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        #GPIO.setmode(GPIO.BOARD)

        #set GPIO Pins
        self.trigger = trigger_pin
        self.echo = echo_pin
        
        #set GPIO direction (IN / OUT)
        GPIO.setup(self.trigger, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    def distance(self, last_value):
        # set Trigger to HIGH
        GPIO.output(self.trigger, True)
        # set Trigger after 0.01ms to LOW
        time.sleep(0.001)
        GPIO.output(self.trigger, False)

        StartTime = time.time()
        StopTime = time.time()
        
        start = StartTime

        # save StartTime
        while GPIO.input(self.echo) == 0:
            #print('stuck in here')
            if time.time()- start >=0.1:
                return last_value
            StartTime = time.time()
        
        
        StopTime = time.time()
        # save time of arrival
        while GPIO.input(self.echo) == 1:
            #print('stuck in here2')
            #if time.time()- StartTime >=0.5:
                #stopTime = StopTime
                
                #break
            StopTime = time.time()
        
        
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300*0.3937008) / 2
        #distance = (TimeElapsed * 34300) / 2

        return distance


def main():
    
    #s = Sonar(13, 18)
    
    try:
        while True:
            dist = s.distance()
            print ("Measured Distance = %.1f in" % dist)
            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

if __name__ == '__main__':
    main()

