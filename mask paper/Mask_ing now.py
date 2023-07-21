import os
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from time import gmtime, strftime
import csv

POPULATION_SIZE = 200

INFECT_DIST_OnM = 0.01
INFECT_CHANCE_OnM0  = 0.01

INFECT_DIST_NoM = 0.4
INFECT_CHANCE_NoM0  = 0.3

Protectionrate = 0.7

SPEED_RANGE = [0.005, 0.01]

DEATH_CHANCE = 0.04
ELDERLY_DEATH_CHANCE = 0.1

TIME_INFECTED = 70
MASK_WEARING = [0, 1]

Q_STAR = 0.85
window = 800

Gama = 0.95
alpha = 0.005
beta = 0.001

simulation = 500
Time_step = 0.1
Time = int(simulation/Time_step)
MC= 1


C_All = [[] for mc in range(MC)]
c_all = [[[] for person in range(POPULATION_SIZE)] for mc in range(MC)]
ACompliance = [[] for mc in range(MC)]
ICompliance = [[[] for person in range(POPULATION_SIZE)] for mc in range(MC)]

# C_Indi= [0 for person in range(POPULATION_SIZE)]
# Glocost = 0
# Invicost= [0 for person in range(POPULATION_SIZE)]

# Maskstatus= [[] for person in range(POPULATION_SIZE)]
# Allcompliance= [[] for person in range(POPULATION_SIZE)]


# Avgstatus = [[] for person in range(POPULATION_SIZE)]
# Basecompliance = [np.random.uniform(0.1, 0.15) for person in range(POPULATION_SIZE)] 
# AverageCompliance = []
# IndividualCompliance = [[] for person in range(POPULATION_SIZE)]
# Compliance = [[] for person in range(POPULATION_SIZE)]
# AvgAllcompliance= [[] for person in range(POPULATION_SIZE)]

IniBasecompliance = np.random.uniform(0.1, 0.15)

def population_setup(population_size):

    population = []

    for i in range(0, population_size):
        status = 0
        age = np.random.normal(45, 90)
        x_pos = random.uniform(0, 5)
        y_pos = random.uniform(0, 5)
        x_dir = random.uniform(-1, 1)
        y_dir = random.uniform(-1, 1)
        speed = random.uniform(SPEED_RANGE[0], SPEED_RANGE[1])
        infected_since = 0
        #Mask = np.random.choice(MASK_WEARING)
        #Mask = 0

        if np.random.random()< IniBasecompliance:  #
            Mask = 1
        else:
            Mask = 0   


        population.append([status, age, x_pos, y_pos, x_dir, y_dir, speed, infected_since, Mask])



    return population

def movement_update(population):

    for i in population: 
        i[2] = i[2] + (i[4] * i[6])
        i[3] = i[3] + (i[5] * i[6])



def Cost(population):

    C = GlobalC(population, Glocost)
    c = Individual(population, C_Indi)
    sum_compliance = 0
    compliance ={}


    
    for i in population:       
        Compliance[population.index(i)]= Basecompliance[population.index(i)]+C+c[population.index(i)]

        if np.random.random()< Compliance[population.index(i)]:  #
            i[8] = 1
        else:
            i[8] = 0

        sum_compliance+= i[8]
        Allcompliance[population.index(i)].append(i[8])


    Avg_compliance = sum_compliance/POPULATION_SIZE
    compliance['AverageC'] = Avg_compliance

    for i in range(POPULATION_SIZE):
        if len(Allcompliance[i])<= window:
            AvgAllcompliance[i] = sum(Allcompliance[i])/len(Allcompliance[i])
        else:
            AvgAllcompliance[i] = sum(Allcompliance[i][-window:])/window


    compliance['IndividualC'] = AvgAllcompliance

    return compliance



def GlobalC(population, Glocost):
    Sum_Mask = 0


    for i in population:
        Sum_Mask += i[8] 
    
    Glo = Glocost+alpha*(Q_STAR-Sum_Mask/POPULATION_SIZE)
    Glo = max(Glo, 0)

    return Glo

def Individual(population, C_Indi):


    for i in population:
        Maskstatus[population.index(i)].append(i[8])


    for i in range(POPULATION_SIZE):
        if len(Maskstatus[i])<=window:
            Avgstatus[i] = sum(Maskstatus[i])/len(Maskstatus[i])
        else:
            Avgstatus[i] = sum(Maskstatus[i][-window:])/window    




    for i in population:
        Invicost[population.index(i)] = max(C_Indi[population.index(i)]+beta*(Q_STAR-Avgstatus[population.index(i)]),0)
    

    return Invicost




def check_infect(population):

    for i in population:
        if i[0] == 1:
            if i[8]==0:
                for j in population:            
                    if math.sqrt((j[2] - i[2])**2 + (j[3] - i[3])**2) < INFECT_DIST_NoM and j[0] == 0:
                        INFECT_CHANCE_NoM = INFECT_CHANCE_NoM0*(1-i[8]*Protectionrate)*(1-j[8]*Protectionrate)
                        if random.uniform(0,1) < INFECT_CHANCE_NoM:
                            j[0] = 1
                         
            elif i[8]==1:
                for j in population:            
                    if math.sqrt((j[2] - i[2])**2 + (j[3] - i[3])**2) < INFECT_DIST_OnM and j[0] == 0:
                        INFECT_CHANCE_OnM= INFECT_CHANCE_OnM0*(1-i[8]*Protectionrate)*(1-j[8]*Protectionrate)
                        if random.uniform(0,1) < INFECT_CHANCE_OnM:
                            j[0] = 0
                       

