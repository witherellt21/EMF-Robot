'''
 Filename: IRsensor.py
 Author: Taylor Witherell
 Description: An open class for an IR sensor to take data from get voltage out data from
 an IR sensor
'''
import RPi.GPIO as IO

class IR():

    def __init__(self, input_pin):

        self.pin = input_pin

        IO.setwarnings(False)

        IO.setmode(IO.BCM)
        IO.setup(self.pin, IO.IN)

    def status(self):
        return IO.input(self.pin)
