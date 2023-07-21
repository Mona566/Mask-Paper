import matplotlib.pyplot as plt
import numpy as np
from scipy import signal   
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from matplotlib.lines import Line2D
import networkx as nx
#import random
from random import random, sample
import os
#import winsound
from time import gmtime, strftime
from shutil import copyfile
import csv
from scipy.signal import butter, lfilter, freqz, filtfilt

import numpy as np
import pandas as pd
import seaborn as sns



MC=25
# SELF_QUARANTINE_TIME = 20 # time it takes for someone infected to stop moving, being the asymptomatic phase of covid
simulation = 250
Time_step = 0.1
Time = int(simulation/Time_step)

AllInfectedrate2030 =[]
AllInfectedrate3040 =[]
AllInfectedrate5060 =[]
AllInfectedrate7080 =[]

Infectedrate2030= np.loadtxt(r"/Users/liannazhao/Desktop/mask figure/infected_rate20_30.csv", delimiter=',')
Infectedrate3040= np.loadtxt(r"/Users/liannazhao/Desktop/mask figure/infected_ratetry30403.csv", delimiter=',')
Infectedrate5060= np.loadtxt(r"/Users/liannazhao/Desktop/mask figure/infected_rate5060try2.csv", delimiter=',')
Infectedrate7080= np.loadtxt(r"/Users/liannazhao/Desktop/mask figure/infected_rate7080try2.csv", delimiter=',')


for i in range(len(Infectedrate2030)):
   for j in Infectedrate2030[i]:
      AllInfectedrate2030.append(j) 

# for i in range(len(Infectedrate2030)):
#    for j in Infectedrate2030[i][:20]:
#       AllInfectedrate2030.append(j) 

for i in range(len(Infectedrate3040)):
   for j in Infectedrate3040[i]:
      AllInfectedrate3040.append(j)  

for i in range(len(Infectedrate5060)):
   for j in Infectedrate5060[i]:
      AllInfectedrate5060.append(j) 

for i in range(len(Infectedrate7080)):
   for j in Infectedrate7080[i]:
      AllInfectedrate7080.append(j) 

fig5, ax5 = plt.subplots(figsize=(8,4))
# ax5.grid(linestyle='--')
# ax5.set_xlabel('Time (Sec)')
# ax5.set_ylabel('Delaytime')
# ax5.set_ylabel('The proportion of infected people', color='black')

# Create a DataFrame from the lists
df = pd.DataFrame(list(zip(AllInfectedrate2030,AllInfectedrate3040,AllInfectedrate5060,AllInfectedrate7080)), columns =["20%-30% mask", "30%-40% mask", "50%-60% mask", "70%-80% mask"]) 

# Reshape the DataFrame from wide format to long format
df_melt = df.melt(var_name='', value_name='The proportion of infected people')

# Create a boxplot
sns.boxplot(x='', y='The proportion of infected people', data=df_melt)


# # data=[AllInfectedrate2030,AllInfectedrate3040,AllInfectedrate5060,AllInfectedrate7080]
# # labels = ["20%-30% mask wearing", "30%-40% mask wearing", "50%-60% mask wearing", "70%-80% mask wearing"]
# sns.boxplot(list(data.values()),labels=data.keys())

ax5.set_ylim(0,100) # 限制x的值为[0,20]
# plt.legend()

plt.show()

