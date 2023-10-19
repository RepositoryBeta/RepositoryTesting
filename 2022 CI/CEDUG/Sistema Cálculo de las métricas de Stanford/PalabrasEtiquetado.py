# -*- coding: utf-8 -*-
import openpyxl
import nltk
import codecs
import FiltradoOraciones
import pandas as pd
import os
import statsmodels
from statsmodels.stats.inter_rater import fleiss_kappa as fk
import numpy as np
#OBTENCIÓN DE LOS DATOS DEL ARCHIVO DE MÉTRICAS STANFORD (TABLA GENERAL - TABLA COMPACTA DE BLOQUES)
datos = pd.read_excel('resultados/respaldo/Metricas_Stanford - COMPACTA.xlsx',engine="openpyxl",sheet_name= 0)
dfMetricas = pd.DataFrame(datos)
datos = pd.read_excel('resultados/respaldo/Metricas_Stanford - COMPACTA.xlsx',engine="openpyxl",sheet_name= 1, index_col=0)
dfBloques = pd.DataFrame(datos)
datosAnotado = pd.read_excel('resultados/Datos del Anotado.xlsx',engine="openpyxl",sheet_name= 1, index_col=0)
dfAnotado = pd.DataFrame(datosAnotado)
datosAnotado2 = pd.read_excel('resultados/Datos del Anotado.xlsx',engine="openpyxl",sheet_name= 0, index_col=0)
dfAnotado2 = pd.DataFrame(datosAnotado2)
cont = 0
palabrasEtiquetado = []
cantAnotadores = []
listArchivos = []
listNivel = ['Basico','Intermedio','Avanzado']
cantPalabra = []
listCantPalCoincidencia = []
for i in dfMetricas.index:
    listCantPalAnotadas = []
    listCantidadPalRep = []
    diccCantPalAnotadas = {}
    diccCantPalCoincidencia = {}
    cantPal = []
    palabraAnotada = []
    for nivel in listNivel:
        #print("Inicio: " +str(i))
        nombreArchivo = dfMetricas['Unnamed: 0'][i]
        bloque = dfMetricas['BLOQUE'][i]
        #print(dfAnotado)
        rsCedula = dfAnotado.query('Selección == "'+bloque+'" and Nivel == "'+nivel+'"')
        print(rsCedula)

        #rsCedula.groupby('Cedula')['Selección'].sum()
        #print(rsCedula)
        print("Analizando texto: " + nombreArchivo + "\n")
        print("Nivel: " +nivel)
        #OBTENER FILTRADO POR CEDULA DE ANOTADORES Y EL TEXTO

        for k in rsCedula.index:
            #print("Anotador: " +str(rsCedula['Cedula'][k]))
            rsAnotado = dfAnotado2[dfAnotado2.Nombre_archivo.isin([nombreArchivo])&dfAnotado2.Cedula.isin([rsCedula['Cedula'][k]])]
            print(rsAnotado)
            #OBTENER TODAS LAS PALABRAS ANOTADAS EN EL TEXTO POR TODOS LOS ANOTADORES
            #print("Palabras anotadas: ")
            for j in rsAnotado.index:
                #print(rsAnotado['Palabra'][j])
                palabraAnotada.append(rsAnotado['Palabra'][j])
            print(palabraAnotada)
            #LISTA QUE CONTIENE LA CANTIDAD DE PALABRAS ANOTADAS EN EL TEXTO POR LOS ANOTADORES.
            cantPal.append(len(rsAnotado))
            print("Cantidad de palabras anotadas: "+str(len(rsAnotado)))
            print("\n")
    listCantPalRep = [0,0,0,0,0,0,0,0,0]
    #OBTENER LAS PALABRAS SIN REPETICIONES
    listPalabraUnica = list(set(palabraAnotada))
    print(listPalabraUnica)
    #diccCantPalAnotadas[nivel] = cantPal
    #print(diccCantPalAnotadas)
    #RECORRIDO DE LA LISTA DE LA PALABRAS ÚNICAS
    for listaPU in listPalabraUnica:
        repet = 0
        #RECORRIDO DE LA LISTA DE LAS PALABRAS ANOTADAS EN EL TEXTO
        for listaPA in palabraAnotada:
            #print(listaPU)
            if(listaPU == listaPA):
                repet +=1
        if(repet > 0):
            print("La palabra " +listaPU +" tiene " +str(repet) +" Anotador(es).")
            listCantPalRep[repet - 1] += 1
        palabrasEtiquetado.append(listaPU)
        cantAnotadores.append(repet)
        listArchivos.append(nombreArchivo)
    #print("\n\n")
    print("Cantidad de Palabras: ")
    print(cantPal)
    print("Cantidad de Palabras repetidas: ")
    print(listCantPalRep)
    if len(cantPal) < 10:
        cantPalabra.append(cantPal)
    listCantPalCoincidencia.append(listCantPalRep)
