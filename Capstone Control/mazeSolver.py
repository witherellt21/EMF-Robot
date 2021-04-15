'''
Filename: controlMain.py

Author: Taylor Witherell

Description:  Main running loop for control/operator side of the robot
'''

import time
import pygame
import math
from getData import Receiver
from pygamePieces import Robot, Barrier
from ps3controller import Controller
from PIL import ImageFont

# Toggle simulation elements
server_online = False
receiving_data = False
pygame_running = True

# Color List
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128)
black = (0, 0, 0)
grey = (200, 200, 200)

# GUI Attributes
height = 12*66
width = 12*99

foot = 36

#sim_height = height/2
#sim_width = height/2
sim_height = height
sim_width = width
sim_x = 0
sim_y = 0
robot_height = robot_width = 3/4*foot
scanner_height = scanner_width = 1/2*foot


# ---------------- Initialize Pygame -----------------
pygame.init()

def drawDivider():
    pygame.draw.rect(sim_surface, (255,255,255), (sim_width*2/3, sim_y, sim_width/100, sim_height),0)

def barrierExists(barrierList, x, y):
    for barrier in barrierList:
        if barrier.x == x and barrier.y == y:
            return True
    return False

def displayText(surface, text, font, x, y, color, background):
    txt = font.render(text, True, color, background)
    textRect = txt.get_rect()
    center = textRect.width/2
    x -= center
    textRect.center = (x, y)
    surface.blit(txt, textRect)

def getDirectionofExit():

    exit_direction  = []
    
    x_dir = robot.x - exit_location[0]
    y_dir = robot.y - exit_location[1]

    if x_dir > 0:
        exit_direction.append('left')
    elif x_dir < 0:
        exit_direction.append('right')
    else:
        exit_direction.append('center')

    if y_dir > 0:
        exit_direction.append('up')
    elif y_dir < 0:
        exit_direction.append('down')
    else:
        exit_direction.append('center')

    return exit_direction
        



# ---------------- Initialize Pygame Pieces -----------------
if pygame_running:
    
    screen = pygame.display.set_mode((width, height))
    sim_surface = pygame.Surface((sim_width, sim_height))

    robotX = sim_width*29/33
    robotY = sim_height* 20/22

    robot_angle = 0
    scanner_angle = 0
    angle_change = 0

    robot = Robot(sim_surface, robotX, robotY, robot_height, robot_width, (255, 255, 255))
    scanner = Robot(sim_surface, robotX, robotY, scanner_height, scanner_width, (0, 0, 255))

    y_change = 0
    x_change = 0

    y_axis = 0

    barrierList = []
    barrier_width = sim_height * 1/132

    font = pygame.font.Font('freesansbold.ttf', 32)
    font_24 = pygame.font.Font('freesansbold.ttf', 24) 

    #Side right
    barrier = Barrier(sim_surface, sim_width * 30/33, sim_height * 16 / 22, barrier_width, sim_height * 4/22)
    barrierList.append(barrier)

    #Side right
    #barrier = Barrier(sim_surface, sim_width * 33/33, sim_height * 20/22, barrier_width, sim_height * 4/22)
    #barrierList.append(barrier)

    #Side left
    barrier = Barrier(sim_surface, sim_width * 28/33, sim_height * 18 / 22, barrier_width, sim_height * 2/22)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 26/33, sim_height * 16 / 22, sim_width * 4/33, barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 24/33, sim_height * 12 / 22, barrier_width, sim_width * 4/33)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 26/33, sim_height * 14 / 22, barrier_width, sim_width * 2/33)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 16/33, sim_height * 20 / 22, sim_width * 12/33, barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 22/33, sim_height * 18 / 22, sim_width * 4/33, barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 22/33, sim_height * 16 / 22, barrier_width, sim_width * 4/33)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 18/33, sim_height * 18 / 22, sim_width * 2/33, barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 18/33, sim_height * 16 / 22, sim_width * 4/33, barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 16/33, sim_height * 8 / 22, barrier_width, sim_width * 12/33)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 22/33, sim_height * 12 / 22, barrier_width, sim_width * 2/33 + barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 16/33, sim_height * 14 / 22, sim_width * 6/33, barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 24/33, sim_height * 12 / 22, sim_width * 6/33, barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 30/33, sim_height * 8 / 22, barrier_width, sim_width * 8/33)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 26/33, sim_height * 14 / 22, sim_width * 2/33, barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 18/33, sim_height * 10 / 22, sim_width * 10/33, barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 16/33, sim_height * 8 / 22, sim_width * 10/33, barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 28/33, sim_height * 8 / 22, sim_width * 2/33, barrier_width)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 26/33, sim_height * 8 / 22, barrier_width, sim_width * 2/33)
    barrierList.append(barrier)

    #Top center
    barrier = Barrier(sim_surface, sim_width * 18/33, sim_height * 12 / 22, sim_width * 4/33, barrier_width)
    barrierList.append(barrier)

    exit_location = [sim_width * 27/33, sim_height * 8 / 22]




