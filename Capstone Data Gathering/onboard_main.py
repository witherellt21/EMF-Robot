'''
Author: Taylor Witherell
Filename: onboard_main.py
Description: Main loop for robot to send and receive data.
'''
import board
#print(board.__version__)
from server import Server
from sonar import Sonar
#import pygame
import time
from CameraServo import Camera
from armcontrol import Arm, Claw  # NEEED TO DOWNLOAD BOARD DEPOENDENCY
#from imu import IMU
from IRsensor import IR
from adafruit_motorkit import MotorKit
import serial
from usfs import USFS_Master
import math
from turnFunctions import robotManuevers as rm


# ---------------- Toggle Features -----------------
sonars_activated = False 
imu_activated = False
ir_sensor_activated = False
server_online = True
motors_running = True
trigger_turn = False
keyboard_control = False
camera_active = True
cubesensor_active = False
usfs_active = True

arm_active = True
claw_active = True

autonomous = False

# ---------------- Initialize Server -----------------
if server_online:
    # Set the client to the server's IP and PORT address
    #IP = '192.168.2.2'
    IP = '192.168.2.2'
    PORT = 20002
    server = Server(IP, PORT)

    server.start()
    server.receiveConnection()

    print('Connection Received')




# ----------------- Initialize Sonar -----------------
if sonars_activated:
    
    s_front = Sonar(6, 18)
    s_left = Sonar(5, 17)
    s_right = Sonar(12, 27)
    #s_backright = Sonar(13, 22)
    #s_backleft = Sonar(16, 23)
    
    
def drive(turn):
    #print(turn)
    
    if turn == 'left':
        pass
        


# ------------------ Initialize IMU ------------------
if imu_activated:
    imu = IMU()



# ------------------ Initialize IR -------------------
if ir_sensor_activated:
    #ir = IR(17)
    pass



# ---------------- Initialize Motors -----------------
#print("motor1")
if motors_running:
    robot = MotorKit()
if arm_active: 
    arm = Arm(0x61)
if claw_active:
    claw = Claw(0x62)





# ---------------- Initialize Cube Sensor -----------------
if cubesensor_active:
    ser = serial.Serial(port='/dev/ttyS0', baudrate = 9600, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS, timeout =1)



# ---------------- Initialize USFS -----------------
yaw = '0'

if usfs_active:
    MAG_RATE = 100
    ACCEL_RATE = 200
    GYRO_RATE = 200
    BARO_RATE = 50
    Q_RATE_DIVISOR = 3

    usfs = USFS_Master(MAG_RATE, ACCEL_RATE, GYRO_RATE, BARO_RATE, Q_RATE_DIVISOR)

    if not usfs.begin():
        print(usfs.getErrorString())
        exit(1)

    usfs.checkEventStatus()

    if usfs.gotError():
        print('ERROR: ' + usfs.getErrorString())
        exit(1)
    
    def getYaw(last_value):
        if (usfs.gotQuaternion()):
            
            qw, qx, qy, qz = usfs.readQuaternion()
            
            yaw = math.atan2(2.0 * (qx * qy + qw * qz), qw * qw + qx * qx - qy * qy - qz * qz)
            
            yaw *= 180.0 / math.pi
            yaw += 9.1
            if yaw < 0: yaw += 360.0
            
            yaw += 200
            
            return yaw
        
        return last_value
    
    print("\nAligning USFS...\n")
    for i in range(200):
        yaw = getYaw(yaw)

def turn(direction, angle, start_pos):
    robot.motor3.throttle = 0
    robot.motor4.throttle = 0
    time.sleep(1)
    curr_orientation = start_pos
    last_value = start_pos
        
    while abs(curr_orientation - start_pos) <=angle:
        if direction == 'right':
            robot.motor3.throttle = -0.65
            robot.motor4.throttle = 0.65
        elif direction == 'left':
            robot.motor3.throttle = 0.65
            robot.motor4.throttle = -0.65
            
        curr_orientation = getYaw(curr_orientation)
        if abs(curr_orientation - last_value) >= 10 or curr_orientation < 0:
            curr_orientation = last_value
        else:
            last_value = curr_orientation

    robot.motor3.throttle = 0
    robot.motor4.throttle = 0
    time.sleep(1)
    
