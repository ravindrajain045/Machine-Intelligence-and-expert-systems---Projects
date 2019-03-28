from random import (random, randint)
import matplotlib.pyplot as plt

__all__ = ['individual', 'random_population']

class individual:
    def __init__(self, elements):
        self.elements = elements
        self.fitness = individual._update_fitness(elements)
    
    def mate(self, mate):
        pivot = randint(0, len(self.elements) - 1)
        elements1 = self.elements[:pivot] + mate.elements[pivot:]
        elements2 = mate.elements[:pivot] + self.elements[pivot:]        
        return individual(elements1), individual(elements2)
        
    def mate_2point(self, mate):
        pivot1 = randint(0, int(len(self.elements)/2) - 1)
        pivot2 = randint(int(len(self.elements)/2),len(self.elements)-1)
        elements1 = self.elements[:pivot1] + mate.elements[pivot1:pivot2] + self.elements[pivot2:]
        elements2 = mate.elements[:pivot1] + self.elements[pivot1:pivot2] + mate.elements[pivot2:]         
        return individual(elements1), individual(elements2)
    
    def mutate(self):
        elements = self.elements
        mut_range=10
        idx = randint(0, len(elements) - (1+mut_range))
        for i in range(mut_range):
            elements[idx+i] = 100-elements[idx+i];        
        return individual(elements)

    @staticmethod            
    def _update_fitness(elements):
        fitness = len([1 for item in elements if item==5 ])
        return fitness
        
    @staticmethod
    def gen_random():
        elements = []
        for x in range(100):
            elements.append(randint(0, 101))               
        return individual(elements)
        
class random_population:
    
    def __init__(self, size=100, crossover=0.8, elitism=0.0, mutation=0.05):
        self.elitism = elitism
        self.mutation = mutation
        self.crossover = crossover
        
        buf = []
        for i in range(size): buf.append(individual.gen_random())
        self.population = sorted(buf, key=lambda x: x.fitness)
        self.population = buf
                        
    def roulette_wheel(self):
        size = len(self.population)
        tot_fitness=0;
        for i in range(size):
            tot_fitness+=self.population[i].fitness
        rand_fitness=randint(0, tot_fitness)
        tot_fitness=0
        for i in range(size):
            tot_fitness+=self.population[i].fitness
            if rand_fitness<=tot_fitness:
                return self.population[i]

    def select_parents(self):
        return (self.roulette_wheel(), self.roulette_wheel())
        
    def evolve(self):
        size = len(self.population)
        idx = int(round(size * self.elitism))
        buf = self.population[:idx]
        
        while (idx < size):
            if random() <= self.crossover:
                (p1, p2) = self.select_parents()
                #children = p1.mate_2point(p2)
                children = p1.mate(p2)
                for c in children:
                    if random() <= self.mutation:
                        buf.append(c.mutate())
                    else:
                        buf.append(c)
                idx += 2
            else:
                if random() <= self.mutation:
                    buf.append(self.population[idx].mutate())
                else:
                    buf.append(self.population[idx])
                idx += 1
        
        self.population = sorted(buf[:size], key=lambda x: x.fitness)
        self.population = buf[:size]
        
    def find_fitness(self):
        max_fitness=0
        min_fitness=100
        avg_fitness=0
        for i in range(len(self.population)):
            if(max_fitness<self.population[i].fitness):
                max_fitness=self.population[i].fitness
            if(min_fitness>self.population[i].fitness):
                min_fitness=self.population[i].fitness
            avg_fitness+=self.population[i].fitness
        avg_fitness/=len(self.population)    
        print("Maximum Fitness: %d" % (max_fitness))
        print("Average Fitness: %d" % (avg_fitness))
        print("Minimum Fitness: %d" % (min_fitness))
        return max_fitness,min_fitness,avg_fitness

if __name__ == "__main__":
    maxGenerations = 1000
    pop = random_population(size=100, crossover=0.8, elitism=0.0, mutation=0.05)
    max_fitness=[]
    min_fitness=[]
    avg_fitness=[]
    gen=[]
    conv_thres=300
    max_last_iter=0
    count=0
    for i in range(1, maxGenerations+1):
        print("Generation %d:" % (i))
        maf,mif,avf=pop.find_fitness()
        pop.evolve()
        if(max_last_iter==maf):
            count+=1
        else:
            count=0        
        max_fitness.append(maf)
        min_fitness.append(mif)
        avg_fitness.append(avf)
        gen.append(i)
        if(count==conv_thres):
            break
        max_last_iter=maf
    plt.plot(gen,max_fitness)
    plt.plot(gen,avg_fitness)
    plt.plot(gen,min_fitness)
    plt.ylim([0, 30])
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.title('Maximum, Minimum & Average Fitness vs Generations')
    plt.legend(['Max Fitness', 'Avg Fitness', 'Min Fitness'], loc='upper right')