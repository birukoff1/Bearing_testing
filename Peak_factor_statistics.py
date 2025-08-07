#%% Libraries
import numpy as np
import matplotlib.pyplot as plt
import os
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

Folder = 'New_setup/Test_2/'

Data = {}

with os.scandir(Folder) as bearings:
    for bearing in bearings:
        
        Data[bearing.name] = []
        
        with os.scandir(Folder + bearing.name + '/') as files:
            for file in files:
                
                Time, Signal = Read_data(open(Folder + bearing.name + '/' + file.name))
                
                N = len(Time)
                F_s = 1/Time[1]
                
                Data[bearing.name].append([file.name,
                                           float(np.quantile(np.abs(Signal), 0.95)), # 95-й квантиль
                                           float(np.quantile(np.abs(Signal), 0.98)), # 98-й квантиль
                                           float(np.quantile(np.abs(Signal), 0.99)), # 99-й квантиль
                                           float(max(np.abs(Signal))), # 100-й квантиль
                                           float(np.sqrt(1/N*sum([x**2 for x in Signal])))]) # RMS


#%% Graphs

plt.figure(figsize=(8, 6))
for key, data in Data.items():
    x_vals = [x+1 for x in range(len(data))]
    y_vals = [point[5] for point in data]
    plt.scatter(x_vals, y_vals, label=key)
plt.legend(loc='upper right')
plt.xlim([0.5, 4.5])
plt.grid(True)
plt.xlabel('Измерение')
plt.ylabel('Ускорение, м/с^2')
plt.title('Среднеквадратичное ускорение')
plt.show()

plt.figure(figsize=(8, 6))
for key, data in Data.items():
    x_vals = [x+1 for x in range(len(data))]
    y_vals = [point[4]/point[5] for point in data]
    plt.scatter(x_vals, y_vals, label=key)
plt.legend(loc='upper right')
plt.xlim([0.5, 4.5])
plt.grid(True)
plt.xlabel('Измерение')
plt.ylabel('-')
plt.title('Пик-фактор')
plt.show()


plt.figure(figsize=(8, 6))
for key, data in Data.items():
    x_vals = [x+1 for x in range(len(data))]
    y_vals = [(point[3]-point[2])/(point[1]-point[5]) for point in data]
    plt.scatter(x_vals, y_vals, label=key)
plt.legend(loc='upper right')
plt.xlim([0.5, 4.5])
plt.grid(True)
plt.xlabel('Измерение')
plt.ylabel('-')
plt.title('Пик-фактор+')
plt.show()