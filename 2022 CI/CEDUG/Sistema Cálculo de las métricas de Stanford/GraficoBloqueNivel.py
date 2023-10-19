# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

#OBTENER DATOS DE LAS MÈTRICAS
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 1)
dfMetricasCompacto = pd.DataFrame(datos)
#print(dfMetricasCompacto)
listColumnas = [['B_1Anotador', 'B_2Anotadores', 'B_3Anotadores'],
                ['I_1Anotador', 'I_2Anotadores', 'I_3Anotadores'],
                ['A_1Anotador', 'A_2Anotadores', 'A_3Anotadores']]

fig = plt.figure(figsize=(12,7))
colores = ['blue','green','orange']
contadorGrafico = 0
for i in dfMetricasCompacto.index:
    bloque = dfMetricasCompacto['BLOQUE'][i]
    contador = 0
    for j in range(len(listColumnas)):
        valores = []
        contador += 1
        nivel = ""
        for k in listColumnas[j]:
            valores.append(dfMetricasCompacto[k][i])
        contadorGrafico+=1
        #print(valores)
        if contador == 1:
            nivel = 'Basico'
        elif contador == 2:
            nivel = 'Intermedio'
        else:
            nivel = 'Avanzado'
         #print(nivel)
        fig.tight_layout()
        x = ['1 Anotador',' 2 Anotadores','3 Anotadores']
        limite = max(valores) + 120
        ax = plt.subplot(3,3,contadorGrafico)
        ax.bar(x,valores, color = colores[i])
        for o in range(len(valores)):
            plt.text(o,valores[o]+3,str(valores[o]),ha='center',fontweight= 'bold')
        ax.set_xlabel('Coincidencias', fontdict={'fontsize': 11, 'fontweight': 'bold'})
        ax.set_ylabel('Valores', fontdict={'fontsize': 11, 'fontweight': 'bold'})
        ax.set_title(""+bloque+" - "+nivel, fontdict={'fontsize': 13, 'fontweight': 'bold'})
        ax.set_ylim([0, limite])
        ax.set_yticks(range(0, int(limite), 100))
plt.show()