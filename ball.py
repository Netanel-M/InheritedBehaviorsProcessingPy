class Path():
    def __init__(self, dna_):
        self.dna = dna_

        self.xpath = [map(x, 0, 1, 0, width) for x in self.dna.genes[10:15]]
        self.ypath = [map(y, 0, 1, 0, height) for y in  self.dna.genes[15:20]]

        self.x_index = -1
        self.y_index = -1
                
    def next_destination(self):
        self.x_index += 1
        self.y_index += 1
        if self.x_index == len(self.xpath):
            self.x_index = 0
        if self.y_index == len(self.ypath):
            self.y_index = 0
        return self.xpath[self.x_index], self.ypath[self.y_index]
    
    def current_destination(self):
        return self.xpath[self.x_index], self.ypath[self.y_index]
    
class Organism():
    def __init__(self, dna_):
        self.dna = dna_
        self.fitness = 1

    def getFitness(self):
        return self.fitness
    
    def getDNA(self):
        return self.dna    

class Ball(Organism):
    def __init__(self, dna_):
        Organism.__init__(self, dna_)
        self.pos = PVector(
                           random(width), 
                           random(height)
                           )
        self.acc = PVector(
                           map(self.dna.genes[5], 0,1, -1,1), 
                           map(self.dna.genes[6], 0, 1, -1, 1)
                           )
        self.vel = PVector(0,0)
        
        self.maxspeed = map(self.dna.genes[4], 0, 1, 1, 1)
        self.maxforce = map(self.dna.genes[5], 0, 1, 0.005, 0.01)
        
        self.r1 = map(self.dna.genes[3], 0, 1, 32, 150)
        self.r2 = map(self.dna.genes[4], 0, 1, 32, 150)
        
        self.desiredseparation = (self.r1 + self.r2) / 2
        
        self.body_color = (
                           map(self.dna.genes[0], 0, 1, 0, 255), 
                           map(self.dna.genes[1], 0, 1, 0, 255),  
                           map(self.dna.genes[2], 0, 1, 0, 255)
                           )
        
        self.path = Path(self.dna)
        
    def update(self):
        d = dist(
                 self.path.current_destination()[0],
                 self.path.current_destination()[1],
                 self.pos.x, 
                 self.pos.y)
        
        if d < (self.r1  + self.r2) / 2 :
            self.path.next_destination()
            
        self.vel += self.acc
        self.vel.limit(self.maxspeed)
        self.pos += self.vel
        self.acc.mult(0)
        
    def display(self):
        theta = self.vel.heading2D()
        with pushMatrix():
            translate(self.pos.x, self.pos.y)
            rotate(theta)
            #body
            fill(
                 self.body_color[0],
                 self.body_color[1],
                 self.body_color[2],
                 50
                )
            #noStroke()
            stroke(0)
            strokeWeight(3)
            ellipse(
                    0,
                    0, 
                    self.r1, 
                    self.r2)
            #eyes
            fill(0)
            strokeWeight(1)
            ellipse(0, self.r1/3, self.r1/4, self.r2/4)
            ellipse(0, -self.r1/3, -self.r1/4, -self.r2/4)
            fill(
                 map(self.dna.genes[22], 0, 1, 0, 255),
                 map(self.dna.genes[23], 0, 1, 0, 255),
                 map(self.dna.genes[24], 0, 1, 0, 255)
                 
            )
            noStroke()
            #pupils
            ellipse(0, self.r1/3, 10, 10)
            ellipse(0, -self.r1/3, 10, 10) 
            
            #mouth
            fill(255,0,0)
            stroke(255,0,255)
            strokeWeight(1)
            ellipse(
                    self.r2/4,
                    0,
                    self.r1/map(self.dna.genes[25], 0, 1, 2, 4),
                    self.r2/map(self.dna.genes[26], 0, 1, 2, 4)
                    )       
        textSize(16)
        fill(0)
        text(floor(self.getFitness()), self.pos.x,self.pos.y+self.r2)
        
    def warp(self):
        if self.pos.x > width + self.r1:
            self.pos.x = 0
        elif self.pos.x < 0 - self.r1:
            self.pos.x = width
        if self.pos.y > height + self.r2:
            self.pos.y = 0
        elif self.pos.y < 0 - self.r2:
            self.pos.y = height
            
    def apply_force(self,f):
        self.acc += f
        
    def apply_behaviors(self, vehicles):
        arrive = self.arrive(PVector(
                            self.path.current_destination()[0],
                            self.path.current_destination()[1]
                    )
        )
        separate = self.separate(vehicles)
        align = self.align(vehicles)
        cohesion = self.cohesion(vehicles)
        arrive *= 0.9
        separate *= 3
        cohesion *= -1.5
        align *= 2
        self.apply_force(align)
        self.apply_force(separate)
        self.apply_force(cohesion)
        self.apply_force(arrive)
    
    def seek(self, target):
        desired = target - self.pos
        desired.setMag(self.maxspeed)
        steer = desired -self.vel 
        steer.limit(self.maxforce)
        return steer
    
    def arrive(self, target):
        desired = target - self.pos
        d = desired.mag()
        if d < 100:
            m = map(d, 0, 100, 0, self.maxspeed)
            desired.setMag(m)
        else:
            desired.setMag(self.maxspeed)
        
        steer = desired - self.vel
        steer.limit(self.maxforce)
        return steer
        
    def separate(self, population):
        sum = PVector()
        count=0
        for other in population:
            d = PVector.dist(self.pos, other.pos)
            if ( (d > 0) and (d < self.desiredseparation)):
                diff = self.pos - other.pos
                diff.normalize()
                sum += diff
                count+=1
        
        if count > 0:
            sum.div(count)
            steer = sum - self.vel
            steer.limit(self.maxforce)
            return steer
        else:
            return PVector(0,0)
    
    def align(self, population):
        neighbordist = 100
        sum = PVector()
        count = 0
        for other in population:
            d = PVector.dist(self.pos, other.pos)
            if (d > 0) and (d < neighbordist):
                sum += other.vel
                count += 1
        if count > 0:
            sum /= count
            sum.normalize()
            sum.mult(self.maxspeed)
            steer = sum - self.vel
            steer.limit(self.maxforce)
            return steer
        else:
            return PVector(0,0)

    def cohesion(self, population):
        neighbordist = 100
        sum = PVector()
        count = 0
        for other in population:
            d = PVector.dist(self.pos, other.pos)
            if (d > 0) and (d < neighbordist):
                sum += other.pos
                count += 1
        if count > 0:
            sum /= count
            return self.seek(sum)
        else:
            return PVector(0,0)

    def ellipse_contains(self,a,b):
        if(
            (a > self.pos.x-self.r1) and 
            (a < self.pos.x+self.r1) and  
            (b < self.pos.y+self.r2) and 
            (b > self.pos.y-self.r2)
         ):
            return True
        else:
            return False  