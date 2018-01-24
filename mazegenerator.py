import numpy as np
import pygame

from pygame.locals import *

width = 500
height = 500

pygame.init()

screen = pygame.display.set_mode((width, height))
screen.fill(Color(255,255,255,255))

class border:
    def __init__(self, x, y, pos):
        self.x = x
        self.y = y
        self.pos = pos
        self.len = 100

    def display(self):
        if self.pos == 0:
            pygame.draw.line(screen, (0,0,0), (100+self.x*100, self.y*100), (100+self.x*100, 100+self.y*100), 1)
        else:
            pygame.draw.line(screen, (0,0,0), (self.x*100, 100+self.y*100), (100+self.x*100, 100+self.y*100), 1)




t = 0

for i in range(5):
    for j in range(5):
        b = border(i,j,np.random.randint(2))
        b.display()

pygame.display.update()

running = True
while(running):
    if(pygame.time.get_ticks()>=t+400):
        screen.fill(Color(255,255,255,255))
        for i in range(5):
            for j in range(5):
                if np.random.randint(100)%5 != 0:
                    b = border(i,j,np.random.randint(2))
                    b.display()
        pygame.display.update()
        t+=400
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
