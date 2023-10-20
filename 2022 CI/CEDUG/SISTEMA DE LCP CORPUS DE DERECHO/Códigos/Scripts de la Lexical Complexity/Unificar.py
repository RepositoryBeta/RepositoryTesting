# -*- coding: utf-8 -*-
import pandas as pd
from pandas import ExcelWriter
import openpyxl
import os
import numpy as np

def calcular(df):
    valores = []
    for i in df.index:
        valores.append(int(df['P'][i]))
        valores.append(int(df['N'][i]))

    return valores

datostexto = pd.read_excel('resultados/MatrizConfusionS.xlsx',engine="openpyxl",sheet_name= 0)
dftexto = pd.DataFrame(datostexto)
datosSimple = pd.read_excel('resultados/MatrizConfusionS.xlsx',engine="openpyxl",sheet_name= 1)
dfSimple = pd.DataFrame(datosSimple)
datosM2 = pd.read_excel('resultados/MatrizConfusionM2.xlsx',engine="openpyxl",sheet_name= 0)
dfM2 = pd.DataFrame(datosM2)
datosM3 = pd.read_excel('resultados/MatrizConfusionM3.xlsx',engine="openpyxl",sheet_name= 0)
dfM3 = pd.DataFrame(datosM3)
datosF = pd.read_excel('resultados/MatrizConfusionMF.xlsx',engine="openpyxl",sheet_name= 0)
dfF = pd.DataFrame(datosF)

#MATRICES DE CONFUSION
datosSimple = pd.read_excel('resultados/MatrizConfusionS.xlsx',engine="openpyxl",sheet_name= 2)
dfMCSimple = pd.DataFrame(datosSimple)
datosM2 = pd.read_excel('resultados/MatrizConfusionM2.xlsx',engine="openpyxl",sheet_name= 1)
dfMC2 = pd.DataFrame(datosM2)
datosM3 = pd.read_excel('resultados/MatrizConfusionM3.xlsx',engine="openpyxl",sheet_name= 1)
dfMC3 = pd.DataFrame(datosM3)
datosF = pd.read_excel('resultados/MatrizConfusionMF.xlsx',engine="openpyxl",sheet_name= 1)
dfMCF = pd.DataFrame(datosF)

#CALCULO DE MATRIZ FINAL
MCS = calcular(dfMCSimple)
MC2 = calcular(dfMC2)
MC3 = calcular(dfMC3)
MCF = calcular(dfMCF)

tn = MCS[1] + MC2[1] + MC3[1] + MCF[1] # Ambos negativos.
tp = MCS[0] + MC2[0] + MC3[0] + MCF[0] # Ambos positivos.
fp = MCS[2] + MC2[2] + MC3[2] + MCF[2] # Real (No compleja) - Modelo (Si compleja).
fn = MCS[3] + MC2[3] + MC3[3] + MCF[3] # Real (Si compleja) - Modelo (No compleja).

#CALCULO DE MÉTRICAS
exactitud = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)
sensibilidad = tp / (tp + fn)
especificidad = tn / (tn + fp)
puntuacionF1 = (2 * (precision * sensibilidad)) / (precision + sensibilidad)

matrizRepresentativa = np.array([['VP', 'VN'], ['FP', 'FN']])
print(matrizRepresentativa)
matriz = np.array([[tp, tn], [fp, fn]])

dfMatrizConfusion = pd.DataFrame({'Real': ['V','F'],
                                  'P': [matriz[0][0],matriz[1][0]],
                                  'N': [matriz[0][1],matriz[1][1]],
                                  '': ['', ''],
                                  'Exactitud': [exactitud, ''],
                                  'Precisión': [precision, ''],
                                  'Sensibilidad': [sensibilidad, ''],
                                  'Especificidad': [especificidad, ''],
                                  'PuntuaciónF1': [puntuacionF1, '']
                                  })
dfMatrizConfusion = dfMatrizConfusion[['Real','P', 'N', '', 'Exactitud', 'Precisión', 'Sensibilidad', 'Especificidad', 'PuntuaciónF1']]

writer = ExcelWriter('resultados/MatrizConfusionTotal.xlsx')
dftexto.to_excel(writer, 'Palabras Textos', index=False)
dfSimple.to_excel(writer, 'Palabras Anotado Simple', index=False)
dfM2.to_excel(writer, 'Multipalabra de 2', index=False)
dfM3.to_excel(writer, 'Multipalabra de 3', index=False)
dfF.to_excel(writer, 'Frases', index=False)
dfMatrizConfusion.to_excel(writer, 'Matriz Confusión', index=False)
writer.save()
