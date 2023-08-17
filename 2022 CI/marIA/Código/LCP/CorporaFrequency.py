# -*- coding: utf-8 -*-
from nltk import bigrams
from tkinter import filedialog
from tkinter import ttk
from nltk import FreqDist
import tkinter as tk
import pandas as pd
import threading
import os
import re
import nltk
from nltk.corpus import wordnet
import spacy
from spacy.language import Language
import syllables
from modelo_etiquetadores import modelo_etiquetadores as mode
from lexical_diversity import lex_div as ld
from PIL import Image, ImageTk

class CorporaFrequency(tk.Frame):
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
        nltk.download('omw') #Open Multilingual WordNet
        nltk.download('wordnet')
        self.tipo_etiquetado= spacy.load("es_core_news_sm") # en_core_web_sm
        self.tipo_etiquetado_en= spacy.load("en_core_web_sm")  
        #Images
        imgrnn = Image.open('images\check.png')
        imgrnn = imgrnn.resize((110, 100), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        imgrnn = ImageTk.PhotoImage(imgrnn)
        panel = tk.Label(self, image=imgrnn)
        panel.image = imgrnn 
        panel.place(x=20,y=190)

        self.btn_directory = tk.Button(
            self,
            text="Select Corpus Folder",
            width=26,
            command=self.openDirectory, cursor="circle"
        )
        self.btn_exec = tk.Button(
            self,
            text="Accept",
            width=20,
            command=self.previewAnalyze, cursor="circle"
        )
        self.btn_save = tk.Button(
            self,
            text="Save",
            width=20,
            command=self.previewSave, cursor="circle"
        )

        self.entry = tk.Entry(self, width=60)
        self.tempora = tk.StringVar()
        self.tempora.set("lcp_single_train")
        self.columna_leer = tk.Entry(self, width=60, textvariable=self.tempora)

        self.opcion_es = tk.Radiobutton(self, text="Spanish", variable=self.language, value=1, command=self.stausTipo, cursor="circle")
        self.opcion_en = tk.Radiobutton(self, text="English", variable=self.language, value=2, command=self.stausTipo, cursor="circle")
        self.opcion1 = tk.Radiobutton(self, text="Single-Words", variable=self.var, value=1, command=self.stausTipo, cursor="circle")
        self.opcion2 = tk.Radiobutton(self, text="Multi-Words", variable=self.var, value=2, command=self.stausTipo, cursor="circle")
        self.opcion3 = tk.Radiobutton(self, text="Train", variable=self.desicion, value=3, command=self.stausTipo, cursor="circle")
        self.opcion4 = tk.Radiobutton(self, text="Test", variable=self.desicion, value=4, command=self.stausTipo, cursor="circle")
        self.opcion5 = tk.Radiobutton(self, text="Training Mode System", variable=self.sistema, value=5, command=self.stausTipo, cursor="circle")
        self.opcion6 = tk.Radiobutton(self, text="Prediction Mode System", variable=self.sistema, value=6, command=self.stausTipo, cursor="circle")
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
        label_back = tk.Label(self, text='< Back', fg='blue')
        label_back.bind(" <Button-1>", lambda e: self.controller.show_frame('StartPage'))
        label_back.grid(row=0, column=0, sticky=tk.W)
        label_title = tk.Label(self, text='Feature Of The Words', font="Helvetica 12 bold")
        label_options_language = tk.Label(self, text='Language:',font="Helvetica 8 bold")
        label_options_language.grid(row=3, column=0,sticky=tk.W,padx=15)
        label_options = tk.Label(self, text='Options:',font="Helvetica 8 bold")
        label_title.grid(row=1, column=1)
        label_type_sytem=tk.Label(self,text="Mode System:",font="Helvetica 8 bold")
        label_type_sytem.grid(row=4,column=0, sticky=tk.W,padx=15)
        label_type=tk.Label(self,text="Type:",font="Helvetica 8 bold")
        label_type.grid(row=5,column=0, sticky=tk.W,padx=15)
        self.opcion_es.grid(row=3, column=1,sticky=tk.W)
        self.opcion_en.grid(row=3, column=1,sticky=tk.E)
        self.opcion5.grid(row=4, column=1,sticky=tk.W)
        self.opcion6.grid(row=4, column=1,sticky=tk.E)
        self.opcion3.grid(row=5, column=1,sticky=tk.W)
        self.opcion4.grid(row=5, column=1,sticky=tk.E)
        label_columna = tk.Label(self, text='Columna a leer:',font="Helvetica 8 bold")
        self.btn_directory.grid(row=6, column=0, sticky=tk.W, padx=15)
        self.entry.grid(row=6, column=1,sticky=tk.W)
        label_columna.grid(row=7, column=0, sticky=tk.W,padx=15)
        self.columna_leer.grid(row=7, column=1,sticky=tk.W)
        label_options.grid(row=8, column=0,sticky=tk.W,padx=15)
        self.opcion1.grid(row=8, column=1,sticky=tk.W)
        self.opcion2.grid(row=8, column=1,sticky=tk.E)
        self.btn_exec.grid(row=11, column=1, sticky=tk.W,pady=50)
        self.btn_save.grid(row=11, column=1, sticky=tk.E)
        
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
                            #print(c)
                            token = self.tokenize(c)
                            #print('tokeniza \n')
                            for g in token:
                                lista_temporal.append(g.lower())
                else:
                    for c in df['sentence'].values:
                        if str(c) != 'nan':
                            #print(c)
                            token = self.tokenize_en(c)
                            #print('tokeniza \n')
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
            print("Language: "+str(self.language))
            for id_,word, oracion,complejidad in words:
                #print("JEID --> "+id_)
                freq_abs=0
                            
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
                # Adquiriendo las caracteristicas de los datos dependiendo del tipo como SINGLE o MULTI WORDS
                if self.var.get() == 1:
                    # Si el valor de la complejidad es cero, se envia como dato cero
                    frec_absoluta_word_before=0
                    frec_absoluta_word_after=0
                    frec_relative_word_before=0
                    frec_relative_word_after=0
                    len_word_before=0
                    len_word_after=0
                    
                    possitionToken, numberSentences=self.getPositionWord(word,oracion)
                    print("Possition Token: "+str(possitionToken)+" Number Sentences: "+str(numberSentences))
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
                    noun=0  #Sustantivo: niña, gato
                    nn=0    #
                    sym=0   #Simbolo por ejemplo $,%, §, ©, +, -, ×, ÷, =, :), XD
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
                    
                    temp = [id_,word, freq_abs, freq_rel,len(word), syl,possitionToken,numberSentences,con_syn,hypo,hyper,var_tipo,
                            frec_relative_word_before,frec_relative_word_after,len_word_before,len_word_after,self.puntuacion_diversidad,propn,aux,verb,adp,noun,nn,sym,num,y] #
                else:
                    syl = self.getSyllableNumberMulti(word)   
                    number_type,puntuacion=self.puntuacion_multi_words(oracion)
                    #print(type(word))
                    #Se reemplaza de esa manera las multi palabras ya que para sacar las sílabas en multi palabras se requiere que la palabra se represente de esa manera palabra1_palabra2
                    tempWord = str(word).replace(' ','_')
                    #print(tempWord)
                    con_syn=0;
                    hypo=0
                    hyper=0 
                    if self.language.get()==1:
                        wordnet.synsets(b'\xe7\x8a\xac'.decode('utf-8'), lang='spa')
                    # syno =wordnet.synset(tempWord).lemma_names('spa')
                    # print(syno)
                    # con_syn = len(syno)
                    # print(con_syn)
                        for syn in wordnet.synsets(tempWord, lang='spa'):
                            #syno = syn.lemmas()
                            #print(syno)
                            con_syn=len(syn.lemmas()) #SINONIMOS CUANTOS
                            #print(con_syn)
                            hypo=len(syn.hyponyms()) # CUANTOS HYPO
                            hyper=len(syn.hypernyms()) # CUANTOS HYPER
                    else:
                        for syn in wordnet.synsets(word):
                            con_syn=len(syn.lemmas())
                            hypo=len(syn.hyponyms())
                            hyper=len(syn.hypernyms())
                    #POS de la oracion
                    propn=0 #Nombre Propio
                    aux=0   #Auxiliar
                    verb=0  #Verbo
                    adp=0   #Adposición ejemplo: a, durante
                    noun=0  #Sustantivo: niña, gato
                    nn=0    #
                    sym=0   #Simbolo por ejemplo $,%, §, ©, +, -, ×, ÷, =, :)
                    num=0   #número puede ser 1,2,3
                    if self.language.get()==1:
                        doc=self.tipo_etiquetado(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))
                    else:
                        doc=self.tipo_etiquetado_en(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))
                    
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

                    temp = [id_,word, freq_abs, freq_rel,len(word),syl,number_type,puntuacion,con_syn,hypo,hyper,propn,aux,verb,adp,noun,nn,sym,num,y]
                
                token_freq.append(temp)
            print("SI HAY")
        else:#Modo del Test sin nivel de complejidad
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
                if self.language.get() == 1:
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


                    con_syn=0;
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
                        doc=self.tipo_etiquetado(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))
                    else:
                        doc=self.tipo_etiquetado_en(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))

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
              
                    temp = [id_,word, freq_abs, freq_rel,len(word), syl,possitionToken,numberSentences,con_syn,hypo,hyper,var_tipo,
                            frec_relative_word_before,frec_relative_word_after,len_word_before,len_word_after,self.puntuacion_diversidad,propn,aux,verb,adp,noun,nn,sym,num] #
                else:
                    syl = self.getSyllableNumberMulti(word) 
                    number_word_sentence,puntuacion=self.puntuacion_multi_words(oracion)
                    #Se reemplaza de esa manera las multi palabras ya que para sacar las sílabas en multi palabras
                    #Se requiere que la palabra se represente de esa manera palabra1_palabra2
                    tempWord = str(word).replace(' ','_')
                    print(tempWord)
                    con_syn=0;
                    hypo=0
                    hyper=0 #buscar
                    wordnet.synsets(b'\xe7\x8a\xac'.decode('utf-8'), lang='spa')
                    # syno =wordnet.synset(tempWord).lemma_names('spa')
                    # print(syno)
                    # con_syn = len(syno)
                    # print(con_syn)
                    for syn in wordnet.synsets(tempWord, lang=u"spa"):
                        #syno = syn.lemmas()
                        #print(syno)
                        con_syn=len(syn.lemmas()) #SINONIMOS CUANTOS
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
                        doc=self.tipo_etiquetado(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))
                    else:
                        doc=self.tipo_etiquetado_en(oracion.replace(',','').replace(':','').replace(';','').replace('¿','').replace('?','').replace('(','').replace(')','').replace('!','').replace('|','').replace('*','').replace('=','').replace('.-','').replace('.',''))
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
        try:
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
                            df = pd.DataFrame(
                                order_list,
                                columns=['id','token', 'abs_frecuency',
                                        'rel_frecuency', 'length', 'number_syllables','token_possition','number_token_sentences',
                                        'number_synonyms','number_hyponyms','number_hypernyms', 'Part_of_speech',
                                        'freq_relative_word_before','freq_relative_word_after','len_word_before',
                                        'len_word_after','mtld_diversity','propn','aux','verb','adp','noun','nn','sym','num','complexity'] #
                            )

                        
                        else:
                            df = pd.DataFrame(
                                order_list,
                                columns=['id','token', 'abs_frecuency','rel_frecuency', 'length', 'number_syllables','number_token_sentences','mtld_diversity',
                                         'number_synonyms','number_hyponyms','number_hypernyms',
                                         'propn','aux','verb','adp','noun','nn','sym','num', 
                                         'complexity']   )
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
                    self.fitCellWidth(writer, df, self.tempora.get(), 1)
                    writer.save()
                    self.label_message.config(text='Saved successfully')

                print("==ARCHIVO COMPLEX CALCULADO==")
                self.mensaje("Analisis Exitoso",1)
                self.statusButtonsHabilitar()
        except:
            self.mensaje("Ocurrió un Error",3)

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