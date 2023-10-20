import codecs
import os
import pandas as pd
from pandas import ExcelWriter
import openpyxl
import socket
import math


def filtrar (texto_split, tipo):
    # RECIBIR EL TEXTO COMO VIENE EN LOS ARCHIVOS
    texto = []
    casos = ["\'", "\"", "!", "¡", "¿", "?", "(", ")", "{", "}", "[", "]", "<", ">", "|", "#", "$", "%", ":", ";", ",",
             "+", "*", "=", "-", "/", "\\", "‘", "^", "’", "~", ".", "&", "≥", "”", "—", '°', '²', '–', '×', '′']
    casos2 = ['′', '0', '2', '–', '×', '4', '°', '²', '3', '7', '6', '8', '9', '1', '5', '≥', "”", "—", "\'", "\"", "!",
              "¡", "¿", "?", "(", ")", "{", "}", "[", "]", "<", ">", "|", "#", "$", "%", ":", ";", ",", "+", "*", "=", "-", "/", "\\", "‘", "^", "’", "~", ".", "&","_",'_']
    index = 0
    ultimo = len(texto_split) - 1

    if tipo == "T":
        for w in texto_split:
            if (index == 0):
                longitud = len(w)
                texto_split[0] = w[longitud - 5:longitud]
                index += 1
            else:
                if (index == ultimo):
                    longitud = len(w)
                    for i in range(longitud):
                        if w[i] == ".":
                            texto_split[ultimo] = w[:i + 1]
                else:
                    index += 1

    # FILTRO DE CARACTERES ESPECIALES
    ubicacion = []
    oracion = []
    palabrasAnotado = []
    for w in texto_split:
        #print(w)
        longitud = len(w)
        if longitud > 1:
            for i in range(longitud):
                if w[i] in casos:
                    ubicacion.append(i)
            if len(ubicacion) > 0:
                contador = 0
                if ubicacion[0] == 0:
                    if len(ubicacion) > 1:
                        if ubicacion[len(ubicacion) - 1] + 1 == longitud:
                            for u in ubicacion:
                                if (contador < len(ubicacion) - 1):
                                    oracion.append(w[u + 1:ubicacion[contador + 1]].strip())
                                    contador += 1
                        else:
                            for u in ubicacion:
                                if (contador < len(ubicacion) - 1):
                                    oracion.append(w[u + 1:ubicacion[contador + 1]].strip())
                                    contador += 1
                            oracion.append(w[ubicacion[(len(ubicacion) - 1)] + 1:].strip())
                    else:
                        oracion.append(w[ubicacion[0] + 1:].strip())
                else:
                    oracion.append(w[0:ubicacion[0]].strip())
                    if len(ubicacion) > 1:
                        if ubicacion[len(ubicacion) - 1] + 1 == longitud:
                            for u in ubicacion:
                                if contador < len(ubicacion) - 1:
                                    oracion.append(w[u + 1:ubicacion[contador + 1]].strip())
                                    contador += 1
                        else:
                            for u in ubicacion:
                                if (contador < len(ubicacion) - 1):
                                    oracion.append(w[u + 1:ubicacion[contador + 1]].strip())
                                    contador += 1
                            oracion.append(w[ubicacion[(len(ubicacion) - 1)] + 1:].strip())
                    else:
                        if ubicacion[0] + 1 == longitud:
                            pass
                        else:
                            oracion.append(w[ubicacion[0] + 1:].strip())
            else:
                oracion.append(w)
            ubicacion = []
        else:
            if w in casos2:
                #print(w)
                pass
            else:
                if tipo=="T":
                    oracion.append(w.strip())
                else:
                    oracion.append(w)
        if tipo == "A":
            palabrasAnotado.append(oracion)
            oracion = []
    if tipo == "T":
        oracionesConFiltro = oracion
        #print(oracionesConFiltro)
        oracionesSinCarEsp = oracionesConFiltro
        # FILTRO DE CADENAS VACÍAS
        oracion = []
        for w in oracionesSinCarEsp:
            if len(w) > 1:
                oracion.append(w)
            elif len(w) == 1:
                if w in casos2:
                    pass
                else:
                    oracion.append(w)
            else:
                pass
        oracionesConFiltro = oracion
        oracionesSinCarEsp = oracionesConFiltro

        # FILTRO DE NÚMEROS Y DIRECCIONES IP
        oracion = []
        for w in oracionesSinCarEsp:
            num = None
            for conv in (int, float, complex):
                try:
                    num = conv(w)
                    break
                except ValueError:
                    pass
            if num is None:
                try:
                    socket.inet_aton(w)
                except socket.error:
                    oracion.append(w)
        oracionesSinNum = oracion

        return oracionesSinNum
    else:
        oracionesConFiltro = []
        # FILTRO DE CADENAS VACÍAS
        oracion = []
        for palabraC in palabrasAnotado:
            for w in palabraC:
                if len(w) > 0 :
                    oracion.append(w)
                else:
                    pass
            oracionesConFiltro.append(oracion)
            oracion = []
        oracionesSinCarEsp = oracionesConFiltro

        # FILTRO DE NÚMEROS Y DIRECCIONES IP
        oracion = []
        oracionesSinNum = []
        for palabraC in oracionesSinCarEsp:
            for w in palabraC:
                w_split = w.split()
                #print(w_split)
                for w_s in w_split:
                    #print(w_s)
                    num = None
                    for conv in (int, float, complex):
                        try:
                            num = conv(w_s)
                            break
                        except ValueError:
                            pass
                    if num is None:
                        try:
                            socket.inet_aton(w_s)
                        except socket.error:
                            oracion.append(w_s)
            #print(' '.join(oracion))
            oracionesSinNum.append(' '.join(oracion))
            oracion = []

        return oracionesSinNum


