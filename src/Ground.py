### Author: Navin Ipe
### Created: March 2019
### License: Proprietary. No form of this shall be shared or copied in any form without the explicit permission of the author

class Ground:
    x = 0 #col
    y = 0 #row
    thickness = 1
    friction = 1.0
    
    def __init__(self, xOffset, yOffset):
        self.x = self.x + xOffset
        self.y = self.y + yOffset
    
    def addGround(self, physicsEnviron, space):
        points = [(-100,0),(100,0),(112,12),(125,0),(137,12),(150,0),(162,12),(175,0),(200,0),(250,25),(250,0),(325,0),(362,50),(375,50),(375,0),(425,0),(425,12),(448,12),(448,0),(475,0),(475,12),(485,12),(485,0),(512,0),(512,12),(527,12),(527,0),(590,0),(590,10),(610,10),(610,15),(625,15),(625,25),(646,25),(646,35),(660,35),(660,45),(680,48),(710,-10),(755,5),(755,20),(780,25),(850,25),(825,0),(865,0),(895,25),(925,25),(935,0),(980,-75),(1100,-75)];
        
        for i in range(1,len(points)):            
            #floor = physicsEnviron.Segment(space.static_body, (self.x, self.y), (self.x+1100, self.y-10), self.thickness)
            floor = physicsEnviron.Segment(space.static_body, (self.x+points[i-1][0], self.y+points[i-1][1]), (self.x+points[i][0], self.y+points[i][1]), self.thickness)
            floor.friction = self.friction
            space.add(floor)  
        return space

        