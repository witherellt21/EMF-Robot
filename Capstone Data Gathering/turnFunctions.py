import time
import board
from adafruit_motorkit import MotorKit


class robotManuevers:
    
    def __init__(self, robot = MotorKit(address = 0x60)):
        self.wheels = robot
        
    def overturnLeft(self):
        self.wheels.motor3.throttle = 0
        self.wheels.motor4.throttle = 0
        time.sleep(.5)
        self.wheels.motor3.throttle = 0.80
        self.wheels.motor4.throttle = -0.67
        time.sleep(.8)
        self.wheels.motor3.throttle = 0
        self.wheels.motor4.throttle = 0
        time.sleep(.5)
        
    def turnLeft(self):
        self.wheels.motor3.throttle = 0
        self.wheels.motor4.throttle = 0
        time.sleep(.75)
        self.wheels.motor3.throttle = 0.7
        self.wheels.motor4.throttle = -0.65
        time.sleep(.91)
        self.wheels.motor3.throttle = 0
        self.wheels.motor4.throttle = 0
        time.sleep(.5)
        
    def turnRight90(self):
        self.wheels.motor3.throttle = 0
        self.wheels.motor4.throttle = 0
        time.sleep(.5)
        self.wheels.motor3.throttle = -0.68
        self.wheels.motor4.throttle = 0.67
        time.sleep(.89)
        self.wheels.motor3.throttle = 0
        self.wheels.motor4.throttle = 0
        time.sleep(.5)
        
    def goStraight(self):
        self.wheels.motor3.throttle = 0.64
        self.wheels.motor4.throttle = 0.54
#         time.sleep(0.5)
#         self.wheels.motor3.throttle = 0
#         self.wheels.motor4.throttle = 0
#         time.sleep(0.5)
    
    def goStraightVeerLeft(self):
        self.wheels.motor3.throttle = 0.59
        self.wheels.motor4.throttle = 0.48
#         time.sleep(0.5)
#         self.wheels.motor3.throttle = 0
#         self.wheels.motor4.throttle = 0
#         time.sleep(0.5)

    def goBack(self):
        self.wheels.motor3.throttle = -0.75
        self.wheels.motor4.throttle = -0.75
        time.sleep(0.5)
        self.wheels.motor3.throttle = 0
        self.wheels.motor4.throttle = 0
        time.sleep(0.5)

    def turnAround(self):
        self.wheels.motor3.throttle = -0.75
        self.wheels.motor4.throttle = -0.75
        time.sleep(2)
        self.wheels.motor3.throttle = 0
        self.wheels.motor4.throttle = 0
        time.sleep(0.5)
        
    def stopMoving(self):
        self.wheels.motor3.throttle = 0
        self.wheels.motor4.throttle = 0
            
 
    
if __name__ == '__main__':
    wheels = robotManuevers()
    wheels.stopMoving()
# time.sleep(5)
#goStraight()
#goBack()
#turnLeft90()
#turnRight90()
#turnAround()