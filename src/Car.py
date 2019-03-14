### Author: Navin Ipe
### Created: March 2019
### License: Proprietary. No form of this shall be shared or copied in any form without the explicit permission of the author

from pymunk import Vec2d
#import numpy as np
import random

class Car:
    space = []
    physics = []
    x = 0
    y = 0
    friction = 1.5   
    #---range of values possible for properties of car
    speed_range = range(10, 30, 5)#15
    chWd_range = range(5, 70, 5)#50#chassis width
    chHt_range = range(5, 50, 5)#10#chassis height
    wheel1Radius_range = range(6, 25, 5)#15 
    wheel2Radius_range = range(6, 25, 5)#15 
    chassisMass_range = range(10, 500, 50)#100
    wheel1Mass_range = range(10, 500, 50)#100
    wheel2Mass_range = range(10, 500, 50)#100  
    #---column of end of track
    maxFitness = 0
    fitness = 0
    #---properties of car    
    speed = 0
    chWd = 0#chassis width
    chHt = 0#chassis height
    wheel1Radius = 0 
    wheel2Radius = 0
    chassisMass = 0
    wheel1Mass = 0
    wheel2Mass = 0  
    #---parts to add or remove from space
    chassis_b = []
    chassis_s = []
    wheel1_b = []
    wheel1_s = []
    wheel2_b = []
    wheel2_s = []  
    pin1 = []
    pin2 = []
    pin3 = []
    pin4 = []
    motorJoint1 = []
    motorJoint2 = []
    
    def __init__(self, space, physics, xStartPos, yStartPos):
        self.space = space
        self.physics = physics
        self.x = xStartPos
        self.y = yStartPos
        self.reinitializeWithRandomValues()    
        
    def reinitializeWithRandomValues(self):
        self.speed = random.choice(self.speed_range)
        self.chWd = random.choice(self.chWd_range)
        self.chHt = random.choice(self.chHt_range)
        self.wheel1Radius = random.choice(self.wheel1Radius_range)
        self.wheel2Radius = random.choice(self.wheel2Radius_range)
        self.chassisMass = random.choice(self.chassisMass_range)
        self.wheel1Mass = random.choice(self.wheel1Mass_range)
        self.wheel2Mass = random.choice(self.wheel2Mass_range)     
    
    def getValues(self):
        v = []
        v.append(self.speed); v.append(self.chWd)
        v.append(self.chHt); v.append(self.wheel1Radius)
        v.append(self.wheel2Radius); v.append(self.chassisMass)
        v.append(self.wheel1Mass); v.append(self.wheel2Mass)
        return v
        
    def setValues(self, v):
        i = 0
        self.speed = v[i]; i = i + 1
        if self.speed < self.speed_range[0] or self.speed > self.speed_range[-1]:
            self.speed = random.choice(self.speed_range)
        self.chWd = v[i]; i = i + 1
        if self.chWd < self.chWd_range[0] or self.chWd > self.chWd_range[-1]:
            self.chWd = random.choice(self.chWd_range)        
        self.chHt = v[i]; i = i + 1
        if self.chHt < self.chHt_range[0] or self.chHt > self.chHt_range[-1]:
            self.chHt = random.choice(self.chHt_range)        
        self.wheel1Radius = v[i]; i = i + 1
        if self.wheel1Radius < self.wheel1Radius_range[0] or self.wheel1Radius > self.wheel1Radius_range[-1]:
            self.wheel1Radius = random.choice(self.wheel1Radius_range)        
        self.wheel2Radius = v[i]; i = i + 1
        if self.wheel2Radius < self.wheel2Radius_range[0] or self.wheel2Radius > self.wheel2Radius_range[-1]:
            self.wheel2Radius = random.choice(self.wheel2Radius_range)        
        self.chassisMass = v[i]; i = i + 1
        if self.chassisMass < self.chassisMass_range[0] or self.chassisMass > self.chassisMass_range[-1]:
            self.chassisMass = random.choice(self.chassisMass_range)        
        self.wheel1Mass = v[i]; i = i + 1
        if self.wheel1Mass < self.wheel1Mass_range[0] or self.wheel1Mass > self.wheel1Mass_range[-1]:
            self.wheel1Mass = random.choice(self.wheel1Mass_range)        
        self.wheel2Mass = v[i]; i = i + 1
        if self.wheel2Mass < self.wheel2Mass_range[0] or self.wheel2Mass > self.wheel2Mass_range[-1]:
            self.wheel2Mass = random.choice(self.wheel2Mass_range)        
    
    def setEndOfTrackAsMaxFitness(self, endOfTrack):
        self.maxFitness = endOfTrack
        
    def createCar(self):
        chassisXY = Vec2d(self.x, self.y)
        self.fitness = 0
        moment = self.physics.moment_for_box(self.chassisMass, (self.chWd, self.chHt))
        self.chassis_b = self.physics.Body(self.chassisMass, moment)
        self.chassis_s = self.physics.Poly.create_box(self.chassis_b, (self.chWd, self.chHt))
        self.chassis_s.color = 10,150,40
        self.chassis_b.position = chassisXY + (0, 0)
        self.space.add(self.chassis_b, self.chassis_s)           
        
        #---wheel1 (left side wheel)
        #w1 = self.addChassis(chassisXY, -chWd, 0, mass, 5, 30) #special rectangular wheel        
        moment = self.physics.moment_for_circle(self.wheel1Mass, 0, self.wheel1Radius)
        self.wheel1_b = self.physics.Body(self.wheel1Mass, moment)
        self.wheel1_s = self.physics.Circle(self.wheel1_b, self.wheel1Radius)
        self.wheel1_s.friction = self.friction
        self.wheel1_s.color = 180,180,180
        self.wheel1_b.position = chassisXY - (self.chWd, 0)
        self.space.add(self.wheel1_b, self.wheel1_s)          

        #---wheel2 (right side wheel)
        #w1 = self.addChassis(chassisXY, -chWd, 0, mass, 5, 30) #special rectangular wheel        
        moment = self.physics.moment_for_circle(self.wheel2Mass, 0, self.wheel2Radius)
        self.wheel2_b = self.physics.Body(self.wheel2Mass, moment)
        self.wheel2_s = self.physics.Circle(self.wheel2_b, self.wheel2Radius)
        self.wheel2_s.friction = self.friction
        self.wheel2_s.color = 180,180,180
        self.wheel2_b.position = chassisXY - (-self.chWd, 0)
        self.space.add(self.wheel2_b, self.wheel2_s)         
        
        self.pin1 = self.physics.PinJoint(self.wheel1_b, self.chassis_b, (0,0), (-self.chWd/2,0))
        self.pin2 = self.physics.PinJoint(self.wheel2_b, self.chassis_b, (0,0), (self.chWd/2,0))
        self.pin3 = self.physics.PinJoint(self.wheel1_b, self.chassis_b, (0,0), (0,-self.chHt/2))
        self.pin4 = self.physics.PinJoint(self.wheel2_b, self.chassis_b, (0,0), (0,-self.chHt/2))
        self.space.add(self.pin1, self.pin2, self.pin3, self.pin4)
        self.motorJoint1 = self.physics.SimpleMotor(self.wheel1_b, self.chassis_b, self.speed); self.motorJoint1.max_force = 10000000
        self.motorJoint2 = self.physics.SimpleMotor(self.wheel2_b, self.chassis_b, self.speed); self.motorJoint2.max_force = 10000000
        self.space.add(self.motorJoint1, self.motorJoint2)
        
    def removeCar(self):
        self.space.remove(self.chassis_b)
        self.space.remove(self.chassis_s)
        self.space.remove(self.wheel1_b)
        self.space.remove(self.wheel1_s)
        self.space.remove(self.wheel2_b)
        self.space.remove(self.wheel2_s)
        self.space.remove(self.pin1)
        self.space.remove(self.pin2)
        self.space.remove(self.pin3)
        self.space.remove(self.pin4)
        self.space.remove(self.motorJoint1)
        self.space.remove(self.motorJoint2)

    def updateFitness(self):
        if self.chassis_b.position.x > self.fitness:
            self.fitness = self.chassis_b.position.x
        if self.fitness > self.maxFitness:
            self.fitness = self.maxFitness
    
    def getFitness(self):
        return self.fitness
            
   