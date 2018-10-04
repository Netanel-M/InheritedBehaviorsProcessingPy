class DNA():
    def __init__(self, lngth):
        self.lngth = lngth
        self.genes = [random(0,1) for x in range(lngth)]
        self.fitness = 0.0
        
    def set_genes(self, newgenes):
        self.genes = newgenes
        
    def getPhrase(self):
        return "".join(self.genes)
        
    def crossover(self, partner):
        child = DNA(self.lngth)
        midpoint = int(random(len(self.genes)))
        
        for i in range(len(self.genes)):
            if i > midpoint:
                child.genes[i] = self.genes[i]
            else:
                child.genes[i] = partner.genes[i]
        return child
    
    def mutate(self, mutationRate):
        for i in range(len(self.genes)):
            if random(1) < mutationRate:
                self.genes[i] = random(1)