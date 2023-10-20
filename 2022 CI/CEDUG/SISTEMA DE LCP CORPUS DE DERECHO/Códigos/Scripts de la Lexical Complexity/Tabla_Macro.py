import pandas as pd
import os
import openpyxl


datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 0)
dfMetricas = pd.DataFrame(datos)
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 1)
dfMaterias = pd.DataFrame(datos)
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 2)
dfSemestre = pd.DataFrame(datos)
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 3)
dfCarrera = pd.DataFrame(datos)
datosAnotado = pd.read_excel('resultados/Datos del Anotado.xlsx',engine="openpyxl",sheet_name= 1)
dfAnotado = pd.DataFrame(datosAnotado)
datosAnotado2 = pd.read_excel('resultados/Datos del Anotado.xlsx',engine="openpyxl",sheet_name= 0)
dfAnotado2 = pd.DataFrame(datosAnotado2)
cont = 0
cantPalabras = []
cantPalabrasRepetidas = []
for i in dfMetricas.index:
    nombreArchivo = dfMetricas['Unnamed: 0'][i]
    semestre = dfMetricas['SEMESTRE'][i]
    rsCedula = dfAnotado.query('Nivel == '+str(semestre))
    rsCedula.groupby('Cedula')['Nivel'].sum()
    cantPalabra = []
    palabraAnotada = []

    print("Analizando texto: " + nombreArchivo + "\n")

    #OBTENER FILTRADO POR CEDULA DE ANOTADORES Y EL TEXTO
    for k in rsCedula.index:
        #print("Anotador: " +str(rsCedula['Cedula'][k]))
        rsAnotado = dfAnotado2[dfAnotado2.Nombre_archivo.isin([nombreArchivo])&dfAnotado2.Cedula.isin([rsCedula['Cedula'][k]])]

        #OBTENER TODAS LAS PALABRAS ANOTADAS EN EL TEXTO POR TODOS LOS ANOTADORES
        #print("Palabras anotadas: ")
        for j in rsAnotado.index:
            #print(rsAnotado['Palabra'][j])
            palabraAnotada.append(rsAnotado['Palabra'][j])

        #LISTA QUE CONTIENE LA CANTIDAD DE PALABRAS ANOTADAS EN EL TEXTO POR LOS ANOTADORES.
        cantPalabra.append(len(rsAnotado))
        #print("Cantidad de palabras anotadas: "+str(len(rsAnotado)))
        #print("\n")

    listCantidadPalRep = [0,0,0,0]
    #OBTENER LAS PALABRAS SIN REPETICIONES
    listPalabraUnica = list(set(palabraAnotada))

    #RECORRIDO DE LA LISTA DE LA PALABRAS ÚNICAS
    for listaPU in listPalabraUnica:
        repet = 0

        #RECORRIDO DE LA LISTA DE LAS PALABRAS ANOTADAS EN EL TEXTO
        for listaPA in palabraAnotada:
            #print(listaPU)
            if(listaPU == listaPA):
                repet +=1
        if(repet > 1):
            #print("La palabra " +listaPU +" tiene " +str(repet) +" Anotador(es).")
            listCantidadPalRep[repet - 2] += 1
    #print("\n\n")

    #print(listCantidadPalRep)
    cantPalabras.append(cantPalabra)
    cantPalabrasRepetidas.append(listCantidadPalRep)
    dfColumnasAnotadores = pd.DataFrame(cantPalabras, columns= ['Anotador_1', 'Anotador_2', 'Anotador_3', 'Anotador_4', 'Anotador_5'])
    dfColumnasPalabrasAnotadores = pd.DataFrame(cantPalabrasRepetidas, columns= ['2 Anotadores', '3 Anotadores', '4 Anotadores', '5 Anotadores'])
    #print(palabraAnotada)
    #print(listPalabraUnica)


dfConcatenado = pd.concat([dfColumnasAnotadores,dfColumnasPalabrasAnotadores],axis=1)
dfConcatenadoGlobal = pd.concat([dfMetricas,dfConcatenado],axis=1)
#print(dfConcatenadoGlobal)
#print(dfColumnasAnotadores)
#print(dfColumnasPalabrasAnotadores)

writer = pd.ExcelWriter('resultados/Metricas_Stanford.xlsx')
dfConcatenadoGlobal.to_excel(writer,'Tabla general',index=False)
dfMaterias.to_excel(writer,'Tabla compacta materias',index=False)
dfSemestre.to_excel(writer,'Tabla compacta semestres',index=False)
dfCarrera.to_excel(writer,'Tabla compacta carreras',index=False)
writer.save()
writer.close()