#OBTENER LISTADO DE PALABRAS DE EXCEL DE ANOTADO
#PALABRAS DEL ANOTADO

datosAnotado = pd.read_excel('resultados/Datos del Anotado.xlsx',engine="openpyxl",sheet_name= 0)
dfAnotado = pd.DataFrame(datosAnotado)
dfAnotado = dfAnotado.dropna(subset=["Posicion_en_el_texto"])
listaPalabraAnotad = []
for i in dfAnotado.index:
    pal = ""
    pal +=str(dfAnotado['Palabra'][i])
    palabra = pal.lower()
    if palabra == 'nan':
        palabra ="null"
    listaPalabraAnotad.append(palabra)

listaPalabraAnotado = filtrar(listaPalabraAnotad,"A")
listaPalFinal = list(set(listaPalabraAnotado))
listaPalabraSimple = []
listaMulti2 = []
listaMulti3 = []
listaFrase = []
for pal in listaPalFinal:
    if len(pal.split()) == 1: listaPalabraSimple.append(pal)
    elif len(pal.split()) == 2: listaMulti2.append(pal)
    elif len(pal.split()) == 3: listaMulti3.append(pal)
    else: listaFrase.append(pal)

print(len(listaPalFinal))

dfSimple = pd.DataFrame({'Palabra': [w for w in listaPalabraSimple]})
dfSimple = dfSimple[['Palabra']]
dfMulti2 = pd.DataFrame({'Palabra': [w for w in listaMulti2]})
dfMulti2 = dfMulti2[['Palabra']]
dfMulti3 = pd.DataFrame({'Palabra': [w for w in listaMulti3]})
dfMulti3 = dfMulti3[['Palabra']]
dfFrase = pd.DataFrame({'Palabra': [w for w in listaFrase]})
dfFrase = dfFrase[['Palabra']]

ruta = './CREA_total.txt'

f = open(ruta)
lines = f.readlines()
f.close()
crea = {}
for l in lines[1:]:  # those words not in the 1000 most frequent words in CREA are low frequency words
    data = l.strip().split()
    if (float(data[2].replace(',', '')) >= 1000):
        crea[data[1]] = float(data[2].replace(',', ''))