def wall_bounce(population):
    for i in population:
        if i[2] <= 0 or i[2] >= 5:
            i[4] = i[4] * -1

        if i[3] <= 0 or i[3] >= 5:
            i[5] = i[5] * -1

def update(population):

    global Glocost, C_Indi


    x_pos = random.uniform(0, 5)
    y_pos = random.uniform(0, 5)
    population[0][0] = 1
    population[0][2]= x_pos
    population[0][3]= y_pos
    population[0][7] = 10



if __name__ == '__main__':

    for mc in range(MC):
        Maskstatus= [[] for person in range(POPULATION_SIZE)]
        Allcompliance= [[] for person in range(POPULATION_SIZE)]
        C_Indi= [0 for person in range(POPULATION_SIZE)]
        Glocost = 0
        Invicost= [0 for person in range(POPULATION_SIZE)]
        Avgstatus = [[] for person in range(POPULATION_SIZE)]
        Basecompliance = [np.random.uniform(0.1, 0.15) for person in range(POPULATION_SIZE)] 
        AverageCompliance = []
        IndividualCompliance = [[] for person in range(POPULATION_SIZE)]
        Compliance = [[] for person in range(POPULATION_SIZE)]
        AvgAllcompliance= [[] for person in range(POPULATION_SIZE)]


        population = population_setup(POPULATION_SIZE) # use setup function to initialize population array 
        for i in range(Time):
            update(population)

            movement_update(population)
            wall_bounce(population)
            check_infect(population)

            
            Glocost = GlobalC(population, Glocost)
            C_All[mc].append(Glocost)

            C_Indi= Individual(population, C_Indi)
            for i in range(POPULATION_SIZE):
                c_all[mc][i].append(C_Indi[i])


            Com = Cost(population)  
            ACompliance[mc].append(Com['AverageC'])  

            for i in range(POPULATION_SIZE):
                ICompliance[mc][i].append(Com['IndividualC'][i])

    AvgC_All = []   
    Avgc_all = [[] for person in range(POPULATION_SIZE)]
    AvgACompliance= []
    AvgICompliance= [[] for person in range(POPULATION_SIZE)]
  
    for j in range(len(C_All[0])):
        middle= 0
        for i in range(MC):
            middle+=C_All[i][j]
        AvgC_All.append(middle/MC)

    
    
    for i in range(len(c_all[0][0])):
        for k in range(POPULATION_SIZE):
            value= 0
            for j in range(MC):
                value+= c_all[j][k][i]
            Avgc_all[k].append(value/MC)

    for j in range(len(ACompliance[0])):
        middle1= 0
        for i in ACompliance:
            middle1+=i[j]
        AvgACompliance.append(middle1/MC)
    
    for i in range(len(ICompliance[0][0])):
        for k in range(POPULATION_SIZE):
            value1= 0
            for j in range(MC):
                value1+= ICompliance[j][k][i]
            AvgICompliance[k].append(value1/MC)

    # AvgC_All = sum(C_All)/len(C_All)
    # Avgc_all = sum(c_all)/len(c_all)
    # AvgACompliance = sum(ACompliance)/len(ACompliance)
    # AvgICompliance = sum(ICompliance)/len(ICompliance)



    fig1 = plt.figure(figsize=(8,8))
    spec1 = fig1.add_gridspec(ncols=1, nrows=2, height_ratios=[1,1])
    
    main_plot = fig1.add_subplot(spec1[0,0])

    other = fig1.add_subplot(spec1[1,0])

    main_plot.plot(np.arange(0, simulation, Time_step), AvgC_All, color='blue')
    main_plot.set_xlabel('Time (sec)')
    main_plot.set_ylabel('Global cost')


    for i in range(POPULATION_SIZE):
        other.plot(np.arange(0, simulation, Time_step),Avgc_all[i])

    other.set_xlabel('Time (sec)')
    other.set_ylabel('Individual cost')



    fig2 = plt.figure(figsize=(8,8))
    spec2 = fig2.add_gridspec(ncols=1, nrows=2, height_ratios=[1,1])
    
    one = fig2.add_subplot(spec2[0,0])

    two = fig2.add_subplot(spec2[1,0])

    one.plot(np.arange(0, simulation, Time_step), AvgACompliance, color='blue')
    one.plot(np.arange(0, simulation, Time_step), [0.85 for i in range(int((simulation)/Time_step))], color='red', linestyle="--")
    one.set_xlabel('Time (sec)')
    one.set_ylabel('Average compliance')
    one.set_ylim(0, 1) 
 

    for i in range(POPULATION_SIZE):
        two.plot(np.arange(0, simulation, Time_step), AvgICompliance[i])
    two.plot(np.arange(0, simulation, Time_step), [0.85 for i in range(int((simulation)/Time_step))], color='red', linestyle="--")
    two.set_xlabel('Time (sec)')
    two.set_ylabel('Individual compliance')
    two.set_ylim(0, 1) 
  

    
    np.savetxt('average_global.csv', AvgC_All, delimiter=',') 
    np.savetxt('average_individual.csv', Avgc_all, delimiter=',')  
    np.savetxt('AvgACompliance.csv', AvgACompliance, delimiter=',')  
    np.savetxt('AvgICompliance.csv', AvgICompliance, delimiter=',')  



    plt.show()