nivelComplejidad = []
for coincidencia in cantAnotadores:
    complejidad = 0
    if coincidencia > 2:
        complejidad = coincidencia/9
    nivelComplejidad.append(complejidad)
print(len(nivelComplejidad))
columnas1 = ['Palabra Anotada', 'Cantidad de Anotadores']
columnas2 = ['id', 'Texto', 'Sentencia', 'Palabra', 'Nivel de Complejidad']
dfPalEti = pd.DataFrame()
dfNivelComp = pd.DataFrame()
for anot in columnas1:
    dfPalEti[anot] = None
for comp in columnas2:
    dfNivelComp[comp] = None
id = []
listOraciones = []

#BLOQUE 2
textComplexityStanford = FiltradoOraciones.FiltradoOraciones()
nltk.download('stopwords')

#BLOQUE 3
raiz = 'textos_analizar/Derecho'
indir = raiz
data = []
carrera = os.listdir(indir)
for indice in range(len(palabrasEtiquetado)):
    archivo = listArchivos[indice]
    for root, dirs, filenames in os.walk(indir):
        if archivo in filenames:
            root = root.replace("\\", '/')
            try:
                file = codecs.open(root + '/' +archivo, 'rb', encoding='utf-8')
                text = file.read()
            except UnicodeDecodeError:
                file = codecs.open(root + '/' +archivo, 'rb', encoding='latin-1')
                text = file.read()
            #print(text)
            print("\t\t\tProcesando texto: " +archivo)
            oraciones = textComplexityStanford.ProcesarTexto(text)
            #print("Texto filtrado:")
            #print(oraciones)
            texto = ""
            textUni = ""
            band = False
            contador = 0
            for sentence in oraciones:
                contador+=1
                #print(sentence)
                for w in sentence:
                    textUni += w + " "
                    if palabrasEtiquetado[indice] in w:
                        for word in sentence:
                            texto += word + " "
                        listOraciones.append(texto)
                        band = True
                        break
                if band == False:
                    if palabrasEtiquetado[indice] in textUni:
                        #print(palabrasEtiquetado[indice])
                        listOraciones.append(textUni)
                        band = True
                        break
                if band == True:
                    break
            if band==False:
                print(text)
                print(palabrasEtiquetado[indice])
#print(listOraciones)
print('Oraciones: '+str(len(listOraciones)))
print('Archivos: '+str(len(listArchivos)))
print('Palabras: '+str(len(palabrasEtiquetado)))
for i in range(len(palabrasEtiquetado)):
    id.append(i+1)
for val in range(len(palabrasEtiquetado)):
    dfPalEti.loc[val+1] = [palabrasEtiquetado[val],cantAnotadores[val]]
    dfNivelComp.loc[val+1] = [id[val],listArchivos[val],listOraciones[val],palabrasEtiquetado[val],nivelComplejidad[val]]
### id, text, sentence, token, complexity
###CEDUC_single_train --- NOMBRE DEL ARCHIVO
#CALCULAR FLEISS KAPPA
matrizFleiss = []
for ind in range(len(palabrasEtiquetado)):
    #if cantAnotadores[ind] > 1:
        #matrizFleiss.append([cantAnotadores[ind]-1,8-(cantAnotadores[ind]-1)])
    matrizFleiss.append([cantAnotadores[ind],9-cantAnotadores[ind]])
resultadoFleiss = fk(matrizFleiss,method='fleiss')
print(matrizFleiss)
print(resultadoFleiss)

dfValFleiss = pd.DataFrame()
dfValFleiss['Fleiss'] = None
dfValFleiss.loc['Fleiss'] = resultadoFleiss

writer = pd.ExcelWriter('resultados/CEDUC_single_train.xlsx')
dfPalEti.to_excel(writer,'Palabras')
dfValFleiss.to_excel(writer,'Kappa-Fleiss',index=False)
dfNivelComp.to_excel(writer,'Nivel de Complejidad',index=False)

writer.save()
writer.close()