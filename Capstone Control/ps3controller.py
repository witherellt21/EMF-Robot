#!/usr/bin/env python3

'''
Filename: ps3controller.py

Author: Taylor Witherell

Description: Class and tested for ps3 controller support to be integrated
                with robot control mechanism
'''

import pygame

class Controller:

    def __init__(self):

        pygame.init()

        # Set up the joystick
        pygame.joystick.init()

        self.joystick = None
        self.joystick_names = []

        # Enumerate joysticks
        for i in range(0, pygame.joystick.get_count()):
            self.joystick_names.append(pygame.joystick.Joystick(i).get_name())

        # By default, load the first available joystick.
        if (len(self.joystick_names) > 0):
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def get_axes(self):
        right_horiz = self.joystick.get_axis(0)
        right_vert = self.joystick.get_axis(1)
        left_horiz = self.joystick.get_axis(2)
        left_vert = self.joystick.get_axis(3)

        return right_horiz, left_horiz, left_vert

    def run(self):

        while (True):

            # Pump events
            pygame.event.get()

            # Display axis values
            for k in range(self.joystick.get_numaxes()):
                print('%d:%+3.3f' % (k, self.joystick.get_axis(k)), end=' ')

            print(' | ', end='')
           
            # Display button values
            for k in range(self.joystick.get_numbuttons()):
                print('%2d:%d' % (k, self.joystick.get_button(k)), end=' ')

            print()

    def quit(self):
        pygame.display.quit()

if __name__ == '__main__':
   '''
   This will prevent main code being run when someone does from ps3controller import *
   '''
   c = Controller()
   c.run()
