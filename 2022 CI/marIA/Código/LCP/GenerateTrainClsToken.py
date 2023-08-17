#from transformers import BertTokenizer, BertModel, AutoTokenizer, AutoModelForMaskedLM
from numpy import average
import torch # Obtenemos los embeddings de BERT para cada token
import torch.nn as nn
import pandas as pd
from tkinter import filedialog
 #Bert Spanish
#tokenizer = BertTokenizer.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased')
#model = BertModel.from_pretrained('dccuchile/bert-base-spanish-wwm-uncased')
#Bert English
#tokenizer_en = BertTokenizer.from_pretrained('bert-base-uncased')
#model_en = BertModel.from_pretrained("bert-base-uncased")

# def saveResultadofinal():
#     try:
#         filename = filedialog.asksaveasfilename(
#             title="Save file",
#             defaultextension=".xlsx",
#             filetypes=(("xlsx files", "*.xlsx"),)
#         )
#         new_dt.to_excel(filename, sheet_name="result_final")
#         self.mensaje('Successful analysis', 1)
#     except:
#         self.mensaje("Ocurrió un error",3)

# def text_to_vec_cls_token(self, text, token, model):
#     """ Genera un vector a partir de un texto """
#     #Cuando la letra 'ü' se convierte en UNK, se pasará a convertir en 'u'
#     #para que el tokenizer pueda separar las palabras, ya que dichas palabras han sido etiquetadas como complejas
    
#     if self.language.get()==1:
#         if token.find("ü"):
#             #print("Token 'ü' >> "+str(token))
#             token = token.replace('ü','u')
#             text = text.replace('ü','u')
#         input = self.tokenizer(text)
#         input_ids = torch.tensor([input.input_ids[:212]]) 
#         attention_mask = torch.tensor([input.attention_mask[:212]])
#         output = self.model(input_ids, attention_mask)
#         tokens = self.tokenizer.convert_ids_to_tokens(input.input_ids)
#     else:
#         input = self.tokenizer_en(text, return_tensors='pt')
#         output = self.model(**input)
#         tokens = self.tokenizer_en.convert_ids_to_tokens(input.input_ids)
    
#     embeddings = list(zip(tokens, output.last_hidden_state.tolist()[0]))
#     self.lenSentence.append(len(input.input_ids))
#     result = []
#     if self.language.get()==1:
#         tokens_id_temp = self.tokenizer(token)
#         tokens_temp = tokenizer.convert_ids_to_tokens(tokens_id_temp.input_ids)
#     else:
#         tokens_id_temp = self.tokenizer_en(token)
#         tokens_temp = tokenizer_en.convert_ids_to_tokens(tokens_id_temp.input_ids)
#     token_sep = []
#     for temp in tokens_temp:
#         if(temp!='[CLS]' and temp != '[SEP]'):
#             token_sep.append(temp)
#     cls_sep = []
#     #print("Palabra Tokenizado >>")
#     #print(token_sep)
#     if len(token_sep)==1:
#         for tks in embeddings:
#             if tks[0] == '[CLS]':
#                 cls_sep = tks[1]
#         #print(tks[0])
#             if tks[0] ==token:
#             #print("Token >> "+str(tks))
#             #print(" >>>>>>> ---- <<<<<<<< ")
#             #print(">>>>LONGITUD >>>"+str(len(tks[1])))
#                 result = tks[1]
#     elif len(token_sep)>1:
#         tks_temp = []
#         for tks in embeddings:
#         #print(tks[0])
#             if tks[0] == '[CLS]':
#                 cls_sep = tks[1]
#             for tks_sep in token_sep:
#                 if tks[0] ==tks_sep:
#             #print("Token >> "+str(tks))
#             #print(" >>>>>>> ---- <<<<<<<< ")
#             #print(">>>>LONGITUD >>>"+str(len(tks[1])))
#                     tks_temp.append(tks[1])
        
#         if len(tks_temp)>=1:
#             result = average(tks_temp,axis=0)
#         #print("LEN AVG >> "+str(len(result)))
#         #result = tks_temp      
#     return cls_sep, result

data = pd.read_excel('corpus/Español/_com_train/Single/result_train_s.xlsx',
                    sheet_name='lcp_single_train') 


dat_b = data['bert_token']
dat_b = dat_b.values.tolist()
#print(dat_b[0])
print(dat_b[0])
# print("Len: >> " + str(len(dat_b[0])))
#print([brt for brt in dat_b])
##dfs = pd.DataFrame([brd for brd in dat_b])
#print("DFS >> "+str(dfs))
print("Type >> " + str(type(dat_b)))
df = pd.concat([data,pd.DataFrame([brd for brd in dat_b])],axis=1)
                                #print(df) #[df,pd.DataFrame([brt for brt in bert])]
#data.append(dfs)
df = df.drop(['bert_token'], axis=1)


# # Crear archivo
#writer = pd.ExcelWriter('train_cls_token.xlsx', engine='xlsxwriter')

# # Convert de dataframe and insert in document
#df.to_excel(writer, sheet_name='result_single_train', index=False)


# # Close Document
# writer.save()

filename = filedialog.asksaveasfilename(
        title="Save file",
        defaultextension=".xlsx",
        filetypes=(("xlsx files", "*.xlsx"),)
    )
df.to_excel(filename, sheet_name="result_final")