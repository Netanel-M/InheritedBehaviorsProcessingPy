from DNA import DNA
from ball import Ball
from population import BallPopulation

def setup():
    global population
    #size(900,900)
    fullScreen()
    popmax = 10
    mutationRate = 0.02
    population = BallPopulation(mutationRate, popmax, 30)
    #population.show_paths = True
    
def draw():
    background(127)
    blendMode(REPLACE)
    if mousePressed and mouseButton == LEFT:
        population.step(raise_fitness=True)
    else:
        population.step()
    
    fill(0)
    textSize(16)
    text("Press and hold the left mouse button over a creature to increase its fitness", 10, 20)
    text("Press the right mouse button to generate a new generation", 10, 40)
    text("Press spacebar to show paths", 10, 60)
    textSize(24)
    text("Generation: {}".format(population.getGenerations()), 10, height-32)
        
def mousePressed():
    if mouseButton == RIGHT:
        background(255)
        population.selection()
        population.reproduction()
        
def keyPressed():
    if key == " ":
        if population.show_paths == True:
            population.show_paths = False
        else:
            population.show_paths = True