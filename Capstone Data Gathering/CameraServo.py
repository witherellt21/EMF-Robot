from gpiozero import Servo
import time

class Camera():
    
    
    def __init__(self, servoPin):
        
        self.pin = servoPin

    def FaceForward(self):
        s = Servo(self.pin, min_pulse_width = 0.5/1000, max_pulse_width = 10/1000, frame_width = 20/1000)
        s.max()
        time.sleep(0.3)
        s.detach()
        #time.sleep(1)

    def FaceBackward(self):
       s = Servo(self.pin, min_pulse_width = 0.5/1000, max_pulse_width = 10/1000, frame_width = 20/1000)
       s.min()
       time.sleep(0.3)
       s.detach()
       #time.sleep(1)


    def FaceRight(self):
       s = Servo(self.pin, min_pulse_width = 1.1/1000, max_pulse_width = 10/1000, frame_width = 20/1000)
       s.min()
       time.sleep(0.3)
       s.detach()
       #time.sleep(1)

    def FaceLeft(self):
       s = Servo(self.pin, min_pulse_width = 1/1000, max_pulse_width = 10.6/1000, frame_width = 20/1000)
       s.max()
       time.sleep(0.3)
       s.detach()
       #time.sleep(1)
       
def main():
    c = Camera(4)
    time.sleep(2)
    c.FaceRight()
    time.sleep(2)
    c.FaceForward()
    time.sleep(2)
    c.FaceLeft()
    
if __name__ == "__main__":
    main()


