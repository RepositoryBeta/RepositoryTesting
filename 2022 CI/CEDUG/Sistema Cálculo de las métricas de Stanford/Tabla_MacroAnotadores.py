import pandas as pd
import os
import openpyxl

#OBTENCIÓN DE LOS DATOS DEL ARCHIVO DE MÉTRICAS STANFORD (TABLA GENERAL - TABLA COMPACTA DE BLOQUES)
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 0)
dfMetricas = pd.DataFrame(datos)
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 1, index_col=0)
dfBloques = pd.DataFrame(datos)
datosAnotado = pd.read_excel('resultados/Datos del Anotado.xlsx',engine="openpyxl",sheet_name= 1, index_col=0)
dfAnotado = pd.DataFrame(datosAnotado)
datosAnotado2 = pd.read_excel('resultados/Datos del Anotado.xlsx',engine="openpyxl",sheet_name= 0, index_col=0)
dfAnotado2 = pd.DataFrame(datosAnotado2)
cont = 0
#cantPalabras = []
#cantPalabrasRepetidas = []
listNivel = ['Basico','Intermedio', 'Avanzado']
cantPalabra = []
listCantPalCoincidencia = []
for i in dfMetricas.index:
    listCantPalAnotadas = []
    listCantidadPalRep = []
    diccCantPalAnotadas = {}
    diccCantPalCoincidencia = {}
    for nivel in listNivel:
        #print("Inicio: " +str(i))
        nombreArchivo = dfMetricas['Unnamed: 0'][i]
        bloque = dfMetricas['BLOQUE'][i]
        #print(dfAnotado)
        rsCedula = dfAnotado.query('Selección == "'+bloque+'" and Nivel == "'+nivel+'"')
        print(rsCedula)

        #rsCedula.groupby('Cedula')['Selección'].sum()
        cantPal = []
        palabraAnotada = []
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
        print(cantPal)
        listCantPalRep = [0,0,0]
        #OBTENER LAS PALABRAS SIN REPETICIONES
        listPalabraUnica = list(set(palabraAnotada))
        print(listPalabraUnica)
        diccCantPalAnotadas[nivel] = cantPal
        print(diccCantPalAnotadas)
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
        #print("\n\n")
        print(listCantPalRep)
        for cant in listCantPalRep:
            listCantidadPalRep.append(cant)
    print(listCantidadPalRep)
    for m in diccCantPalAnotadas:
        for n in diccCantPalAnotadas[m]:
            listCantPalAnotadas.append(n)
    listCantPalCoincidencia.append(listCantidadPalRep)
    cantPalabra.append(listCantPalAnotadas)
    print(cantPalabra)
    print(listCantPalCoincidencia)
#cantPalabrasRepetidas.append(listCantidadPalRep)
#print(cantPalabrasRepetidas)
#print(cantPalabra)
#if len(cantPalabra) < 10:
#    cantPalabras.append(cantPalabra)
dfColumnasAnotadores = pd.DataFrame(cantPalabra, columns= ['Anotador_B1', 'Anotador_B2', 'Anotador_B3',
                                                                'Anotador_I1', 'Anotador_I2', 'Anotador_I3',
                                                                'Anotador_A1', 'Anotador_A2', 'Anotador_A3'])

dfColumnasPalabrasAnotadores = pd.DataFrame(listCantPalCoincidencia, columns= ['B_1Anotador', 'B_2Anotadores', 'B_3Anotadores',
                                                                               'I_1Anotador', 'I_2Anotadores', 'I_3Anotadores',
                                                                               'A_1Anotador', 'A_2Anotadores', 'A_3Anotadores'])
#print(palabraAnotada)
#print(listPalabraUnica)


dfConcatenado = pd.concat([dfColumnasAnotadores,dfColumnasPalabrasAnotadores],axis=1)
dfConcatenadoGlobal = pd.concat([dfMetricas,dfConcatenado],axis=1)
rsBloque = dfConcatenadoGlobal.groupby(['BLOQUE'])[['Anotador_B1', 'Anotador_B2', 'Anotador_B3', 'Anotador_I1', 'Anotador_I2',
                                                    'Anotador_I3', 'Anotador_A1', 'Anotador_A2', 'Anotador_A3', 'B_1Anotador',
                                                    'B_2Anotadores', 'B_3Anotadores', 'I_1Anotador', 'I_2Anotadores',
                                                    'I_3Anotadores', 'A_1Anotador', 'A_2Anotadores', 'A_3Anotadores']].sum()
dfBloque = pd.DataFrame(rsBloque)
dfConcatenadoBloque = pd.concat([dfBloques,dfBloque],axis=1)
#dfBloque.drop(['BLOQUE'])
#dfBloque = dfBloque.drop(dfBloque.columns[[-1]], axis='columns')
print(dfBloque)
print(dfBloques)
#print(dfConcatenadoGlobal)
#print(dfColumnasAnotadores)
#print(dfColumnasPalabrasAnotadores)
print(dfConcatenadoBloque)
writer = pd.ExcelWriter('resultados/Metricas_Stanford.xlsx')
dfConcatenadoGlobal.to_excel(writer,'Tabla general',index=False)
dfConcatenadoBloque.to_excel(writer,'Tabla compacta bloques')
#dfSemestre.to_excel(writer,'Tabla compacta semestres',index=False)
#dfCarrera.to_excel(writer,'Tabla compacta carreras',index=False)

writer.save()
writer.close()