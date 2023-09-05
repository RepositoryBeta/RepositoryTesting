from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch
import pandas as pd
from numpy import average
tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
model = AutoModelForMaskedLM.from_pretrained("xlm-roberta-base")
id_=[]
token_=[]
vector_=[]
vectorSentenc_=[]

# definimos los columnas que tomaremos del archivo que se analizar
# data = pd.read_excel('corpus/train/Single/lcp_single_train.xlsx',
#                    sheet_name='lcp_single_train') 

#token = ['definitorio','nan']
#sentence = ['texto 57 Aquí lo tenemos un poco más definitorio lo que es, nos dice, Aprendizaje supervisado: En este caso, se trata de un tipo de aprendizaje que permite al ordenador aprender mediante los patrones que le han sido proporcionados de forma previa','puntero inicio es NULL']

token = ['liberatoria','running','modelos','ba','nac']
sentence = ['permite la extinción de derechos (extintiva) o adquisiciones de cosas ajenas (liberatoria - usucapión)',
'texto 58 ¿Cuáles son los estados de una actividad? 1) Activa (Running): La actividad está encima de la pila, lo que quiere decir que es visible y tiene el foco',
'texto 8 Flujo de actividades Los productos que deben crearse Resultados del trabajo(modelos, documentos, datos informes.) ¿Qué y cuando? La asignación de tareas a cada miembro del equipo y al equipo como un todo',
'texto 10 A diferencia de la Inteligencia de negocios (BI), la Analítica de negocios (BA, Business Analytics) pone su atención sólo en el desarrollo de los modelos de análisis descriptivos',
'texto 48 ¿Qué es el control de acceso a la red? Las soluciones de control de acceso a la red (NAC) admiten la visibilidad de red y la administración de acceso mediante la aplicación de políticas en dispositivos y usuarios de la red corporativa']

# token = ['long','size','cache','reuse','unlimited','etiqueta','cycle','public']
# sentence = ['TEXTO 37 Pone la sección, estas son palabras que usan en ese momento el compilador pero es propio del lenguaje, utiliza una variable lc1 y le han dicho que va a ser .long y le da de una vez el valor de .long y aquí está almacenando la constante 23',
# 'texto 15 Su sintaxis es: CREATE TABLESPACE nb_tablespace DATAFILE ‘nb_archivo’ [SIZE entero [K|M][REUSE]] [AUTOEXTEND {OFF|ON claúsulas}] [‘nb_archivo’ [SIZE entero [K|M][REUSE] [AUTOEXTEND {OFF|ON claúsulas}], ] [DEFAULT STORAGE (INITIAL tamaño NEXT tamaño MINEXTENTS tamaño MAXEXTENTS tamaño PCTINCREASE valor )] [ONLINE|OFFLINE]',
# 'texto 68 Sintaxis de Secuencias: CREATE SEQUENCE secuencia [INCREMENT BY n] [START WITH n] [{MAXVALUE n | NOMAXVALUE}] [{MINVALUE n | NOMINVALUE}] [{CYCLE | NOCYCLE}] [{CACHE n| NOCACHE}]',
# 'texto 15 Su sintaxis es: CREATE TABLESPACE nb_tablespace DATAFILE ‘nb_archivo’ [SIZE entero [K|M][REUSE]] [AUTOEXTEND {OFF|ON claúsulas}] [‘nb_archivo’ [SIZE entero [K|M][REUSE] [AUTOEXTEND {OFF|ON claúsulas}], ] [DEFAULT STORAGE (INITIAL tamaño NEXT tamaño MINEXTENTS tamaño MAXEXTENTS tamaño PCTINCREASE valor )] [ONLINE|OFFLINE]',
# 'El formato AUTOEXTEND ON es: AUTOEXTEND ON NEXT entero {K|M} MAXSIZE {UNLIMITED| entero {K|M}}',
# '[etiqueta] [instrucción | directiva [operandos]] [comentario]',
# 'texto 68 Sintaxis de Secuencias: CREATE SEQUENCE secuencia [INCREMENT BY n] [START WITH n] [{MAXVALUE n | NOMAXVALUE}] [{MINVALUE n | NOMINVALUE}] [{CYCLE | NOCYCLE}] [{CACHE n| NOCACHE}]',
# 'Sintaxis: CREATE [PUBLIC] SYNONYM nombre FOR objeto; objeto es el objeto al que se referirá el sinónimo']