# ========================================= AUTOMATION =============================================
method = 'lefthandwithhelp'

simulation = 'inactive'

drive_counter = 0
drive_threshold = 3
drive_speed = -6

    

# Set control mode to either "user-controlled" or "automated
control_mode = "automated"
turn_factor = ''

# -------------------- Begin Mainloop --------------------
print('Beginning Simulation... \n\n')


running = True
while running:

    if pygame_running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    robot.angle = 0
                if event.key == pygame.K_DOWN:
                    robot.angle = 180
                if event.key == pygame.K_LEFT:
                    robot.angle = 90
                if event.key == pygame.K_RIGHT:
                    robot.angle = 270

                if event.key == 32:
                    if simulation == 'inactive':
                        simulation = 'active'
                    else:
                        simulation = 'inactive'
                        robot.x = robotX
                        robot.y = robotY
                        robot._direction = 'up'
                        robot.angle = 0
                        
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_axis = 0
                if event.key == pygame.K_DOWN:
                    y_axis = 0
                if event.key == pygame.K_LEFT:
                    angle_change = 0
                if event.key == pygame.K_RIGHT:
                    angle_change = 0

        screen.fill(white)    
        sim_surface.fill(black)

        impossible_moves = []

        for b in barrierList:
            b.draw()
            direction = robot.getDirection(b)
            if direction:
                #print(robot.getDistance(b, direction), direction)
                if abs(robot.getDistance(b, direction)) < foot + 1:
                    if direction not in impossible_moves:
                        impossible_moves.append(direction)
        
        #robot_angle += angle_change
        #scanner_angle += angle_change
                    
        # Convert angle output to radians

        if simulation == 'active':
            
            angle = robot.angle / 180 * math.pi
            x_change = drive_speed * math.sin(angle)
            y_change = drive_speed * math.cos(angle)
        
            robot.y += y_change
            robot.x += x_change
            scanner.y += y_change
            scanner.x += x_change

        #drawDivider()
        robot.draw()
        #scanner.draw(scanner_angle)

        #Left hand on the wall method
        if method == 'lefthand':
            if simulation == 'active':
                
                robot_status = 'turned'

                if robot._direction == 'up':
                    if 'left' in impossible_moves:
                        if 'up' in impossible_moves:
                            if 'right' in impossible_moves:
                                robot.turnDown()
                            else:
                                robot.turnRight()
                        else:
                            drive_counter += 1
                    else:
                        if drive_counter > drive_threshold:
                            robot.turnLeft()
                            drive_counter = 0

                elif robot._direction == 'left':
                    if 'down' in impossible_moves:
                        if 'left' in impossible_moves:
                            if 'up' in impossible_moves:
                                robot.turnRight()
                            else:
                                robot.turnUp()
                        else:
                            drive_counter += 1
                    else:
                        if drive_counter > drive_threshold:
                            robot.turnDown()
                            drive_counter = 0
                elif robot._direction == 'down':
                    if 'right' in impossible_moves:
                        if 'down' in impossible_moves:
                            if 'left' in impossible_moves:
                                robot.turnUp()
                            else:
                                robot.turnLeft()
                        else:
                            drive_counter += 1
                    else:
                        if drive_counter > drive_threshold:
                            robot.turnRight()
                            drive_counter = 0
                elif robot._direction == 'right':
                    if 'up' in impossible_moves:
                        if 'right' in impossible_moves:
                            if 'down' in impossible_moves:
                                robot.turnLeft()
                            else:
                                robot.turnDown()
                        else:
                            drive_counter += 1
                    else:
                        if drive_counter > drive_threshold:
                            robot.turnUp()
                            drive_counter = 0

        #Left hand on the wall method with help of where the exit is
        if method == 'lefthandwithhelp':
            if simulation == 'active':
                
                robot_status = 'turned'

                print(getDirectionofExit())
                robot.getPreferredMoves(method, getDirectionofExit())

                if robot.firstMove in impossible_moves():
                    if robot.secondMove in impossible_moves():
                        if robot.thirdMove in impossible_moves():
                            robot.executeMove(robot.fourthMove)
                        else:
                            robot.executeMove(robot.thirdMove)
                    else:
                        drive_counter += 1

                elif drive_counter > drive_threshold:
                    robot.executeMove(robot.firstMove)
                    drive_counter = 0
                
        # Display message when in autonomous mode
        if control_mode == "autonomous":
            mode_string = 'Mode: Autonomous'
            displayText(sim_surface, mode_string, font_24, width * 4/7, height * 3/18, white, black)

        screen.blit(sim_surface, (sim_x, sim_y))
        pygame.display.update()
        
    time.sleep(.01)

pygame.quit()
