'''
Filename: controlMain.py

Author: Taylor Witherell

Description:  Main running loop for control/operator side of the robot
'''

import time
import pygame
import math
from getData import Receiver
from pygamePieces import Robot, Barrier, LaneRobot, Cockpit, Compass
from ps3controller import Controller
from PIL import ImageFont

# Toggle simulation elements
server_online = True
receiving_data = True
pygame_running = True
controller_connected = True
trigger_turn = False
keyboard_control = False
cubeDetection = True
data_status = 'GUI'
simulation = 'lanecontrol'

# Color List
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128)
black = (0, 0, 0)
grey = (200, 200, 200)

# GUI Attributes
height = 800
width = 300

sim_height = height/3
sim_width = width
sim_x = 0
sim_y = 0

cockpit_height = height/3
cockpit_width = width
cockpit_x = sim_x
cockpit_y = sim_y + sim_height

compass_height = sim_height
compass_width = sim_width
compass_x = sim_x
compass_y = cockpit_y + sim_height


# ---------------- Initialize Receiver/Server -----------------
if server_online:
    # Make sure IP and PORT match server side IP and PORT
    IP = '192.168.2.2'
    PORT = 20001
    r = Receiver(IP, PORT)
    r.client.connect()



# ---------------- Initialize Pygame -----------------
pygame.init()

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


# ---------------- Initialize Pygame Pieces -----------------
if pygame_running:
    
    screen = pygame.display.set_mode((width, height))
    sim_surface = pygame.Surface((sim_width, sim_height))
    cockpit_surface = pygame.Surface((cockpit_width, cockpit_height))
    compass_surface = pygame.Surface((compass_width, compass_height))

    if simulation == 'minimap':
        robotX = sim_width*6/7
        robotY = sim_height* 8/9

        robot_angle = 0
        scanner_angle = 0

        robot_height = robot_width = sim_height * 4/90
        scanner_height = scanner_width = sim_height * 2/90

        robot = Robot(sim_surface, robotX, robotY, robot_height, robot_width, (255, 255, 255))
        scanner = Robot(sim_surface, robotX, robotY, scanner_height, scanner_width, (0, 0, 255))

        y_change = 0
        x_change = 0

        barrierList = []
        barrier_width = sim_height/100

    elif simulation == 'lanecontrol':
        robotX = sim_width/2
        robotY = sim_height/2

        pixels_per_inch = sim_height/36

        robot_height = 10*pixels_per_inch
        robot_width =  8* pixels_per_inch
    
        robot = LaneRobot(sim_surface, robotX, robotY, robot_height, robot_width, (255, 255, 255), pixels_per_inch)
    

    cockpit = Cockpit(cockpit_surface, cockpit_x, cockpit_y, cockpit_height, cockpit_width)
    compass = Compass(compass_surface, compass_x, compass_y, compass_height, compass_width)
    orientation = 0
        
    font_14 = pygame.font.Font('freesansbold.ttf', 14)
    font_18 = pygame.font.Font('freesansbold.ttf', 18)
    font_24 = pygame.font.Font('freesansbold.ttf', 24)


# ---------------- Initialize Receiver/Server -----------------
if server_online:
    # Make sure IP and PORT match server side IP and PORT
    IP = '192.168.2.2'
    PORT = 20003
    r = Receiver(IP, PORT)
    r.client.connect()


# ---------------- Initialize Variables -----------------
temp_data = 0
accel_data = '0'
gyro_data = '0'
sonar_data = '0'

front_dist = '20'
backleft_dist = '5'
backright_dist = '5'
left_dist = '3'
right_dist = '4'
ir_data = 1
arm_data = 'up'

emf_data = '0,0'

intensity1 = 0
intensity2 = 0

yaw = 0.0

turn_prediction = 'forward'

ax = ''
ay = ''
az = ''
gx = ''
gy = ''
gz = ''
temp = ''

message = ','


# ---------------- Initialize Controller -----------------
if controller_connected:
    c = Controller()

# Set control mode to either "user-controlled" or "automated
control_mode = "user-controlled"
turn_factor = ''
drive_control = 'none'

mag = ''


