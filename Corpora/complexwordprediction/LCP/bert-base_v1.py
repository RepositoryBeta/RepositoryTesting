from numpy import average, nan
from pandas.core.reshape.concat import concat
from transformers import BertTokenizer, BertModel
import torch # Obtenemos los embeddings de BERT para cada token
import torch.nn as nn
import pandas as pd
import xlsxwriter

tokenizer = BertTokenizer.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased')
model = BertModel.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased')
texto = []
tokens = []
id_corpus = [] 
bert = []
lenSentence = []

def text_to_vec(text, model):
  """ Genera un vector a partir de un texto """
  input = tokenizer(text)
  input_ids = torch.tensor([input.input_ids[:512]]) 
  attention_mask = torch.tensor([input.attention_mask[:512]])
  output = model(input_ids, attention_mask)
  return output.last_hidden_state[0][0]

def text_to_vec_token(text, token, model):
  """ Genera un vector a partir de un texto """
  input = tokenizer(text)
  #print("INPUT IDS"+str(input.input_ids[:512]))
  #print("LEN >> "+str(len(input.input_ids)))
  input_ids = torch.tensor([input.input_ids[:512]]) 
  #print(str(torch.tensor([input.input_ids[:212]])))
  attention_mask = torch.tensor([input.attention_mask[:512]])
  #print(str(torch.tensor([input.attention_mask[:212]])))
  output = model(input_ids, attention_mask)
  tokens = tokenizer.convert_ids_to_tokens(input.input_ids)
  #print(tokens)
  embeddings = list(zip(tokens, output.last_hidden_state.tolist()[0]))
  lenSentence.append(len(input.input_ids))
  result = []
  tokens_id_temp = tokenizer(token)
  tokens_temp = tokenizer.convert_ids_to_tokens(tokens_id_temp.input_ids)
  token_sep = []
  for temp in tokens_temp:
    if(temp!='[CLS]' and temp != '[SEP]'):
      token_sep.append(temp)
  print("Palabra Tokenizado >>")
  print(token_sep)
  if len(token_sep)==1:
    for tks in embeddings:
      #print(tks[0])
      if tks[0] ==token:
        #print("Token >> "+str(tks))
        #print(" >>>>>>> ---- <<<<<<<< ")
        #print(">>>>LONGITUD >>>"+str(len(tks[1])))
        result = tks[1]
  elif len(token_sep)>1:
    tks_temp = []
    for tks in embeddings:
      #print(tks[0])
      for tks_sep in token_sep:
        if tks[0] ==tks_sep:
          #print("Token >> "+str(tks))
          #print(" >>>>>>> ---- <<<<<<<< ")
          #print(">>>>LONGITUD >>>"+str(len(tks[1])))
          tks_temp.append(tks[1])
      
    if len(tks_temp)>=1:
      result = average(tks_temp,axis=0)
    #print("LEN AVG >> "+str(len(result)))
    #result = tks_temp      
  return result

# definimos los columnas que tomaremos del archivo que se analizar
data = pd.read_excel('Pruebas/Single/lcp_single_train.xlsx',
                      sheet_name='lcp_single_train') 
# Tokenizamos un texto y generamos datos de entrada para la red neuronal

text = """texto 5 de ahí nosotros tenemos lo que es contabilidad y nosotros manejamos en hogares, empresas en el mercado, todo el mundo manejan lo que es contabilidad, porque hacen el registro verdad, de todos sus hechos económicos dentro de una libretita, la notación
"""
#tokens_ = "mercado"
tokens_ = "libretita"
#tokens_ = "notación"

for id, corpus, sentence, token, complexity in data.values:
  if token=='null' or token=='nan' or len(str(token))==0 or token=="" or token=='NULL':
    token='NULL'
  print("Token >> "+str(token)+" << Embeddings")
  id_corpus.append(id)
  texto.append(sentence)
  tokens.append(token)
  #vecs = text_to_vec(sentence, model)
  vecs = text_to_vec_token(sentence, token, model)
  bert.append(vecs)

#vecs = text_to_vec_token(text, tokens_, model)

#print("Vector Resultante >> "+str(vecs))
df = pd.DataFrame({'id': id_corpus,
                   'Token': tokens,
                   'Setence': texto,
                   'Longitud': lenSentence,
                   'Bert': bert
                   })

namesSec=[]
i=0
for brt in bert:
  i+=1
  namesSec.append("Embb"+str(i))

df = pd.concat(
    [df,pd.DataFrame([brt for brt in bert])
    ], axis=1)

#workbook = xlsxwriter.Workbook("Pruebas/BertPrueba.xlsx")
#worksheet = workbook.add_worksheet()

# Crear archivo
writer = pd.ExcelWriter('Pruebas/BertPrueba.xlsx', engine='xlsxwriter')

# Convert de dataframe and insert in document
df.to_excel(writer, sheet_name='lcp_single_train', index=False)

#worksheet.write_row(97,768,bert)
#workbook.close()

# Close Document
writer.save()

# maxs = df.max('Longitud')
# print(maxs)

#tokens = tokenizer.convert_ids_to_tokens(input.input_ids)
#print(tokens)
#print(str(len(input.input_ids)))


# Estos son los tokens generados (se puede ver cómo el algoritmo WordPiece separa algunas palabras)
#print(tokens)

# Obtenemos los embeddings de BERT para cada token
# Preparamos batch de entrada (1 solo sample)
#input_ids = torch.tensor([input.input_ids[:512]])
#attention_mask = torch.tensor([input.attention_mask[:512]]) #Este argumento indica al modelo qué tokens deben ser atendidos y cuáles no.
#print(input.input_ids)

# Ejecutamos red neuronal sobre el batch
#output = model(input_ids, attention_mask)

# Los ID de entrada (input_ids) son a menudo los únicos parámetros necesarios para pasar al modelo como entrada. 
# Son índices de tokens, representaciones numéricas de tokens que construyen las secuencias que serán utilizadas como entrada por el modelo .

#print(output)

# Tomamos los embeddings
#embeddings = list(zip(tokens, output.last_hidden_state.tolist()[0]))
# Veamos el vector generado para un token ("pseudocódigo")
#print(embeddings[1])




res_lcp = pd.read_excel('corpus/train/Single/result_car_train.xlsx',
                      sheet_name='lcp_single_train') 

# for id in res_lcp.values:
#   for id_corpus, bert in data.values:
i = 0
StringBert = "Embb"
Hola = [(StringBert+str(bert.index(int(brt)+1))) for brt in bert if len(brt)>1]
print(Hola)
    







  
