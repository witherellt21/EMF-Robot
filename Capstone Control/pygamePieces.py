import math
import pygame

def drawArrow(angle, x, y, height, width, cx, cy):

    tip = (x, y -height/2)
    right_corner = (x+width/2, y -height/5)
    left_corner = (x-width/2, y -height/5)

    top_left = (x-width/5, y -height/2 + 10)
    top_right = (x+width/5, y -height/2 + 10)
    bottom_left = (x-width/4, y +height/2)
    bottom_right = (x+width/4, y +height/2)

    coordinates = (tip, right_corner, left_corner)
    coordinates2 = (top_left, top_right, bottom_right, bottom_left)

    coordinates3 = []
    coordinates3 = []
    for i in range(len(coordinates)):
        coordinates3.append(rotate(cx, cy, angle*math.pi/180, coordinates[i]))

    coordinates4 = []
    for i in range(len(coordinates2)):
        coordinates4.append(rotate(cx, cy, angle*math.pi/180, coordinates2[i]))

    coordinates3 = tuple(coordinates3)
    coordinates4 = tuple(coordinates4)

    return coordinates3, coordinates4

def rotate( x, y, angle, p):

    s = math.sin(angle)
    c = math.cos(angle)
    # translate point back to origin:

    p = list(p)

    p[0] -= x
    p[1] -= y

    # rotate point

    xnew = p[0] * c - p[1] * s
    ynew = p[0] * s + p[1] * c

    # translate point back:
    p[0] = xnew + x
    p[1] = ynew + y
    
    return tuple(p)


class Robot():

    def __init__(self, screen, x, y, height, width, color):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.screen = screen
        self.center = (self.x, self.y)
        self.surface = pygame.Surface((self.width, self.height))
        self.angle = 0
        self._direction = 'up'

        #For automation:
        self.firstMove = 'left'
        self.secondMove = 'up'
        self.thirdMove = 'right'
        self.fourthMove = 'down'

    def draw(self, _angle):

        angle = math.pi*_angle/180

        angle = math.pi*_angle/180
        
        point_of_triangle = (self.x + self.height/2 * math.cos(math.pi*90/180 + angle), (self.y - self.height/2 * math.sin(math.pi*90/180 + angle)))
        bottom_left = (self.x + self.height/2 * math.cos(math.pi*225/180 + angle), self.y - self.height/2 * math.sin(math.pi*225/180 + angle))
        bottom_right = (self.x + self.height/2 * math.cos(math.pi*315/180 + angle), self.y - self.height/2 * math.sin(math.pi*315/180 + angle))
        coordinates = [bottom_left, point_of_triangle, bottom_right]
    
        pygame.draw.polygon(self.screen, self.color, coordinates)

    #Gets distance of adjacent barrier from direction
    def getDistance(self, barrier, direction):
        if direction == 'up':
            distance = self.y - barrier.y - barrier.height
        if direction == 'down':
            distance = barrier.y - self.y
        elif direction == 'left':
            distance = self.x - barrier.x - barrier.width
        elif direction == 'right':
            distance = barrier.x - self.x
        return distance

    # Gets direction of adjacent barrier
    def getDirection(self, barrier):
        if (barrier.x <= self.x + self.width/2 and barrier.x >= self.x - self.width/2) or (barrier.x + barrier.width <= self.x + self.width/2 and barrier.x + barrier.width >= self.x - self.width/2):
            if self.y > barrier.y:
                return 'up'
            else:
                return 'down'
        elif (barrier.y <= self.y + self.height/2 and barrier.y >= self.y - self.height/2) or (barrier.y + barrier.height <= self.y + self.height/2 and barrier.y + barrier.height >= self.y - self.height/2):
            if self.x > barrier.x:
                return 'left'
            else:
                return 'right'
        elif self.x >= barrier.x and self.x <= barrier.x + barrier.width:
            if self.y > barrier.y:
                return 'up'
            else:
                return 'down'
        elif self.y >= barrier.y and self.y <= barrier.y + barrier.height:
            if self.x > barrier.x:
                return 'left'
            else:
                return 'right'

    def turnLeft(self):
        self.angle = 90
        self._direction = 'left'

    def turnUp(self):
        self.angle = 0
        self._direction = 'up'

    def turnDown(self):
        self.angle = 180
        self._direction = 'down'

    def turnRight(self):
        self.angle = 270
        self._direction = 'right'

    def executeMove(self, move):
        if move == 'left':
            self.turnLeft()
        elif move == 'right':
            self.turnRight()
        elif move == 'up':
            self.turnUp()
        elif move == 'down':
            self.turnDown()

    #Used for Left hand on the wall with help method
    def getPreferredMoves(self, method, moves ):

        if method == 'lefthandwithhelp':
            if moves[1] == 'up':
                pass
                
    def displayWarnings(self, barrier):
        direction = self.getDirection(barrier)
        if direction != None:
            distance = self.getDistance(barrier, direction)
            if distance < 100:
                if direction == 'up':
                    self.displayWarningUp(distance)
                if direction == 'down':
                    self.displayWarningDown(distance)
                if direction == 'right':
                    self.displayWarningRight(distance)
                if direction == 'left':
                    self.displayWarningLeft(distance)

    def displayWarningUp(self, distance):
        if distance < 40:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y - 23, 20, 5),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y - 30, 20, 5),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y - 37, 20, 5),0)

        elif distance < 70:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y - 23, 20, 5),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y - 30, 20, 5),0)
        else: pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y - 23, 20, 5),0)

    def displayWarningDown(self, distance):

        if distance < 40:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y + self.height/2 + 10, 20, 5),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y + self.height/2 + 17, 20, 5),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y + self.height/2 + 24, 20, 5),0)

        elif distance < 70:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y + 23, 20, 5),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y + 30, 20, 5),0)
        else: pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2, self.y + 23, 20, 5),0)

    def displayWarningLeft(self, distance):

        if distance < 40:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2 - 10, self.y - self.height/2, 5, 20),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2 - 17, self.y - self.height/2, 5, 20),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2 - 24, self.y - self.height/2, 5, 20),0)

        elif distance < 70:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2 - 10, self.y - self.height/2, 5, 20),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2 - 17, self.y - self.height/2, 5, 20),0)
        else: pygame.draw.rect(self.screen, (255, 0, 0), (self.x - self.width/2 - 10, self.y - self.height/2, 5, 20),0)


    def displayWarningRight(self, distance):
        if distance < 40:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x + self.width/2 + 10, self.y - self.height/2, 5, 20),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x + self.width/2 + 17, self.y - self.height/2, 5, 20),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x + self.width/2 + 24, self.y - self.height/2, 5, 20),0)

        elif distance < 70:
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x + self.width/2 + 10, self.y - self.height/2, 5, 20),0)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.x + self.width/2 + 17, self.y - self.height/2, 5, 20),0)
        else: pygame.draw.rect(self.screen, (255, 0, 0), (self.x + self.width/2 + 10, self.y - self.height/2, 5, 20),0)

