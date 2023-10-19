# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

def mostrarGrafica(Opcion,listMet,listBlo):
    listaValores = []
    metricasGrafica = listMet[int(Opcion)-1]
    #print(metricasGrafica)
    for j in listBlo:
        listaValores.append(j[metricasGrafica])
    valoresunidos = []
    for i in listaValores:
        for j in i:
            valoresunidos.append(j)
    ax.boxplot(listaValores)
    ax.set_xticklabels(listBloque, fontdict={'fontsize': 10, 'fontweight': 'bold'})
    limite = max(valoresunidos) + 5
    minimo = min(valoresunidos)
    ax.set_xlabel("Bloques", fontdict={'fontsize': 13, 'fontweight': 'bold'})
    ax.set_ylabel("Valores", fontdict={'fontsize': 13, 'fontweight': 'bold'})
    ax.set_ylim([minimo, limite])
    ax.set_yticks(range(int(minimo), int(limite), 2))
    plt.title("Gráfica de la métrica "+metricasGrafica, fontdict={'fontsize': 16, 'fontweight': 'bold'})
    plt.show()
#OBTENER DATOS DE LAS MÈTRICAS
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 0)
dfMetricas = pd.DataFrame(datos)
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 1)
dfMetricasCompacto = pd.DataFrame(datos)
#print(df)
listBloque = []
for i in dfMetricas.index:
    bloque = dfMetricas['BLOQUE'][i]
    listBloque.append(bloque)
listBloque = list(set(listBloque))
listBloque = sorted(listBloque)
#print(listBloque)
listBloqueFinal = []
for blo in listBloque:
    rsTextos = dfMetricas.query('BLOQUE == "' + blo + '"')
    dfTextos = pd.DataFrame(rsTextos)
    #print(dfTextos)
    diccListTexto = dfTextos.to_dict('list')
    listBloqueFinal.append(diccListTexto)

#print(diccListTexto)
fig, ax = plt.subplots()
#print(bloques)
diccListMetrica = dfMetricasCompacto.to_dict('list')
listaMetricas = []
for metrica in diccListMetrica:
    if metrica != 'BLOQUE':
        #Metricas[metrica] = diccListMetrica[metrica]
        if len(listaMetricas) < 18:
            listaMetricas.append(metrica)
#print(Metricas)
#print(listaMetricas)
opcion = 0
print('Listado de las métricas para gráficos')
cont = 0
for met in listaMetricas:
    print("" + str(cont + 1) + ".- " + met)
    cont += 1
opcion = input("Elija la opción  graficar: ")

mostrarGrafica(opcion,listaMetricas,listBloqueFinal)