# ------------------- Configure Robot --------------------

arm_status = 'up'
m1_throttle = 0
m2_throttle = 0

camera_vert_axis = 0
camera_horiz_axis = 0



# -------------------- Begin Mainloop --------------------
print('Beginning Simulation... \n\n')

elapsedList = []
controllerList = []
serverList = []
pygameList = []


launch = time.time()

running = True
while running:

    start = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.JOYHATMOTION:
            camera_vert_axis = event.value[1]
            camera_horiz_axis = event.value[0]

        if keyboard_control:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    drive_control = 'left'
                elif event.key == pygame.K_UP:
                    drive_control = 'forward'
                elif event.key == pygame.K_DOWN:
                    drive_control = 'backward'
                elif event.key == pygame.K_RIGHT:
                    drive_control = 'right'
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    drive_control = 'none'
                elif event.key == pygame.K_UP:
                    drive_control = 'none'
                elif event.key == pygame.K_DOWN:
                    drive_control = 'none'
                elif event.key == pygame.K_RIGHT:
                    drive_control = 'none'

            message += drive_control

    if trigger_turn:
        trigger = ''

    
    controller_start = time.time()
    if controller_connected:
        
        # Use start button to quit simulation
        if c.joystick.get_button(9):
            running = False
        
        # Get joystick values for drive control
        scan_axis, x_axis, y_axis = c.get_axes()
        y_axis = - y_axis

        trigger = ''
        if trigger_turn:
            # Get trigger data to control turning
            if c.joystick.get_button(6):
                robot_angle += 2
                scanner_angle += 2
                trigger =  "triggerleft"
            if c.joystick.get_button(7):
                robot_angle -= 2
                scanner_angle -= 2
                trigger = "triggerright"

        if c.joystick.get_button(4):
            message += ",emf,"
            time.sleep(0.2)
        if c.joystick.get_button(5):
            message += ",ultrasonic,"
            time.sleep(0.2)

        # Control camera movements using D-pad
        if camera_vert_axis:
            if camera_vert_axis > 0:
                #print('Face camera forward')
                message += ",cameraforward,"
                time.sleep(0.2)
            else:
                #print('Face camera backward')
                message += ",camerabackward,"
                time.sleep(0.2)
        if camera_horiz_axis:
            if camera_horiz_axis > 0:
                #print('Face camera right')
                message += ",cameraright,"
                time.sleep(0.2)
            else:
                #print('Face camera left')
                message += ",cameraleft,"
                time.sleep(0.2)
        
        #Control arm using A and B button

        if c.joystick.get_button(2):
            message += ",armdown,"
            armup = False
            time.sleep(0.2)
        elif c.joystick.get_button(1):
            message += ",armup,"
            armup = True
            time.sleep(0.2)
        
        if c.joystick.get_button(0):
            message += ",clawopen,"
        elif c.joystick.get_button(3):
            message += ",clawclosed,"

        if c.joystick.get_button(8):
            
            if control_mode == 'user-controlled':
                control_mode = 'autonomous'
            else:
                control_mode = 'user-controlled'
            time.sleep(0.4)
        

        # Decrease sensitivity
        if abs(x_axis) < 0.004:
            x_axis = 0
        if abs(y_axis) < 0.004:
            y_axis = 0
        if abs(scan_axis) < 0.004:
            scan_axis = 0
        #time.sleep(1)
        turn_factor = 0

        if y_axis < 0 and abs(y_axis) <= 0.1:
            y_axis = 0

        if abs(x_axis) + abs(y_axis) > 1:
            x_hold = x_axis
            x_axis = x_axis / (abs(x_axis) + abs(y_axis))
            y_axis = y_axis / (abs(x_hold) + abs(y_axis))

        
        mag = round(abs(x_axis) + abs(y_axis), 2)
        if y_axis < 0:
            mag = -mag

        if x_axis:
            turn_factor = round(x_axis, 3)
            
        # Add controller input to control message

        if mag > 0:
            if turn_factor < 0:
                m1_throttle = mag
                m2_throttle = mag + turn_factor
            elif turn_factor > 0:
                m1_throttle = mag - turn_factor
                m2_throttle = mag
            else:
                m1_throttle = mag
                m2_throttle = mag
        elif mag < 0:
            if turn_factor < 0:
                m1_throttle = mag
                m2_throttle = mag - turn_factor
            elif turn_factor > 0:
                m1_throttle = mag + turn_factor
                m2_throttle = mag
            else:
                m1_throttle = mag
                m2_throttle = mag
        else:
            m1_throttle = 0
            m2_throttle = 0

            
        if trigger_turn:
            if trigger == 'triggerleft':
                m1_throttle = mag
                m2_throttle = -mag
            if trigger == 'triggerright':
                m1_throttle = -mag
                m2_throttle = mag
        
        
        message += 'm1 = ' + str(m1_throttle) + ", m2 = " + str(m2_throttle) + ","
        message += control_mode

        r.send_msg(message)

        
    controllerList.append(time.time() - controller_start)

    server_start = time.time()

    if server_online and receiving_data:
        r.receive_msg()

        #GET TEMPERATURE DATA
        #temp_data = r.getTemp(temp_data)

        #GET SONAR DATA
        sonar_data = r.getSonar(sonar_data)
        sonar_total = sonar_data.split(',')

        if len(sonar_total) == 5:
            if not sonar_total[0].strip('[').strip(' ') == 'None':
                front_dist = sonar_total[0].strip('[').strip(' ')
            if not sonar_total[1].strip(' ') == 'None':
                right_dist = sonar_total[1].strip(' ')
            if not sonar_total[2].strip(' ') == 'None':
                backleft_dist = sonar_total[2].strip(' ')
            if not sonar_total[3].strip(' ') == 'None':
                backright_dist = sonar_total[3].strip(' ')
            if not sonar_total[4].strip(']').strip(' ') == 'None':
                left_dist = sonar_total[4].strip(']').strip(' ')

        '''
        #GET IR PROXIMITY DATA
        ir_data = r.getIR(ir_data)

        
        #GET ACCELEROMETER DATA
        accel_data = r.getAccel(accel_data)
        a_datalist = accel_data.split(',')
        if len(a_datalist) >= 3:
            ax = a_datalist[0].strip('[')
            ay = a_datalist[1]
            az = a_datalist[2].strip(']')

        
        #GET GYROSCOPE DATA
        gyro_data = r.getGyro(gyro_data)
        g_datalist = gyro_data.split(',')
        if len(g_datalist) >= 3:
            gx = g_datalist[0].strip('[')
            gy = g_datalist[1]
            gz = g_datalist[2].strip(']')
        
            if 'sonar' in g_datalist[2]:
                gz = g_datalist[2].strip(']sonar')
            else: gz = g_datalist[2].strip(']')

        '''
        
        #GET ARM DATA
        arm_data = r.getArm(arm_data)

        if arm_data == 'up':
            arm_status = 'up'

        elif arm_data == 'down':
            arm_status = 'down'

            
        #GET USFS DATA
        yaw = r.getYaw(yaw)

        #GET CUBE SENSOR DATA
        emf_data = r.getEMF(emf_data)

        emf_datalist = emf_data.split(',')
        intensity1 = emf_datalist[0]
        intensity2 = emf_datalist[1]
        
        if data_status == 'printing':
            print('\n')
            print('ax =', ax)
            print('ay =', ay)
            print('az =', az)

            print('\n')
            print('gx =', gx)
            print('gy =', gy)
            print('gz =', gz)
            
            print('\n')
            print('temp = ', temp_data)
            print('front = ', front_dist)
            print('right = ', right_dist)
            print('backleft = ', backleft_dist)
            print('backright = ', backright_dist)
            print('left = ', left_dist)


        if left_dist != 'None' and float(left_dist) >= 15:
            turn_prediction = 'left'
        elif front_dist != 'None' and float(front_dist) >= 15:
            turn_prediction = 'forward'
        elif right_dist != 'None' and float(right_dist) >= 15:
            turn_prediction = 'right'
        #elif float(backright_dist) >= 15 and float(backleft_dist) >= 15:
        else:
            turn_prediction = 'backward'

        #if the robot receives a none, stop and get new reading
            


    pygame_start = time.time()
    if pygame_running:

        screen.fill(white)
        sim_surface.fill(black)
        cockpit_surface.fill(black)
        compass_surface.fill(black)


        if simulation == 'minimap':
            # Convert angle output to radians
            angle = robot_angle / 180 * math.pi
            
            if controller_connected:
                # Adjust translational movements based on direction        
                x_change = - y_axis * math.sin(angle)
                y_change = - y_axis * math.cos(angle)

                # Change direction that robot is looking
                scanner_angle -= x_axis - 2*scan_axis
                robot_angle -= x_axis
                
            
            robot.y += y_change
            robot.x += x_change
            scanner.y += y_change
            scanner.x += x_change

            robot.draw(robot_angle)
            scanner.draw(scanner_angle)

            #robot.displayWarnings()

        
        elif simulation == 'lanecontrol':
            distances = [front_dist, left_dist, right_dist, backright_dist, backleft_dist]
            #print(front_dist)
            robot.draw()
            robot.drawBarriers(front_dist, left_dist, right_dist, backright_dist, backleft_dist)
            robot.drawPredictionArrow(turn_prediction)

        cockpit.drawThrottles(abs(m1_throttle), abs(m2_throttle))

        cockpit.drawIntensity(int(intensity1), int(intensity2))

        displayText(cockpit_surface, "M1", font_14, cockpit.width*13/60, cockpit.height/25, white, black )
        displayText(cockpit_surface, "M2", font_14, cockpit.width*26/60, cockpit.height/25, white, black )
        displayText(cockpit_surface, "EMF INTENSITY", font_14, cockpit.width*57/60, cockpit.height/25, white, black )

        cockpit.drawArrowArm(arm_status)

        cockpit.autoSignal(control_mode == 'autonomous')
        pygame.draw.line(cockpit_surface, (255, 255, 255), (cockpit.width/4, cockpit.height*30/50), (cockpit.width/4, cockpit.height), 2)
        pygame.draw.line(cockpit_surface, (255, 255, 255), (cockpit.width/2, cockpit.height*30/50), (cockpit.width/2, cockpit.height), 2)
        pygame.draw.line(cockpit_surface, (255, 255, 255), (cockpit.width*3/4, cockpit.height*30/50), (cockpit.width*3/4, cockpit.height), 2)

        displayText(cockpit_surface, "Arm", font_14, cockpit.width/6, cockpit.height*28/40, white, black)
        displayText(cockpit_surface, "Auto?", font_14, cockpit.width*22.5/50, cockpit.height*28/40, white, black)

        compass.drawCompass(float(yaw))
        displayText(compass_surface, "N", font_14, compass.width *262/500, compass.height/16, white, black)
        displayText(compass_surface, "W", font_14, compass.width *7/80, compass.height/2, white, black)
        displayText(compass_surface, "E", font_14, compass.width *77/80, compass.height/2, white, black)
        displayText(compass_surface, "S", font_14, compass.width *259/500, compass.height*15/16, white, black)

        screen.blit(compass_surface, (compass_x, compass_y))
        screen.blit(cockpit_surface, (cockpit_x, cockpit_y))
        screen.blit(sim_surface, (sim_x, sim_y))
        pygame.display.update()
         
    pygameList.append(time.time() - pygame_start)
    
    message = ','

    elapsed = time.time() - start
    elapsedList.append(elapsed)
        
    time.sleep(0.001)

total = 0
for time in elapsedList:
    total += time

if controller_connected:
    controller_total = 0
    for time in controllerList:
        controller_total += time

    print('Average Elapsed Time for controller code: ', controller_total/len(controllerList))

if server_online:            
    server_total = 0
    for time in serverList:
        server_total += time

    print('Average Elapsed Time for server code: ', server_total/len(serverList))

if pygame_running:
    pygame_total = 0
    for time in pygameList:
        pygame_total += time
    print('Average Elapsed Time for pygame code: ', pygame_total/len(pygameList))
                          
print('Average Elapsed Time: ', total/len(elapsedList))

pygame.quit()
