### Author: Navin Ipe
### Created: March 2019
### License: Proprietary. No form of this shall be shared or copied in any form without the explicit permission of the author

from pymunk import Vec2d

class Car:
    space = []
    physics = []
    x = 0
    y = 0
    speed = 15
    friction = 1.5
    
    def __init__(self, space, physics, xOffset, yOffset):
        self.space = space
        self.physics = physics
        self.x = xOffset
        self.y = yOffset
        
    def addWheel(self, centerPoint, xOffset, yOffset, mass, radius):
        moment = self.physics.moment_for_circle(mass, 0, radius)
        wheel_b = self.physics.Body(mass, moment)
        wheel_s = self.physics.Circle(wheel_b, radius)
        wheel_s.friction = self.friction
        #wheel_s.color = 52,219,119
        wheel_b.position = centerPoint - (xOffset, yOffset)
        self.space.add(wheel_b, wheel_s)   
        return wheel_b
        
    def addChassis(self, chassisXY, xOffset, yOffset, mass, width, height):
        size = (width, height)
        moment = self.physics.moment_for_box(mass, size)
        chassis_b = self.physics.Body(mass, moment)
        chassis_s = self.physics.Poly.create_box(chassis_b, size)
        chassis_b.position = chassisXY + (xOffset, yOffset)
        self.space.add(chassis_b, chassis_s)   
        return chassis_b
        
    def createCar(self):
        chassisXY = Vec2d(self.x, self.y)
        chWd = 50#chassis width
        chHt = 10#chassis height
        wheelRadius = 15; mass = 100
        ch = self.addChassis(chassisXY, 0, 0, mass, chWd, chHt)
        w1 = self.addChassis(chassisXY, -chWd, 0, mass, 5, 30) #self.addWheel(chassisXY, chWd, 0, mass, wheelRadius)
        w2 = self.addWheel(chassisXY, -chWd, 0, mass, wheelRadius)

        self.space.add(self.physics.PinJoint(w1, ch, (0,0), (-chWd/2,0)), 
                       self.physics.PinJoint(w2, ch, (0,0), (chWd/2,0)),
                       self.physics.PinJoint(w1, ch, (0,0), (0,-chHt/2)), 
                       self.physics.PinJoint(w2, ch, (0,0), (0,-chHt/2)))                     
        self.space.add(self.physics.SimpleMotor(w1, ch, self.speed), self.physics.SimpleMotor(w2, ch, self.speed))
        