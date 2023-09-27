import nltk
import codecs
import TextComplexityStanford
import pandas as pd
import os
import spacy

#BLOQUE 2
textComplexityStanford = TextComplexityStanford.TextComplexityStanford()
nltk.download('stopwords')

#BLOQUE 3
raiz = 'textos_analizar/Entidades'
indir = raiz
data = []
carrera = os.listdir(indir)
df = []
cont = 0
for c in carrera :
    indir = indir +'/' +c
    seleccion = os.listdir(indir)
    cont_sec = 0
    if os.path.exists(indir):
        ruta = ""
        for root, dirs, filenames in os.walk(indir):
            filenames.sort()
            for index, f in enumerate(filenames):
                contCconj = 0
                contSconj = 0
                contPropn = 0
                contPron = 0
                contNoun = 0
                contVerb = 0
                contAdp = 0
                contAux = 0
                contDet = 0
                contAdv = 0
                contAdj = 0
                if(index == 0):
                    p = seleccion[cont_sec]
                    cont_sec+=1
                root = root.replace("\\", '/')
                name = f
                print(root + '/' + f)
                try:
                    file = codecs.open(root + '/' + f, 'rb', encoding='utf-8')
                    text = file.read()
                except UnicodeDecodeError:
                    file = codecs.open(root + '/' + f, 'rb', encoding='latin-1')
                    text = file.read()
                print("Carrera: " +c)
                print("\t\t\tProcesando texto: " +f +"---" + text)
                oraciones = textComplexityStanford.ProcesarTexto(text)
                print("Texto filtrado:")
                print(oraciones)
                texto = ""
                for sentence in oraciones:
                    for w in sentence:
                        texto += w + " "

                chapters = texto.split("CHAPTER")[0:]
                #print(chapters)
                chapter1 = chapters[0]
                #print(chapter1)
                nlp = spacy.load("es_core_news_sm")
                doc = nlp(chapter1)
                sentences = list(doc.sents)

                for i in range (len(sentences)):
                    sentence = (sentences[i])
                    for token in sentence:
                        if(token.pos_ =="NUM"):
                            continue
                        else:
                            if(token.pos_ == "CCONJ"): contCconj+=1
                            elif(token.pos_ == "SCONJ"): contSconj+=1
                            elif(token.pos_ == "PROPN"): contPropn+=1
                            elif (token.pos_ == "PRON"): contPron+=1
                            elif (token.pos_ == "NOUN"): contNoun+=1
                            elif (token.pos_ == "VERB"): contVerb+=1
                            elif (token.pos_ == "ADP"): contAdp+=1
                            elif (token.pos_ == "AUX"): contAux+=1
                            elif (token.pos_ == "DET"): contDet+=1
                            elif (token.pos_ == "ADV"): contAdv+=1
                            elif (token.pos_ == "ADJ"): contAdj+=1

                #text_processed = textComplexityStanford.textProcessing(new_text)
                #print("\nTexto separado en oraciones")
                #print(text_processed)

                lexcomplexity = textComplexityStanford.lexicalComplexity()
                ssreadability = textComplexityStanford.ssReadability()
                sencomplexity = textComplexityStanford.sentenceComplexity()
                autoreadability = textComplexityStanford.autoReadability()
                pmarks = textComplexityStanford.punctuationMarks()
                mltd = textComplexityStanford.metricaMtld()
                if (index == 0 and cont == 0):
                    df = pd.DataFrame({name: [autoreadability[0], ssreadability[0], lexcomplexity[2], lexcomplexity[1],
                                            lexcomplexity[0], ssreadability[1], lexcomplexity[3], sencomplexity[0],
                                            lexcomplexity[4], lexcomplexity[5], lexcomplexity[6], ssreadability[2],
                                            sencomplexity[1], sencomplexity[2], sencomplexity[3], autoreadability[1],
                                            pmarks, mltd, c, contCconj, contSconj, contPropn, contPron, contNoun,
                                            contVerb, contAdp, contAux, contDet, contAdv, contAdj]},
                                    index='N_charac N_w N_dcw N_cw N_lfw N_rw N_s N_cs LDI ILFW LC SSR ASL CS SCI ARI PM MTLD BLOQUE '
                                            'CCONJ SCONJ PROPN PRON NOUN VERB ADP AUX DET ADV ADJ'.split())
                    cont+=1
                else:
                    df[name] = ([autoreadability[0], ssreadability[0], lexcomplexity[2], lexcomplexity[1], lexcomplexity[0],
                                ssreadability[1], lexcomplexity[3], sencomplexity[0], lexcomplexity[4], lexcomplexity[5],
                                lexcomplexity[6], ssreadability[2], sencomplexity[1], sencomplexity[2], sencomplexity[3],
                                autoreadability[1], pmarks, mltd, c, contCconj, contSconj, contPropn, contPron, contNoun,
                                            contVerb, contAdp, contAux, contDet, contAdv, contAdj])
                # print(df)
                file.close()
        indir = raiz
    else:
        print("La ruta especificada no existe")
