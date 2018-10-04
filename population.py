from random import choice
from DNA import DNA
from ball import Ball

class Population():
    def __init__(self, mutationRate, popmax, dna_length):
        self.mutationRate = mutationRate
        self.matingPool = []
        self.generations = 0
        self.popmax = popmax
        self.population = [ Ball( DNA(dna_length)) for x in range(self.popmax) ]   
             
    def step(self):
        for p in self.population:
            p.display()
            p.apply_behaviors(self.population)
            p.update()

    def selection(self):
        self.matingPool = []
        maxFitness = self.getMaxFitness()
        for i in range(len(self.population)):
            fitnessNormal = map(self.population[i].getFitness(), 0, maxFitness, 0, 1)
            n = int(fitnessNormal * 100)
            for j in range(n):
                self.matingPool.append(self.population[i])
    
    def reproduction(self):
        for i in range(len(self.population)):
            mom = choice(self.matingPool)
            dad = choice(self.matingPool)
            momgenes = mom.getDNA()
            dadgenes = dad.getDNA()
            child = momgenes.crossover(dadgenes)
            child.mutate(self.mutationRate)
            self.population[i] = Ball(child)
        self.generations += 1
        
    def getGenerations(self):
        return self.generations

    def getMaxFitness(self):
        record = 0
        for i in range(len(self.population)):
            if self.population[i].getFitness() > record:
                record = self.population[i].getFitness()
        return record
                        
class BallPopulation(Population):
    def __init__(self, mutationRate, popmax, dna_length):
        Population.__init__(self, mutationRate, popmax, dna_length)
        self.show_paths = False
        
    def step(self, raise_fitness=False):
        Population.step(self)
        for p in self.population:
            p.warp()
            if self.show_paths:
                stroke(255, 50)
                line(p.pos.x, p.pos.y,p.path.current_destination()[0], p.path.current_destination()[1])
            if raise_fitness:
                if p.ellipse_contains(mouseX, mouseY):
                    p.fitness += 0.1