'''
def alignRight(curr_orientation):
    last_value = curr_orientation
    while curr_orientation <= 263:
        robot.motor3.throttle = -0.6
        robot.motor4.throttle = 0.6
        
        curr_orientation = getYaw(curr_orientation)
        if abs(curr_orientation - last_value) >= 10 or curr_orientation < 0:
            curr_orientation = last_value
        else:
            last_value = curr_orientation
    robot.motor3.throttle = 0
    robot.motor4.throttle = 0
        
def alignLeft(curr_orientation):
    last_value = curr_orientation
    while abs(curr_orientation) >=263:
        robot.motor3.throttle = 0.6
        robot.motor4.throttle = -0.6
        
        curr_orientation = getYaw(curr_orientation)
        if abs(curr_orientation - last_value) >= 10 or curr_orientation < 0:
            curr_orientation = last_value
        else:
            last_value = curr_orientation
    robot.motor3.throttle = 0
    robot.motor4.throttle = 0
'''

def goStraight():
    robot.motor3.throttle = 0.64
    robot.motor4.throttle = 0.57
    
def stopMoving():
    robot.motor3.throttle = 0
    robot.motor4.throttle = 0

# ---------------- Initialize Camera -----------------
if camera_active:
    c = Camera(4)

dist = '0'
temp = '0'
gyro = '0'
acc = '0'
ir_status = 1
msg = '0'

arm_status = 'up'

control = 'stop'
turn_status = "None"

m1_throttle = 0
m2_throttle = 0


distances = [1000.0, 1000.0, 1000.0, 1000.0, 1000.0]

front_dist = 0
backleft_dist = 0
backright_dist = 0
left_dist = 0
right_dist = 0


#sensor1 = '0'
#sensor2 = '0'


turn_prediction = ''

sensor1 = '0'
sensor2 = '0'

turnCount = 0


print("\nBegin Robot Simulation.\n")
if motors_running:
    robot.motor3.throttle = 0
    robot.motor4.throttle = 0
    