class LaneRobot():

    def __init__(self, screen, x, y, height, width, color, pixels_per_inch):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.screen = screen
        self.center = (self.x, self.y)
        self.angle = 0
        self._direction = 'up'

        self.ppi = pixels_per_inch

    def draw(self):
        
        coordinates = (self.x-self.width/2, self.y-self.height/2, self.width, self.height)
        pygame.draw.rect(self.screen, self.color, pygame.Rect(coordinates))

        pygame.draw.line(self.screen, (255, 255, 255), (0, self.height*4.4), (self.width*10, self.height*4.4), 2)
        

    def drawBarriers(self, front, left, right, backright, backleft):

        '''
        for i in range(len(distances)):
            if distances[i] != None:
                distances[i] == round(distances[i],
        '''

        barrier_thickness = 1.5*self.ppi

        if front != 'None' and float(front) <= 15:
            #Draw front barrier
            front_coords = (self.x-self.width/2, self.y-self.height/2 - barrier_thickness - float(front) *self.ppi, self.width, barrier_thickness)
            pygame.draw.rect(self.screen, (150, 150, 255), pygame.Rect(front_coords))

        if left != 'None' and float(left) <= 15:
            #Draw left barrier
            left_coords = (self.x-self.width/2 - barrier_thickness - float(left)*self.ppi, self.y-self.height/2, barrier_thickness, self.height)
            pygame.draw.rect(self.screen, (150, 150, 255), pygame.Rect(left_coords))

        if right != 'None' and float(right) <= 15:
            #Draw right barrier
            right_coords = (self.x+self.width/2 + float(right)*self.ppi, self.y-self.height/2, barrier_thickness, self.height)
            pygame.draw.rect(self.screen, (150, 150, 255), pygame.Rect(right_coords))
        '''
        if backright != 'None' and float(backright) <= 15:
            #Draw backright barrier
            backright_coords = (self.x, self.y+self.height/2 + float(backright)*self.ppi, self.width/2, barrier_thickness)
            pygame.draw.rect(self.screen, (150, 150, 255), pygame.Rect(backright_coords))

        if backleft != 'None' and float(backleft) <= 15:
            #Draw backleft barrier
            backleft_coords = (self.x-self.width/2, self.y+self.height/2 + float(backleft)*self.ppi, self.width/2, barrier_thickness)
            pygame.draw.rect(self.screen, (150, 150, 255), pygame.Rect(backleft_coords))
        '''
    def drawPredictionArrow(self, direction):

        height = 60
        width = 30

        if direction == 'left':
            coordinates1, coordinates2 = drawArrow(-90, self.x, self.y-height/2, 60, 30, self.x, self.y)

        elif direction == 'right':
            coordinates1, coordinates2 = drawArrow(90, self.x, self.y-height/2, 60, 30, self.x, self.y)

        elif direction == 'forward':
            coordinates1, coordinates2 = drawArrow(0, self.x, self.y-height/2, 60, 30, self.x, self.y)

        elif direction == 'backward':
            coordinates1, coordinates2 = drawArrow(180, self.x, self.y-height/2, 60, 30, self.x, self.y)

        elif direction == 'none':
            return

        rect = pygame.draw.polygon(self.screen, (255, 0, 0), coordinates2)
        triangle = pygame.draw.polygon(self.screen, (255, 0, 0), coordinates1)