def sentence_token_vec_roberta(sentence,tokens_ex):
    result = []
    tokens_ex = str(tokens_ex).lower()
    sentence = str(sentence).lower().replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').replace('{',' ').replace('}',' ').replace('.',' ')
    input = tokenizer(sentence)
    tokens = tokenizer.convert_ids_to_tokens(input.input_ids)
    print(tokens)
    #print(str(len(input.input_ids)))

    input_ids = torch.tensor([input.input_ids[:512]])
    attention_mask = torch.tensor([input.attention_mask[:512]])

    # Ejecutamos red neuronal sobre el batch
    output = model(input_ids, attention_mask)
    #print("Output "+str(output))

    embeddings = list(zip(tokens, output.logits.tolist()[0]))
    #print("print Ebbeddings")

    #for tks in embeddings:
    #    print("length embeddings: "+str(len(tks[1])) + " word: " + str(tks[0]))
    tokens_ex_temp = tokenizer(tokens_ex, return_tensors="pt")
    tokens_temp = tokenizer.convert_ids_to_tokens(tokens_ex_temp.input_ids.numpy()[0])
    #print(tokens_temp)
    token_sep = []
    for temp in tokens_temp:
        if(temp!='<s>' and temp != '</s>'):
            token_sep.append(temp)
    #print("Palabra Tokenizado >>")
    #print(token_sep)
    if len(token_sep)==1:
        for tks in embeddings:
            print("************* Len embeddings: "+str(len(tks[1]))+ " ****** de: "+tks[0])
            #tks_ebb = str(tks[0]).replace('_','')
            if tks[0] ==token_sep[0]:
                #print(tks[0])
                result = tks[1]
    elif len(token_sep)>1:
        tks_temp = []
        for tks in embeddings:
            print("************* Len embeddings: "+str(len(tks[1]))+ " ****** de: "+tks[0])
            #print(tks[0])
            for tks_sep in token_sep:
                #tks_ebb = str(tks[0]).replace('_','')
                #print('TKS '+str(tks[0]))
                #print('TKS_SEP '+str(tks_sep))
                if tks[0] == tks_sep:
                    #print('tks[0] '+str(tks[0]))
                    #print('tks_sep '+str(tks_sep))
                    #print('tks_ebb '+str(tks[0]))
                    tks_temp.append(tks[1])
            #print('tksTemp: '+str(tks_temp))
        if len(tks_temp)>=1:
            result = average(tks_temp, axis=0)
            #print("AVERAGE "+str(average(tks_temp)))
    #print(len(result))
    return result

def text_to_vec_avg_token_roberta(text, token):
    """ Genera un vector a partir de un texto """
    avg = []
    token = str(token).lower()
    text = str(text).lower().replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').replace('{',' ').replace('}',' ').replace('.',' ')
    input = tokenizer(text)
    tokens = tokenizer.convert_ids_to_tokens(input.input_ids)
    input_ids = torch.tensor([input.input_ids[:512]])
    attention_mask = torch.tensor([input.attention_mask[:512]])
    print(tokens)
    # Ejecutamos red neuronal sobre el batch
    output = model(input_ids, attention_mask)
    embeddings = list(zip(tokens, output.logits.tolist()[0]))
    avg = []
    for emb in embeddings:
        print("************* Len embeddings "+emb[0]+ " ************* "+str(len(emb[1])))
        ag = average(emb[1])
        #print("average x token!!! "+str(ag))
        avg.append(ag)
    return avg

data = pd.DataFrame({'id': token,
                     'token': sentence})

for token, sentence in data.values:
    if token=='NULL':
        token=str('NULL')
    if token=='null' or token=='nan' or len(str(token))==0 or token=="":
        token=str('NULL')
    print('-----------START----------')
    print('Token: '+str(token))
    print('Sentence: '+str(sentence))
    results = sentence_token_vec_roberta(sentence, token)
    #print(results)
    results = average(results)
    print('Result: '+str(results))
    print('-----------END----------')

# count=0
# print("INICIA")
# for id, corpus, sentence, token, complexity in data.values:
#     count= count+1
#     if token=='NULL':
#         token=str('NULL')
#     if token=='null' or str(token)=='nan' or len(str(token))==0 or token=="":
#         token=str('NULL')
#     #print('Id: '+str(id)+' Token: '+str(token))
#     res = sentence_token_vec_roberta(sentence, token)
#     sentRes = text_to_vec_avg_token_roberta(sentence, token)
#     res = average(res)
#     avgRob = average(sentRes)
#     #print(res)
#     id_.append(id)
#     token_.append(token)
#     vector_.append(res)
#     vectorSentenc_.append(avgRob)
#     if count % 200 == 0:
#         print("Count || "+str(count)+" Id:"+str(id))
#     #print('saliooo')

# #Formar Excel
# df = pd.DataFrame({'id': id_,
#                 'token': token_,
#                 'vectorToken': vector_,
#                 'vectorSentences': vectorSentenc_})

# # Crear archivo
# writer = pd.ExcelWriter('Tokenizador_xlm-roberta_v3.xlsx', engine='xlsxwriter')

# # Convert de dataframe and insert in document
# df.to_excel(writer, sheet_name='Roberta', index=False)


# # Close Document
# writer.save()