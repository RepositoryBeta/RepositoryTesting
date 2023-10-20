# -*- coding: utf-8 -*-
import nltk
import os
from nltk.tag import StanfordPOSTagger
import re
import socket
from functools import reduce
from lexical_diversity import lex_div as ld
import numpy as np

class TextComplexityStanford():
        
    def __init__(self):
                
        os.environ['CLASSPATH'] = 'stanford-postagger-full-2017-06-09'
        os.environ['STANFORD_MODELS']  = 'stanford-postagger-full-2017-06-09/models/'
        if (os.name == 'nt'):
            java_path = "C:/Program Files/Java/jdk-11.0.10/bin/java.exe"
            #java_path = "C:/Windows/System32/java.exe"
            os.environ['JAVAHOME'] = java_path
        self.spanishTagger = nltk.tag.stanford.StanfordPOSTagger('spanish.tagger', encoding='utf8')
        self.englishTagger = nltk.tag.stanford.StanfordPOSTagger('english.tagger', encoding='utf8')
        # Para leer el texto que introcucimos
        ruta='./CREA_total.txt'
        
        f = open(ruta)
        lines = f.readlines()
        f.close()
        crea = {}
        for l in lines[1:]: # those words not in the 1000 most frequent words in CREA are low frequency words
            data = l.strip().split()
            if(float(data[2].replace(',', ''))>= 1000):
                crea[data[1]] = float(data[2].replace(',', ''))
        self.crea = crea


        ruta = './List_Buchanan.txt'
        f = open(ruta)
        lines = f.readlines()
        f.close()
        buchanan = {}
        for l in lines[1:]: # abstracción de todas las 1500 palabras de la lista de buchanan
            data = l.strip().split()
            buchanan[data[1]] = data[0]
        self.buchanan = buchanan
    pass

    def ProcesarTexto(self, text,  lang = 'es'):

        self.lang = lang
        #RECIBIR EL TEXTO COMO VIENE EN LOS ARCHIVOS
        texto_split = text.split()
        texto = []
        casos = ["\'", "\"", "!", "¡", "¿", "?", "(", ")", "{", "}", "[", "]", "<", ">", "|", "#", "$", "%",":", ";", ",", "+", "*", "=", "-", "/", "\\", "‘", "^", "’", "~", ".", "&"]
        index = 0 
        ultimo = len(texto_split) - 1
        for w in texto_split:
            if(index == 0):
                longitud = len(w)
                texto_split[0] = w[longitud-5:longitud]
                index+=1
            else:
                if(index==ultimo):
                    longitud = len(w)
                    for i in range(longitud):
                        if w[i] == ".":
                            texto_split[ultimo] = w[:i+1]
                else:
                    index+=1

#SEPARAR EL CARACTER DE PUNTO DE LAS PALABRAS.
        for w in texto_split:
            palabra = ""
            simb_inicio = ""
            simb_final = ""
            final = len(w)
            if (final > 1):

                if (w[final - 1] == "."):
                    palabra = w[:final - 1]
                    simb_final = w[final - 1:]
                    texto.append(palabra)
                    texto.append(simb_final)
                else:
                    texto.append(w)
            else:
                texto.append(w)
        self.texto = texto

#SEPARAR EL TEXTO EN ORACIONES
        oracion = []
        oraciones = []
        for w in texto:
            if(w != "."):
                oracion.append(w)
            else:
                oraciones.append(oracion)
                oracion = []

        self.oracionesSinFiltro = oraciones
        print("Oraciones Sin Filtrar")
        print(self.oracionesSinFiltro)
        print("\n")
        #return oraciones

