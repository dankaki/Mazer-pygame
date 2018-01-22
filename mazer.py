import numpy as np
import pygame

from pygame.locals import *

pygame.init()
width = 640
height = 480

class bullet:
    def __init__(self, x1, y1, angle):
        self.x = x1
        self.y = y1
        self.speed = 0.5
        self.angle = angle
        self.size = 3
        self.lifetime = 5000 + pygame.time.get_ticks()
        self.dead = False

    def display(self):
        pygame.draw.circle(screen, (20,20,20), (int(self.x),int(self.y)), self.size, 0)
        self.dead = pygame.time.get_ticks() >= self.lifetime

    def move(self):
        self.x += np.cos(self.angle)*self.speed
        self.y += np.sin(self.angle)*self.speed
        if  self.y + self.size >= height or self.y - self.size <= 0:
            self.angle *= -1
        if self.x + self.size >= width or self.x - self.size <= 0:
            self.angle = np.pi - self.angle

class tank:
    def __init__(self,x1,y1,enemy):
        self.speed = (0,0)
        self.mass = 5
        self.size = 40
        self.rad = self.size * np.sqrt(2)/2
        self.motor_speed = 0.3
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1+self.size
        self.y2 = self.y1
        self.x3 = self.x2
        self.y3 = x1 + self.size
        self.x4 = x1
        self.y4 = y1+self.size
        self.xf = x1 + (self.size/2)
        self.yf = y1 - (self.size/4)
        self.direction = np.arctan2(self.y1-self.y4, self.x1-self.x4)
        if enemy:
            self.color = (255,0,0)
        else:
            self.color = (0,0,255)

    def display(self):
        pygame.draw.polygon(screen, self.color, [
        [int(self.x1), int(self.y1)],
        [int(self.xf), int(self.yf)],
        [int(self.x2), int(self.y2)],
        [int(self.x3), int(self.y3)],
        [int(self.x4), int(self.y4)]], 0)

    def check_frames(self):
        if self.yf<=0 or self.yf>=height or self.xf<=0 or self.xf>=width: self.move_backward()
        if self.x3<=0 or self.x3>=width or self.y3<=0 or self.y3>=height: self.move_forward()
        if self.x4<=0 or self.x4>=width or self.y4<=0 or self.y4>=height: self.move_forward()
        if self.x1<=0 or self.x1>=width or self.y1<=0 or self.y1>=height: self.rotate_right()
        if self.x2<=0 or self.x2>=width or self.y2<=0 or self.y2>=height: self.rotate_left()


    def rotate_left(self):
        self.rotation_angle = 2*self.motor_speed/self.size
        self.ang01 = np.arctan2(self.y3 - self.y1, self.x1 - self.x3)
        self.ang02 = np.arctan2(self.y4 - self.y2, self.x2 - self.x4)

        self.ang1 = self.ang01 + self.rotation_angle
        if self.ang1 >= np.pi*2: self.ang1 -= (np.pi*2)
        elif self.ang1<0: self.ang1 += (np.pi*2)

        self.ang2 = self.ang02 + self.rotation_angle
        if self.ang2 >= np.pi*2: self.ang2 -= (np.pi*2)
        elif self.ang2<0: self.ang2 += (np.pi*2)

        self.x1 += self.rad * (np.cos(self.ang1)-np.cos(self.ang01))
        self.y1 -= self.rad * (np.sin(self.ang1)-np.sin(self.ang01))

        self.x2 += self.rad * (np.cos(self.ang2)-np.cos(self.ang02))
        self.y2 -= self.rad * (np.sin(self.ang2)-np.sin(self.ang02))

        self.x3 += self.rad * (np.cos(np.pi+self.ang1)-np.cos(np.pi+self.ang01))
        self.y3 -= self.rad * (np.sin(np.pi+self.ang1)-np.sin(np.pi+self.ang01))

        self.x4 += self.rad * (np.cos(np.pi+self.ang2)-np.cos(np.pi+self.ang02))
        self.y4 -= self.rad * (np.sin(np.pi+self.ang2)-np.sin(np.pi+self.ang02))

        self.xf = (self.x1 + self.x2)/2
        self.yf = (self.y1 + self.y2)/2
        self.direction = np.arctan2(self.y1-self.y4, self.x1-self.x4)
        self.xf += (self.size/4)*np.cos(self.direction)
        self.yf += (self.size/4)*np.sin(self.direction)

    def rotate_right(self):
        self.rotation_angle = -2*self.motor_speed/self.size
        self.ang01 = np.arctan2(self.y3 - self.y1, self.x1 - self.x3)
        self.ang02 = np.arctan2(self.y4 - self.y2, self.x2 - self.x4)

        self.ang1 = self.ang01 + self.rotation_angle
        if self.ang1 >= np.pi*2: self.ang1 -= (np.pi*2)
        elif self.ang1<0: self.ang1 += (np.pi*2)

        self.ang2 = self.ang02 + self.rotation_angle
        if self.ang2 >= np.pi*2: self.ang2 -= (np.pi*2)
        elif self.ang2<0: self.ang2 += (np.pi*2)

        self.x1 += self.rad * (np.cos(self.ang1)-np.cos(self.ang01))
        self.y1 -= self.rad * (np.sin(self.ang1)-np.sin(self.ang01))

        self.x2 += self.rad * (np.cos(self.ang2)-np.cos(self.ang02))
        self.y2 -= self.rad * (np.sin(self.ang2)-np.sin(self.ang02))

        self.x3 += self.rad * (np.cos(np.pi+self.ang1)-np.cos(np.pi+self.ang01))
        self.y3 -= self.rad * (np.sin(np.pi+self.ang1)-np.sin(np.pi+self.ang01))

        self.x4 += self.rad * (np.cos(np.pi+self.ang2)-np.cos(np.pi+self.ang02))
        self.y4 -= self.rad * (np.sin(np.pi+self.ang2)-np.sin(np.pi+self.ang02))

        self.xf = (self.x1 + self.x2)/2
        self.yf = (self.y1 + self.y2)/2
        self.direction = np.arctan2(self.y1-self.y4, self.x1-self.x4)
        self.xf += (self.size/4)*np.cos(self.direction)
        self.yf += (self.size/4)*np.sin(self.direction)


    def move_forward(self):
        self.direction = np.arctan2(self.y1-self.y4, self.x1-self.x4)
        self.x1 += np.cos(self.direction) * self.motor_speed
        self.y1 += np.sin(self.direction) * self.motor_speed
        self.x2 += np.cos(self.direction) * self.motor_speed
        self.y2 += np.sin(self.direction) * self.motor_speed
        self.x3 += np.cos(self.direction) * self.motor_speed
        self.y3 += np.sin(self.direction) * self.motor_speed
        self.x4 += np.cos(self.direction) * self.motor_speed
        self.y4 += np.sin(self.direction) * self.motor_speed
        self.xf += np.cos(self.direction) * self.motor_speed
        self.yf += np.sin(self.direction) * self.motor_speed

    def move_backward(self):
        self.direction = np.pi+np.arctan2(self.y1-self.y4, self.x1-self.x4)
        self.x1 += np.cos(self.direction) * self.motor_speed
        self.y1 += np.sin(self.direction) * self.motor_speed
        self.x2 += np.cos(self.direction) * self.motor_speed
        self.y2 += np.sin(self.direction) * self.motor_speed
        self.x3 += np.cos(self.direction) * self.motor_speed
        self.y3 += np.sin(self.direction) * self.motor_speed
        self.x4 += np.cos(self.direction) * self.motor_speed
        self.y4 += np.sin(self.direction) * self.motor_speed
        self.xf += np.cos(self.direction) * self.motor_speed
        self.yf += np.sin(self.direction) * self.motor_speed

