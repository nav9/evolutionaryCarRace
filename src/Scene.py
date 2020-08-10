### Author: Navin 
### Created: March 2019
### License: MIT

import sys
import random
from random import uniform

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
import pymunk.pygame_util
import pymunk.autogeometry

from Ground import Ground
from Car import Car

class Scene:
    fps = 60.0
    font = []
    worldWidth = 1224
    worldHeight = 710
    gravity = 900
    generations = 500
    allTimeBestFit = 0
    allTimeBestFitGen = 0
    numCars = 4
    trackX = 20 
    trackY = 100
    trackGap = 190
    sleepTimeThreshold = 0.3
    timeToTry = 15 #second
    space = []
    screen = []
    game = []#pygame reference
    physics = []#pymunk reference
    draw_options = []
    clock = []
    tracks = []
    popu = []
    #---Differential Evolution parameters
    masterBeta = 2.0#beta is real number belongs to [0 -> 2]
    vBeta = 0#variable beta
    crProba = 0.3#crossover probability range [0 -> 1]
    
    def __init__(self):
        self.vBeta = self.masterBeta
        self.game = pygame
        self.physics = pymunk;
        self.game.init()
        self.screen = self.game.display.set_mode((self.worldWidth, self.worldHeight))
        self.clock = self.game.time.Clock() 
        self.font = pygame.font.SysFont("Arial", 20)
        #--- Physics
        self.space = self.physics.Space() 
        self.space.gravity = 0, self.gravity
        self.space.sleep_time_threshold = self.sleepTimeThreshold
        
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.physics.pygame_util.positive_y_is_up = False
        
        #---add tracks                
        trackPositions = []; endOfTrack = 0
        if self.numCars < 4:
            print("A minimum population of 4 is required for Differential Evolution")
            return
        for y in range(self.numCars):
            trackPositions.append(self.trackY)
            self.trackY += self.trackGap
        for y in trackPositions:           
            track = Ground(self.trackX, y)
            endOfTrack = track.getEndOfTrack()
            self.space = track.addGround(self.physics, self.space)

        #---add cars        
        for y in trackPositions:
            car = Car(self.space, self.physics, 100, y-10)
            car.setEndOfTrackAsMaxFitness(endOfTrack)            
            self.popu.append(car)
        
    def runLoop(self):
        for g in range(1, self.generations):
            #---car updations
            for b in self.popu:
                b.createCar()
                #b.reinitializeWithRandomValues()
            total_time = 0
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
                #---car updations
                for b in self.popu:
                    b.updateFitness()
                #---scene
                bestFit = 0
                for b in self.popu:
                    if b.getFitness() > bestFit:
                        bestFit = b.getFitness(); 
                    if b.getFitness() > self.allTimeBestFit:    
                        self.allTimeBestFit = b.getFitness(); self.allTimeBestFitGen = g
                self.screen.blit(self.font.render("Generation: "+str(g)+" of "+str(int(self.generations))+".   Time remaining: "+str(int(self.timeToTry-total_time))+".   Best fitness now: "+str(int(bestFit))+".   All time best fitness: "+str(int(self.allTimeBestFit))+" in gen "+str(int(self.allTimeBestFitGen)), 1, THECOLORS["darkgrey"]), (5, 5))
                self.game.display.flip()
                dt = self.clock.tick(self.fps)#creates a delay
                total_time += dt/1000.
                
                #---reset after specified time
                if total_time > self.timeToTry:
                    for b in self.popu:
                        b.removeCar()
                    break
            #---Differential Evolution
            fit = []; oldSel = []; sel = []; i = 0
            for b in self.popu:
                fit.append(b.getFitness())
                sel.append(i); oldSel.append(i)
                i = i + 1
            
            bestFitnessThisGen = max(fit)
            fittestCar = fit.index(bestFitnessThisGen)
            leastFitCar = fit.index(min(fit))
            for b in range(len(self.popu)):
                sel = []
                for s in oldSel:
                    sel.append(s)
                
                if b == fittestCar:#don't mess with the fittest
                    continue
                del sel[b]
                #---randomly choose three others for DE
                x1 = random.choice(sel); sel.remove(x1)
                x2 = random.choice(sel); sel.remove(x2)
                x3 = random.choice(sel); sel.remove(x3)
                mutant = []
                x1 = self.popu[x1].getValues()
                x2 = self.popu[x2].getValues()
                x3 = self.popu[x3].getValues()
                prev = self.popu[b].getValues()
                for i in range(len(x1)):
                    mutant.append(x1[i] + round(self.vBeta * (x2[i] - x3[i])))
                if mutant == prev:
                    self.popu[b].reinitializeWithRandomValues()
                else:
                    #---crossover
                    for i in range(len(prev)):
                        if uniform(0,1) <= self.crProba:
                            mutant[i] = prev[i]
                    self.popu[b].setValues(mutant) 
                self.popu[leastFitCar].reinitializeWithRandomValues()
            
            #---beta is reduced to encourage exploitation and reduce exploration
            if self.vBeta > 1/40: 
                self.vBeta = self.vBeta - 1/40
