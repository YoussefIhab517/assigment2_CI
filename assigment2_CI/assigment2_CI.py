'''
Name:Youssef Ehab 
ID:20210465
'''
import random
import numpy as np
from statistics import mode
def generate_chromosomes(number,length):
    chromosomes=[]
    i=0
    while(len(chromosomes)!=number):
        chromosomes.append("")
        for j in range(length):
            x= random.randint(0,1)
            chromosomes[i]+=str(x)
        i+=1
    return chromosomes
def decode_pop(chromosomes,length):
    decoded_pop=[]
    for i in range(len(chromosomes)):
        var_list=[]
        temp1=chromosomes[i][0:int(length/2)]
        temp2=chromosomes[i][int(length/2):]
        var_list.append(decode(temp1,length/2))
        var_list.append(decode(temp2,length/2))
        decoded_pop.append(var_list)
    return decoded_pop
def decode_pop_gray(chromosomes,length):
    decoded_pop=[]
    for i in range(len(chromosomes)):
        var_list=[]
        temp1=chromosomes[i][0:int(length/2)]
        temp2=chromosomes[i][int(length/2):]
        var_list.append(decode_gray(temp1,length/2))
        var_list.append(decode_gray(temp2,length/2))
        decoded_pop.append(var_list)
    return decoded_pop
def decode_gray(chromosome,percision):
    value = 0
    l=len(chromosome)
    x=""
    x+=chromosome[0]
    for i in range(l-1):
        x+=str(int(chromosome[i])^int(chromosome[i+1]))
    value = decode(x,percision)
    return value
def decode(chromosome,percision):
    value = 0
    l=len(chromosome)
    for i in range(l):
        value+= 2**(l-i-1)*int(chromosome[i])
    x= -2+(value/(2**(percision)-1))*4
    return x
def rank_fitness(values):
    fitness=[]
    for i in range(len(values)):
        fitness.append(8-(values[i][0]+0.0317)**2+values[i][1]**2)
    rank= np.array(fitness).argsort().argsort()+1
    sp=1+random.random()
    rank_fitness=[]
    for j in range(len(rank)):
        rank_fitness.append( (2-sp) + 2 * (sp - 1) * (rank[j]-1)/(len(fitness)-1) )
    return fitness,rank,rank_fitness
def rank_fitness2(values):
    fitness=[]
    for i in range(len(values)):
        fitness.append(8-(values[i][0]+0.0317)**2+(1-values[i][0])**2)
    rank= np.array(fitness).argsort().argsort()+1
    sp=1+random.random()
    rank_fitness=[]
    for j in range(len(rank)):
        rank_fitness.append( (2-sp) + 2 * (sp - 1) * (rank[j]-1)/(len(fitness)-1) )
    return fitness,rank,rank_fitness
def calculate_fitness(chromosomes):
    fitness=[]
    for i in range(len(chromosomes)):
        fitness.append(0)
        for j in range(len(chromosomes[i])):
            if chromosomes[i][j]=="1":
                fitness[i]+=1
    return fitness
def calculate_probability(fitness):
    sum=0.0
    probability=[]
    for i in fitness:
        sum+=i
    for i in range(len(fitness)):
        probability.append(fitness[i])
        probability[i]/=sum
    return probability
def calculate_cummulative(probaility):
    cummulativ=[]
    cummulativ.append(probaility[0])
    for i in range(1,len(probaility)):
        cummulativ.append(cummulativ[i-1]+probaility[i])
    return cummulativ
def select(chromosome,cummualtive):
    r = random.random()
    for i in range(len(cummualtive)):
        if r<=cummualtive[i]:
            return chromosome[i]
def crossover(parent1, parent2, pcross, crossover_point):
    if random.random() < pcross:
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    else:
        offspring1 = parent1
        offspring2 = parent2
    return offspring1, offspring2
def mutation(chromosome, pMut):
    mutated_chromosome = ""
    for bit in chromosome:
        if random.random() < pMut:
            if bit=='0':
                mutated_bit='1'
            else:
                mutated_bit='0'
            mutated_chromosome += mutated_bit
        else:
            mutated_chromosome += bit
    return mutated_chromosome
def choose_elite(chromosome,fitness):
    el =[]
    temp=fitness.copy()
    i =temp.index(max(temp))
    el.append(chromosome[i])
    del(temp[i])
    el.append(chromosome[j])
    return el
 
runs=1
population_size=100
generations=100
pcross=0.6
pmut=0.05
ch_length=int(input("enter chromosome length: "))
graycode=bool(input("graycode?(0/1)"))
ranking=bool(input("part 2?(0/1)"))
for j in range(runs):
    print("run ",j+1)
    chromosomes = generate_chromosomes(population_size,ch_length)
    if not graycode:
        var_values= decode_pop(chromosomes,ch_length)
    else:
        var_values= decode_pop_gray(chromosomes,ch_length)
    best_fitness=[]
    avr_fitness=[] 
    for i in range(generations):
        if not ranking:
            fitness,rank,rank_fitnessess=rank_fitness(var_values)
        else:
            fitness,rank,rank_fitnessess=rank_fitness2(var_values)
        best_fitness.append(max(rank_fitnessess))
        avr_fitness.append(sum(rank_fitnessess)/len(rank_fitnessess))
        probabilities=calculate_probability(rank_fitnessess)
        cummulative_prob= calculate_cummulative(probabilities)
        new_population=[]
        while len(new_population)<len(chromosomes):
            selection=[]
            selection.append(select(chromosomes,cummulative_prob))
            selection.append(select(chromosomes,cummulative_prob))
            offspring= crossover(selection[0],selection[1],pcross,int(ch_length/2))
            new_population.append(mutation(offspring[0],pmut))
            new_population.append(mutation(offspring[1],pmut))
        new_population=new_population[0:population_size-2]
        best=choose_elite(chromosomes,rank_fitnessess)
        new_population.extend(best)
        chromosomes=new_population.copy()
        if i==generations-1:
            print("final population: \n",chromosomes,"\n")
    print("best fitness history: \n",best_fitness,"\n")
    print("avr fitness history: \n",avr_fitness,"\n")