#BLOQUE 3
raiz = 'textos_analizar'
indir = raiz
data = []
carrera = os.listdir(indir)
df = []
cont = 0
listaPalabrasTexto = []
for c in carrera :
    indir = indir +'/' +c
    semestre = os.listdir(indir)
    for s in semestre:
        indir = indir + '/' + s
        materia = os.listdir(indir)
        cont_mat = 0
        if os.path.exists(indir):
            ruta = ""
            for root, dirs, filenames in os.walk(indir):
                filenames.sort()
                for index, f in enumerate(filenames):
                    if(index == 0):
                        m = materia[cont_mat]
                        cont_mat+=1
                    root = root.replace("\\", '/')
                    name = f
                    try:
                        file = codecs.open(root + '/' + f, 'rb', encoding='utf-8')
                        text = file.read()
                    except UnicodeDecodeError:
                        file = codecs.open(root + '/' + f, 'rb', encoding='latin-1')
                        text = file.read()

                    #print("Carrera: " +c +"\n \tSemestre: " +s +"\n \t\tMateria: " +m)
                    print("\t\t\tProcesando texto: " +f)

                    #text_processed = filtrar(text.split(),"T")
                    #print(text_processed)
                    #print("\nTexto separado en oraciones")
                    #print(text_processed)
                    #print("\n\n\n")
                    #for sentence in text_processed:
                    #    for w in sentence:
                    #        listaPalabrasTexto.append(w.lower())
                    #print(listaPalabrasTexto)
                    texto_split = text.split()
                    index = 0
                    ultimo = len(texto_split) - 1

#                    if tipo == "T":
                    for w in texto_split:
                        if (index == 0):
                            longitud = len(w)
                            texto_split[0] = w[longitud - 5:longitud]
                            index += 1
                        else:
                            if (index == ultimo):
                                longitud = len(w)
                                for i in range(longitud):
                                    if w[i] == ".":
                                        texto_split[ultimo] = w[:i + 1]
                            else:
                                index += 1

                    for w in texto_split:
                        listaPalabrasTexto.append(w)
                    file.close()
            indir = raiz + '/' + c
        else:
            print("La ruta especificada no existe")
    indir = raiz
#listaPalabrasTexto = list(set(listaPalabrasTexto))
#print(listaPalabrasTexto)


dfListaPTexto = pd.DataFrame({'Palabra': [w for w in listaPalabrasTexto]})
dfListaPTexto = dfListaPTexto[['Palabra']]

writer = ExcelWriter('resultados/Palabras Separadas Texto.xlsx')
dfListaPTexto.to_excel(writer, 'Palabras de texto', index=False)
writer.save()

datosTexto = pd.read_excel('resultados/Palabras Separadas Texto.xlsx',engine="openpyxl",sheet_name= 0)
dfTexto = pd.DataFrame(datosTexto)
#dfTexto = dfAnotado.dropna(subset=["Posicion_en_el_texto"])
#print(len(dfTexto))
listaPalabraText = []
for i in dfTexto.index:
    pal = ""
    pal +=str(dfTexto['Palabra'][i])
    palabra = pal.lower()
    if palabra == 'nan':
        palabra ="null"
    listaPalabraText.append(palabra)
#print(len(listaPalabraText))
#print(listaPalabraText)
text_processed = filtrar(listaPalabraText,"T")
text_processed = list(set(text_processed))
#print(text_processed)
dfListaPTexto = pd.DataFrame({'Palabra': [w for w in text_processed]})
dfListaPTexto = dfListaPTexto[['Palabra']]

writer = ExcelWriter('resultados/Palabras Separadas Texto.xlsx')
dfListaPTexto.to_excel(writer, 'Palabras de texto', index=False)
dfSimple.to_excel(writer, 'Palabras Anotado Simple', index=False)
dfMulti2.to_excel(writer, 'Multipalabra de 2', index=False)
dfMulti3.to_excel(writer, 'Multipalabra de 3', index=False)
dfFrase.to_excel(writer, 'Frases', index=False)
writer.save()