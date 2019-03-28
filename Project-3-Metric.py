import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio 
import pandas as pd
from pprint import pprint

#Load Data
a = sio.loadmat('neuralOut.mat')
NeuralOut = a['neuralOut']

a = sio.loadmat('target.mat')
Target = a['target']

data = pd.DataFrame({'NeuralOut' : [NeuralOut[i] for i in range(len(NeuralOut))] , 'target' : [Target[i] for i in range(len(Target))]})

max_lim = 500
TPF = []
FPF = []

values = pd.DataFrame({'TP':[0],'FP':[0],'TN':[0],'FN':[0]})

for j in range(max_lim):
	threshold = (j/(max_lim*1.0))
    #mapping : {'TP':[1],'FP':[2],'TN':[3],'FN':[4]}
	data['type'] =  np.where((data['NeuralOut'] > threshold) & (data['target'] == 1),1,
                 np.where((data['NeuralOut'] > threshold) & (data['target'] == 0),2,
				   np.where((data['NeuralOut'] < threshold) & (data['target'] == 0),3,
                 np.where((data['NeuralOut'] < threshold) & (data['target'] == 1),4,0))))

	values['TP'] = np.sum(np.where(data['type'] == 1,1.0,0.0))
	values['FP'] = np.sum(np.where(data['type'] == 2,1.0,0.0))
	values['TN'] = np.sum(np.where(data['type'] == 3,1.0,0.0))
	values['FN'] = np.sum(np.where(data['type'] == 4,1.0,0.0))

	TPF.append(values['TP']/(values['TP']+values['FN']))
	FPF.append(values['FP']/(values['TN']+values['FP']))

plt.plot(FPF,TPF)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('FPF')
plt.ylabel('TPF')
plt.title('Receiver Operating Characteristic (ROC)')

area = 0

for i in range(len(FPF)-1):
	area += (FPF[i]-FPF[i+1])*(TPF[i]+TPF[i+1])/2.0

pprint('Area Under the Curve (AUC) = '+str(area[0]))

plt.show()