inp = input("Press Enter")
running = True
while running:
    if not autonomous:
        if server_online:

            if server.disconnect_counter > 10:
                arm.kit.stepper2.release()
                server.receiveConnection()

                print('Connection Received')

    if sonars_activated:
        front_dist = round(s_front.distance(distances[0]), 2)   # Get sonars distance data
        left_dist = round(s_left.distance(distances[4]), 2)
        right_dist = round(s_right.distance(distances[1]), 2)
        #backleft_dist = round(s_backleft.distance(distances[2]), 2)
        #backright_dist = round(s_backright.distance(distances[3]), 2)
        #if front_dist <= 6:
            #if motors_running:
                #control = 'stop'

        distances = [front_dist, right_dist, backleft_dist, backright_dist , left_dist]
        
        
    if imu_activated:
        ag_data_ready = imu.driver.read_ag_status().accelerometer_data_available
        if ag_data_ready:
            temp, acc, gyro = imu.read_ag()   # Get IMU data
    if ir_sensor_activated:
        ir_status = ir.status()   # Print status of proximity sensor

    if cubesensor_active:
        sensor1 = ser.read()
        sensor2 = ser.read()
        
        sensor1 = int.from_bytes(sensor1, "little", signed =False)
        sensor2 = int.from_bytes(sensor2, "little", signed =False)
        #print("sensor1 =", sensor1)
        #print("sensor2 =", sensor2)
        
        
    if usfs_active:
        yaw = getYaw(yaw)

    if motors_running and arm_active:
        arm_status = arm.status

    # Compile a data string to send to the client
    msg = "sonar = " + str(distances) + ",, temp = " + str(temp) + ",, accel = " + str(acc) + \
            ",, gyro = " + str(gyro) + ",, ir = " + str(ir_status) + ',,arm =' + str(arm_status) + ',,emf =' + str(sensor1) + ',' + str(sensor2)
    
    if autonomous:
        sonars_activated = True
        usfs_active = True

        '''
        difference = yaw - 263
        
        if turnCount == -1:
            if abs(difference) > 1:
                if difference < 0:
                    alignRight(yaw)
                    turnCount += 1
                else:
                    alignLeft(yaw)
                    turnCount += 1
        '''
        
        if turnCount == 0:
            if front_dist >= 7:
                goStraight()
            if front_dist<7 and left_dist<40 and right_dist>20:
                stopMoving()
                last_yaw = yaw
                for i in range(4):
                    yaw = getYaw(last_yaw)
                    if abs(yaw-last_yaw) <= 5 and yaw!= last_yaw:
                        break
                    last_yaw = yaw
                turn("right", 86, yaw)
                turnCount+=1
        elif turnCount == 1:
            if front_dist > 11:
                goStraight()
            if front_dist <11 and left_dist>20:
                stopMoving()
                last_yaw = yaw
                for i in range(4):
                    yaw = getYaw(last_yaw)
                    if abs(yaw-last_yaw) <= 5 and yaw!= last_yaw:
                        break
                    last_yaw = yaw
                turn("left", 86, yaw)
                turnCount+=1
                
        elif turnCount == 2:
            if front_dist>9:
                goStraight()
            if front_dist<9 and right_dist>10:
                stopMoving()
                last_yaw = yaw
                for i in range(4):
                    yaw = getYaw(last_yaw)
                    if abs(yaw-last_yaw) <= 5 and yaw!= last_yaw:
                        break
                    last_yaw = yaw
                turn("right", 86, yaw)
                turnCount+=1
        elif turnCount ==3:
            if front_dist>15:
                goStraight()
            if front_dist<15 and left_dist>25:
                stopMoving()
                last_yaw = yaw
                for i in range(4):
                    yaw = getYaw(last_yaw)
                    if abs(yaw-last_yaw) <= 5 and yaw!= last_yaw:
                        break
                    last_yaw = yaw
                turn("left", 88, yaw)
                turnCount += 1
        elif turnCount==4:
            if front_dist>5:
                goStraight()
            else:
                stopMoving()
                autonomous = False
                
    if server_online:
        # If client disconnects from server, reconnect
        if server.disconnect_counter > 0:
            server.receiveConnection()
        # Send sensor data to client

        server.send(msg)

        time.sleep(0.03)

        # Receive control data from client
        control = server.receive()

        if control:
            datalist = control.split(',')
        # Wheels are turned at the same ratio as the joystick is held
        # M1 is right side wheel
        # M2 is left side
        '''
        if trigger_turn:
            if datalist:
                for data in datalist:
                    if 'left' in data:
                        m1_throttle = None
                        m2_throttle = -0.8
                    elif 'right' in data:
                        m1_throttle = -0.8
                        m2_throttle = None
                    elif 'drive' in data:
                        drive = float(data.split('=')[1])
                        m1_throttle = -drive
                        m2_throttle = -drive

        
        #print("Controls")
        if keyboard_control:
            for data in datalist:
                if 'forward' in data:
                    m1_throttle = 0.8
                    m2_throttle = 0.8
                elif 'left' in data:
                    m1_throttle = 0.8
                    m2_throttle = None
                if 'right' in data:
                    m1_throttle = None
                    m2_throttle = 0.8
                if 'backward' in data:
                    m1_throttle = -0.8
                    m2_throttle = -0.8
                if 'none' in data:
                    m1_throttle = None
                    m2_throttle = None
        '''
        if datalist:
            for data in datalist:
                if not autonomous:
                    if 'm1' in data:
                        try:
                            m1_throttle = round(float(data.split('=')[1]), 2)
                        except:
                            pass
                    elif 'm2' in data:
                        try:
                            m2_throttle = round(float(data.split('=')[1]), 2)
                        except:
                            pass                        
                if data == 'cameraforward':
                    c.FaceForward()
                elif data == 'camerabackward':
                    c.FaceBackward()
                elif data == 'cameraleft':
                    c.FaceLeft()
                elif data == 'cameraright':
                    c.FaceRight()
                elif data == 'armup':
                    arm.armUp()
                    arm.status = 'up'
                elif data == 'armdown':
                    arm.armDown()
                    arm.status = 'down'
                elif data == 'clawopen':
                    claw.openClaw()
                elif data == 'clawclosed':
                    claw.closeClaw()
                elif 'autonomous' in data:
                    autonomous = True
                elif 'user-controlled' in data:
                    autonomous = False
                elif 'emf' in data:
                    if cubesensor_active:
                        cubesensor_active = False
                    else: cubesensor_active = True
                elif 'ultrasonic' in data:
                    if sonars_activated:
                        sonars_activated = False
                    else: sonars_activated = True
            
        #print('Motor 1 Throttle =', m1_throttle, '\nMotor 2 Throttle =', m2_throttle)
        if not autonomous:
            if motors_running:

                robot.motor3.throttle = m1_throttle
                robot.motor4.throttle = m2_throttle


    msg = ""

print('done')
