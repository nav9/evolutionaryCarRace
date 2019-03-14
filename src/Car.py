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
    wheel1Radius_range = range(5, 25, 5)#15 
    wheel2Radius_range = range(5, 25, 5)#15 
    chassisMass_range = range(10, 500, 50)#100
    wheel1Mass_range = range(10, 500, 50)#100
    wheel2Mass_range = range(10, 500, 50)#100  
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
    
    def __init__(self, space, physics, xOffset, yOffset):
        self.space = space
        self.physics = physics
        self.x = xOffset
        self.y = yOffset
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
        
    def addWheel(self, centerPoint, xOffset, yOffset, mass, radius):
        moment = self.physics.moment_for_circle(mass, 0, radius)
        wheel_b = self.physics.Body(mass, moment)
        wheel_s = self.physics.Circle(wheel_b, radius)
        wheel_s.friction = self.friction
        #wheel_s.color = 52,219,119
        wheel_b.position = centerPoint - (xOffset, yOffset)
        self.space.add(wheel_b, wheel_s)   
        return wheel_b
        
        
    def createCar(self):
        chassisXY = Vec2d(self.x, self.y)
        
        moment = self.physics.moment_for_box(self.chassisMass, (self.chWd, self.chHt))
        self.chassis_b = self.physics.Body(self.chassisMass, moment)
        self.chassis_s = self.physics.Poly.create_box(self.chassis_b, (self.chWd, self.chHt))
        self.chassis_b.position = chassisXY + (0, 0)
        self.space.add(self.chassis_b, self.chassis_s)           
        
        
        #w1 = self.addChassis(chassisXY, -chWd, 0, mass, 5, 30) #special rectangular wheel
        w1 = self.addWheel(chassisXY, self.chWd, 0, self.wheel1Mass, self.wheel1Radius)
        w2 = self.addWheel(chassisXY, -self.chWd, 0, self.wheel2Mass, self.wheel2Radius)

        self.space.add(self.physics.PinJoint(w1, self.chassis_b, (0,0), (-self.chWd/2,0)), 
                       self.physics.PinJoint(w2, self.chassis_b, (0,0), (self.chWd/2,0)),
                       self.physics.PinJoint(w1, self.chassis_b, (0,0), (0,-self.chHt/2)), 
                       self.physics.PinJoint(w2, self.chassis_b, (0,0), (0,-self.chHt/2)))  
        motorJoint1 = self.physics.SimpleMotor(w1, self.chassis_b, self.speed); motorJoint1.max_force = 10000000
        motorJoint2 = self.physics.SimpleMotor(w2, self.chassis_b, self.speed); motorJoint2.max_force = 10000000
        self.space.add(motorJoint1, motorJoint2)
        
    def removeCar(self):
        self.space.remove(motorJoint1)
        self.space.remove(motorJoint2)
        self.space.remove(motorJoint1)
        