import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

class Arm():

    def __init__(self, _address):
        self.kit = MotorKit(address = _address)
        self.kit.stepper2.release()
        
        self.status = 'up'

    def armUp(self):
        for i in range(100):
            self.kit.stepper2.onestep(direction = stepper.FORWARD, style = stepper.SINGLE)
            time.sleep(0.005)
        self.kit.stepper2.release()
        
    def armDown(self):
        for i in range(90):
            self.kit.stepper2.onestep(direction = stepper.BACKWARD, style = stepper.SINGLE)
            time.sleep(0.005)
        self.kit.stepper2.release()
class Claw():
    
    def __init__(self, _address):
        self.kit = MotorKit(address = _address)
    
    def openClaw(self):
        print('here')
        self.kit.motor3.throttle = .5
        time.sleep(0.1)
        self.kit.motor3.throttle = 0
        
    def closeClaw(self):
        self.kit.motor3.throttle = -.5
        time.sleep(0.1)
        self.kit.motor3.throttle = 0


def main():
    
    a = Arm(0x61)
    
    choice = 'Y'
    while choice == 'Y':
        direction = input("Do you want to move the claw up (u) or down (d): ")
        
        if direction == 'u':
            a.armUp()
        elif direction == 'd':
            a.armDown()
        else:
            choice = input("Hit Y to give new instruction or anything else to quit")


if __name__ == "__main__":
    main()