class Cockpit():

    def __init__(self, screen, x, y, height, width):

        self.screen = screen
        self.height = height
        self.width = width

        #self.center = self.x + self. heig

    def drawThrottles(self, m1, m2):

        offset = -5
        angle = math.tanh((self.width/15)/(self.height*40/50))

        width_m2 = (self.height*45/50-(self.height* 45/50 - m2 * self.height*40/50)) *math.tan(angle)
        width_m1 = (self.height*45/50-(self.height* 45/50 - m1 * self.height*40/50)) *math.tan(angle)

        #outline_angle = math.tanh((self.width/14)/(self.height*45/50))
        #width_outline = self.height*40/50 *math.tan(outline_angle)

        point_of_triangle = (self.width /6, self.height * 25/50 - offset)
        top_left = (self.width/6 - width_m2, self.height* 25/50 - m2* self.height*20/50 -offset )
        top_right = (self.width/6 + width_m2, self.height* 25/50 -  m2* self.height*20/50 -offset)

        m2_coordinates = [top_left, point_of_triangle, top_right]

        m1_point_of_triangle = (self.width *4/10, self.height * 25/50 - offset)        
        m1_top_left = (self.width*4/10-width_m1, self.height* 25/50 - m1 * self.height*20/50 - offset)
        m1_top_right = (self.width*4/10+width_m1, self.height* 25/50 - m1 * self.height*20/50 - offset)
        
        m1_coordinates = [m1_top_left, m1_point_of_triangle, m1_top_right]


        #outline_point = (self.width /6, self.height * 25/50 - offset + 10)
        #outline_left = (self.width/6 - width_outline, self.height* 4/50 -offset )
        #outline_right = (self.width/6 + width_outline, self.height* 5/50 -offset )

        #m1_outline = []

        #m2_outline = [outline_point, outline_left, outline_right]


        green_m1 = (1-m1)*255
        green_m2 = (1-m2)*255

        #pygame.draw.polygon(self.screen, (255, 255, 255), m2_outline)
        #pygame.draw.polygon(self.screen, (255, green_m1, 0), m1_coordinates)
        pygame.draw.polygon(self.screen, (255, green_m2, 0), m2_coordinates)
        pygame.draw.polygon(self.screen, (255, green_m1, 0), m1_coordinates)

        pygame.draw.line(self.screen, (255, 255, 255), (0, self.height * 30/50), (self.width, self.height*30/50), 2)


        

    def drawIntensity(self, intensity1, intensity2):

        def getCoordinates(height, width, x, y, purpose, intensity=1):

            if purpose == 'outline':
                top_left = (x - width/2, y - height/2)
                top_right = (x + width/2, y - height/2)
                bottom_left = (x - width/2, y + height/2)
                bottom_right = (x + width/2, y + height/2)

                coordinates = (top_left, top_right, bottom_right, bottom_left)

            elif purpose == 'meter':
                top_left = (x - width/2, y - intensity * height)
                top_right = (x + width/2, y - intensity * height)
                bottom_left = (x - width/2, y)
                bottom_right = (x + width/2, y)

                coordinates = (top_left, top_right, bottom_right, bottom_left)
        
            return coordinates


        x1 = self.width*20/30
        y1 = self.height/3

        x2 = self.width*25/30
        y2 = self.height/3
        
        height = 90
        width = 30

        intensity1 = float(intensity1)/255
        intensity2 = float(intensity2)/255
        
        pygame.draw.polygon(self.screen, (255, 255, 255), getCoordinates(height, width, x1, y1, 'outline'))
        pygame.draw.polygon(self.screen, (255, 255, 255), getCoordinates(height, width, x2, y2, 'outline'))

        height = 85
        width = 25
        
        pygame.draw.polygon(self.screen, (0, 0, 0), getCoordinates(height, width, x1, y1, 'outline'))
        pygame.draw.polygon(self.screen, (0, 0, 0), getCoordinates(height, width, x2, y2, 'outline'))

        intensity1 = intensity1/260
        intensity2 = intensity2/260
        
        #pygame.draw.polygon(self.screen, (255, (1-intensity1)*255, 0), getCoordinates(height, width, x1, y1+height/2, 'meter', intensity1))
        #pygame.draw.polygon(self.screen, (255, (1-intensity2)*255, 0), getCoordinates(height, width, x2, y2+height/2, 'meter', intensity2))
        pygame.draw.polygon(self.screen, ((1-intensity1)*255, 255, 0), getCoordinates(height, width, x1, y1+height/2, 'meter', intensity1))
        pygame.draw.polygon(self.screen, ((1-intensity2) *255, 255, 0), getCoordinates(height, width, x2, y2+height/2, 'meter', intensity2))
        
    def drawArrowArm(self, arm_status):

        if arm_status == 'up':
            coordinates1, coordinates2 = drawArrow(0, self.width/8, self.height*17/20, 40, 20, self.width/8, self.height*17/20)

        elif arm_status == 'down':
            coordinates1, coordinates2 = drawArrow(180, self.width/8, self.height*17/20, 40, 20, self.width/8, self.height*17/20)
            
        rect = pygame.draw.polygon(self.screen, (255, 255, 255), coordinates2)
        triangle = pygame.draw.polygon(self.screen, (255, 255, 255), coordinates1)

    def autoSignal(self, auto):

        if auto:
            pygame.draw.circle(self.screen, (0, 255, 0), (int(self.width*18.7/50), int(self.height*34/40)), int(self.width/18))
        else:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(self.width*18.7/50), int(self.height*34/40)), int(self.width/18))

        