#FILTRO DE CARACTERES ESPECIALES
        ubicacion = []
        oracion = []
        oracionesConFiltro = []
        caracteres = []
        for sentence in self.oracionesSinFiltro:
            for w in sentence:
                longitud = len(w)
                if longitud > 1:
                    for i in range(longitud):
                        if w[i] in casos:
                            ubicacion.append(i)
                            caracteres.append(w[i])
                    if len(ubicacion) > 0:
                        contador = 0
                        if ubicacion[0] == 0:
                            if len(ubicacion) > 1:
                                if ubicacion[len(ubicacion)-1]+1 == longitud:
                                    for u in ubicacion:
                                        if (contador < len(ubicacion) - 1):
                                            #print(w)
                                            #print(w[u+1:ubicacion[contador+1]])
                                            oracion.append(w[u+1:ubicacion[contador+1]])
                                            contador +=1
                                else:
                                    for u in ubicacion:
                                        if (contador < len(ubicacion) - 1):
                                            #print(w)
                                            #print(w[u+1:ubicacion[contador+1]])
                                            oracion.append(w[u+1:ubicacion[contador+1]])
                                            contador +=1
                                    oracion.append(w[ubicacion[(len(ubicacion)-1)]+1:])
                            else:
                                oracion.append(w[ubicacion[0]+1:])
                        else:
                            oracion.append(w[0:ubicacion[0]])
                            if len(ubicacion) > 1:
                                if ubicacion[len(ubicacion)-1]+1 == longitud:
                                    for u in ubicacion:
                                        if contador < len(ubicacion)-1:
                                            oracion.append(w[u+1:ubicacion[contador+1]])
                                            contador +=1
                                else:
                                    for u in ubicacion:
                                        if (contador < len(ubicacion) - 1):
                                            oracion.append(w[u + 1:ubicacion[contador + 1]])
                                            contador += 1
                                    oracion.append(w[ubicacion[(len(ubicacion) - 1)] + 1:])
                            else:
                                if ubicacion[0]+1 == longitud:
                                    pass
                                else:
                                    oracion.append(w[ubicacion[0]+1:])
                    else:
                        oracion.append(w)
                    ubicacion = []
                else:
                    if w in casos:
                        pass
                    else:
                        oracion.append(w)
            oracionesConFiltro.append(oracion)
            oracion = []

        #LISTA CON LOS CARACTERES ESPECIALES DEL TEXTO (PARA CÁLCULO DE LOS SIGNOS DE PUNTUACIÓN)
        self.caracteresEspeciales = caracteres
        self.oracionesSinCarEsp = oracionesConFiltro
        #return oracionesConFiltro

# FILTRO DE CADENAS VACÍAS
        oracion = []
        oracionesConFiltro = []
        for sentence in self.oracionesSinCarEsp:
            for w in sentence:
                if len(w) > 0:
                    oracion.append(w)
                else:
                    pass
            oracionesConFiltro.append(oracion)
            oracion = []

        print("Oraciones Con Caracteres Especiales Separados")
        self.oracionesSinCarEsp = oracionesConFiltro
        print(self.oracionesSinCarEsp)
        print("\n")

        #return self.oracionesSinCarEsp

#FILTRO DE NÚMEROS Y DIRECCIONES IP
        oracion = []
        oracionesSinNum = []
        for sentence in self.oracionesSinCarEsp:
            for w in sentence:
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
            oracionesSinNum.append(oracion)
            oracion = []
        self.oracionesSinNum = oracionesSinNum
        self.pos_content_sentences = self.oracionesSinNum


