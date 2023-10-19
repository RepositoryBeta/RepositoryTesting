import re
import pandas as pd
# LEYENDO EL CORPUS
xls = pd.ExcelFile('corpus\corpus.xlsx')
sheets = []
sheets = xls.sheet_names
writer = pd.ExcelWriter('corpus\diccionario.xlsx', engine='xlsxwriter')
for hojas in sheets:
    listaPalabras = []
    frecuenciaPalab = []
    palabra_repetidas = []
    tamanio = []
    count = 0
    words = []
    df = pd.read_excel('corpus\corpus.xlsx', sheet_name=hojas)
    for item in df.values.tolist():
        data = re.sub(r"[^\w\s]", '', str(item))
        if data != "":
            listaPalabras.append(data)
    print("=========================================")
    print("WORDS DE PARTICION  "+str(hojas))
    print("=========================================")
    for w in listaPalabras:
        if w not in palabra_repetidas:
            palabra_repetidas.append(w)

    for w in palabra_repetidas:
        count = count+1
        frecuenciaPalab.append(listaPalabras.count(w))
        tamanio.append(len(w))
        words.append(w)
        print(w, '\t\t', listaPalabras.count(w), '\t\t', len(w))

    data = {'Token': words,
            'Freq': frecuenciaPalab,
            'Lenght': tamanio}
    da = pd.DataFrame(data, columns=['Token', 'Freq', 'Lenght'])
    #da.to_csv('corpus\diccionaro_datos.csv', index=0)
    da.to_excel(writer, sheet_name=str(hojas))
    

writer.save()
writer.close()

#conversion de excel a csv
#read_file = pd.read_excel ("corpus\diccionario.xlsx") 
#read_file.to_csv ("corpus\diccionaro_datos.csv",  
#                  index = None, 
#                  header=True) 
#df = pd.DataFrame(pd.read_csv("corpus\diccionaro_datos.csv")) 
#print (df)
