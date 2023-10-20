# -*- coding: utf-8 -*-
import pandas as pd
import openpyxl
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def calcular(df):
    valores = []
    for i in df.index:
        valores.append(int(df['P'][i]))
        valores.append(int(df['N'][i]))

    return valores

datos = pd.read_excel('resultados/MatrizConfusionTotal.xlsx',engine="openpyxl",sheet_name= 5)
df = pd.DataFrame(datos)

#VALORES DE LA MATRIZ DE CONFUSION
MCS = calcular(df)

#MATRIZ DE CONFUSION
matriz = np.array([[MCS[0], MCS[1]], [MCS[2], MCS[3]]])

#print(matriz)

labels = ['Yes','No']

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(matriz)
plt.title('Confusion Matrix')
fig.colorbar(cax)
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels)
plt.xlabel('Predicted Values')
plt.ylabel('Actual Values')
plt.show()