class Compass():
    
    def __init__(self, screen, x, y, height, width):
        self.screen = screen
        self.height = height
        self.width = width

    def drawCompass(self, orientation):

        steps = 20
        tick_spacing = 2*math.pi/steps

        orientation = (2*math.pi - orientation*math.pi/180)

        angle = 0
        while angle <= 2*math.pi:

            x = math.cos(angle)
            y = math.sin(angle)

            radius = self.width/3
            radius2 = self.width/3 + 8
            
            bottom_right = (self.width/2 + math.cos(angle-.01)*radius, self.height/2 - math.sin(angle-0.01)*radius)
            bottom_left = (self.width/2 + math.cos(angle+.01)*radius, self.height/2 - math.sin(angle+0.01)*radius)
            top_right = (self.width/2 + math.cos(angle-.01)*radius2, self.height/2 - math.sin(angle-0.01)*radius2)
            top_left = (self.width/2 + math.cos(angle+.01)*radius2, self.height/2 - math.sin(angle+0.01)*radius2)

            coordinates = (top_left, bottom_left, bottom_right, top_right)
            pygame.draw.polygon(self.screen, (255, 255, 255), coordinates)

            angle += tick_spacing


        bottom_right = (self.width/2 + math.cos(orientation-math.pi/2)*8, self.height/2 - math.sin(orientation-math.pi/2)*8)
        bottom_left = (self.width/2 + math.cos(orientation+math.pi/2)*8, self.height/2 - math.sin(orientation+math.pi/2)*8)
        top = (self.width/2 + math.cos(orientation)*100, self.height/2 - math.sin(orientation)*100)

        coordinates = (bottom_right, top, bottom_left)

        pygame.draw.polygon(self.screen, (255, 0 , 0), coordinates)
            

        
        

class Barrier():

    def __init__(self, screen, x, y, width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.screen = screen
        #self.counter = counter

    def draw(self):
        pygame.draw.rect(self.screen, (255, 255, 255), (self.x, self.y, self.width, self.height),0)
