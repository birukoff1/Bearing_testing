#%% Libraries
import numpy as np
import matplotlib.pyplot as plt


#%% Functions

def Read_data(file):
    
    i=0
    Data = []
    while True:
        line=file.readline()
        i+=1
        
        if line.split(':')[0] == 'Number of frames':
            N = int(line.split(':')[1][1:])
            
        elif line.split(':')[0] == 'Input Rate In kHz':
            F_s = float(line.split(':')[1][1:])*1000.0
            Time = 1/F_s*np.array([x for x in range(N)])
            
        elif not line:
            break
        
        if i >= 20:
            Data.append(float(line.lstrip()))       
    file.close()
     
    return Time, np.array(Data)


#%% Reading the data

file = open('New_setup/Bearing_3/50Hz_10kg.txt')

Time, Data = Read_data(file)

N = len(Time)
F_s = 1/Time[1]

plt.figure(figsize=(8, 6))
plt.plot(Time, Data)
plt.grid(True)
plt.xlim([2, 2.1])
plt.xlabel('Время, с')
plt.ylabel('Напряжение, В')
plt.show()

