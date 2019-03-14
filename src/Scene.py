### Author: Navin Ipe
### Created: March 2019
### License: Proprietary. No form of this shall be shared or copied in any form without the explicit permission of the author

import sys

import pygame
from pygame.locals import *

import pymunk
import pymunk.pygame_util
import pymunk.autogeometry

from Ground import Ground
from Car import Car

class Scene:
    fps = 60.0
    worldWidth = 1224
    worldHeight = 710
    gravity = 900
    sleepTimeThreshold = 0.3
    space = []
    screen = []
    game = []#pygame reference
    physics = []#pymunk reference
    draw_options = []
    clock = []
    tracks = []
    
    def __init__(self):
        self.game = pygame
        self.physics = pymunk;
        self.game.init()
        self.screen = self.game.display.set_mode((self.worldWidth, self.worldHeight))
        self.clock = self.game.time.Clock() 
        #--- Physics
        self.space = self.physics.Space() 
        self.space.gravity = 0, self.gravity
        self.space.sleep_time_threshold = self.sleepTimeThreshold
        
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.physics.pygame_util.positive_y_is_up = False
        
        #---add tracks
        numCars = 4
        x = 20; yPos = 100; trackGap = 190; 
        trackPositions = []  
        for y in range(numCars):
            trackPositions.append(yPos)
            yPos += trackGap
        for y in trackPositions:           
            track = Ground(x, y)
            self.space = track.addGround(self.physics, self.space)
        #---add cars
        popu = []
        for y in trackPositions:
            car = Car(self.space, self.physics, 100, y-10)
            car.createCar()
            popu.append(car)
        
    def runLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or \
                    event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):  
                    sys.exit(0)
                    
            #---updatations
            self.space.step(1./self.fps)#Update the space for the given time step.
            self.screen.fill(pygame.color.THECOLORS["black"])#cls
            self.space.debug_draw(self.draw_options)
            for b in self.space.bodies:
                self.physics.pygame_util.to_pygame(b.position, self.screen)
    
            self.game.display.flip()
#dt = self.clock.tick(fps)#creates a delay
#total_time += dt/1000.        