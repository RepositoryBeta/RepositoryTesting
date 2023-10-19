# -*- coding: utf-8 -*-
import nltk
import os
from nltk.tag import StanfordPOSTagger
import re
import socket


class FiltradoOraciones():
        
    def __init__(self):
                
        os.environ['CLASSPATH'] = 'stanford-postagger-full-2017-06-09'
        os.environ['STANFORD_MODELS']  = 'stanford-postagger-full-2017-06-09/models/'
        if (os.name == 'nt'):
            java_path = "C:/Program Files/Java/jdk-11.0.15.1/bin/java.exe"
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
        #print(texto_split)
        texto = []
        casos = ["\'", "\"", "!", "¡", "¿", "?", "(", ")", "{", "}", "[", "]", "<", ">", "|", "#", "$", "%",":", ";", ",", "+", "*", "=", "-", "/", "\\", "‘", "^", "’", "~", ".", "&"]
        index = 0 
        ultimo = len(texto_split) - 1
        for w in texto_split:
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
        #print("Oraciones Sin Filtrar")
        #print(self.oracionesSinFiltro)
        #print("\n")
        return oraciones