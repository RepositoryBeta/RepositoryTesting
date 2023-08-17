#Bert & XLM RoBERTa
from transformers import BertTokenizer, BertModel, AutoTokenizer, AutoModelForMaskedLM
from numpy import average
#Bert English
tokenizer_en = BertTokenizer.from_pretrained('bert-base-uncased')
model_en = BertModel.from_pretrained("bert-base-uncased")
#token_ ='''cloud'''
#token_ = '''flock'''
token_ = '''hoofs'''
#text = '''It is a moment of important reflection, introduced by Act 41 of 2009, on what is, unfortunately, a widespread and increasingly serious phenomenon, because today paedophiles are not old men who trick children in parks but people who circulate within an internationally organised structure and who use the most modern forms of technology, such as the Internet.'''
#text = '''When the cloud stayed on the tabernacle many days, then the children of Israel kept Yahweh's command, and didn't travel.'''
text =  '''Arise and thresh, daughter of Zion; for I will make your horn iron, and I will make your hoofs brass; and you will beat in pieces many peoples: and I will devote their gain to Yahweh, and their substance to the Lord of the whole earth.'''
input = tokenizer_en(text, return_tensors='pt')
output = model_en(**input)
print(input.input_ids[0])
tokens = tokenizer_en.convert_ids_to_tokens(input.input_ids[0])
embeddings = list(zip(tokens, output.last_hidden_state.tolist()[0]))


tokens_id_temp = tokenizer_en(token_, return_tensors='pt')
tokens_temp = tokenizer_en.convert_ids_to_tokens(tokens_id_temp.input_ids[0])

token_sep = []
for temp in tokens_temp:
    if(temp!='[CLS]' and temp != '[SEP]'):
        token_sep.append(temp)

cls_sep = []
#print("Palabra Tokenizado >>")
#print(token_sep)
if len(token_sep)==1:
    for tks in embeddings:
        if tks[0] == '[CLS]':
            cls_sep = tks[1]
    #print(tks[0])
        if tks[0] ==token_:
        #print("Token >> "+str(tks))
        #print(" >>>>>>> ---- <<<<<<<< ")
        #print(">>>>LONGITUD >>>"+str(len(tks[1])))
            result = tks[1]
elif len(token_sep)>1:
    tks_temp = []
    for tks in embeddings:
    #print(tks[0])
        if tks[0] == '[CLS]':
            cls_sep = tks[1]
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

print("CLS "+str(len(cls_sep))+" >> "+str(cls_sep)) 
print(" -------------------------------------------------------------------------- ")
print(" -------------------------------------------------------------------------- ")
print("TOKEN "+str(len(result))+" >> "+str(result)) 