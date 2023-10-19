import pandas as pd

datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl",index_col= 0)
rs = pd.DataFrame(datos)

#TABLA COMPACTA POR BLOQUES
print("Tabla compacta por bloques")
rsBloque = rs.groupby(['BLOQUE'])[['N_charac', 'N_w', 'N_dcw', 'N_cw', 'N_lfw', 'N_rw', 'N_s', 'N_cs', 'LDI',
                                     'ILFW', 'LC', 'SSR', 'ASL', 'CS', 'SCI', 'ARI', 'PM', 'MTLD', 'CCONJ', 'SCONJ',
                                     'PROPN', 'PRON', 'NOUN', 'VERB', 'ADP', 'AUX', 'DET', 'ADV', 'ADJ']].sum()
dfBloque = pd.DataFrame(rsBloque)
print(dfBloque)

#CREACIÓN DEL EXCEL COMPACTO
writer = pd.ExcelWriter('resultados/Metricas_Stanford.xlsx')
rs.to_excel(writer,'Tabla general')
dfBloque.to_excel(writer,'Tabla compacta bloques')
writer.save()
writer.close()