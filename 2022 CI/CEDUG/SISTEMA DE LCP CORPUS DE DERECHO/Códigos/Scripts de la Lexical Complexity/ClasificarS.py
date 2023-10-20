# -*- coding: utf-8 -*-
import nltk
import pandas as pd
from pandas import ExcelWriter
import openpyxl
import os
from nltk.corpus import stopwords
from nltk.tag import StanfordPOSTagger
import re
import numpy as np

class Clasificacion:

    def __init__(self):
        nltk.download('stopwords')
        self.PC = []

        # OBTENER LISTA CREA
        ruta = './CREA_total.txt'
        f = open(ruta)
        lines = f.readlines()
        f.close()
        crea = {}
        crea2 = {}
        creaT = {}
        creaT2 = {}
        for l in lines[1:]:  # those words not in the 1000 most frequent words in CREA are low frequency words
            data = l.strip().split()
            if (float(data[2].replace(',', '')) >= 1000):
                crea[data[1]] = float(data[2].replace(',', ''))
                palSinTilde = data[1].replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace(
                    "ú", "u")
                crea2[palSinTilde] = float(data[2].replace(',', ''))
            creaT[data[1]] = float(data[2].replace(',', ''))
            palSinTilde = data[1].replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú",
                                                                                                                  "u")
            creaT2[palSinTilde] = float(data[2].replace(',', ''))
        self.crea = crea
        self.crea2 = crea2
        self.creaT = creaT
        self.creaT2 = creaT2

    def matrizConfusion(self,listaModelo,listaReal):
        listM = []
        cont = 0
        for lis in listaModelo:
            listM.append(lis[0])
        listR = []
        for lis in listaReal:
            listR.append(lis[0])

        for lis in listR:
            if lis in listM:
                cont+=1
            else:
                pass

        tnlist = len(listaModelo) - len(listaReal)
        tn = 0  # Ambos negativos.
        tp = 0  # Ambos positivos.
        fp = 0  # Real (No compleja) - Modelo (Si compleja).
        fn = 0  # Real (Si compleja) - Modelo (No compleja).

        for palMod in listaModelo:
            encontrado = False
            for palReal in listaReal:
                if palMod[0] == palReal[0]:
                    if palMod[1] == 1 and palReal[1] == 1:
                        tp += 1
                        encontrado = True
                    elif palMod[1] == 0 and palReal[1] == 1:
                        fn += 1
                        encontrado = True
            if encontrado == False:
                if palMod[1] == 0:
                    tn += 1
                elif palMod[1] == 1:
                    fp += 1

        print(tnlist)
        matrizRepresentativa = np.array([['VP', 'VN'], ['FP', 'FN']])
        print(matrizRepresentativa)
        matrizConfusion = np.array([[tp, tn], [fp, fn]])

        return matrizConfusion

c = Clasificacion()

datostexto = pd.read_excel('resultados/Palabras Separadas Texto.xlsx',engine="openpyxl",sheet_name= 0)
dftexto = pd.DataFrame(datostexto)
datosSimple = pd.read_excel('resultados/Palabras Separadas Texto.xlsx',engine="openpyxl",sheet_name= 1)
dfSimple = pd.DataFrame(datosSimple)


listaTexto = []
for i in dftexto.index:
    pal = ""
    pal +=str(dftexto['Palabra'][i])
    palabra = pal.lower()
    if palabra == 'nan':
        palabra ="null"
    listaTexto.append(palabra)

listaSimple = []
for i in dfSimple.index:
    pal = ""
    pal +=str(dfSimple['Palabra'][i])
    palabra = pal.lower()
    if palabra == 'nan':
        palabra ="null"
    listaSimple.append(palabra)


listaPTUnica = []
for lis in listaTexto:
    if lis not in c.crea:
        listaPTUnica.append([lis, 1])
    elif lis not in c.crea2:
        listaPTUnica.append([lis, 1])
    else:
        listaPTUnica.append([lis, 0])

listaPASimple = []
for lis in listaSimple:
   listaPASimple.append([lis,1])

matriz = c.matrizConfusion(listaPTUnica,listaPASimple)
print(matriz)


dfMatrizConfusion = pd.DataFrame({'Real': ['V','F'],
                                  'P': [matriz[0][0],matriz[1][0]],
                                  'N': [matriz[0][1],matriz[1][1]]})
dfMatrizConfusion = dfMatrizConfusion[['Real','P', 'N']]

df = pd.DataFrame({'Palabra': [w[0] for w in listaPTUnica],
                   'Complejidad': [w[1] for w in listaPTUnica]})
df = df[['Palabra', 'Complejidad']]

dfSimple = pd.DataFrame({'Palabra': [w[0] for w in listaPASimple],
                   'Complejidad': [w[1] for w in listaPASimple]})
dfSimple = dfSimple[['Palabra', 'Complejidad']]

writer = ExcelWriter('resultados/MatrizConfusionS.xlsx')
df.to_excel(writer, 'Palabras Textos', index=False)
dfSimple.to_excel(writer, 'Palabras Anotado Simple', index=False)
dfMatrizConfusion.to_excel(writer, 'Matriz Confusión', index=False)
writer.save()