#FILTRO PARA LAS PALABRAS DE CONTENIDO
        new_pos_sentences = []

        if self.lang == 'es':
            tag = self.spanishTagger.tag
        else:
            tag = self.englishTagger.tag

        for sentence in self.oracionesSinNum:
            new_pos_sentences.append(tag(sentence))
        self.new_pos_sentences = new_pos_sentences

        new_pos_content_sentences_cw = []

        for sentence in self.new_pos_sentences:
            new_pos_content_sentences_cw.append([w[0] for w in sentence if re.match('N.*|V.*|A.*', w[1])])
        self.new_pos_sentences_cw = new_pos_content_sentences_cw

        return self.oracionesSinNum

    def lexicalComplexity(self):

        # PALABRAS COMPLEJAS => LWF FRECUENCIA < 1,000 SEGUN CREA.
        # print("LEXICAL COMPLEXITY INDEX: ")
        count = 0
        for sentence in self.pos_content_sentences:
            count += len([w for w in sentence if w.lower() not in self.crea])
        # Number of low frequency words
        self.N_lfw = 0
        try:
            N_lfw = count
            self.N_lfw = N_lfw
        except:
            self.N_lfw = 0
        # print("Number of low frequency words (N_lfw): ", self.N_lfw, "\n")
        # Number of distinct content words
        self.N_dcw = 0
        try:
            # VOCABULARIO
            #            print(self.pos_content_sentences)
            #            print(set([w.lower() for s in self.pos_content_sentences for w in s]))
            N_dcw = len(set([w.lower() for s in self.pos_content_sentences for w in s]))
            self.N_dcw = N_dcw
        except:
            self.N_dcw = 0

        # print("Number of palabras diferentes (N_dcw): ", self.N_dcw, "\n")
        # Number of sentences
        self.N_s = 0
        try:
            N_s = len(self.pos_content_sentences)
            self.N_s = N_s
        except:
            self.N_s = 0

        # print("Number os sentences (N_s): ", self.N_s, "\n")
        # Number of total content words
        self.N_cw = 0
        try:
            # print([len(s) for s in self.new_pos_sentences_cw])
            N_cw = reduce((lambda x, y: x + y), [len(s) for s in self.new_pos_sentences_cw], 0)
            self.N_cw = N_cw
        except:
            self.N_cw = 0
        # print("Number of total content words (N_cw): ", self.N_lfw, "\n")
        # Lexical Distribution Index
        self.LDI = 0

        try:
            LDI = N_dcw / float(N_s)
            self.LDI = LDI
        except ZeroDivisionError:
            self.LDI = 0

        # print("Lexical Distribution Index (LDI) = ", self.LDI)
        # Index of Low Frequency Words
        self.ILFW = 0
        try:
            ILFW = (N_lfw / float(N_cw)) * 100
            self.ILFW = ILFW
        except ZeroDivisionError:
            self.ILFW = 0

        # print("Index Low Frequency Words (ILFW) = ", self.ILFW)
        # Lexical Complexity
        self.LC = 0
        try:
            LC = (LDI + ILFW) / 2
            self.LC = LC
        except ZeroDivisionError:
            self.LC = 0
        ##print ("Lexical Complexity (LC) =", LC, "\n")

        return self.N_lfw, self.N_cw, self.N_dcw, self.N_s, self.LDI, self.ILFW, self.LC

    def ssReadability(self):
        # Number of words
        count = 0
        for sentence in self.pos_content_sentences:
            for w in sentence:
                count += 1
        N_w = count
        self.N_w = N_w

        # As rare words (rw), we considered those words that cannot be found on the list of
        # 1,500 most common Spanish words provided in Spaulding [1956]. Similarly
        # print("Number of  words (N_w): ", self.N_w, "\n")
        # Number of rare words

        byfreq = sorted(self.buchanan, key=self.buchanan.__getitem__, reverse=True)
        # print(byfreq)
        count = 0
        for sentence in self.pos_content_sentences:
            count += len([w for w in sentence if w.lower() not in byfreq])
        N_rw = count
        self.N_rw = N_rw
        # print("Number of rare words (N_rw): ", self.N_rw, "\n")

        SSR = (1.609 * (self.N_w / self.N_s)) + (331.8 * (self.N_rw / self.N_w)) + 22.0
        self.SSR = SSR
        # print ("SPAULDING SPANISH READABILITY (SSR) ", self.SSR, "\n")

        return self.N_w, self.N_rw, self.SSR

    def sentenceComplexity(self):

        # print("SENTENCE COMPLEXITY INDEX: ")
        ASL = self.N_w / self.N_s
        self.ASL = ASL
        # print("Average Sentence Length (ASL) = ",self.ASL)

        # Number of complex sentences
        N_cs = 0
        for sentence in self.new_pos_sentences:
            # print("\n\nCálculo con nuevas oraciones")
            # print(sentence)
            previous_is_verb = False
            count = 0
            for w in sentence:
                if re.match('V.*', w[1]):
                    if (previous_is_verb):
                        count += 1
                        previous_is_verb = False
                    else:
                        previous_is_verb = True
                else:
                    previous_is_verb = False
            if count > 0:
                N_cs += 1

        self.N_cs = N_cs
        # print("Number of complex sentences: ", self.N_cs, "\n")

        CS = self.N_cs / self.N_s
        self.CS = CS
        # print("Complex Sentences (CS) = ", self.CS)

        SCI = (ASL + CS) / 2
        self.SCI = SCI
        # print("Sentence Complexity Index (SCI) = ", self.SCI, "\n")

        return self.N_cs, self.ASL, self.CS, self.SCI

    def autoReadability(self):

        N_charac = 0
        for characters in self.texto:
            N_charac += len(characters)

        self.N_charac = N_charac
        # print("Number of characters: ", self.N_charac, "\n")

        ARI = (4.71 * (self.N_charac / self.N_w)) + (0.5 * (self.N_w / self.N_s)) - 21.43
        self.ARI = ARI
        # print("AUTOMATED READABILITY INDEX (ARI) = ", self.ARI, '\n')

        return self.N_charac, self.ARI

    def punctuationMarks(self):

        if self.lang == 'es':
            tag = self.spanishTagger.tag
        else:
            tag = self.englishTagger.tag

        '''self.text_tokens es la variable donde cada token corresponde a un 
        término(palabra, número...) o un signo de puntuación.'''
        new_text = tag(self.caracteresEspeciales)
        #print(new_text)
        # Solo nos interesa contar los tokens que sean signo de puntuación.
        PM = 0
        for w in new_text:
            if re.match('F.*', w[1]):
                PM += 1

        self.PM = PM + len(self.pos_content_sentences)
        # print("PUNCTUATION MARKS = ", self.PM, "\n")

        return self.PM

    def metricaMtld(self):
        textMtld = ""
        for sentence in self.pos_content_sentences:
            for w in sentence:
                textMtld += w + " "
        self.textMtld = ld.mtld(textMtld)
        return self.textMtld
