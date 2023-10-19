# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
#OBTENER DATOS DE LAS MÈTRICAS
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 1)
dfMetricasCompacto = pd.DataFrame(datos)
#print(dfMetricasCompacto)
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",sheet_name= 0, index_col=0)
dfMetricas = pd.DataFrame(datos)
#print(dfMetricas)
listColumnas = [['B_1Anotador', 'B_2Anotadores', 'B_3Anotadores'],
                ['I_1Anotador', 'I_2Anotadores', 'I_3Anotadores'],
                ['A_1Anotador', 'A_2Anotadores', 'A_3Anotadores']]
listColExcel = ['B_1Anotador', 'B_2Anotadores', 'B_3Anotadores',
                'I_1Anotador', 'I_2Anotadores', 'I_3Anotadores',
                'A_1Anotador', 'A_2Anotadores', 'A_3Anotadores']
listaCondensados = []
for i in dfMetricasCompacto.index:
    bloque = dfMetricasCompacto['BLOQUE'][i]
    valores = []
    for j in range(len(listColumnas)):
        for k in listColumnas[j]:
            valores.append(dfMetricasCompacto[k][i])
    listaCondensados.append(valores)
#print(listaCondensados)
valoresCondensados = [0,0,0,0,0,0,0,0,0]
for j in range(len(listaCondensados)):
    for k in range(len(listaCondensados[j])):
        #print(listaCondensados[j][k])
        valoresCondensados[k]+=listaCondensados[j][k]
dfCondensado = pd.DataFrame()
for l in range(len(listColExcel)):
    dfCondensado[listColExcel[l]] = None
dfCondensado.loc['Bloques'] = valoresCondensados
#print(dfCondensado)

# CÁLCULO DE ÍNDICE KAPPA COHEN
temp = []
list3 = []
for i in range(len(valoresCondensados)):
    if i == 2 or i == 5 or i == 8:
        temp.append(valoresCondensados[i])
        list3.append(temp)
        temp = []
    else:
        temp.append(valoresCondensados[i])
print(list3)
po = 0
peCohen = 0
kc = 0
diccKappaCohen = {}
n2ij = 0
n2ij_n = 0
pi = 0
promPi = 0
nSujetos = 1
pj = 0
peFleiss = 0
kf = 0
diccKappaFleiss = {}
nivel = ""
for i in range(len(list3)):
    #VARIABLES DE KAPPA FLEISS
    n=sum(list3[i])
    totj = n
    if i == 0:
        nivel = 'Basico'
    elif i == 1:
        nivel = 'Intermedio'
    else:
        nivel = 'Avanzado'
    for j in range(len(list3[i])):
        #BLOQUE IF - ELSE PARA KAPPA COHEN
        if j == 0:
            peCohen = list3[i][j]
        else:
            po+=list3[i][j]
        #BLOQUE PARA KAPPA FLEISS
        n2ij+=(list3[i][j]**2)
        pj = (list3[i][j]/totj)
        peFleiss+=(pj**2)
    n2ij_n = n2ij-n
    pi = (n2ij_n)/(n*(n-1))
    promPi = pi/nSujetos
    #print(po)
    #print(peCohen)
#VALOR FINAL KAPPA COHEN
    kc = (po-peCohen)/(1-peCohen)
    diccKappaCohen[nivel] = kc
    #print('Kappa Cohen: '+str(kc))
#VALOR FINAL KAPPA FLEISS
    #print(n2ij)
    #print(n)
    #print(n2ij_n)
    #print(pi)
    #print(promPi)
    #print(peFleiss)
    kf = (promPi-peFleiss)/(1-peFleiss)
    diccKappaFleiss[nivel] = kf
    #print('Kappa Fleiss: '+str(kf))
    po = 0
    n2ij = 0
    n2ij_n = 0
    pi=0
    promPi = 0
    peFleiss = 0
print('Kappa Cohen:')
print(diccKappaCohen)
print('Kappa Fleiss:')
print(diccKappaFleiss)

dfCohenFleiss = pd.DataFrame()
valoresCohen = []
valoresFleiss = []
for p in diccKappaCohen:
    dfCohenFleiss[p] = None
    valoresCohen.append(diccKappaCohen[p])
for q in diccKappaFleiss:
    valoresFleiss.append(diccKappaFleiss[q])
dfCohenFleiss.loc['Cohen'] = valoresCohen
dfCohenFleiss.loc['Fleiss'] = valoresFleiss
print(dfCohenFleiss)

writer = pd.ExcelWriter('resultados/Metricas_Stanford.xlsx')
dfMetricas.to_excel(writer,'Tabla general')
dfMetricasCompacto.to_excel(writer,'Tabla compacta bloques',index=False)
dfCondensado.to_excel(writer,'Condensado')
dfCohenFleiss.to_excel(writer,'Cohen-Fleiss')
writer.save()
writer.close()

#GRÁFICA DE LOS VALORES CONDENSADOS
fig = plt.figure(figsize=(12,7))
colores = ['blue','green','orange']
valoresGraficos = []
for m in range(len(list3)):
    if m == 0:
        nivel = 'Basico'
    elif m == 1:
        nivel = 'Intermedio'
    else:
        nivel = 'Avanzado'
    for n in range(len(list3[m])):
        valoresGraficos.append(list3[m][n])
    fig.tight_layout()
    x = ['1 Anotador',' 2 Anotadores','3 Anotadores']
    limite = max(valoresGraficos) + 120
    ax = plt.subplot(1,3,m+1)
    ax.bar(x,valoresGraficos, color = colores[m])
    for o in range(len(valoresGraficos)):
        plt.text(o,valoresGraficos[o]+3,str(valoresGraficos[o]),ha='center',fontweight= 'bold')
    ax.set_xlabel('Coincidencias', fontdict={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_ylabel('Valores', fontdict={'fontsize': 11, 'fontweight': 'bold'})
    ax.set_ylim([0, limite])
    ax.set_yticks(range(0, int(limite), 100))
    ax.set_title("Gráfico del nivel "+nivel, fontdict={'fontsize': 13, 'fontweight': 'bold'})
    valoresGraficos = []
plt.show()
