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

    def clasificar(self,lista):

        os.environ['CLASSPATH'] = 'stanford-postagger-full-2017-06-09'
        os.environ['STANFORD_MODELS'] = 'stanford-postagger-full-2017-06-09/models/'
        if (os.name == 'nt'):
            java_path = "C:/Program Files/Java/jdk-11.0.10/bin/java.exe"
            # java_path = "C:/Windows/System32/java.exe"
            os.environ['JAVAHOME'] = java_path
        spanishTagger = nltk.tag.stanford.StanfordPOSTagger('spanish.tagger', encoding='utf8')
        englishTagger = nltk.tag.stanford.StanfordPOSTagger('english.tagger', encoding='utf8')
        lang = "es"

        listaPal = []
        for w in lista:
            wSplit = w.split()
            palabras = []
            for ws in wSplit:
                palabras.append(ws)
            listaPal.append(palabras)

        new_pos_sentences = []

        if lang == 'es':
            tag = spanishTagger.tag
        else:
            tag = englishTagger.tag

        for sentence in listaPal:
            new_pos_sentences.append(tag(sentence))
        wClasificacion = new_pos_sentences

        new_pos_content_sentences_cw = []

        for sentence in wClasificacion:
            new_pos_content_sentences_cw.append([w[0] for w in sentence if re.match('N.*|V.*|A.*', w[1])])
        wContenido = new_pos_content_sentences_cw

        new_pos_content_sentences_cw = []

        for sentence in wClasificacion:
            new_pos_content_sentences_cw.append([w[1] for w in sentence if re.match('N.*|V.*|A.*', w[1])])
        wCContenido = new_pos_content_sentences_cw

        wFinalCContenido = []
        for sentence in wCContenido:
            if len(sentence) > 0:
                wFinalCContenido.append(sentence)

        for estruc in wFinalCContenido:
            self.PC.append(' '.join(estruc))

        return wContenido


    def Frecuencia(self,lista):
        PromComp = []
        frecuencia = 0.00
        promedioF = 0.00
        for lis in lista:
            if len(lis) > 0:
                for w in lis:
                    if w in self.creaT:
                        frecuencia += self.creaT[w]
                    elif w in self.creaT2:
                        frecuencia += self.creaT2[w]
                    else:
                        frecuencia += 1
                promedioF += (frecuencia/float(len(lis)))
                if promedioF >= 1000:
                    PromComp.append([promedioF, 0])
                else:
                    PromComp.append([promedioF, 1])
                frecuencia = 0.00
                promedioF = 0.00
            else:
                frecuencia = None
                promedioF = None
                PromComp.append([None, None])
                frecuencia = 0.00
                promedioF = 0.00

        return PromComp

    def matrizConfusion(self,lista):
        tn = 0  # Ambos negativos.
        tp = 0  # Ambos positivos.
        fp = 0  # Real (No compleja) - Modelo (Si compleja).
        fn = 0  # Real (Si compleja) - Modelo (No compleja).
        listaFiltrada = []
        for lis in lista:
            if lis[2] == None:
                pass
            else:
                listaFiltrada.append(lis)

        for lis in listaFiltrada:
            if lis[3] == 1:
                tp+=1
            else:
                fn+=1

        matrizRepresentativa = np.array([['VP', 'VN'], ['FP', 'FN']])
        print(matrizRepresentativa)
        matrizConfusion = np.array([[tp, tn], [fp, fn]])

        return matrizConfusion

    def Estadistica(self):
        return self.PC

c = Clasificacion()

datosM2 = pd.read_excel('resultados/Palabras Separadas Texto.xlsx',engine="openpyxl",sheet_name= 3)
dfM2 = pd.DataFrame(datosM2)

listaM2 = []
for i in dfM2.index:
    pal = ""
    pal +=str(dfM2['Palabra'][i])
    palabra = pal.lower()
    listaM2.append(palabra)

listaPAM2 = c.clasificar(listaM2)
listaPAM2F = c.Frecuencia(listaPAM2)
print(listaPAM2F)

listaFM2 = []
for i in range(len(listaM2)):
    freqComple = []
    for lis in listaPAM2F[i]:
        freqComple.append(lis)
    listaFM2.append([listaM2[i],' '.join(listaPAM2[i]),freqComple[0],freqComple[1]])
    freqComple = []

print(listaFM2)

matriz = c.matrizConfusion(listaFM2)
print(matriz)

patron = c.Estadistica()


dfMatrizConfusion = pd.DataFrame({'Real': ['V','F'],
                                  'P': [matriz[0][0],matriz[1][0]],
                                  'N': [matriz[0][1],matriz[1][1]]})
dfMatrizConfusion = dfMatrizConfusion[['Real','P', 'N']]

df = pd.DataFrame({'Palabra': [w[0] for w in listaFM2],
                   'Palabra_Contenido': [w[1] for w in listaFM2],
                   'Frecuencia': [w[2] for w in listaFM2],
                   'Complejidad': [w[3] for w in listaFM2],
                   })
df = df[['Palabra','Palabra_Contenido','Frecuencia', 'Complejidad']]

dfpatron = pd.DataFrame({'Patrón': [w for w in patron]})
dfpatron = dfpatron[['Patrón']]

writer = ExcelWriter('resultados/MatrizConfusionM3.xlsx')
df.to_excel(writer, 'Multipalabra de 3', index=False)
dfMatrizConfusion.to_excel(writer, 'Matriz Confusión', index=False)
dfpatron.to_excel(writer, 'Patrón de Multipalabra', index=False)
writer.save()