screen = pygame.display.set_mode((width, height))
screen.fill(Color(255,255,255,255))
my_tank = tank(30,30,False)
en_tank = tank(140,140,True)
my_tank.display()
en_tank.display()

my_fw = False
my_bw = False
my_rt = False
my_lt = False

en_fw = False
en_bw = False
en_rt = False
en_lt = False

pygame.display.set_caption('Tanks in the maze')
pygame.display.update()

bullets = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                my_fw = True
            if event.key == pygame.K_DOWN:
                my_bw = True
            if event.key == pygame.K_RIGHT:
                my_rt = True
            if event.key == pygame.K_LEFT:
                my_lt = True
            if event.key == pygame.K_w:
                en_fw = True
            if event.key == pygame.K_s:
                en_bw = True
            if event.key == pygame.K_d:
                en_rt = True
            if event.key == pygame.K_a:
                en_lt = True
            if event.key == pygame.K_z:
                bullets.append(bullet(en_tank.xf, en_tank.yf, en_tank.direction))
            if event.key == pygame.K_m:
                bullets.append(bullet(my_tank.xf, my_tank.yf, my_tank.direction))
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                my_fw = False
            if event.key == pygame.K_DOWN:
                my_bw = False
            if event.key == pygame.K_RIGHT:
                my_rt = False
            if event.key == pygame.K_LEFT:
                my_lt = False
            if event.key == pygame.K_w:
                en_fw = False
            if event.key == pygame.K_s:
                en_bw = False
            if event.key == pygame.K_d:
                en_rt = False
            if event.key == pygame.K_a:
                en_lt = False
    if my_fw: my_tank.move_forward()
    if my_bw: my_tank.move_backward()
    if my_rt: my_tank.rotate_right()
    if my_lt: my_tank.rotate_left()
    if en_fw: en_tank.move_forward()
    if en_bw: en_tank.move_backward()
    if en_rt: en_tank.rotate_right()
    if en_lt: en_tank.rotate_left()
    for i in range(len(bullets)):
        if bullets[i].dead:
            del bullets[i]
            break
    for i in range(len(bullets)):
        bullets[i].move()
    my_tank.check_frames()
    en_tank.check_frames()
    screen.fill(Color(255,255,255,255))
    for i in range(len(bullets)):
        bullets[i].display()
    en_tank.display()
    my_tank.display()
    pygame.display.update()
