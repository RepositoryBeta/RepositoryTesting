# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

def mostrarGrafica(listOp,listMet,listBlo,Metricas):
    metricasGrafica = []
    listaValores = []
    for i in listOp:
        metricasGrafica.append(listMet[int(i)-1])
        for j in Metricas[listMet[int(i)-1]]:
            listaValores.append(j)
    #print(metricasGrafica)
    limite = max(listaValores) + 1000
    ax.plot(listBlo, Metricas[metricasGrafica[0]], label=metricasGrafica[0], marker = 'o')
    ax.plot(listBlo, Metricas[metricasGrafica[1]], label=metricasGrafica[1], marker = 'o')
    ax.plot(listBlo, Metricas[metricasGrafica[2]], label=metricasGrafica[2], marker = 'o')
    ax.set_xlabel("Bloques", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
    ax.set_ylabel("Valores", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
    #ax.set_ylim([0, limite])
    ax.set_yticks(range(0, int(limite), 500))
    ax.legend(loc=0)
    plt.show()

#OBTENER DATOS DE LAS MÈTRICAS
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 1)
dfMetricas = pd.DataFrame(datos)
#print(df)
diccListBloque = dfMetricas.to_dict('list')
#print(d_list)
fig, ax = plt.subplots()
bloques = diccListBloque['BLOQUE']
#print(bloques)
Metricas = {}
listaMetricas = []
for metrica in diccListBloque:
    if metrica != 'BLOQUE':
        Metricas[metrica] = diccListBloque[metrica]
        if len(listaMetricas) < 18:
            listaMetricas.append(metrica)
#print(Metricas)
#print(listaMetricas)
cantidad = 3
opcion = 0
listaOpciones = []

print('Listado de las métricas para gráficos')
cont = 0
for met in listaMetricas:
    print("" + str(cont + 1) + ".- " + met)
    cont += 1
opcion = input("Elija su opción número " + str(cantidad) + ": ")
cantidad-=1
listaOpciones.append(opcion)

while cantidad!=0 and opcion!=0:
    print('Listado de las métricas para gráficos')
    cont = 0
    for met in listaMetricas:
        print(""+str(cont+1)+".- " +met)
        cont+=1
    opcion = input("Elija la opción " +str(cantidad) +": ")
    cantidad -= 1
    listaOpciones.append(opcion)
#print(listaOpciones)

mostrarGrafica(listaOpciones,listaMetricas,bloques, Metricas)