#indir = raiz

new_df = df.transpose()
print("\n La tabla final es:\n ")
print(new_df)
new_df.to_excel('resultados/Metricas_Stanford.xlsx', sheet_name='Hoja 3')
print("excel 1")
datos = pd.read_excel('resultados/Metricas_Stanford.xlsx',engine="openpyxl")
rs = pd.DataFrame(datos)
"""
#TABLA COMPACTA POR MATERIAS
print("Tabla compacta por selecciones")
rsSeleccion = rs.groupby(['SELECCION'])[['N_charac', 'N_w', 'N_dcw', 'N_cw', 'N_lfw', 'N_rw', 'N_s', 'N_cs', 'LDI',
                                     'ILFW', 'LC', 'SSR', 'ASL', 'CS', 'SCI', 'ARI', 'PM', 'MTLD', 'CCONJ', 'SCONJ',
                                     'PROPN', 'PRON', 'NOUN', 'VERB', 'ADP', 'AUX', 'DET', 'ADV', 'ADJ']].sum()
dfSeleccion = pd.DataFrame(rsSeleccion)
print(dfSeleccion)

#TABLA COMPACTA POR SEMESTRES
print("Tabla compacta por niveles")
rsNivel = rs.groupby(['NIVEL'])[['N_charac', 'N_w', 'N_dcw', 'N_cw', 'N_lfw', 'N_rw', 'N_s', 'N_cs', 'LDI',
                                     'ILFW', 'LC', 'SSR', 'ASL', 'CS', 'SCI', 'ARI', 'PM', 'MTLD', 'CCONJ', 'SCONJ',
                                     'PROPN', 'PRON', 'NOUN', 'VERB', 'ADP', 'AUX', 'DET', 'ADV', 'ADJ']].sum()
dfNivel = pd.DataFrame(rsNivel)
print(dfNivel)

#TABLA COMPACTA POR SEMESTRES
print("Tabla compacta por semestres")
rsSemestre = rs.groupby(['SEMESTRE'])[['N_charac', 'N_w', 'N_dcw', 'N_cw', 'N_lfw', 'N_rw', 'N_s', 'N_cs', 'LDI',
                                     'ILFW', 'LC', 'SSR', 'ASL', 'CS', 'SCI', 'ARI', 'PM', 'MTLD', 'CCONJ', 'SCONJ',
                                     'PROPN', 'PRON', 'NOUN', 'VERB', 'ADP', 'AUX', 'DET', 'ADV', 'ADJ']].sum()
dfSemestre = pd.DataFrame(rsSemestre)
print(dfSemestre)

#TABLA COMPACTA POR CARRERAS
print("Tabla compacta por carreras")
rsCarrera = rs.groupby(['CARRERA'])[['N_charac', 'N_w', 'N_dcw', 'N_cw', 'N_lfw', 'N_rw', 'N_s', 'N_cs', 'LDI',
                                     'ILFW', 'LC', 'SSR', 'ASL', 'CS', 'SCI', 'ARI', 'PM', 'MTLD', 'CCONJ', 'SCONJ',
                                     'PROPN', 'PRON', 'NOUN', 'VERB', 'ADP', 'AUX', 'DET', 'ADV', 'ADJ']].sum()
dfCarrera = pd.DataFrame(rsCarrera)
print(dfCarrera)
"""
# writer = pd.ExcelWriter('resultados/Metricas_Stanford.xlsx')
# new_df.to_excel(writer,'Tabla general')
# #dfSeleccion.to_excel(writer,'Tabla compacta selecciones')
# #dfNivel.to_excel(writer,'Tabla compacta niveles')
# #dfSemestre.to_excel(writer,'Tabla compacta semestres')
# #dfCarrera.to_excel(writer,'Tabla compacta carreras')
# writer._save()
# writer.close()