# -*- coding: utf-8 -*-
import nltk
from nltk import bigrams
from tkinter import filedialog
from tkinter import ttk
from nltk import FreqDist
import tkinter as tk
import pandas as pd
import threading
import os
import re

from nltk.corpus import wordnet
import spacy
import syllables
import mode
#from modelo_etiquetadores import modelo_etiquetadores as mode
from lexical_diversity import lex_div as ld
from PIL import Image, ImageTk
#Bert & XLM RoBERTa
from transformers import BertTokenizer, BertModel, AutoTokenizer, AutoModelForMaskedLM
from transformers import RobertaTokenizer, RobertaModel
import torch # Obtenemos los embeddings de BERT para cada token
import torch.nn as nn
from numpy import average
import numpy as np
from sklearn import preprocessing

class CorporaFrequencyRNN(tk.Frame):
    datosFinalesTokenX = []
    datosFinalesEtiquY = []
    columna_leer = ''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.freq_words = []
        self.temporaziador=""
        self.token_pos = []
        self.num_sentences = []        
        self.directory = None
        self.finish = False
        self.label_message = tk.Label(self, text=' ')
        self.language = tk.IntVar()
        self.language.set(1)
        self.var = tk.IntVar()
        self.var.set(1)
        self.desicion = tk.IntVar()
        self.desicion.set(3)
        self.sistema = tk.IntVar()
        self.sistema.set(5)
        self.puntuacion_diversidad=0
        self.ubicacion_word=0
        self.palabra_anterior=""
        self.palabra_posterior=""
        nltk.download('omw') #wordnet
        nltk.download('wordnet') 
        self.tipo_etiquetado= spacy.load("es_core_news_sm") # en_core_web_sm
        self.tipo_etiquetado_en= spacy.load("en_core_web_sm") # en_core_web_sm
        
        #Images
        imgrnn = Image.open('images\machinelearningmodel_preview_rev_1.png')
        imgrnn = imgrnn.resize((110, 100), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        imgrnn = ImageTk.PhotoImage(imgrnn)
        panel = tk.Label(self, image=imgrnn)
        panel.image = imgrnn 
        panel.place(x=20,y=210)

        self.btn_directory = tk.Button(
            self,
            text="Select Corpus Folder",
            width=26,
            command=self.openDirectory, cursor="circle"
        )
        self.btn_exec = tk.Button(
            self,
            text="Accept",
            width=20, activebackground='yellow',
            command=self.previewAnalyze, cursor="circle"
        )
        self.btn_save = tk.Button(
            self,
            text="Save",
            width=20, activebackground='blue',
            command=self.previewSave, cursor="circle"
        )

        self.entry = tk.Entry(self, width=60)
        self.tempora = tk.StringVar()
        self.tempora.set("lcp_single_train")
        self.columna_leer = tk.Entry(self, width=60, textvariable=self.tempora)

        self.opcionBert = tk.IntVar()
        self.opcionBert.set(0)
        self.opcionMaria = tk.IntVar()
        self.opcionMaria.set(0)
        self.opcionRoberta = tk.IntVar()
        self.opcionRoberta.set(0)
        self.opcionRob = tk.IntVar()
        self.opcionRob.set(0)

        self.opcionAvgBert = tk.IntVar()
        self.opcionAvgBert.set(0)
        self.opcionAvgRoberta = tk.IntVar()
        self.opcionAvgRoberta.set(0)

        self.opcion_es = tk.Radiobutton(self, text="Spanish", variable=self.language, value=1, command=self.stausTipo, cursor="circle")
        self.opcion_en = tk.Radiobutton(self, text="English", variable=self.language, value=2, command=self.stausTipo, cursor="circle")
        self.opcion1 = tk.Radiobutton(self, text="Single-Words", variable=self.var, value=1, command=self.stausTipo, cursor="circle")
        self.opcion2 = tk.Radiobutton(self, text="Multi-Words", variable=self.var, value=2, command=self.stausTipo, cursor="circle")
        self.opcion3 = tk.Radiobutton(self, text="Train", variable=self.desicion, value=3, command=self.stausTipo, cursor="circle")
        self.opcion4 = tk.Radiobutton(self, text="Test", variable=self.desicion, value=4, command=self.stausTipo, cursor="circle")
        self.opcion5 = tk.Radiobutton(self, text="Training Mode System", variable=self.sistema, value=5, command=self.stausTipo, cursor="circle")
        self.opcion6 = tk.Radiobutton(self, text="Prediction Mode System", variable=self.sistema, value=6, command=self.stausTipo, cursor="circle")
        self.chk_bert = tk.Checkbutton(self, text="Roberta Large BNE",variable=self.opcionBert, onvalue=1, offvalue=0)
        self.chk_maria = tk.Checkbutton(self, text="MarIA",variable=self.opcionMaria, onvalue=1, offvalue=0)
        # self.chk_roberta = tk.Checkbutton(self, text="XMLRoberta",variable=self.opcionRoberta, onvalue=1, offvalue=0)
        # self.chk_avgbert = tk.Checkbutton(self, text="Average Bert",variable=self.opcionAvgBert, onvalue=1, offvalue=0)
        # self.chk_avgroberta = tk.Checkbutton(self, text="Average XMLRoberta",variable=self.opcionAvgRoberta, onvalue=1, offvalue=0)
        # self.chk_Robert = tk.Checkbutton(self, text="Roberta",variable=self.opcionRob, onvalue=1, offvalue=0)

        #MarIA Spanish cuando es ajustado al dominio
        self.tokenizer = RobertaTokenizer.from_pretrained('C:/Users/TIA/Desktop/org/PROY FINAL VERSION #2.0 B-A/marIA')
        self.model = RobertaModel.from_pretrained("C:/Users/TIA/Desktop/org/PROY FINAL VERSION #2.0 B-A/marIA")

        #MarIA Spanish cuando es ajustado al dominio y afinado
        #self.tokenizer = RobertaTokenizer.from_pretrained('C:/Users/TIA/Desktop/org/PROY FINAL VERSION #2.0 B-A/marIA-ajustado')
       # self.model = RobertaModel.from_pretrained("C:/Users/TIA/Desktop/org/PROY FINAL VERSION #2.0 B-A/marIA-ajustado")

        #Bert English
       
        # self.model_en = BertModel.from_pretrained("first_model/")
        self.tokenizer_en = RobertaTokenizer.from_pretrained('PlanTL-GOB-ES/roberta-large-bne')
        self.model_en = RobertaModel.from_pretrained("first_model/")
        self.lenSentence = []

        #XLM-RoBERTa --> Spanish - English <-- Multilinguistico
        self.tokenizer_xlm = AutoTokenizer.from_pretrained("xlm-roberta-base")
        self.model_xlm = AutoModelForMaskedLM.from_pretrained("xlm-roberta-base")
        self.init()


    def stausTipo(self):  
        if self.desicion.get()==3:
            if self.var.get()==1:
                self.tempora.set("lcp_single_train")
            elif self.var.get()==2:
                self.tempora.set("lcp_multi_train")
               
        elif self.desicion.get()==4:
            if self.var.get()==1:
                self.tempora.set("lcp_single_test")
               
            elif self.var.get()==2:
                self.tempora.set("lcp_multi_test")
    
    def init(self):
        label_back = tk.Label(self, text='< Back', fg='purple')
        label_back.bind(" <Button-1>", lambda e: self.controller.show_frame('StartPage'))
        label_back.grid(row=0, column=0, sticky=tk.W)
        label_title = tk.Label(self, text='Feature Of The Words With RoBERTa-Large-BNE & MarIA', font="Helvetica 12 bold")
        label_options_language = tk.Label(self, text='Language:',font="Helvetica 8 bold")
        label_options_language.grid(row=2, column=0,sticky=tk.W,padx=15)
        label_options = tk.Label(self, text='Options:',font="Helvetica 8 bold")
        label_title.grid(row=1, column=1)
        label_type_sytem=tk.Label(self,text="Mode System:",font="Helvetica 8 bold")
        label_type_sytem.grid(row=3,column=0, sticky=tk.W,padx=10)
        label_type=tk.Label(self,text="Type:",font="Helvetica 8 bold")
        label_type.grid(row=4,column=0, sticky=tk.W,padx=10)
        label_options_rnn = tk.Label(self, text='Options RNN:',font="Helvetica 8 bold")
        self.opcion_es.grid(row=2, column=1,sticky=tk.W)
        self.opcion_en.grid(row=2, column=1,sticky=tk.E)
        self.opcion5.grid(row=3, column=1,sticky=tk.W)
        self.opcion6.grid(row=3, column=1,sticky=tk.E)
        self.opcion3.grid(row=4, column=1,sticky=tk.W)
        self.opcion4.grid(row=4, column=1,sticky=tk.E)
        label_columna = tk.Label(self, text='Columna a leer:',font="Helvetica 8 bold")
        self.btn_directory.grid(row=5, column=0, sticky=tk.W, padx=10)
        self.entry.grid(row=5, column=1,sticky=tk.W)
        label_columna.grid(row=6, column=0, sticky=tk.W,padx=10)
        self.columna_leer.grid(row=6, column=1,sticky=tk.W)
        label_options.grid(row=7, column=0,sticky=tk.W,padx=10)
        self.opcion1.grid(row=7, column=1,sticky=tk.W)
        self.opcion2.grid(row=7, column=1,sticky=tk.E)
        self.btn_exec.grid(row=10, column=1, sticky=tk.W,pady=50)
        self.btn_save.grid(row=10, column=1, sticky=tk.E)
        label_options_rnn.grid(row=8, column=0,sticky=tk.W,padx=10)
        self.chk_bert.grid(row=8, column=1, sticky=tk.W, padx=4, pady=2)
        self.chk_maria.grid(row=8, column=2, sticky=tk.W, padx=4, pady=2)
        # self.chk_roberta.grid(row=8, column=1, sticky=tk.E, padx=4, pady=2)
        # self.chk_avgbert.grid(row=9, column=1, sticky=tk.W, padx=4, pady=2)
        # self.chk_avgroberta.grid(row=9, column=1, sticky=tk.E, padx=4, pady=2)


        self.statusButtonsHabilitar()
        # self.btn_plt.grid(row=, column=2, sticky=tk.W, padx=4, pady=10)
        #self.label_message.grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=4, pady=10)

    def getDataExcel(self, directory):
        xlsx = pd.ExcelFile(directory)
        # lcp_single_train
        words_complex = pd.read_excel(xlsx, usecols=['sentence'])
        words = []
        for row in words_complex.iterrows():
            for value in row:
                words.append(value.lower())
        return words

    def previewAnalyze(self):
        try:
            thread = threading.Thread(target=self.analyze)
            thread.start()
        except:
            self.mensaje("Ocurrió un Error",3)

    def analyze(self):
        #try:
        print("Inicia")
        self.statusButtonsDesabilitar()
        self.finish = False
        words = []
        files = []
        token_freq = []
        path = self.directory
        self.label_message.config(text='Processing...')
        self.update()
        dale_chall=[]
        lista_temporal=[]
    
        if self.sistema.get()==5:
            for root_dir, dirs, files_name in os.walk(path):
                for f in files_name:
                    print("Files "+f)
                    word_va = pd.read_excel(path + '/' + f, usecols=['id','sentence','token','complexity'])
                    direccion_tm = path + '/' + f
                    print("direccion"+direccion_tm)
                    if self.var.get() == 1:
                        print("single")
                    else:
                        print("multi")

                    for id_,sent,row,c in word_va.values:
                        #print(row)
                        if row=='null' or row=='nan' or len(str(row))==0 or row=="":
                            row='null'
                        teme=[id_,str(row).lower(),sent,c]
                        words.append(teme)   
            print("Ciclo")
        else:
            for root_dir, dirs, files_name in os.walk(path):
                for f in files_name:
                    word_va = pd.read_excel(path + '/' + f, usecols=['id','sentence','token'])
                    direccion_tm = path + '/' + f
                    if self.var.get() == 1:
                        print("single")
                    else:
                        print("multi")

                    for id_,sent,row in word_va.values:
                        if row=='null' or row=='nan' or len(str(row))==0 or row=="":
                            row='null'
                        teme=[id_,str(row).lower(),sent]
                        words.append(teme)   

                
        #freq = FreqDist(words)
        ds = pd.read_excel(direccion_tm)
        data_modificado = []
        self.temporaziador=direccion_tm
        if self.sistema.get()==5:
            for id_, corpus, sentences, token, y in ds.values:
                if token=='null' or token=='nan' or len(str(token))==0 or token=="":
                    token='null'
                arreglo = [id_, corpus, sentences, str(token).lower(), y]
                data_modificado.append(arreglo)

            dp = pd.DataFrame(data_modificado, columns=ds.columns)
            if os.path.exists(direccion_tm):
                os.remove(direccion_tm)

            print("==ARCHIVO ESTANDARIZADO==")
            dp.to_excel(direccion_tm, sheet_name=self.tempora.get(), index=False)

            df = pd.read_excel(direccion_tm)
            temp = []
    
            if self.var.get()==1:
                if self.language.get()==1:
                    for c in df['sentence'].values:
                        if str(c) != 'nan':
                            print(c)
                            token = self.tokenize(c)
                            print('tokeniza \n')
                            for g in token:
                                #print("LISTA TEMPORAL APPEND")
                                #print(g.lower())
                                lista_temporal.append(g.lower()) 
                            print("paso")
                else:
                    for c in df['sentence'].values:
                        if str(c) != 'nan':
                            print(c)
                            token = self.tokenize_en(c)
                            print('tokeniza \n')
                            for g in token:
                                lista_temporal.append(g.lower()) 
                
                

            else:
                if self.language.get()==1:
                    for row in df['sentence'].values:
                        token = self.tokenize(row)
                        words_bigrams = list(bigrams(token))
                        li = []
                        for x, y in words_bigrams:
                            z = x + " " + y
                            li.append(z)
                        for word in li:
                            lista_temporal.append(word.lower())
                else:
                    for row in df['sentence'].values:
                        token = self.tokenize_en(row)
                        words_bigrams = list(bigrams(token))
                        li = []
                        for x, y in words_bigrams:
                            z = x + " " + y
                            li.append(z)
                        for word in li:
                            lista_temporal.append(word.lower())


            freq = FreqDist(lista_temporal)
            count = 0
            for id_,word, oracion,complejidad in words:
                count= count+1
                #print("JEID --> "+id_)
                freq_abs=0
                if word=='NULL':
                    word=str('NULL')
                if word=='null' or word=='nan' or len(str(word))==0 or word=="":
                    word=str('null')
                
                for h1, h2 in freq.items():
                    if h1==word:
                        freq_abs=h2
                        break
                
                
                # Calculamos la frecuencia absoluta de cada palabra
                freq_rel = freq_abs / len(lista_temporal) # TOTAL DE PALABRAS CON DISTINCT
                # Configuramos el filtro de búsqueda entre la columna token y la palabra que se analiza
                filter1 = df['token'.lower()] == word
                # obtenemos los valores de complejidad de cada palabra
                #y = df[filter1]['complexity']
                y=complejidad
                # Calculamos el promedio de los valores complejos de todaslas ocurrencias de cada palabra
                y2 = df[filter1]['complexity'].mean()
                # Si el valor del promedio de complejidad es vacio se asigna cero
                if str(y2) == 'nan':
                    y2 = 0.00000000
                # Adquiriendo las caracterisiticas de los datos dependiendo del tipo como SINGLE o MULTI WORDS
                if self.var.get() == 1:
                    # Si el valor de la complejidade es cero, se envia como dato cero
                    frec_absoluta_word_before=0
                    frec_absoluta_word_after=0
                    frec_relative_word_before=0
                    frec_relative_word_after=0
                    len_word_before=0
                    len_word_after=0
                    
                    possitionToken, numberSentences=self.getPositionWord(word,oracion)
                
                    if self.palabra_anterior!="":
                    
                        for h3, h4 in freq.items():
                            if h3==self.palabra_anterior:
                                frec_absoluta_word_before=h4
                                len_word_before=len(self.palabra_anterior)
                                break
                    else:
                        frec_absoluta_word_before=0

                    if self.palabra_posterior!="":
                        for h3, h4 in freq.items():
                            if h3==self.palabra_posterior:
                                frec_absoluta_word_after=h4
                                len_word_after=len(self.palabra_posterior)
                                break
                    else:
                        frec_absoluta_word_after=0

                    if frec_absoluta_word_before>0:
                        frec_relative_word_before=frec_absoluta_word_before/len(lista_temporal)
                    if frec_absoluta_word_after>0:
                        frec_relative_word_after=frec_absoluta_word_after/len(lista_temporal)


                    con_syn=0;
                    hypo=0
                    hyper=0 
                    
                    for syn in wordnet.synsets(word):
                        con_syn=len(syn.lemmas()) #SINONIMOS CUANTOS
                        hypo=len(syn.hyponyms()) # CUANTOS HYPO
                        hyper=len(syn.hypernyms()) # CUANTOS HYPER
                    #Part-of-speech
                    if self.language.get()==1:
                        doc=self.tipo_etiquetado(word)
                    else:
                        doc=self.tipo_etiquetado_en(word)
                    var_tipo=0
                    for tok in doc:
                        var_tipo= mode.definicionTipo(str(tok.pos_))
                    #print("sigue..")
                    # Calculamos la cantidad de silabas de cada palabra
                    syl = self.getSyllableNumber(word) 
                    #print(id_) 

                    #POS de la oracion
                    propn=0 #Nombre Propio
                    aux=0   #Auxiliar
                    verb=0  #Verbo
                    adp=0   #Adposición ejemplo: a, durante
                    noun=0  #Sustantivo: niña, gato, Sandra
                    nn=0    #
                    sym=0   #Simbolo por ejemplo $,%, §, ©, +, -, ×, ÷, =, :), 😝, XD
                    num=0   #número puede ser 1,2,3
                    if self.language.get()==1:
                        docx=self.tipo_etiquetado(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))
                    else:
                        docx=self.tipo_etiquetado_en(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))
                    #print(doc)
                    for tok in docx:
                        #print(tok)
                        #print(tok.pos_)
                        if(tok.pos_ == 'PROPN'):
                            propn+=1
                        elif(tok.pos_ == 'AUX'):
                            aux+=1
                        elif(tok.pos_ == 'VERB'):
                            verb+=1
                        elif(tok.pos_ == 'ADP'):
                            adp+=1
                        elif(tok.pos_ == 'NOUN'):
                            noun+=1
                        elif(tok.pos_ == 'NN'):
                            nn+=1
                        elif(tok.pos_ == 'SYM'):
                            sym+=1
                        elif(tok.pos_ == 'NUM'):
                            num+=1
                    if self.opcionBert.get()== 1 and self.opcionRoberta.get() == 0:
                        if self.opcionAvgBert.get()==1:
                            print("Ingreso 2")
                            em1 = self.text_to_vec_token(oracion,word, self.model)
                            #print("em1: "+str(em1))
                            avgTokenBert = average(em1)
                            em = self.text_to_vec_avg_token(oracion,word, self.model)
                            #print("Len ************* "+str(len(em)))
                            avgClsBert = average(em)
                            #print("<< ************* Result Bert ************* >> "+str(avgBert))

                            temp = [id_,word, freq_abs, freq_rel,len(word), syl,possitionToken,numberSentences,con_syn,hypo,hyper,var_tipo,
                                    frec_relative_word_before,frec_relative_word_after,len_word_before,len_word_after,self.puntuacion_diversidad,
                                    propn,aux,verb,adp,noun,nn,sym,num,y,avgClsBert,avgTokenBert]
                        else:
                            print("Ingreso 3")
                            #bert = self.text_to_vec_cls_token(oracion, word, self.model)
                            #bert = self.text_to_vec_token(oracion, word, self.model)
                            bert_cls, bert_token = self.text_to_vec_cls_token(oracion, word, self.model)
                            temp = [id_,word, freq_abs, freq_rel,len(word), syl,possitionToken,numberSentences,con_syn,hypo,hyper,var_tipo,
                                frec_relative_word_before,frec_relative_word_after,len_word_before,len_word_after,self.puntuacion_diversidad,
                                propn,aux,verb,adp,noun,nn,sym,num,y,bert_cls,bert_token]

                            # tempx = [freq_abs, freq_rel,len(word), syl,possitionToken,numberSentences,con_syn,hypo,hyper,var_tipo,
                            #         frec_relative_word_before,frec_relative_word_after,len_word_before,len_word_after,self.puntuacion_diversidad,
                            #         propn,aux,verb,adp,noun,nn,sym,num]
                            #Normaliza 23k
                            #sc = preprocessing.StandardScaler() #Verificar
                            #tempx_ = sc.fit_transform(tempx)
                            #Genera las incrustraciones
                            # temp_1 = [id_,word]
                            # temp_2 = [bert_cls, bert_token]
                            # temp_3 = [y]
                            #Unifica los datos
                            # temp.append(temp_1, axis=1)
                            # temp.append(tempx, axis=1)
                            # temp.append(temp_3, axis=1)
                            # temp.append(temp_2, axis=1)
                            #print("Len TEmp Normalizado + RNN "+str(len(temp[0])))
                    elif self.opcionBert.get()== 0 and self.opcionRoberta.get() == 1:
                        if self.opcionAvgRoberta.get()==1:
                            print()
                        else:
                            #print("JEJE XD")
                            s_sep, token_xlm=self.s_token_vec_roberta(oracion, word) #, token_xlm
                            temp = [id_,word, freq_abs, freq_rel,len(word), syl,possitionToken,numberSentences,con_syn,hypo,hyper,var_tipo,
                                frec_relative_word_before,frec_relative_word_after,len_word_before,len_word_after,self.puntuacion_diversidad,
                                propn,aux,verb,adp,noun,nn,sym,num,y,s_sep,token_xlm] #,token_xlm
                            #print("JAJA XD "+str(len(s_sep)))
                            #print("JIJI XD "+str(len(token_xlm)))
                    elif self.opcionBert.get()== 1 and self.opcionRoberta.get() == 1:
                        if self.opcionAvgBert.get()==1 and self.opcionAvgRoberta.get()==1:
                            em1 = self.text_to_vec_token(oracion,word, self.model)                            
                            em = self.text_to_vec_avg_token(oracion,word, self.model)
                            bert_cls = average(em)
                            bert_token = average(em1)
                            roberta_s, roberta_token=self.s_token_vec_roberta(oracion, word) 
                            temp = [id_,word, freq_abs, freq_rel,len(word), syl,possitionToken,numberSentences,con_syn,hypo,hyper,var_tipo,
                                frec_relative_word_before,frec_relative_word_after,len_word_before,len_word_after,self.puntuacion_diversidad,
                                propn,aux,verb,adp,noun,nn,sym,num,y,bert_cls,bert_token,roberta_s,roberta_token] 
                else:
                    syl = self.getSyllableNumberMulti(word)   
                    number_type,puntuacion=self.puntuacion_multi_words(oracion)
                    #print(type(word))
                    tempWord = str(word).replace(' ','_')
                    print(tempWord)
                    con_syn=0;
                    hypo=0
                    hyper=0 
                    wordnet.synsets(b'\xe7\x8a\xac'.decode('utf-8'), lang='spa')
                    # syno =wordnet.synset(tempWord).lemma_names('spa')
                    # print(syno)
                    # con_syn = len(syno)
                    # print(con_syn)
                    for syn in wordnet.synsets(tempWord, lang='spa'):
                        syno = syn.lemmas()
                        #print(syno)
                        con_syn=len(syno) #SINONIMOS CUANTOS
                        #print(con_syn)
                        hypo=len(syn.hyponyms()) # CUANTOS HYPO
                        hyper=len(syn.hypernyms()) # CUANTOS HYPER

                    #POS de la oracion
                    propn=0 #Nombre Propio
                    aux=0   #Auxiliar
                    verb=0  #Verbo
                    adp=0   #Adposición ejemplo: a, durante
                    noun=0  #Sustantivo: niña, gato, sandra
                    nn=0    #
                    sym=0   #Simbolo por ejemplo $,%, §, ©, +, -, ×, ÷, =, :), 😝, XD
                    num=0   #número puede ser 1,2,3
                    if self.language.get()==1:
                        docx=self.tipo_etiquetado(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))
                    else:
                        docx=self.tipo_etiquetado_en(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))

                    #print(doc)
                    for tok in doc:
                        #print(tok)
                        #print(tok.pos_)
                        if(tok.pos_ == 'PROPN'):
                            propn+=1
                        elif(tok.pos_ == 'AUX'):
                            aux+=1
                        elif(tok.pos_ == 'VERB'):
                            verb+=1
                        elif(tok.pos_ == 'ADP'):
                            adp+=1
                        elif(tok.pos_ == 'NOUN'):
                            noun+=1
                        elif(tok.pos_ == 'NN'):
                            nn+=1
                        elif(tok.pos_ == 'SYM'):
                            sym+=1
                        elif(tok.pos_ == 'NUM'):
                            num+=1
                    bert = self.text_to_vec_token(oracion, word, self.model)
                    temp = [id_,word, freq_abs, freq_rel,len(word),syl,number_type,puntuacion,con_syn,hypo,hyper,propn,aux,verb,adp,noun,nn,sym,num,y,bert]
                print("ID: "+str(id_))
                if count % 200 == 0:
                    print("Count || "+str(count))
                token_freq.append(temp)
            print("SI HAY")
        else:
            for id_, corpus, sentences, token in ds.values:
                if token=='null' or token=='nan' or len(str(token))==0 or token=="":
                    token='null'
                arreglo = [id_, corpus, sentences, str(token).lower()]
                data_modificado.append(arreglo)

            dp = pd.DataFrame(data_modificado, columns=ds.columns)
            if os.path.exists(direccion_tm):
                os.remove(direccion_tm)

            print("==ARCHIVO ESTANDARIZADO==")
            dp.to_excel(direccion_tm, sheet_name=self.tempora.get(), index=False)

            df = pd.read_excel(direccion_tm)
            temp = []
            
            
            if self.var.get()==1:
                if self.language.get()==1:
                    for c in df['sentence'].values:
                        token = self.tokenize(c)
                        for g in token:
                            lista_temporal.append(g.lower()) 
                else:
                    for c in df['sentence'].values:
                        token = self.tokenize_en(c)
                        for g in token:
                            lista_temporal.append(g.lower()) 
            else:
                if self.language.get()==1:
                    for row in df['sentence'].values:
                        token = self.tokenize(row)
                        words_bigrams = list(bigrams(token))
                        li = []
                        for x, y in words_bigrams:
                            z = x + " " + y
                            li.append(z)
                        for word in li:
                            lista_temporal.append(word.lower())
                else:
                    for row in df['sentence'].values:
                        token = self.tokenize_en(row)
                        words_bigrams = list(bigrams(token))
                        li = []
                        for x, y in words_bigrams:
                            z = x + " " + y
                            li.append(z)
                        for word in li:
                            lista_temporal.append(word.lower())

            freq = FreqDist(lista_temporal)

            for id_,word, oracion in words:
                freq_abs=0
                if word=='NULL':
                    word=str('NULL')
                if word=='null' or word=='nan' or len(str(word))==0 or word=="":
                    word=str('null')
                
                for h1, h2 in freq.items():
                    if h1==word:
                        freq_abs=h2
                        break
                # Calculamos la frecuencia absoluta de cada palabra
                freq_rel = freq_abs / len(lista_temporal)
                # Configuramos el filtro de búsqueda entre la columna token y la palabra que se analiza
                filter1 = df['token'.lower()] == word
                # Adquiriendo las caracterisiticas de los datos dependiendo del tipo como SINGLE o MULTI WORDS
                if self.var.get() == 1:
                    # Si el valor de la complejidade es cero, se envia como dato cero
                    frec_absoluta_word_before=0
                    frec_absoluta_word_after=0
                    frec_relative_word_before=0
                    frec_relative_word_after=0
                    len_word_before=0
                    len_word_after=0
                    
                    possitionToken, numberSentences=self.getPositionWord(word,oracion)
                
                    if self.palabra_anterior!="":
                    
                        for h3, h4 in freq.items():
                            if h3==self.palabra_anterior:
                                frec_absoluta_word_before=h4
                                len_word_before=len(self.palabra_anterior)
                                break
                    else:
                        frec_absoluta_word_before=0

                    if self.palabra_posterior!="":
                        for h3, h4 in freq.items():
                            if h3==self.palabra_posterior:
                                frec_absoluta_word_after=h4
                                len_word_after=len(self.palabra_posterior)
                                break
                    else:
                        frec_absoluta_word_after=0

                    if frec_absoluta_word_before>0:
                        frec_relative_word_before=frec_absoluta_word_before/len(lista_temporal)
                    if frec_absoluta_word_after>0:
                        frec_relative_word_after=frec_absoluta_word_after/len(lista_temporal)


                    con_syn=0
                    hypo=0
                    hyper=0 
                    
                    for syn in wordnet.synsets(word):
                        con_syn=len(syn.lemmas())
                        hypo=len(syn.hyponyms())
                        hyper=len(syn.hypernyms())
                    #Part-of-speech
                    if self.language.get()==1:
                        doc=self.tipo_etiquetado(word)
                    else:
                        doc=self.tipo_etiquetado_en(word)
                    var_tipo=0
                    for tok in doc:
                        var_tipo= mode.definicionTipo(str(tok.pos_))
                    # Calculamos la cantidad de silabas de cada palabra
                    syl = self.getSyllableNumber(word)

                    #POS de la oracion
                    propn=0 #Nombre Propio
                    aux=0   #Auxiliar
                    verb=0  #Verbo
                    adp=0   #Adposición ejemplo: a, durante
                    noun=0  #Sustantivo: niña, gato
                    nn=0    #
                    sym=0   #Simbolo por ejemplo $,%, §, ©, +, -, ×, ÷, =, :), 😝, XD
                    num=0   #número puede ser 1,2,3
                    if self.language.get()==1:
                        docx=self.tipo_etiquetado(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))
                    else:
                        docx=self.tipo_etiquetado_en(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))

                    #print(doc)
                    for tok in docx:
                        #print(tok)
                        #print(tok.pos_)
                        if(tok.pos_ == 'PROPN'):
                            propn+=1
                        elif(tok.pos_ == 'AUX'):
                            aux+=1
                        elif(tok.pos_ == 'VERB'):
                            verb+=1
                        elif(tok.pos_ == 'ADP'):
                            adp+=1
                        elif(tok.pos_ == 'NOUN'):
                            noun+=1
                        elif(tok.pos_ == 'NN'):
                            nn+=1
                        elif(tok.pos_ == 'SYM'):
                            sym+=1
                        elif(tok.pos_ == 'NUM'):
                            num+=1
                    #bert = self.text_to_vec_token(oracion, word, self.model)
                    #bert = []
                    print("Ingreso 1")
                    bert_cls, bert_token = self.text_to_vec_cls_token(oracion, word, self.model)
                    
                    temp = [id_,word, freq_abs, freq_rel,len(word), syl,possitionToken,numberSentences,con_syn,hypo,hyper,var_tipo,
                            frec_relative_word_before,frec_relative_word_after,len_word_before,len_word_after,self.puntuacion_diversidad,propn,aux,verb,adp,noun,nn,sym,num,bert_cls,bert_token]
                else:
                    syl = self.getSyllableNumberMulti(word) 
                    number_word_sentence,puntuacion=self.puntuacion_multi_words(oracion)
                    #print(type(word))
                    tempWord = str(word).replace(' ','_')
                    #print(tempWord)
                    con_syn=0;
                    hypo=0
                    hyper=0 
                    wordnet.synsets(b'\xe7\x8a\xac'.decode('utf-8'), lang='spa')
                    # syno =wordnet.synset(tempWord).lemma_names('spa')
                    # print(syno)
                    # con_syn = len(syno)
                    # print(con_syn)
                    for syn in wordnet.synsets(tempWord, lang=u"spa"):
                        syno = syn.lemmas()
                        #print(syno)
                        con_syn=len(syno) #SINONIMOS CUANTOS
                        #print(con_syn)
                        hypo=len(syn.hyponyms()) # CUANTOS HYPO
                        hyper=len(syn.hypernyms()) # CUANTOS HYPER
                    
                    #POS de la oracion
                    propn=0 #Nombre Propio
                    aux=0   #Auxiliar
                    verb=0  #Verbo
                    adp=0   #Adposición ejemplo: a, durante
                    noun=0  #Sustantivo: niña, gato, sandra
                    nn=0    #
                    sym=0   #Simbolo por ejemplo $,%, §, ©, +, -, ×, ÷, =, :), 😝, XD
                    num=0   #número puede ser 1,2,3
                    if self.language.get()==1:
                        docx=self.tipo_etiquetado(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))
                    else:
                        docx=self.tipo_etiquetado_en(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))

                    #print(doc)
                    for tok in docx:
                        #print(tok)
                        #print(tok.pos_)
                        if(tok.pos_ == 'PROPN'):
                            propn+=1
                        elif(tok.pos_ == 'AUX'):
                            aux+=1
                        elif(tok.pos_ == 'VERB'):
                            verb+=1
                        elif(tok.pos_ == 'ADP'):
                            adp+=1
                        elif(tok.pos_ == 'NOUN'):
                            noun+=1
                        elif(tok.pos_ == 'NN'):
                            nn+=1
                        elif(tok.pos_ == 'SYM'):
                            sym+=1
                        elif(tok.pos_ == 'NUM'):
                            num+=1
                    #bert = self.text_to_vec_token(oracion, word, self.model)

                    temp = [id_,word, freq_abs, freq_rel,len(word), syl,number_word_sentence,puntuacion,con_syn,hypo,hyper,propn,aux,verb,adp,noun,nn,sym,num]
                
                token_freq.append(temp)

        print("Number of tokens read: " + str(len(token_freq)))
        order_list = sorted(token_freq, key=lambda x: x[2])
        self.freq_words = order_list
        # Anable buttons while saving
        self.label_message.config(text='Finalizing process.')
        self.update()
        self.finish = True
        self.previewSave()
            
            
        #except:
            #self.mensaje("Ocurrió un Error, revisar los formatos de los archivos a analizar",3)  

    def tokenize_en(self, text):
        pattern = r'[^a-zA-Z]'  
        #r'[^a-zA-Z]' 
        #^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$
        token = re.split(pattern, str(text))
        # token = regexp_tokenize(text, pattern)
        words = []
        for w in token:
            if re.match(r'\w', w, re.IGNORECASE) and not w.isdigit():
                words.append(w)
        return words
        
    def tokenize(self, text):
        texto_split = text.split()
        texto = []
        for w in texto_split:
            #s = w.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','')
            #if(str(s).find("^")):
                #print(s)
            texto.append(w.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))
            #replace('1)','').replace('2)','')
            #.replace('+','').replace('-','')
        return texto

    def previewSave(self):
        thread = threading.Thread(target=self.save)
        thread.start()

    def save(self):
        #try:
            if self.finish is True:
                self.statusButtonsDesabilitar()
                filename = filedialog.asksaveasfilename(
                    title="Save File",
                    defaultextension=".xlsx",
                    filetypes=(("xlsx files", "*.xlsx"),)
                )
                if filename != "":
                    # Disable buttons
                    self.label_message.config(text='Saving...')
                    self.update()

                    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

                    order_list = sorted(
                        self.freq_words, key=lambda x: x[2], reverse=True)

                    idx = []
                    for count in range(len(order_list)):
                        idx.append(count + 1)

                    df_idx = pd.DataFrame(
                        idx,
                        columns=['Order']
                    )

                    if self.sistema.get()==5:
                        if self.var.get() == 1:
                            if self.opcionBert.get()==1 and self.opcionRoberta.get() == 0:
                            #avgTokenBert,avgBert
                                if self.opcionAvgBert.get()==1:
                                    df = pd.DataFrame(
                                        order_list,
                                        columns=['id','token', 'abs_frecuency',
                                                'rel_frecuency', 'length', 'number_syllables','token_possition','number_token_sentences',
                                                'number_synonyms','number_hyponyms','number_hypernyms', 'Part_of_speech',
                                                'freq_relative_word_before','freq_relative_word_after','len_word_before',
                                                'len_word_after','mtld_diversity','propn','aux','verb','adp','noun','nn','sym','num','complexity','avgClsBert','avgTokenBert'] #'avgTokenBert','avgBert'
                                    )
                                else:
                                    print("DDD >>> Paso >>>> Aqui estoy Ingreso 3")
                                    df_ = pd.DataFrame(
                                        order_list,
                                        columns=['id','token', 'abs_frecuency',
                                                'rel_frecuency', 'length', 'number_syllables','token_possition','number_token_sentences',
                                                'number_synonyms','number_hyponyms','number_hypernyms', 'Part_of_speech',
                                                'freq_relative_word_before','freq_relative_word_after','len_word_before',
                                                'len_word_after','mtld_diversity','propn','aux','verb','adp','noun','nn','sym','num','complexity','bert_cls','bert_token']
                                    )
                                    print("Concat...")
                                    #print(df['bert'])
                                    #print([brt for brt in df['bert']])
                                    print(">>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<")
                                    dfs = pd.concat([df_,pd.DataFrame([brt for brt in df_['bert_cls']])],axis=1)
                                    df = pd.concat([dfs,pd.DataFrame([brts for brts in df_['bert_token']])],axis=1)
                                    #print(df) #[df,pd.DataFrame([brt for brt in bert])]
                                    print("Type Data <S>: >> "+str(type(df['bert_cls'])))
                                    print("Type Data Token: >> "+str(type(df['bert_token'])))
                                    df = df.drop(['bert_cls'], axis=1)
                                    df = df.drop(['bert_token'], axis=1)
                            elif self.opcionBert.get()==0 and self.opcionRoberta.get() == 1:
                                if self.opcionAvgRoberta.get()==1:
                                    df = pd.DataFrame(
                                        order_list,
                                        columns=['id','token', 'abs_frecuency',
                                                'rel_frecuency', 'length', 'number_syllables','token_possition','number_token_sentences',
                                                'number_synonyms','number_hyponyms','number_hypernyms', 'Part_of_speech',
                                                'freq_relative_word_before','freq_relative_word_after','len_word_before',
                                                'len_word_after','mtld_diversity','propn','aux','verb','adp','noun','nn','sym','num','complexity','avgTokenRoberta','avgSentenceRoberta']
                                    )
                                else:
                                    df = pd.DataFrame(
                                        order_list,
                                        columns=['id','token', 'abs_frecuency',
                                                'rel_frecuency', 'length', 'number_syllables','token_possition','number_token_sentences',
                                                'number_synonyms','number_hyponyms','number_hypernyms', 'Part_of_speech',
                                                'freq_relative_word_before','freq_relative_word_after','len_word_before',
                                                'len_word_after','mtld_diversity','propn','aux','verb','adp','noun','nn','sym','num','complexity','s_sep','token_xlm'] #,'token_xlm'
                                    )
                                    print("Concat...")
                                    #print(df['bert'])
                                    #print([brt for brt in df['bert']])
                                    #print(">>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<")
                                    #dfs
                                    #df = pd.concat([df_,pd.DataFrame([rbrt for rbrt in df_['s_sep']])],axis=1)
                                    #df = pd.concat([dfs,pd.DataFrame([rbrts for rbrts in df_['token_xlm']])],axis=1)
                                    #print(df) #[df,pd.DataFrame([brt for brt in bert])]
                                    #print("Type Data RS: >> "+str(type(df['s_sep'])))
                                    #print("Type Data RToken: >> "+str(type(df['token_xlm'])))
                                    #df = df.drop(['s_sep'], axis=1)
                                    #df = df.drop(['token_xlm'], axis=1)
                            elif self.opcionBert.get()==1 and self.opcionRoberta.get() == 1:
                                if self.opcionAvgBert.get()==1 and self.opcionAvgRoberta.get()==1:
                                    df = pd.DataFrame(
                                        order_list,
                                        columns=['id','token', 'abs_frecuency',
                                                'rel_frecuency', 'length', 'number_syllables','token_possition','number_token_sentences',
                                                'number_synonyms','number_hyponyms','number_hypernyms', 'Part_of_speech',
                                                'freq_relative_word_before','freq_relative_word_after','len_word_before',
                                                'len_word_after','mtld_diversity','propn','aux','verb','adp','noun','nn','sym','num','complexity','bert_cls','robertaBase_token','roberta_s','roberta_token']
                                    )
                               
                        else:
                            df = pd.DataFrame(
                                order_list,
                                columns=['id','token', 'abs_frecuency','rel_frecuency', 'length', 'number_syllables','number_token_sentences','mtld_diversity',
                                         'number_synonyms','number_hyponyms','number_hypernyms',
                                         'propn','aux','verb','adp','noun','nn','sym','num', 
                                         'complexity','bert']   )
                            df = pd.concat([df,pd.DataFrame([brt for brt in df['bert']])],axis=1)
                            #print(df) #[df,pd.DataFrame([brt for brt in bert])]
                            df = df.drop(['bert'], axis=1)
                    else:
                        if self.var.get() == 1:
                            df = pd.DataFrame(
                                order_list,
                                columns=['id','token', 'abs_frecuency',
                                        'rel_frecuency', 'length', 'number_syllables','token_possition','number_token_sentences',
                                        'number_synonyms','number_hyponyms','number_hypernyms', 'Part_of_speech',
                                        'freq_relative_word_before','freq_relative_word_after','len_word_before',
                                        'len_word_after','mtld_diversity','propn','aux','verb','adp','noun','nn','sym','num']
                            )
                        
                        else:
                            df = pd.DataFrame(
                                order_list,
                                columns=['id','token', 'abs_frecuency','rel_frecuency', 'length', 'number_syllables','number_token_sentences','mtld_diversity',
                                         'number_synonyms','number_hyponyms','number_hypernyms','propn','aux','verb','adp','noun','nn','sym','num']   )
                

                    df_idx.to_excel(
                        writer, sheet_name=self.tempora.get(), index=False)
                    df.to_excel(writer, sheet_name=self.tempora.get(),
                                index=False, startcol=1)
                    #self.fitCellWidth(writer, df, self.tempora.get(), 1)
                    writer.save()
                    self.label_message.config(text='Saved successfully')

                print("==ARCHIVO COMPLEX CALCULADO==")
                self.mensaje("Analisis Exitoso",1)
                self.statusButtonsHabilitar()
        #except:
        #    self.mensaje("Ocurrió un Error",3)

    def openDirectory(self):
        directory = filedialog.askdirectory(title="Select folder")
        if directory != self.directory and directory != "":
            self.directory = directory
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.directory)

    def fitCellWidth(self, writer, df, sheet_name, start_col=0):
        worksheet = writer.sheets[sheet_name]  # pull worksheet object
        for idx, col in enumerate(df):
            series = df[col]
            max_len = max((series.astype(str).map(
                len).max(), len(str(series.name)))) + 1
            worksheet.set_column(idx + start_col, idx + start_col,
                                 max_len)  # set column width

    # Funcion para obtener la cantidad de sílabas de una palabra
    def getSyllableNumber(self, token):
        return syllables.estimate(token)
    
    def getSyllableNumberMulti(self, token):
        if self.language.get()==1:
            lista=self.tokenize(token)
        else:
            lista=self.tokenize_en(token)
        suma=0
        for i in lista:
            suma=suma+syllables.estimate(i)
        return suma

    #funcion para obtener la posición de la palabra dentro de un texto
    def getPositionWord(self, token, sentences):
        self.palabra_anterior=""
        self.palabra_posterior=""
        self.puntuacion_diversidad=0
        positionWord = 0
        wordsSentences = []
        if str(sentences) != 'nan':
            if self.language.get()==1:
                wordsSentences = self.tokenize(sentences)
            else:
                wordsSentences = self.tokenize_en(sentences)
        numberWords = len(wordsSentences)
        self.puntuacion_diversidad=ld.mtld(wordsSentences)
        self.ubicacion_word=0
        tipo=True
        ubicacion_actual=0
        
        

        for word in wordsSentences:
            if str(word).lower() == str(token).lower():
                ubicacion_actual=positionWord/numberWords
                tipo=False
                break
            positionWord = positionWord + 1
           
        if tipo!=True:   
            if positionWord>0:
                self.palabra_anterior=wordsSentences[positionWord-1].lower()
            else:
                self.palabra_anterior=""
            if positionWord<numberWords-1:
                self.palabra_posterior=wordsSentences[positionWord+1].lower()
            else:
                self.palabra_posterior=""
          
            return ubicacion_actual,numberWords
        else:
            return -1, -1
        
    def puntuacion_multi_words(self,orac):
        if self.language.get()==1:
            wordsSentences = self.tokenize(orac)
        else:
            wordsSentences = self.tokenize_en(orac)
        return  len(wordsSentences),ld.mtld(wordsSentences)
    
    def statusButtonsDesabilitar(self):
     
        self.entry['state']=tk.DISABLED
        self.columna_leer['state']=tk.DISABLED
        self.opcion1['state']=tk.DISABLED
        self.opcion2['state']=tk.DISABLED
        self.opcion3['state']=tk.DISABLED
        self.opcion4['state']=tk.DISABLED
        self.opcion5['state']=tk.DISABLED
        self.opcion6['state']=tk.DISABLED
        self.btn_directory['state']=tk.DISABLED
        self.btn_exec['state']=tk.DISABLED
        self.btn_save['state']=tk.DISABLED
    
    def statusButtonsHabilitar(self):
        self.entry['state']=tk.NORMAL
        self.columna_leer['state']=tk.NORMAL
        self.opcion1['state']=tk.NORMAL
        self.opcion2['state']=tk.NORMAL
        self.opcion3['state']=tk.NORMAL
        self.opcion4['state']=tk.NORMAL
        self.opcion5['state']=tk.NORMAL
        self.opcion6['state']=tk.NORMAL
        self.btn_directory['state']=tk.NORMAL
        self.btn_exec['state']=tk.NORMAL
        self.btn_save['state']=tk.NORMAL
         
    def mensaje(self, texto, tipo):
        if tipo == 1:
            tk.messagebox.showinfo(message=texto, title="Information")
        if tipo == 2:
            tk.messagebox.showwarning(message=texto, title="Waening")
        if tipo == 3:
            tk.messagebox.showerror(message=texto, title="Error")

    #Versión Español
    def text_to_vec_token(self, text, token, model):
        """ Genera un vector a partir de un texto """
        #Cuando la letra 'ü' se convierte en UNK, se pasará a convertir en 'u'
        #para que el tokenizer pueda separar las palabras, ya que dichas palabras han sido etiquetadas como complejas
        text = text.lower()
        if self.language.get()==1:
            if token.find("ü"):
                #print("Token 'ü' >> "+str(token))
                token = token.replace('ü','u')
                text = text.replace('ü','u')
            input = self.tokenizer(text)
            input_ids = torch.tensor([input.input_ids[:212]]) 
            attention_mask = torch.tensor([input.attention_mask[:212]])
            output = self.model(input_ids, attention_mask)
            tokens = self.tokenizer.convert_ids_to_tokens(input.input_ids)
        else:
            input = self.tokenizer_en(text, return_tensors='pt')
            output = self.model_en(**input)
            tokens = self.tokenizer_en.convert_ids_to_tokens(input.input_ids[0])
        #print("---------tokens"+str(tokens))
        embeddings = list(zip(tokens, output.last_hidden_state.tolist()[0]))
        self.lenSentence.append(len(input.input_ids))
        result = []
        if self.language.get()==1:
            tokens_id_temp = self.tokenizer(token)
            tokens_temp = self.tokenizer.convert_ids_to_tokens(tokens_id_temp.input_ids)
        else:
            tokens_id_temp = self.tokenizer_en(token)
            tokens_temp = self.tokenizer_en.convert_ids_to_tokens(tokens_id_temp.input_ids)
        token_sep = []
        # print("Palabra Tokenizado Tokens Temp>>")
        # print(tokens_temp)
        for temp in tokens_temp:
            if(temp!='[CLS]' and temp != '[SEP]'):
                token_sep.append(temp)
        # print("Palabra Tokenizado >>")
        # print(token_sep)
        if len(token_sep)==1:
            for tks in embeddings:
                #print(str(tks[0])+" Token: "+str(token))
                if tks[0] ==token:
                #print("Token >> "+str(tks))
                #print(" >>>>>>> ---- <<<<<<<< ")
                #print(">>>>LONGITUD >>>"+str(len(tks[1])))
                    result = tks[1]
        elif len(token_sep)>1:
            tks_temp = []
            for tks in embeddings:
                #print(str(tks[0])+" Token: "+str(token))
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

    #Version 768 Incrustaciones
    def text_to_vec_cls_token(self, text, token, model):
        """ Genera un vector a partir de un texto """
        #Cuando la letra 'ü' se convierte en UNK, se pasará a convertir en 'u'
        #para que el tokenizer pueda separar las palabras, ya que dichas palabras han sido etiquetadas como complejas
        token = str(token).lower()
        text = str(text).lower().replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').replace('{',' ').replace('}',' ').replace('.',' ')
        if self.language.get()==1:
            if token.find("ü"):
                #print("Token 'ü' >> "+str(token))
                token = token.replace('ü','u')
                text = text.replace('ü','u')
            input = self.tokenizer(text)
            #print("input: "+str(input))
            input_ids = torch.tensor([input.input_ids[:512]]) 
            attention_mask = torch.tensor([input.attention_mask[:512]])
            #print("inputs_ids: "+str(input_ids[0]))
            #print("attention_mask: "+str(attention_mask[0]))
            output = self.model(input_ids, attention_mask)
            tokens = self.tokenizer.convert_ids_to_tokens(input.input_ids)
            print("Tokeniz.. >> "+str(tokens))
        else:
            input = self.tokenizer_en(text, return_tensors='pt', padding=True, truncation=True,max_length=512,)
            output = self.model_en(**input)
            tokens = self.tokenizer_en.convert_ids_to_tokens(input.input_ids[0])
        
        embeddings = list(zip(tokens, output.last_hidden_state.tolist()[0]))
        self.lenSentence.append(len(input.input_ids))
        result = []
        if self.language.get()==1:
            tokens_id_temp = self.tokenizer(token)
            tokens_temp = self.tokenizer.convert_ids_to_tokens(tokens_id_temp.input_ids)
        else:
            tokens_id_temp = self.tokenizer_en(token, return_tensors='pt')
            tokens_temp = self.tokenizer_en.convert_ids_to_tokens(tokens_id_temp.input_ids[0])
        token_sep = []
        print("<Token> : "+str(tokens_temp))
        for temp in tokens_temp:
            if(temp!='<s>' and temp != '</s>'):
                token_sep.append(temp)
        cls_sep = []
        #print("Palabra Tokenizado >>")
        #print(token_sep)
        if len(token_sep)==1:
            for tks in embeddings:
                if tks[0] == '<s>':
                    print(tks[0])
                    cls_sep = tks[1]
                if tks[0] ==token_sep[0]:
                    print("Token_sep: "+str(token_sep[0]))
                #print("Token >> "+str(tks))
                #print(" >>>>>>> ---- <<<<<<<< ")
                #print(">>>>LONGITUD >>>"+str(len(tks[1])))
                    result = tks[1]
        elif len(token_sep)>1:
            tks_temp = []
            for tks in embeddings:
                if tks[0] == '<s>':
                    print(tks[0])
                    cls_sep = tks[1]
                for tks_sep in token_sep:
                    if tks[0] ==tks_sep:
                #print("Token >> "+str(tks))
                #print(" >>>>>>> ---- <<<<<<<< ")
                #print(">>>>LONGITUD >>>"+str(len(tks[1])))
                        tks_temp.append(tks[1])
            
            if len(tks_temp)>=1:
                result = np.max(tks_temp,axis=0)
            #print("LEN AVG >> "+str(len(result)))
            #result = tks_temp   
            print("CLS "+str(len(cls_sep))+" >> ") 
            print(" -------------------------------------------------------------------------- ")
            print(" -------------------------------------------------------------------------- ")
            print("TOKEN "+str(len(result))+" >> ")    
        return cls_sep, result
    
    #Versión Español
    def text_to_vec_avg_token(self, text, token, model):
        """ Genera un vector a partir de un texto """
        #Cuando la letra 'ü' se convierte en UNK, se pasará a convertir en 'u'
        #para que el tokenizer pueda separar las palabras, ya que dichas palabras han sido etiquetadas como complejas
        if token.find("ü"):
            #print("Token 'ü' >> "+str(token))
            token = token.replace('ü','u')
            text = text.replace('ü','u')
        input = self.tokenizer(text)
        input_ids = torch.tensor([input.input_ids[:512]]) 
        attention_mask = torch.tensor([input.attention_mask[:512]])
        output = self.model(input_ids, attention_mask)
        tokens = self.tokenizer.convert_ids_to_tokens(input.input_ids)
        embeddings = list(zip(tokens, output.last_hidden_state.tolist()[0]))
        avg = []
        # for emb in embeddings:
        #     #print("************* Len embeddings "+emb[0]+ " ************* "+str(len(emb[1])))
        #     ag = average(emb[1])
        #     #print("average x token!!! "+str(ag))
        #     avg.append(ag)
        for emb in embeddings:
            #print("************* Len embeddings "+emb[0]+ " ************* "+str(len(emb[1])))
            if emb[0] == '[CLS]':
                avg = emb[1]
            #print("average x token!!! "+str(ag))
            
        return avg
    
    #Versión Inglés


    #XLM - RoBERTa Versión Ingles & Español
    def sentence_token_vec_roberta(self, sentence,tokens_ex):
        result = []
        tokens_ex = str(tokens_ex).lower()
        sentence = str(sentence).lower().replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').replace('{',' ').replace('}',' ').replace('.',' ')
        input = self.tokenizer_xlm(sentence)
        tokens = self.tokenizer_xlm.convert_ids_to_tokens(input.input_ids)
        #print(tokens)
        #print(str(len(input.input_ids)))
        input_ids = torch.tensor([input.input_ids[:512]])
        attention_mask = torch.tensor([input.attention_mask[:512]])

        # Ejecutamos red neuronal sobre el batch
        output = self.model_xlm(input_ids, attention_mask)
        #print("Output "+str(output))

        embeddings = list(zip(tokens, output.logits.tolist()[0]))
        #print("print Ebbeddings")

        #for tks in embeddings:
        #    print("length embeddings: "+str(len(tks[1])) + " word: " + str(tks[0]))
        tokens_ex_temp = self.tokenizer_xlm(tokens_ex, return_tensors="pt")
        tokens_temp = self.tokenizer_xlm.convert_ids_to_tokens(tokens_ex_temp.input_ids.numpy()[0])
        #print(tokens_temp)
        token_sep = []
        for temp in tokens_temp:
            if(temp!='<s>' and temp != '</s>'):
                token_sep.append(temp)
        #print("Palabra Tokenizado >>")
        #print(token_sep)
        if len(token_sep)==1:
            for tks in embeddings:
                if tks[0] ==token_sep[0]:
                    result = tks[1]
        elif len(token_sep)>1:
            tks_temp = []
            for tks in embeddings:
                #print("************* Len embeddings "+tks[0]+ " ************* "+str(len(tks[1])))
                #print(tks[0])
                for tks_sep in token_sep:
                    #tks_ebb = str(tks[0]).replace('_','')
                    #print('TKS '+str(tks[0]))
                    #print('TKS_SEP '+str(tks_sep))
                    if tks[0] == tks_sep:
                        tks_temp.append(tks[1])
                #print('tksTemp: '+str(tks_temp))
            if len(tks_temp)>=1:
                result = average(tks_temp, axis=0)
                #print("AVERAGE "+str(average(tks_temp)))
        #print(len(result))
        return result

    def text_to_vec_avg_token_roberta(self, text, token):
        """ Genera un vector a partir de un texto """
        avg = []
        token = str(token).lower()
        text = str(text).lower().replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').replace('{',' ').replace('}',' ').replace('.',' ')
        input = self.tokenizer_xlm(text)
        tokens = self.tokenizer_xlm.convert_ids_to_tokens(input.input_ids)
        input_ids = torch.tensor([input.input_ids[:512]])
        attention_mask = torch.tensor([input.attention_mask[:512]])
        # Ejecutamos red neuronal sobre el batch
        output = self.model_xlm(input_ids, attention_mask)
        embeddings = list(zip(tokens, output.logits.tolist()[0]))
        avg = []
        for emb in embeddings:
            print("************* Len embeddings "+emb[0]+ " ************* "+str(len(emb[1])))
            ag = average(emb[1])
            #print("average x token!!! "+str(ag))
            avg.append(ag)
        return avg

    def s_token_vec_roberta(self, sentence,tokens_ex):
        result = []
        tokens_ex = str(tokens_ex).lower()
        sentence = str(sentence).lower().replace('(',' ').replace(')',' ').replace('[',' ').replace(']',' ').replace('{',' ').replace('}',' ').replace('.',' ').replace("'",' ').replace('"',' ').replace('/k','/ k').replace('::',' ')
        input = self.tokenizer_xlm(sentence)
        tokens = self.tokenizer_xlm.convert_ids_to_tokens(input.input_ids)
        #print(tokens)
        #print(str(len(input.input_ids)))
        input_ids = torch.tensor([input.input_ids[:512]])
        attention_mask = torch.tensor([input.attention_mask[:512]])

        # Ejecutamos red neuronal sobre el batch
        output = self.model_xlm(input_ids, attention_mask)
        #print("Output "+str(output))

        embeddings = list(zip(tokens, output.logits.tolist()[0]))
        #print("print Ebbeddings")

        #for tks in embeddings:
        #    print("length embeddings: "+str(len(tks[1])) + " word: " + str(tks[0]))
        tokens_ex_temp = self.tokenizer_xlm(tokens_ex, return_tensors="pt")
        tokens_temp = self.tokenizer_xlm.convert_ids_to_tokens(tokens_ex_temp.input_ids.numpy()[0])
        #print(tokens_temp)
        s_sep = []
        token_sep = []
        for temp in tokens_temp:
            if(temp!='<s>' and temp != '</s>'):
                token_sep.append(temp)
        #print("Palabra Tokenizado >>")
        #print(token_sep)
        if len(token_sep)==1:
            for tks in embeddings:
                if tks[0] == '<s>':
                    s_sep = tks[1]
                if tks[0] ==token_sep[0]:
                    result = tks[1]
        elif len(token_sep)>1:
            tks_temp = []
            for tks in embeddings:
                if tks[0] == '<s>':
                    s_sep = tks[1]
                #print("************* Len embeddings "+tks[0]+ " ************* "+str(len(tks[1])))
                #print(tks[0])
                for tks_sep in token_sep:
                    #tks_ebb = str(tks[0]).replace('_','')
                    #print('TKS '+str(tks[0]))
                    #print('TKS_SEP '+str(tks_sep))
                    if tks[0] == tks_sep:
                        tks_temp.append(tks[1])
                #print('tksTemp: '+str(tks_temp))
            if len(tks_temp)>=1:
                result = average(tks_temp, axis=0)
                #print("AVERAGE "+str(average(tks_temp)))
        #print(len(result))
        s_sep = average(s_sep)
        result = average(result)
        return s_sep, result

prueba = CorporaFrequencyRNN()