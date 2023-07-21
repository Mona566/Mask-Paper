import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pandas as pd

average_global= np.loadtxt(r"/Users/liannazhao/Desktop/Mask data collected/average_global.csv", delimiter=',')
eco2= []
tvoc= []
Avgco2= []
Avgtvoc= []
Avgstatus = []
Invicost= []


C_Indi = 0
Mask_status = []
window= 9
Gama = 0.95
alpha = 0.005
beta = 0.001
Q_STAR = 0.85

average_global= np.loadtxt(r"/Users/liannazhao/Desktop/Mask data collected/average_global.csv", delimiter=',')
file1=pd.read_csv(r'/Users/liannazhao/Desktop/mask_wearing.csv')
file1=np.array(file1)


for item in file1:
       eco2.append(item[1])
       tvoc.append(item[2])
       Avgco2.append(item[3])
       Avgtvoc.append(item[4])


       if item[3]<=500 and item[4]<=50:
              Mask_status.append(0)               
              #self.Cost= self.Cost-1
              #Token= self.Cost
       
       elif item[3]>400 and item[4]>50:
              Mask_status.append(1)                    
              #self.Cost= self.Cost+1
              #Token= self.Cost
       else:
              print(item[3], item[4])


for i in range(len(Mask_status)):
       if i+window< len(Mask_status):
              a= sum(Mask_status[i:i+window])/window
              Avgstatus.append(a)
       else:
              b= Avgstatus[-1]
              Avgstatus.append(b)


# if len(Mask_status)<=window:
#        Avgstatus.append(sum(Mask_status)/len(Mask_status)) 
# else:
#        Avgstatus.append(sum(Mask_status[-window:])/window) 

for i in Avgstatus:
       a= max(C_Indi+beta*(Q_STAR-i),0)
       Invicost.append(a) 

gcost= average_global[0:1000:20]

#Part_gcost= random.sample(list(gcost), 50)
cost= []
for i in range(len(Invicost)):
       cost.append(Invicost[i]+gcost[i]) 

# plt.subplots(figsize=(8,4))
# plt.grid(linestyle='--')
# plt.xlabel('Time (sec)')
# plt.ylabel('Global cost')
# plt.plot(gcost, linewidth=2, color='tab:blue')  

plt.subplots(figsize=(8,4))
plt.grid(linestyle='--')
plt.xlabel('Time (sec)')
plt.ylabel('Token')
plt.plot(cost) 
# plt.plot(tvoc) 
# plt.plot(Avgco2) 
# plt.plot(Avgtvoc) 

plt.show()

