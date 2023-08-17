# -*- coding: utf-8 -*-
from matplotlib import markers
from matplotlib.colors import Colormap
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_validate, train_test_split, RepeatedKFold
from sklearn import metrics, preprocessing
from sklearn.preprocessing import PolynomialFeatures
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from tkinter import filedialog
from getpass import getuser
import tkinter as tk
import pandas as pd
import numpy as np
import threading
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sps
import statsmodels.api as sm
from etiqueta_lickert import etiqueta_lickert as lickert

class RandomForestClasificator(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.window_separator = None
        self.directoryReference = None
        self.directoryReferenceTest = None
        self.clf = []
        self.x_train = []
        self.x_test = []
        self.y_train = []
        self.y_test = []
        self.tokenizer = []
        self.modelo = []
        self.y_pred = []
        self.data = []
        self.data_test = []
        self.interval = 0
        self.noTrees = 0
        self.valueK = 1
        self.new_dt = []
        self.new_experiment = []
        self.data_x_grafica = []
        self.dic = []
        self.language = tk.IntVar()
        self.language.set(1)
        self.opcion = tk.IntVar()
        self.opcion.set(1)
        self.modo = tk.IntVar()
        self.modo.set(3)
        self.polynomialFeatures = tk.IntVar()
        self.standardScaler = tk.IntVar()
        self.id_word = []
        self.token_temp = []
        self.tipografica1=tk.IntVar()
        self.cantidad_arbol=tk.IntVar()
        self.cantidad_feature=tk.IntVar()
        self.opcionBert = tk.IntVar()
        self.opcionBert.set(0)
        self.opcionOnlyBert = tk.IntVar()
        self.opcionOnlyBert.set(0)
        self.opcion15k1_23k0 = tk.IntVar()
        self.opcion15k1_23k0.set(0)
        self.cantidad_feature_temp=tk.IntVar()
        self.opcionAvgBert = tk.IntVar()
        self.opcionAvgBert.set(0)
        self.opcionRoberta = tk.IntVar()
        self.opcionRoberta.set(0)
        self.opcionOnlyRoberta = tk.IntVar()
        self.opcionOnlyRoberta.set(0)
        self.opcionAvgSentRoberta = tk.IntVar()
        self.opcionAvgSentRoberta.set(0)
        self.opcionCrossValidation = tk.IntVar()
        self.opcionCrossValidation.set(0)

        #Pruebas - Test
        self.p1_ = []
        self.p2_ = []
        self.p3_ = []
        self.poly_ = []
        self.scaler_ = []
        self.nodos_ = []
        self.valueK_ = []
        self.caracteristicas_ = []
        self.data_cross_mae = []
        self.data_cross_mse = []
        self.data_cross_rmse = []

        # Etiquetas
        self.label_message = tk.Label(self, text=' ', font="Helvetica 10 bold")
        self.label_arboles = tk.Label(self, text='No. Trees', font="Helvetica 8 bold")
        self.label_since = tk.Label(self, text='Since', font="Helvetica 8 bold")
        self.label_distribuccion = tk.Label(self, text='Distribution Range', font="Helvetica 8 bold")
        self.label_K = tk.Label(self, text='SelectKBest (K value)', font="Helvetica 8 bold")
        self.label_result = tk.Label(self, text='name (Result File)', font="Helvetica 8 bold")
        self.label_type_system=tk.Label(self,text='Mode System:', font='Helvetica 8 bold')
        # botones
        self.btn_reference = tk.Button(self, text="File to Train (.xlsx)", width=20, fg='blue',
                                       activebackground='green', command=self.openDirectoryActual, cursor="circle")
        self.btn_referenceTest = tk.Button(self, text="File to Test (.xlsx)", width=20, fg='blue',
                                           activebackground='yellow', command=self.openDirectoryActualTest, cursor="circle")
        self.btn_verificar = tk.Button(self, text="Analyze", width=22, fg='blue',
                                       activebackground='red',      command=self.previewAnalyze, cursor="circle")
        self.btn_graficarBarras = tk.Button(self, text="Graph Error Margin", width=22, fg='blue',
                                            activebackground='gold', command=self.graficarNodo, cursor="circle")
        self.btn_graficarModel = tk.Button(self, text="Graph Model", width=22, fg='blue',
                                           activebackground="gold", command=self.graficarModel, cursor="circle")
        self.btn_save_end = tk.Button(self, text="Save Result End", width=22, fg='blue',
                                      activebackground='green', command=self.saveResultadofinal, cursor="circle")
        self.btn_campana_gaus = tk.Button(self, text="Normal Distribution (GAUSS) ", width=22, fg='blue',
                                      activebackground='white', command=self.graficaCampanGauss, cursor="circle")
        self.btn_others = tk.Button(self, text="Graph Others ", width=22, fg='blue',
                                      activebackground='white', command=self.graficaOthers, cursor="circle")
        self.btn_prueba = tk.Button(self, text="Generate Test", width=22, fg='red',
                                            activebackground='yellow', command=self.generarPrueba, cursor="circle")
        self.btn_experimento = tk.Button(self, text="Generate Experiment", width=22, fg='red',
                                            activebackground='yellow', command=self.previewAnalyzeExperiment, cursor="circle")
        #previewAnalyzeExperiment
        #self.btn_graficarBarrasAll = tk.Button(self, text="Graph Error Margin All", width=22, fg='purple',
        #                                    activebackground='blue', command=self.graficarNodo, cursor="circle")

        # Radios
        self.system_performance = tk.Radiobutton(self, text="System Performance Mode", variable=self.modo, value=3,command=self.modeSytem, cursor="circle")
        self.system_prediction = tk.Radiobutton(self, text="word prediction mode", variable=self.modo, value=4,command=self.modeSytem, cursor="circle")
        self.opSimple = tk.Radiobutton(self, text="Single-Words", variable=self.opcion, value=1, cursor="circle")
        self.opMulti = tk.Radiobutton(self, text="Multi-Words", variable=self.opcion, value=2, cursor="circle")

        # check
        self.chk_polynomialFeatures = tk.Checkbutton(self, text="Polynomial Features",
        variable=self.polynomialFeatures, onvalue=1, offvalue=0)
        self.chk_standardScaler = tk.Checkbutton(self, text="Standard Scaler",variable=self.standardScaler, onvalue=1, offvalue=0)
        self.chk_grafica1 = tk.Checkbutton(self, text="Campana Gauss curve", variable=self.tipografica1, onvalue=1, offvalue=0)
        self.chk_grafica2 = tk.Checkbutton(self, text="Campana Gauss all",variable=self.tipografica1, onvalue=2, offvalue=0)
        self.chk_bert = tk.Checkbutton(self, text="Features Bert",variable=self.opcionBert, onvalue=1, offvalue=0)
        self.chk_only_bert = tk.Checkbutton(self, text="Only Bert",variable=self.opcionOnlyBert, onvalue=1, offvalue=0)
        self.chk_avg_bert = tk.Checkbutton(self, text="Average Bert",variable=self.opcionAvgBert, onvalue=1, offvalue=0)
        self.chk_roberta = tk.Checkbutton(self, text="Features XML-RoBERTa",variable=self.opcionRoberta, onvalue=1, offvalue=0)
        self.chk_only_roberta = tk.Checkbutton(self, text="Average Token XML-RoBERTa",variable=self.opcionOnlyRoberta, onvalue=1, offvalue=0)
        self.chk_avg_roberta = tk.Checkbutton(self, text="Average Sentences XML-RoBERTa",variable=self.opcionAvgSentRoberta, onvalue=1, offvalue=0)
        self.chk_opcion_vCross = tk.Checkbutton(self, text="Cross Validation",variable=self.opcionCrossValidation, onvalue=1, offvalue=0)
        # cajas de texto
        self.entryPath = tk.Entry(self, width=60)
        self.entryPathTest = tk.Entry(self, width=60)
        self.entryTrees = tk.Entry(self, width=30,textvariable=self.cantidad_arbol)
        self.cantidad_arbol.set(100)
        self.entrySince = tk.Entry(self, width=30)
        self.entryRange = tk.Entry(self, width=30)
        self.entryK = tk.Entry(self, width=30,textvariable=self.cantidad_feature)
        if self.opcionBert.get()==0:
            self.cantidad_feature.set(15)
        else:
            if self.opcionOnlyBert.get()==0:
                if self.opcionAvgBert.get()==0:
                    self.cantidad_feature.set(791)
                else:
                    self.cantidad_feature.set(25)
            else:
                self.cantidad_feature.set(768)
        #self.cantidad_feature.set(17)
        self.path = self.createPath()
        self.resultado_name = tk.Entry(self, width=30)

        #Opciones de Lenguaje
        self.opcion_es = tk.Radiobutton(self, text="Spanish", variable=self.language, value=1, cursor="circle")
        self.opcion_en = tk.Radiobutton(self, text="English", variable=self.language, value=2, cursor="circle")
        self.init()

    def createPath(self):
        letter = os.getenv('SystemDrive')
        user = getuser()
        path = letter + '/' + 'Users/' + user + '/Desktop'
        return path

    def verificador(self):

        if len(self.entryPath.get()) > 0 and len(self.entryTrees.get()) > 0:

            if int(self.entryTrees.get()) > 0:
                self.readFile()
            else:
                self.mensaje('No. trees must be greater than zero', 2)
                self.modeSytem()

        else:
            self.mensaje('Los campos de archivos del entrenamiento y de test no deben estar vacios', 3)
            self.modeSytem()

    def init(self):
        label_back = tk.Label(self, text='< Back', fg='blue')
        label_back.bind("<Button-1>", lambda e: self.controller.show_frame('StartPage'))
        label_title = tk.Label(self, text='Word prediction', font="Helvetica 12 bold")
        label_optiones = tk.Label(self, text='Options', font="Helvetica 8 bold")
        label_back.grid(row=0, column=0, sticky=tk.W)
        label_title.grid(row=0, column=1, columnspan=3, sticky='nswe', pady=6)
        label_type_word=tk.Label(self,text='Type:',font='Helvetica 8 bold')
        self.label_type_system.grid(row=1,column=0,sticky=tk.W)
        label_type_word.grid(row=2,column=0,sticky=tk.W)
        self.opSimple.grid(row=2, column=1, sticky='we')
        self.opMulti.grid(row=2, column=2, sticky='we')
        self.system_performance.grid(row=1,column=1,sticky='we')
        self.system_prediction.grid(row=1,column=2,sticky='we')
        label_optiones.grid(row=4, column=4, sticky=tk.W, padx=2, pady=2)
        self.btn_reference.grid(row=3, column=0, columnspan=1, sticky=tk.W, padx=4, pady=2)
        self.entryPath.grid(row=3, column=1, columnspan=2,sticky=tk.W, padx=6, pady=2)
        self.btn_referenceTest.grid(row=4, column=0, columnspan=1, sticky=tk.W, padx=4, pady=2)
        self.entryPathTest.grid(row=4, column=1, columnspan=2, sticky=tk.W, padx=6, pady=2)
        self.btn_verificar.grid(row=5, column=4, sticky=tk.W, padx=2, pady=2)
        self.label_arboles.grid(row=5, column=0, sticky=tk.W, padx=4, pady=2)
        self.entryTrees.grid(row=5, column=1, sticky=tk.W, padx=4, pady=2)
        self.btn_graficarBarras.grid(row=6, column=4, sticky=tk.W, padx=2, pady=2)
        self.label_since.grid(row=6, column=0, sticky=tk.W, padx=4, pady=2)
        self.entrySince.grid(row=6, column=1, sticky=tk.W, padx=4, pady=2)
        self.chk_polynomialFeatures.grid(row=6, column=2, sticky=tk.W, padx=4, pady=2)
        self.btn_graficarModel.grid(row=7, column=4, sticky=tk.W, padx=2, pady=2)
        self.label_distribuccion.grid(row=7, column=0, sticky=tk.W, padx=4, pady=2)
        self.entryRange.grid(row=7, column=1, sticky=tk.W, padx=4, pady=2)
        self.chk_standardScaler.grid(row=7, column=2, sticky=tk.W, padx=4, pady=2)
        label_option_feature=tk.Label(self,text="Options For The Algorithm",font="Helvetica 8 bold")
        label_option_feature.grid(row=5,column=2,sticky=tk.W)
        self.chk_grafica1.grid(row=8, column=2, sticky=tk.W, padx=4, pady=2)
        label_option_define=tk.Label(self,text="Options For Neural Networks",font="Helvetica 8 bold")
        label_option_define.grid(row=9,column=1,sticky=tk.W)
        self.chk_bert.grid(row=10, column=1, sticky=tk.W, padx=4, pady=2)
        self.chk_only_bert.grid(row=11, column=1, sticky=tk.W, padx=4, pady=2)
        self.chk_avg_bert.grid(row=12, column=1, sticky=tk.W, padx=4, pady=2)
        self.chk_roberta.grid(row=10, column=2, sticky=tk.W, padx=4, pady=2)
        self.chk_only_roberta.grid(row=11, column=2, sticky=tk.W, padx=4, pady=2)
        self.chk_avg_roberta.grid(row=12, column=2, sticky=tk.W, padx=4, pady=2)
        self.chk_opcion_vCross.grid(row=10, column=0, sticky=tk.W, padx=4, pady=2)

        label_options_language = tk.Label(self, text='Language:',font="Helvetica 8 bold")
        label_options_language.grid(row=1, column=4,sticky=tk.W,padx=15)
        self.opcion_es.grid(row=2, column=4,sticky=tk.W)
        self.opcion_en.grid(row=2, column=4,sticky=tk.E)

        #self.chk_grafica2.grid(row=9, column=2, sticky=tk.W, padx=4, pady=2)
        self.btn_save_end.grid(row=8, column=4, sticky=tk.W, padx=2, pady=2)
        self.label_K.grid(row=8, column=0, sticky=tk.W, padx=4, pady=2)
        self.entryK.grid(row=8, column=1, sticky=tk.W, padx=4, pady=2)
        self.btn_campana_gaus.grid(row=9,column=4,sticky=tk.W, padx=2,pady=2)
        #self.btn_others.grid(row=9,column=4,stick=tk.W, padx=2,pady=2)
        self.btn_prueba.grid(row=10,column=4,stick=tk.W, padx=2,pady=2)
        self.btn_experimento.grid(row=11,column=4,stick=tk.W, padx=2,pady=2)
        # self.label_result.grid(row=9, column=0, sticky=tk.W, padx=4, pady=2)
        # self.resultado_name.grid(row=9,column=1, sticky=tk.W, padx=4, pady=2)
        # self.label_message.grid(row=9, column=0, sticky='nswe', padx=4, pady=2)

        self.btn_experimento['state']=tk.DISABLED

    def openDirectoryActual(self):
        directory2reference = filedialog.askopenfilename(initialdir=self.path)
        if directory2reference != self.directoryReference and directory2reference != "":
            self.directoryReference = directory2reference
            self.entryPath.delete(0, tk.END)
            self.entryPath.insert(0, self.directoryReference)

    def openDirectoryActualTest(self):
        directory2reference = filedialog.askopenfilename(initialdir=self.path)
        if directory2reference != self.directoryReferenceTest and directory2reference != "":
            self.directoryReferenceTest = directory2reference
            self.entryPathTest.delete(0, tk.END)
            self.entryPathTest.insert(0, self.directoryReferenceTest)

    def readFile(self):
        self.bloqueComponentes()
        # definimos los columnas que tomaremos del archivo que se analizar
        self.data = pd.read_excel(self.directoryReference) 
        self.data_test = pd.read_excel(self.directoryReferenceTest)
        self.model()
        

    # feature selection
    def seleccion_caracteristicas(self, X_train, y_train, X_test):
        # obtenemos el valor de k
        self.valueK = int(self.entryK.get())
        # configure to select a subset of features
        print(len(X_train))
        print(len(X_train[0]))
        print('Value K ' + str(self.valueK))
        fs = SelectKBest(score_func=f_regression, k=self.valueK)
        print("FS >> "+str(fs))
        # learn relationship from training data
        fs.fit(X_train, y_train)
        #print("J Prueba")
        #print(fs.get_support())
        # transform train input data
        X_train_fs = fs.transform(X_train)
        # transform test input data
        X_test_fs = fs.transform(X_test)
        print(">>><<<")
        return X_train_fs, X_test_fs, fs

    def model(self):
        # Caracteristicas archivo SINGLE
        # [3] abs_frecuency             [4] rel_frecuency                   [5] length
        # [6] number_syllables          [7] token_possition                 [8] number_token_sentences
        # [9] number_synonyms           [10] number_hyponyms                [11] number_hypernyms
        # [12] Part_of_speech           [13] frecuency_relative_word_before [14] frecuency_relative_word_after
        # [15] length_word_before       [16] length_word_after              [17] mtld_lexical_diversity 
        # [18] PROPN                    [19] AUX                            [20] VERB 
        # [21] ADP                      [22] NOUN                           [23] NN
        # [24] SYM                      [25] NUM                            [26] complexity              

        # Caracteristicas archivo MULTI
        # [3] abs_frecuency             [4] rel_frecuency                   [5] length
        # [6] number_syllables          [7] number_token_sentences          [8] mtld_lexical_diversity 
        # [9] number_synonyms           [10] number_hyponyms                [11] number_hypernyms
        # [12] PROPN                    [13] AUX                            [14] VERB 
        # [15] ADP                      [16] NOUN                           [17] NN
        # [18] SYM                      [19] NUM                            [20] complexity

        x_train = []
        x_test = []
        y_train = []
        self.valueK = int(self.entryK.get())
        # Opcion para palabras sueltas (single)
     
        if self.opcion.get() == 1:
            print("Opcion 1 Single >> Palabras Simples ")
            if self.opcionBert.get() ==0 and self.opcionRoberta.get() == 0:
                x_train = self.data.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]].values
                x_test = self.data_test.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]].values
                #x_train = self.data.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]].values
                #x_test = self.data_test.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]].values
                self.id_word = self.data_test.iloc[:, 1].values
                self.token_temp = self.data_test.iloc[:, 2].values
                if self.modo.get()==3:
                    self.y_test = self.data_test.iloc[:, 18].values
                    #self.y_test = self.data_test.iloc[:, 26].values
                y_train = self.data.iloc[:, 18].values
                #y_train = self.data.iloc[:, 26].values
            elif self.opcionOnlyBert.get() == 0 and self.opcionRoberta.get() == 0:
                print("Todes")
                if self.opcionAvgBert.get() == 0:
                    print("Prueba de metodo Bert")
                    #x_train = self.data.iloc[:,self.data != [1,2,26]].values
                    #x_train = self.data.iloc[:,[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]:].values
                    x_train = self.data.iloc[:,np.r_[3:26, 27:795]].values
                    print("DATA SIZE >> "+str(self.data.size))
                    print("No sale >>"+str(x_train[0]))
                    print("Len x_train >> "+str(len(x_train[0])))
                    x_test = self.data_test.iloc[:,np.r_[3:26, 27:795]].values
                    #x_test = self.data_test.iloc[:,[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]:].values
                    self.id_word = self.data_test.iloc[:, 1].values
                    self.token_temp = self.data_test.iloc[:, 2].values
                    print("SS >> "+str(self.token_temp[0]))
                    if self.modo.get()==3:
                        self.y_test = self.data_test.iloc[:, 26].values
                    y_train = self.data.iloc[:, 26].values
                else:
                    print("ENtro..")
                    x_train = self.data.iloc[:,np.r_[3:26, 27:29]].values
                    x_test = self.data_test.iloc[:,np.r_[3:26, 27:29]].values
                    print(len(x_train[0]))
                    print(x_train[0])
                    self.id_word = self.data_test.iloc[:, 1].values
                    self.token_temp = self.data_test.iloc[:, 2].values
                    if self.modo.get()==3:
                        self.y_test = self.data_test.iloc[:, 26].values
                    y_train = self.data.iloc[:, 26].values
                print("<< Fin cargar data de caracteristicas >>")
            elif self.opcionOnlyBert.get() == 1 and self.opcionRoberta.get() == 0:
                print("Prueba de metodo Only Bert")
                x_train = self.data.iloc[:,4:772].values
                print("DATA SIZE >> "+str(self.data.size))
                print("No sale >>"+str(x_train[0]))
                print("Len x_train only bert >> "+str(len(x_train[0])))
                x_test = self.data_test.iloc[:,4:772].values
                self.id_word = self.data_test.iloc[:, 1].values
                self.token_temp = self.data_test.iloc[:, 2].values
                print("SS >> "+str(self.token_temp[0]))
                if self.modo.get()==3:
                    self.y_test = self.data_test.iloc[:, 3].values
                y_train = self.data.iloc[:, 3].values
                print("<< Fin cargar data de caracteristicas Only Bert >>")
            elif self.opcionBert.get()==0 and self.opcionRoberta.get()==1:
                #Opción Solo Roberta
                if self.opcionOnlyRoberta.get() == 0 and self.opcionAvgSentRoberta.get() == 1:
                    x_train = self.data.iloc[:,np.r_[3:26, 28:29]].values
                    x_test = self.data_test.iloc[:,np.r_[3:26, 28:29]].values
                    print(len(x_train[0]))
                    print(x_train[0])
                    print("TRAIN SOLO sentence AVG")
                elif self.opcionOnlyRoberta.get() == 1 and self.opcionAvgSentRoberta.get() == 0:
                    x_train = self.data.iloc[:,np.r_[3:26, 27:28]].values
                    x_test = self.data_test.iloc[:,np.r_[3:26, 27:28]].values
                    print(self.data.iloc[:3])
                    print(len(x_train[0]))
                    print(x_train[0])
                    print("TRAIN SOLO TOKEN AVG")
                else:
                    x_train = self.data.iloc[:,np.r_[3:26, 27:29]].values
                    x_test = self.data_test.iloc[:,np.r_[3:26, 27:29]].values
                    print(len(x_train[0]))
                    print(x_train[0])
                    print("TRAIN SOLO TOKEN + sentence AVG")

                self.id_word = self.data_test.iloc[:, 1].values
                self.token_temp = self.data_test.iloc[:, 2].values
                print("Complejidad Sent: "+str(self.token_temp[0]))
                if self.modo.get()==3:
                    self.y_test = self.data_test.iloc[:, 26].values
                y_train = self.data.iloc[:, 26].values

            elif self.opcionBert.get() == 1 and self.opcionRoberta.get() == 1:
                var = 1
                #Opción Bert & Roberta
                if self.opcionAvgBert.get() == 1 and self.opcionOnlyRoberta.get() == 1 and self.opcionAvgSentRoberta.get() == 1:
                    x_train = self.data.iloc[:,np.r_[3:26, 27:31]].values
                    x_test = self.data_test.iloc[:,np.r_[3:26, 27:31]].values
                    print(len(x_train[0]))
                    print(x_train[0])
                    print("TRAIN BERT - ROBERTA SOLO TOKEN ALL + sentence ALL AVG")
                elif self.opcionAvgBert.get() == 1 and self.opcionOnlyRoberta.get() == 1 and self.opcionAvgSentRoberta.get() == 0:
                    x_train = self.data.iloc[:,np.r_[3:26, 27:30]].values
                    x_test = self.data_test.iloc[:,np.r_[3:26, 27:30]].values
                    print(len(x_train[0]))
                    print(x_train[0])
                    print("TRAIN BERT - ROBERTA SOLO TOKEN ALL + sentence Bert AVG")
                elif self.opcionOnlyBert.get() == 0 and self.opcionAvgBert.get() == 1 and self.opcionOnlyRoberta.get() == 0 and self.opcionAvgSentRoberta.get() == 1:
                    x_train = self.data.iloc[:,np.r_[3:26, 28:29,30:31]].values
                    x_test = self.data_test.iloc[:,np.r_[3:26, 28:29, 30:31]].values
                    print(len(x_train[0]))
                    print(x_train[0])
                    print("TRAIN BERT - ROBERTA SOLO sentence ALL AVG")
                elif self.opcionAvgBert.get() == 0 and self.opcionOnlyRoberta.get() == 1 and self.opcionAvgSentRoberta.get() == 0:
                    x_train = self.data.iloc[:,np.r_[3:26, 27:28,29:30]].values
                    x_test = self.data_test.iloc[:,np.r_[3:26, 27:28, 29:30]].values
                    print(len(x_train[0]))
                    print(x_train[0])
                    print("TRAIN BERT - ROBERTA SOLO TOKEN ALL AVG")
                else:
                    var = 0
                    print("No está incluido en las opciones.")

                if var == 1:
                    self.id_word = self.data_test.iloc[:, 1].values
                    self.token_temp = self.data_test.iloc[:, 2].values
                    print("Complejidad Sent: "+str(self.token_temp[0]))
                    if self.modo.get()==3:
                        self.y_test = self.data_test.iloc[:, 26].values
                    y_train = self.data.iloc[:, 26].values
        else:
            # Opcion para multi palabras
            # x_train = self.data.iloc[:, [3, 4, 5, 6, 7, 8]].values
            # x_test = self.data_test.iloc[:, [3, 4, 5, 6, 7, 8]].values
            x_train = self.data.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]].values
            x_test = self.data_test.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]].values
            self.id_word = self.data_test.iloc[:, 1].values
            self.token_temp = self.data_test.iloc[:, 2].values
            #y_train = self.data.iloc[:, 9].values
            y_train = self.data.iloc[:, 20].values #Nivel de complejidad
            if self.modo.get()==3:
                #self.y_test = self.data_test.iloc[:, 9].values
                self.y_test = self.data_test.iloc[:, 20].values

        #   Usando la implementacion de caracteristicas plinomiales == PolynomialFeatures
        if self.polynomialFeatures.get() == 1:
            poly = PolynomialFeatures(degree=2, interaction_only=True) #Verificar
            x_train = poly.fit_transform(x_train)
            x_test = poly.fit_transform(x_test)

        # Usando la implementacion del Escalado
        if self.standardScaler.get() == 1:
            sc = preprocessing.StandardScaler() #Verificar
            x_train = sc.fit_transform(x_train)
            x_test = sc.transform(x_test)
            

        # Para seleccionar cantidad d ecaracteristicas, dato se ingresa desde la interfaz
        print("Antes de las caracteristicas")
        self.x_train, self.x_test, y_train_prueba = self.seleccion_caracteristicas(x_train, y_train, x_test)       
        self.y_train = y_train
        print("Antes de la ejecución de Random Forest")
        self.algoritmoRamdomForestRegressor()
        print("Luego T")
        # except :
        #   self.mensaje('check if your selection is correct (single-words or multi-words)',3)

    def algoritmoRamdomForestRegressor(self):
        print("Inixi")
        #DataSet debe ya estar definido, la cual es self.x_train como característica y 
        #self.y_train como nivel de complejidad que ese el factor a predecir
        self.noTrees = int(str(self.entryTrees.get()))
        print(self.noTrees)
        #Defino modelo que en este es RandomForestRegressor
        # Preparamos el RandomForestRegressor con parámetros considerados
        regressor = RandomForestRegressor(n_estimators=self.noTrees, random_state=0)
        #Variable de repetición
        #cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
        #X_train, X_test, y_train, y_test = train_test_split(self.x_train, self.y_train, test_size=0.2, random_state=0)
        #Cross Validation
        mae_cross = 0
        mse_cross = 0
        rmse_cross = 0
        if self.opcionCrossValidation.get()==1:
            n_scores = cross_validate(regressor, self.x_train, self.y_train, scoring=['neg_mean_absolute_error', 'neg_mean_squared_error','neg_root_mean_squared_error'], cv=5)
            # report performance
            mae_cross = n_scores['test_neg_mean_absolute_error'].mean()
            mse_cross = n_scores['test_neg_mean_squared_error'].mean()
            rmse_cross = n_scores['test_neg_root_mean_squared_error'].mean()
        # print(n_scores)
        # print("N_scores MAE: "+str(n_scores['test_neg_mean_absolute_error']))
        # print("N_scores MAE Mean: "+str(n_scores['test_neg_mean_absolute_error'].mean()))
        # print("N_scores MAE Std: "+str(n_scores['test_neg_mean_absolute_error'].std()))
        # print("N_scores MSE: "+str(n_scores['test_neg_mean_squared_error']))
        # print("N_scores MSE Mean: "+str(n_scores['test_neg_mean_squared_error'].mean()))
        # print("N_scores MSE Std: "+str(n_scores['test_neg_mean_squared_error'].std()))
        #print('MAE: %.3f (%.3f)' % (np.mean(n_scores), np.std(n_scores)))
        # # Ajustamos el regressor con los datos de entrenamiento
        model = regressor.fit(self.x_train, self.y_train)
        # # Predecimos la complejidad mediante los datos de evaluacion
        self.y_pred = model.predict(self.x_test)
        self.new_dt=[] 
        conjunto_datos=[]
        escala_lickert=[]
      
        for i in self.y_pred:
            escala_lickert.append(lickert.scalaLickert(i))
        
        if self.modo.get()==3:
            statistical_data = '**METRICAS RANDOM FOREST REGRESSOR (RF)**' 
            statistical_data += '\nMean absolute Error ' + str(metrics.mean_absolute_error(self.y_test, self.y_pred))
            statistical_data += '\nMean Squared Error:' + str(metrics.mean_squared_error(self.y_test, self.y_pred))
            statistical_data += '\nRoot Mean Squared Error:' +  str(np.sqrt(metrics.mean_squared_error(self.y_test, self.y_pred)))
            if self.opcionCrossValidation.get()==1:
                statistical_data += '\n\n**METRICAS CROSS VALIDATION - RF**' 
                statistical_data += '\nMean absolute Error ' + str(mae_cross)
                statistical_data += '\nMean Squared Error:' + str(mse_cross)
                statistical_data += '\nRoot Mean Squared Error:' +  str(rmse_cross)
            print(self.noTrees)

            #conjunto_datos={'Id':self.id_word,'ValuePredict':self.y_pred,'ValueReal':self.y_test,'ScalaLcikert':escala_lickert}
            conjunto_datos={'Id':self.id_word,'Token':self.token_temp,'ValuePredict':self.y_pred,'ValueReal':self.y_test,'ScalaLickert':escala_lickert}
            self.new_dt = pd.DataFrame(conjunto_datos, columns = ['Id','Token','ValuePredict', 'ValueReal','ScalaLickert'])
            lickert.scalaLickert
            tk.messagebox.showinfo(message=statistical_data, title="Información")
        
        else:
            #conjunto_datos={'Id':self.id_word,'ValuePredict':self.y_pred,'ScalaLickert':escala_lickert}
            conjunto_datos={'Id':self.id_word,'Token':self.token_temp,'ValuePredict':self.y_pred,'ScalaLickert':escala_lickert}

            self.new_dt = pd.DataFrame(conjunto_datos, columns = ['Id','Token','ValuePredict','ScalaLickert'])
        
        
        #Prueba - Cargar Datos
        print("Prueba Cargar DAtos")
        if len(self.entryTrees.get()) > 0 and len(self.entrySince.get())>0 and len(self.entryRange.get())>0:
            self.noTrees = int(str(self.entryTrees.get()))
            self.noTrees = self.noTrees
            self.interval = int(str(self.entrySince.get()))
            distribuccion = int(str(self.entryRange.get()))
            data_cross_mae = []
            data_cross_mse = []
            data_cross_rmse = []

            print("CARGAR DATOS")
            for estimator in range(self.interval, self.noTrees, distribuccion):
                mae_cross = 0
                mse_cross = 0
                rmse_cross = 0
                regressor = RandomForestRegressor(
                        n_estimators=estimator, random_state=0)
                if self.opcionCrossValidation.get()==1:
                    n_scores = cross_validate(regressor, self.x_train, self.y_train, scoring=['neg_mean_absolute_error', 'neg_mean_squared_error','neg_root_mean_squared_error'], cv=5)
                    # report performance
                    mae_cross = n_scores['test_neg_mean_absolute_error']
                    mse_cross = n_scores['test_neg_mean_squared_error']
                    rmse_cross = n_scores['test_neg_root_mean_squared_error']
                regressor.fit(self.x_train, self.y_train)
                y2 = regressor.predict(self.x_test)
                    
                #print("========> "+str(estimator))
                #print("----> "+str(self.valueK))
                self.nodos_.append(estimator)
                #print('mean'+str(metrics.mean_absolute_error(self.y_test, y2)))
                #print('mse'+str(metrics.mean_squared_error(self.y_test, y2)))
                #print(('rmse '+str(np.sqrt(metrics.mean_squared_error(self.y_test, y2)))))
                self.p1_.append(metrics.mean_absolute_error(self.y_test, y2))
                self.p2_.append(metrics.mean_squared_error(self.y_test, y2))
                self.p3_.append(np.sqrt(metrics.mean_squared_error(self.y_test, y2)))
                self.valueK_.append(self.valueK)
                if self.polynomialFeatures.get() == 1:
                    self.poly_.append(1)
                    #print("Poly: 1")
                else:
                    self.poly_.append(0)
                    #print("Poly: 0")

                if self.standardScaler.get() == 1:
                    self.scaler_.append(1)
                    #print("Standard Scaler: 1")
                else:
                    self.scaler_.append(0)
                    #print("Standard Scaler: 0")
                
                if self.opcionCrossValidation.get()==1:
                    self.data_cross_mae.append(mae_cross)
                    self.data_cross_mse.append(mse_cross)
                    self.data_cross_rmse.append(rmse_cross)

            #Formar Excel
            if self.opcionCrossValidation.get()==1:
                dfs = pd.DataFrame({'No.Nodos': self.nodos_,
                                    'ValueK': self.valueK_,
                                    'polynomialFeatures': self.poly_,
                                    'standardScaler':  self.scaler_,
                                    'M.A.E.': self.p1_,
                                    'M.S.E.': self.p2_,
                                    'R.M.S.E.': self.p3_,
                                    'CValidation M.A.E.': self.data_cross_mae,
                                    'CValidation M.S.E.': self.data_cross_mse,
                                    'CValidation R.M.S.E.': self.data_cross_rmse})
            else:
                dfs = pd.DataFrame({'No.Nodos': self.nodos_,
                                    'ValueK': self.valueK_,
                                    'polynomialFeatures': self.poly_,
                                    'standardScaler':  self.scaler_,
                                    'M.A.E.': self.p1_,
                                    'M.S.E.': self.p2_,
                                    'R.M.S.E.': self.p3_})
            print(dfs)

            # Crear archivo
            #writer = pd.ExcelWriter('Experimentos.xlsx', engine='xlsxwriter')

            # Convert de dataframe and insert in document
            #df.to_excel(writer, sheet_name='Nodos', index=False)

            # Close Document
            #writer.save()
        self.saveResultadofinal()

    def saveResultadofinal(self):
        self.bloqueComponentes()
        try:
            filename = filedialog.asksaveasfilename(
                title="Save file",
                defaultextension=".xlsx",
                filetypes=(("xlsx files", "*.xlsx"),)
            )

            self.new_dt.to_excel(filename, sheet_name="result_final")
            self.mensaje('Successful analysis', 1)
            self.modeSytem()
        except:
            self.mensaje("Ocurrió un error",3)
            self.modeSytem()

    def saveResultadoExperimento(self):
        self.bloqueComponentes()
        try:
            filename = filedialog.asksaveasfilename(
                title="Save file",
                defaultextension=".xlsx",
                filetypes=(("xlsx files", "*.xlsx"),)
            )

            self.new_experiment.to_excel(filename, sheet_name="result_experimento")
            self.mensaje('Successful analysis', 1)
            self.modeSytem()
        except:
            self.mensaje("Ocurrió un error",3)
            self.modeSytem()

    def previewAnalyze(self):
        thread = threading.Thread(target=self.verificador)
        thread.start()

    def graficarNodo(self):
        self.bloqueComponentes()
        try:
            if len(self.entryTrees.get()) > 0 and len(self.entrySince.get())>0 and len(self.entryRange.get())>0:
                self.noTrees = int(str(self.entryTrees.get()))
                self.noTrees = self.noTrees
                self.interval = int(str(self.entrySince.get()))
                distribuccion = int(str(self.entryRange.get()))
                print( str(self.interval)+'\t\t'+ str(self.noTrees)+'\t\t'+ str(distribuccion))
                x = []
                y = []
                for estimator in range(self.interval, self.noTrees, distribuccion):
                    regressor = RandomForestRegressor(
                        n_estimators=estimator, random_state=0)
                    regressor.fit(self.x_train, self.y_train)
                    y2 = regressor.predict(self.x_test)
                    x.append(estimator)
                    y.append(metrics.mean_absolute_error(self.y_test, y2))
                    
                    print("========> "+str(estimator))
                    
                    print('mean'+str(metrics.mean_absolute_error(self.y_test, y2)))
                    print('mse'+str(metrics.mean_squared_error(self.y_test, y2)))
                    print(('rmse '+str(np.sqrt(metrics.mean_squared_error(self.y_test, y2)))))

                plt.plot(x, y)
                plt.xlabel('NUMBER OF TREES')
                plt.title("ERROR ABSOLUTE MARGIN")
                plt.ylabel('MAE ')
                plt.show()
            else:
                self.mensaje('Ocurrió un error, revise lo campos', 3)
            self.modeSytem()
        except:
            self.mensaje("Ocurrió un error",3)
            self.modeSytem()

    def graficarModel(self):
        self.bloqueComponentes()
        #try:
        if len(self.y_test) > 0 and len(self.y_pred) > 0 and len(self.x_test) > 0:
            x = range(len(self.x_test))
            y = self.y_test
            z = self.y_pred

            plt.scatter(x, y, c='b', alpha=1, marker='.', label='complexity') #c='b'
            plt.scatter(x, z, alpha=1, marker='.', label='Predicted' , color ='m') #c='r'
            # plt.scatter(x, r, c='g', alpha=1, marker='.', label='Corpus Complejidad')

            plt.xlabel('x')
            plt.ylabel('y')
            plt.title("Random Forest Reggresor")
            plt.grid(color='#D3D3D3', linestyle='solid')
            plt.legend(loc='lower right')
            plt.show()
            self.new_dt=[]
            self.new_dt=pd.DataFrame({'Id':self.id_word,'Token':self.token_temp,'Valor_Real':self.y_test,'Predict':self.y_pred})       
        # to_excel(self.resultado_name.get(),sheet_name='example')
            self.saveResultadofinal()
        
        else:
            self.mensaje("Tiene que analizar primero para despues graficar", 2)
        self.modeSytem()
        #except:
            #self.mensaje("Ocurrió un error",3)
            #self.modeSytem()

    def mensaje(self, texto, tipo):
        if tipo == 1:
            tk.messagebox.showinfo(message=texto, title="Information")
        if tipo == 2:
            tk.messagebox.showwarning(message=texto, title="Warning")
        if tipo == 3:
            tk.messagebox.showerror(message=texto, title="Error")

    def graficaCampanGauss(self):
        self.bloqueComponentes()
        #try: 
        tipo=True;
        if self.tipografica1.get()==1:
            sns.distplot(self.y_pred,color ='crimson', bins = 30,hist=tipo)#color='red'
            plt.show()
        else:
            x = self.y_pred
            fig, axes = plt.subplots(ncols=2, figsize=(12, 4))
            for ax in axes:
                sns.kdeplot(x, shade=False, color='crimson', ax=ax) #color='crimson'
                kdeline = ax.lines[0]
                xs = kdeline.get_xdata()
                ys = kdeline.get_ydata()
                if ax == axes[0]:
                    middle = x.mean()
                    sdev = x.std()
                    left = middle - sdev
                    right = middle + sdev
                    ax.set_title('Showing mean and sdev')
                else:
                    left, middle, right = np.percentile(x, [25, 50, 75])
                    ax.set_title('Showing median and quartiles')
                ax.vlines(middle, 0, np.interp(middle, xs, ys), color='crimson', ls=':') #color='crimson'
                ax.fill_between(xs, 0, ys, facecolor='crimson', alpha=0.2) #color='crimson'
                ax.fill_between(xs, 0, ys, where=(left <= xs) & (xs <= right), interpolate=True, facecolor='crimson', alpha=0.2) #color='crimson'
                # ax.set_tylim(ymin=0)
            plt.show()
        self.modeSytem()
        #except:
            #self.mensaje("Ocurrió un error",3)
            #self.modeSytem()

    def graficaOthers(self):
        # Gráficos
        # ==============================================================================

        # Diagnóstico errores (residuos) de las predicciones de entrenamiento
        # ==============================================================================
        y_train=self.y_test
        prediccion_train=self.y_pred
        residuos_train   = np.subtract(prediccion_train,y_train)
        fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(9, 8))

        axes[0, 0].scatter(y_train, prediccion_train, edgecolors=(0, 0, 0), alpha = 0.4)
        axes[0, 0].plot([y_train.min(), y_train.max()], [y_train.min(), y_train.max()],
                        'k--', color = 'black', lw=2)
        axes[0, 0].set_title('Valor predicho vs valor real', fontsize = 10, fontweight = "bold")
        axes[0, 0].set_xlabel('Real')
        axes[0, 0].set_ylabel('Predicción')
        axes[0, 0].tick_params(labelsize = 7)

        axes[0, 1].scatter(list(range(len(y_train))), residuos_train,
                        edgecolors=(0, 0, 0), alpha = 0.4)
        axes[0, 1].axhline(y = 0, linestyle = '--', color = 'black', lw=2)
        axes[0, 1].set_title('Residuos del modelo', fontsize = 10, fontweight = "bold")
        axes[0, 1].set_xlabel('id')
        axes[0, 1].set_ylabel('Residuo')
        axes[0, 1].tick_params(labelsize = 7)

        sns.histplot(
            data    = residuos_train,
            stat    = "density",
            kde     = True,
            line_kws= {'linewidth': 1},
            color   = "firebrick",
            alpha   = 0.3,
            ax      = axes[1, 0]
        )

        axes[1, 0].set_title('Distribución residuos del modelo', fontsize = 10,
                            fontweight = "bold")
        axes[1, 0].set_xlabel("Residuo")
        axes[1, 0].tick_params(labelsize = 7)

        
        sm.qqplot(
            residuos_train,
            fit   = True,
            line  = 'q',
            ax    = axes[1, 1], 
            color = 'firebrick',
            alpha = 0.4,
            lw    = 2
        )
        axes[1, 1].set_title('Q-Q residuos del modelo', fontsize = 10, fontweight = "bold")
        axes[1, 1].tick_params(labelsize = 7)

        axes[2, 0].scatter(prediccion_train, residuos_train,
                        edgecolors=(0, 0, 0), alpha = 0.4)
        axes[2, 0].axhline(y = 0, linestyle = '--', color = 'black', lw=2)
        axes[2, 0].set_title('Residuos del modelo vs predicción', fontsize = 10, fontweight = "bold")
        axes[2, 0].set_xlabel('Predicción')
        axes[2, 0].set_ylabel('Residuo')
        axes[2, 0].tick_params(labelsize = 7)

        # Se eliminan los axes vacíos
        fig.delaxes(axes[2,1])

        fig.tight_layout()
        plt.subplots_adjust(top=0.9)
        fig.suptitle('Diagnóstico residuos', fontsize = 12, fontweight = "bold");
        plt.show()
    
    def modeSytem(self):
        self.btn_experimento['state']=tk.DISABLED
        if self.modo.get()==3:
            self.btn_verificar['state']=tk.NORMAL
            self.btn_campana_gaus['state']=tk.NORMAL
            self.btn_graficarBarras['state']=tk.NORMAL
            self.btn_graficarModel['state']=tk.NORMAL
            self.btn_save_end['state']=tk.NORMAL 
            self.btn_campana_gaus['state']=tk.NORMAL
            self.chk_polynomialFeatures['state']=tk.NORMAL
            self.chk_standardScaler['state']=tk.NORMAL
            self.chk_grafica1['state']=tk.NORMAL
            self.chk_bert['state']=tk.NORMAL
            self.chk_only_bert['state']=tk.NORMAL
            # cajas de texto
            self.entryTrees['state']=tk.NORMAL
            self.entrySince['state']=tk.NORMAL
            self.entryRange['state']=tk.NORMAL
            self.entryK['state']=tk.NORMAL
            if self.opcionBert.get()==0:
                self.cantidad_feature.set(15)
            else:
                if self.opcionOnlyBert.get()==0:
                    if self.opcionAvgBert.get()==0:
                        self.cantidad_feature.set(791)
                    else:
                        self.cantidad_feature.set(25)
                else:
                    self.cantidad_feature.set(768)
            #self.cantidad_feature.set(17)
            self.opSimple['state']=tk.NORMAL
            self.opMulti['state']=tk.NORMAL
            self.entryPath['state']=tk.NORMAL
            self.entryPathTest['state']=tk.NORMAL
            self.system_performance['state']=tk.NORMAL
            self.system_prediction['state']=tk.NORMAL
            self.btn_reference['state']=tk.NORMAL
            self.btn_referenceTest['state']=tk.NORMAL
        else:
            self.btn_verificar['state']=tk.NORMAL
            self.btn_campana_gaus['state']=tk.DISABLED
            self.btn_graficarBarras['state']=tk.DISABLED
            self.btn_graficarModel['state']=tk.DISABLED
            self.btn_save_end['state']=tk.NORMAL 
            self.btn_campana_gaus['state']=tk.DISABLED
            self.chk_polynomialFeatures['state']=tk.DISABLED
            self.chk_standardScaler['state']=tk.DISABLED
            self.chk_grafica1['state']=tk.DISABLED
            self.chk_bert['state']=tk.DISABLED
            self.chk_only_bert['state']=tk.DISABLED
            self.opSimple['state']=tk.NORMAL
            self.opMulti['state']=tk.NORMAL
            self.entryPath['state']=tk.NORMAL
            self.entryPathTest['state']=tk.NORMAL
            # cajas de texto
            self.entryTrees['state']=tk.DISABLED
            self.entrySince['state']=tk.DISABLED
            self.entryRange['state']=tk.DISABLED
            self.entryK['state']=tk.DISABLED
            #Campos por default mejor prediccion
            self.cantidad_arbol.set(250)
            if self.opcionBert.get()==0:
                self.cantidad_feature.set(15)
            else:
                if self.opcionOnlyBert.get()==0:
                    self.cantidad_feature.set(791)
                else:
                    self.cantidad_feature.set(768)
            #self.cantidad_feature.set(15) #17 #23
            self.system_performance['state']=tk.NORMAL
            self.system_prediction['state']=tk.NORMAL
            self.btn_reference['state']=tk.NORMAL
            self.btn_referenceTest['state']=tk.NORMAL

    def bloqueComponentes(self):
        self.btn_verificar['state']=tk.DISABLED
        self.btn_campana_gaus['state']=tk.DISABLED
        self.btn_graficarBarras['state']=tk.DISABLED
        self.btn_graficarModel['state']=tk.DISABLED
        self.btn_save_end['state']=tk.DISABLED
        self.btn_experimento['state']=tk.DISABLED
        #self.btn_prueba['state']=tk.DISABLED #Borrar solo para prueba
        self.chk_polynomialFeatures['state']=tk.DISABLED
        self.chk_standardScaler['state']=tk.DISABLED
        self.chk_grafica1['state']=tk.DISABLED
        self.chk_bert['state']=tk.DISABLED
        self.chk_only_bert['state']=tk.DISABLED
        self.chk_roberta['state']=tk.DISABLED
        self.chk_bert['state']=tk.DISABLED
        self.chk_only_bert['state']=tk.DISABLED
        self.chk_avg_bert['state']=tk.DISABLED
        self.chk_avg_roberta['state']=tk.DISABLED
        self.chk_only_roberta['state']=tk.DISABLED
        # cajas de texto
        self.entryTrees['state']=tk.DISABLED
        self.entrySince['state']=tk.DISABLED
        self.entryRange['state']=tk.DISABLED
        self.entryK['state']=tk.DISABLED
        self.entryPath['state']=tk.DISABLED
        self.entryPathTest['state']=tk.DISABLED
        self.btn_reference['state']=tk.DISABLED
        self.btn_referenceTest['state']=tk.DISABLED
        self.chk_grafica1['state']=tk.DISABLED
        self.chk_grafica2['state']=tk.DISABLED
        self.system_performance['state']=tk.DISABLED
        self.system_prediction['state']=tk.DISABLED
        self.opSimple['state']=tk.DISABLED
        self.opMulti['state']=tk.DISABLED
        self.chk_opcion_vCross['state']=tk.DISABLED

    def bloqueoComponentesOnlyBert(self):
        self.chk_avg_bert['state']=tk.DISABLED
        self.chk_avg_roberta['state']=tk.DISABLED
        self.chk_only_roberta['state']=tk.DISABLED
            
    def generarPrueba1(self):
        self.bloqueComponentes()
        try:
            if len(self.entryTrees.get()) > 0 and len(self.entrySince.get())>0 and len(self.entryRange.get())>0:
                self.noTrees = int(str(self.entryTrees.get()))
                self.noTrees = self.noTrees
                self.interval = int(str(self.entrySince.get()))
                distribuccion = int(str(self.entryRange.get()))
                print( str(self.interval)+'\t\t'+ str(self.noTrees)+'\t\t'+ str(distribuccion))
                x = []
                y = []
                p1 = []
                p2 = []
                p3 = []
                poly = []
                scaler = []
                nodos = []
                valueK = []

                for estimator in range(self.interval, self.noTrees, distribuccion):
                    regressor = RandomForestRegressor(
                        n_estimators=estimator, random_state=0)
                    regressor.fit(self.x_train, self.y_train)
                    y2 = regressor.predict(self.x_test)
                    x.append(estimator)
                    y.append(metrics.mean_absolute_error(self.y_test, y2))
                    
                    print("========> "+str(estimator))
                    print("----> "+str(self.valueK))
                    nodos.append(estimator)
                    print('mean'+str(metrics.mean_absolute_error(self.y_test, y2)))
                    print('mse'+str(metrics.mean_squared_error(self.y_test, y2)))
                    print(('rmse '+str(np.sqrt(metrics.mean_squared_error(self.y_test, y2)))))
                    p1.append(metrics.mean_absolute_error(self.y_test, y2))
                    p2.append(metrics.mean_squared_error(self.y_test, y2))
                    p3.append(np.sqrt(metrics.mean_squared_error(self.y_test, y2)))
                    valueK.append(self.valueK)
                    if self.polynomialFeatures.get() == 1:
                        poly.append(1)
                        print("Poly: 1")
                    else:
                        poly.append(0)
                        print("Poly: 0")

                    if self.standardScaler.get() == 1:
                        scaler.append(1)
                        print("Standard Scaler: 1")
                    else:
                        scaler.append(0)
                        print("Standard Scaler: 0")
                #Formar Excel
                df = pd.DataFrame({'No.Nodos': nodos,
                                'ValueK': valueK,
                                'polynomialFeatures': poly,
                                'standardScaler': scaler,
                                'M.A.E.': p1,
                                'M.S.E.': p2,
                                'R.M.S.E.': p3})
                print(df)

                # Crear archivo
                writer = pd.ExcelWriter('Experimentos.xlsx', engine='xlsxwriter')

                # Convert de dataframe and insert in document
                df.to_excel(writer, sheet_name='Nodos', index=False)


                # Close Document
                writer.save()

                plt.plot(x, y)
                plt.xlabel('NUMBER OF TREES')
                plt.title("ERROR ABSOLUTE MARGIN")
                plt.ylabel('MAE ')
                plt.show()
            else:
                self.mensaje('Ocurrió un error, revise lo campos', 3)
            self.modeSytem()
        except:
            self.mensaje("Ocurrió un error",3)
            self.modeSytem()


    def generarPrueba(self):
        self.bloqueComponentes()
        try:
            #Formar Excel
            if self.opcionCrossValidation.get()==1:
                df = pd.DataFrame({'No.Nodos': self.nodos_,
                                'ValueK': self.valueK_,
                                'polynomialFeatures': self.poly_,
                                'standardScaler': self.scaler_,
                                'M.A.E.': self.p1_,
                                'M.S.E.': self.p2_,
                                'R.M.S.E.': self.p3_,
                                'CValidation M.A.E.': self.data_cross_mae,
                                'CValidation M.S.E.': self.data_cross_mse,
                                'CValidation R.M.S.E.': self.data_cross_rmse
                                })
                pr = df[['No.Nodos','ValueK','polynomialFeatures','standardScaler','M.A.E.','M.S.E.','R.M.S.E.','CValidation M.A.E.','CValidation M.S.E.','CValidation R.M.S.E.']].sort_values(['No.Nodos'],ascending=True)
                self.new_experiment = pd.DataFrame(pr, columns = ['No.Nodos','ValueK','polynomialFeatures','standardScaler','M.A.E.','M.S.E.','R.M.S.E.','CValidation M.A.E.','CValidation M.S.E.','CValidation R.M.S.E.'])
            else:
                df = pd.DataFrame({'No.Nodos': self.nodos_,
                                'ValueK': self.valueK_,
                                'polynomialFeatures': self.poly_,
                                'standardScaler': self.scaler_,
                                'M.A.E.': self.p1_,
                                'M.S.E.': self.p2_,
                                'R.M.S.E.': self.p3_})
                pr = df[['No.Nodos','ValueK','polynomialFeatures','standardScaler','M.A.E.','M.S.E.','R.M.S.E.']].sort_values(['No.Nodos'],ascending=True)
                self.new_experiment = pd.DataFrame(pr, columns = ['No.Nodos','ValueK','polynomialFeatures','standardScaler','M.A.E.','M.S.E.','R.M.S.E.'])
            print(df)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print(pr)
            self.saveResultadoExperimento()
            # # Crear archivo
            # writer = pd.ExcelWriter('ExperimentosAverageRiBert.xlsx', engine='xlsxwriter')

            # # Convert de dataframe and insert in document
            # df.to_excel(writer, sheet_name='Nodos', index=False)
            
            # # Close Document
            # writer.save()

            # x = pr['No.Nodos']
            # y = pr['M.A.E.']
            # print(x)
            # print(y)

            # plt.plot(x, y)
            # plt.xlabel('NUMBER OF TREES')
            # plt.title("ERROR ABSOLUTE MARGIN")
            # plt.ylabel('MAE ')
            # plt.show()
            # print("Generado Gráfica MAE")
            self.modeSytem()
        except:
            self.mensaje("Ocurrió un error",3)
            self.modeSytem()
    
    def graficarNodoAll(self):
        self.bloqueComponentes()
        try:
            if len(self.entryTrees.get()) > 0 and len(self.entrySince.get())>0 and len(self.entryRange.get())>0:
                self.noTrees = int(str(self.entryTrees.get()))
                self.noTrees = self.noTrees
                self.interval = int(str(self.entrySince.get()))
                distribuccion = int(str(self.entryRange.get()))
                print( str(self.interval)+'\t\t'+ str(self.noTrees)+'\t\t'+ str(distribuccion))
                x = []
                y = []
                for estimator in range(self.interval, self.noTrees, distribuccion):
                    regressor = RandomForestRegressor(
                        n_estimators=estimator, random_state=0)
                    regressor.fit(self.x_train, self.y_train)
                    y2 = regressor.predict(self.x_test)
                    x.append(estimator)
                    y.append(metrics.mean_absolute_error(self.y_test, y2))
                    
                    print("========> "+str(estimator))
                    
                    print('mean'+str(metrics.mean_absolute_error(self.y_test, y2)))
                    print('mse'+str(metrics.mean_squared_error(self.y_test, y2)))
                    print(('rmse '+str(np.sqrt(metrics.mean_squared_error(self.y_test, y2)))))

                plt.plot(x, y)
                plt.xlabel('NUMBER OF TREES')
                plt.title("ERROR ABSOLUTE MARGIN")
                plt.ylabel('MAE ')
                plt.show()
            else:
                self.mensaje('Ocurrió un error, revise lo campos', 3)
            self.modeSytem()
        except:
            self.mensaje("Ocurrió un error",3)
            self.modeSytem()

    #RESULTADOS DE EXPERIMENTOS, METODOS TEMPORALES
    def saveTestExperiment(self):
        #Prueba - Cargar Datos
        print("Prueba Cargar Datos")
        if len(self.entryTrees.get()) > 0 and len(self.entrySince.get())>0 and len(self.entryRange.get())>0:
            self.noTrees = int(str(self.entryTrees.get()))
            self.noTrees = self.noTrees+1
            self.interval = int(str(self.entrySince.get()))
            distribuccion = int(str(self.entryRange.get()))
            print("CARGAR DATOS")
            #Identificar de cuántas caracteristicas es
            featuresTemp = 0
            if self.opcionOnlyBert.get() == 1:
                featuresTemp = 768
            elif self.opcionBert.get() == 1:
                featuresTemp = 791
            elif self.opcion15k1_23k0.get() == 1:
                featuresTemp = 15
            else:
                featuresTemp = 23
            #Polynomial
            polyTemp = 0
            if self.polynomialFeatures.get() == 1:
                polyTemp = 1
            else:
                polyTemp = 0
            #Standard
            standardTemp = 0
            if self.standardScaler.get() == 1:
                standardTemp = 1
            else:
                standardTemp = 0
            varTemp = 0
            for estimator in range(self.interval, self.noTrees, distribuccion):
                varTemp=varTemp+1
                regressor = RandomForestRegressor(
                        n_estimators=estimator, random_state=0)
                regressor.fit(self.x_train, self.y_train)
                y2 = regressor.predict(self.x_test)
                    
                #print("========> "+str(estimator))
                #print("----> "+str(self.valueK))
                self.nodos_.append(estimator)
                self.p1_.append(metrics.mean_absolute_error(self.y_test, y2))
                self.p2_.append(metrics.mean_squared_error(self.y_test, y2))
                self.p3_.append(np.sqrt(metrics.mean_squared_error(self.y_test, y2)))
                self.valueK_.append(self.cantidad_feature_temp.get())
                self.caracteristicas_.append(featuresTemp)
                self.poly_.append(polyTemp)
                self.scaler_.append(standardTemp)

                if (varTemp % 30) == 0:
                    print("VarTemp >> "+str(varTemp))
                    dfsTemp = pd.DataFrame({'No.Nodos': self.nodos_,
                                            'ValueK': self.valueK_,
                                            'polynomialFeatures': self.poly_,
                                            'standardScaler':  self.scaler_,
                                            'M.A.E.': self.p1_,
                                            'M.S.E.': self.p2_,
                                            'R.M.S.E.': self.p3_,
                                            'Feautures': self.caracteristicas_})
                    pr = dfsTemp[['No.Nodos','ValueK','polynomialFeatures','standardScaler','M.A.E.','M.S.E.','R.M.S.E.','Feautures']].sort_values(['No.Nodos'],ascending=True)
                    # Crear archivo
                    writer = pd.ExcelWriter('_ExperimentosPrueba'+str(varTemp)+'_'+str(featuresTemp)+'k_Spanish.xlsx', engine='xlsxwriter')
                    # Convert de dataframe and insert in document
                    dfsTemp.to_excel(writer, sheet_name='Nodos', index=False)
                    # Close Document
                    writer.save()

            #Formar Excel
            # dfs = pd.DataFrame({'No.Nodos': self.nodos_,
            #                     'ValueK': self.valueK_,
            #                     'polynomialFeatures': self.poly_,
            #                     'standardScaler':  self.scaler_,
            #                     'M.A.E.': self.p1_,
            #                     'M.S.E.': self.p2_,
            #                     'R.M.S.E.': self.p3_})
            #print(dfs)
        
        #Prueba Procesar Datos
        #Formar Excel
            df = pd.DataFrame({'No.Nodos': self.nodos_,
                               'ValueK': self.valueK_,
                               'polynomialFeatures': self.poly_,
                               'standardScaler': self.scaler_,
                               'M.A.E.': self.p1_,
                               'M.S.E.': self.p2_,
                               'R.M.S.E.': self.p3_,
                               'Feautures': self.caracteristicas_})
            #print(df)
            pr = df[['No.Nodos','ValueK','polynomialFeatures','standardScaler','M.A.E.','M.S.E.','R.M.S.E.','Feautures']].sort_values(['No.Nodos'],ascending=True)
            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            #print(pr)
            # Crear archivo
            writer = pd.ExcelWriter('ExperimentosResultSpanish'+'_'+str(featuresTemp)+'k.xlsx', engine='xlsxwriter')

            # Convert de dataframe and insert in document
            df.to_excel(writer, sheet_name='Nodos', index=False)
            
            # Close Document
            writer.save()

            print("SaveResultExp")

    def modelExperiment(self):
        # Caracteristicas archivo SINGLE
        # [3] abs_frecuency             [4] rel_frecuency                   [5] length
        # [6] number_syllables          [7] token_possition                 [8] number_token_sentences
        # [9] number_synonyms           [10] number_hyponyms                [11] number_hypernyms
        # [12] Part_of_speech           [13] frecuency_relative_word_before [14] frecuency_relative_word_after
        # [15] length_word_before       [16] length_word_after              [17] mtld_lexical_diversity 
        # [18] PROPN                    [19] AUX                            [20] VERB 
        # [21] ADP                      [22] NOUN                           [23] NN
        # [24] SYM                      [25] NUM                            [26] complexity              

        # Caracteristicas archivo MULTI
        # [3] abs_frecuency             [4] rel_frecuency                   [5] length
        # [6] number_syllables          [7] number_token_sentences          [8] mtld_lexical_diversity 
        # [9] number_synonyms           [10] number_hyponyms                [11] number_hypernyms
        # [12] PROPN                    [13] AUX                            [14] VERB 
        # [15] ADP                      [16] NOUN                           [17] NN
        # [18] SYM                      [19] NUM                            [20] complexity

        x_train = []
        x_test = []
        y_train = []
        self.valueK = int(self.entryK.get())
        print(self.entryK.get())
        # Opcion para palabras sueltas (single)
     
        if self.opcion.get() == 1:
            print("Opcion 1 Single >> Palabras Simples ")
            if self.opcionBert.get() ==0:
                if self.opcion15k1_23k0.get() == 1:
                    x_train = self.data.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]].values
                    x_test = self.data_test.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]].values
                    self.id_word = self.data_test.iloc[:, 1].values
                    self.token_temp = self.data_test.iloc[:, 2].values
                    if self.modo.get()==3:
                        self.y_test = self.data_test.iloc[:, 26].values
                    y_train = self.data.iloc[:, 26].values
                else:
                    x_train = self.data.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]].values
                    x_test = self.data_test.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]].values
                    self.id_word = self.data_test.iloc[:, 1].values
                    self.token_temp = self.data_test.iloc[:, 2].values
                    if self.modo.get()==3:
                        self.y_test = self.data_test.iloc[:, 26].values
                    y_train = self.data.iloc[:, 26].values
            else:
                if self.opcionOnlyBert.get() ==0:
                    print("Prueba de metodo Bert")
                    x_train = self.data.iloc[:,np.r_[3:26, 27:795]].values
                    x_test = self.data_test.iloc[:,np.r_[3:26, 27:795]].values
                    self.id_word = self.data_test.iloc[:, 1].values
                    self.token_temp = self.data_test.iloc[:, 2].values
                    #print("SS >> "+str(self.token_temp[0]))
                    if self.modo.get()==3:
                        self.y_test = self.data_test.iloc[:, 26].values
                    y_train = self.data.iloc[:, 26].values
                    print("<< Fin cargar data de caracteristicas >>")
                else:
                    print("Prueba de metodo Only Bert")
                    x_train = self.data.iloc[:,27:795].values
                    x_test = self.data_test.iloc[:,27:795].values
                    self.id_word = self.data_test.iloc[:, 1].values
                    self.token_temp = self.data_test.iloc[:, 2].values
                    if self.modo.get()==3:
                        self.y_test = self.data_test.iloc[:, 26].values
                    y_train = self.data.iloc[:, 26].values
                    print("<< Fin cargar data de caracteristicas Only Bert >>")
        else:
            # Opcion para multi palabras
            # x_train = self.data.iloc[:, [3, 4, 5, 6, 7, 8]].values
            # x_test = self.data_test.iloc[:, [3, 4, 5, 6, 7, 8]].values
            x_train = self.data.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]].values
            x_test = self.data_test.iloc[:, [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]].values
            self.id_word = self.data_test.iloc[:, 1].values
            self.token_temp = self.data_test.iloc[:, 2].values
            #y_train = self.data.iloc[:, 9].values
            y_train = self.data.iloc[:, 20].values
            if self.modo.get()==3:
                #self.y_test = self.data_test.iloc[:, 9].values
                self.y_test = self.data_test.iloc[:, 20].values

        #   Usando la implementacion de caracteristicas plinomiales == PolynomialFeatures
        if self.polynomialFeatures.get() == 1:
            poly = PolynomialFeatures(degree=2, interaction_only=True) #Verificar
            x_train = poly.fit_transform(x_train)
            x_test = poly.fit_transform(x_test)

            # Usando la implementacion del Escalado
        if self.standardScaler.get() == 1:
            sc = preprocessing.StandardScaler() #Verificar
            x_train = sc.fit_transform(x_train)
            x_test = sc.transform(x_test)
            

        # Para seleccionar cantidad d ecaracteristicas, dato se ingresa desde la interfaz
        print("Antes de las caracteristicas")
        distribuccion = 59
        interval = 296 # k=355
        print(interval)
        print(self.valueK)
        print(self.cantidad_feature.get())
        for valork_temp in range(interval, self.cantidad_feature.get(), distribuccion):
            #self.cantidad_feature.get()
            #Seleccion Caracterisicas
            self.cantidad_feature_temp.set(valork_temp)
            fs = SelectKBest(score_func=f_regression, k=valork_temp)
            fs.fit(x_train, y_train)
            self.x_train = fs.transform(x_train)
            self.x_test = fs.transform(x_test)
            y_train_prueba = fs
            print("FS >> "+str(fs))
            print(">>><<<")
            #
            #self.x_train, self.x_test, y_train_prueba = self.seleccion_caracteristicas(x_train, y_train, x_test)       
            self.y_train = y_train
            print("Antes de la ejecución de Random Forest")
            self.saveTestExperiment()
            print("Luego T")
        # except :
        #   self.mensaje('check if your selection is correct (single-words or multi-words)',3)

    def readFileExperiment(self):
        self.bloqueComponentes()
        # definimos los columnas que tomaremos del archivo que se analizar
        self.data = pd.read_excel(self.directoryReference) 
        self.data_test = pd.read_excel(self.directoryReferenceTest)

        
        #15K
        # self.opcionOnlyBert.set(0)
        # self.opcionBert.set(0)
        # self.opcion15k1_23k0.set(1)
        # self.cantidad_feature.set(15)
        # self.polynomialFeatures.set(0)
        # self.standardScaler.set(0)
        # self.modelExperiment()
        # self.polynomialFeatures.set(1)
        # self.standardScaler.set(1)
        # self.modelExperiment()
        # self.polynomialFeatures.set(0)
        # self.standardScaler.set(1)
        # self.modelExperiment()
        # self.polynomialFeatures.set(1)
        # self.standardScaler.set(0)
        # self.modelExperiment()
        
        print("Termino Experimento 15k")
        #23k
        # self.opcionOnlyBert.set(0)
        # self.opcionBert.set(0)
        # self.opcion15k1_23k0.set(0)
        # self.cantidad_feature.set(23)
        # self.polynomialFeatures.set(0)
        # self.standardScaler.set(0)
        # self.modelExperiment()
        # self.polynomialFeatures.set(1)
        # self.standardScaler.set(1)
        # self.modelExperiment()
        # self.polynomialFeatures.set(1)
        # self.standardScaler.set(0)
        # self.modelExperiment()
        # self.polynomialFeatures.set(0)
        # self.standardScaler.set(1)
        # self.modelExperiment()
        print("Termino Experimento 23k")
        #OnlyBert 768k
        self.opcionOnlyBert.set(1)
        self.opcionBert.set(1)
        self.opcion15k1_23k0.set(0)
        self.cantidad_feature.set(768)
        self.polynomialFeatures.set(0)
        self.standardScaler.set(0)
        self.modelExperiment()
        self.polynomialFeatures.set(1)
        self.standardScaler.set(1)
        self.modelExperiment()
        self.polynomialFeatures.set(1)
        self.standardScaler.set(0)
        self.modelExperiment()
        self.polynomialFeatures.set(0)
        self.standardScaler.set(1)
        self.modelExperiment()
        print("Termino Experimento 768k")
        #23k + 768k Bert
        # self.opcionOnlyBert.set(0)
        # self.opcionBert.set(1)
        # self.opcion15k1_23k0.set(0)
        # self.cantidad_feature.set(791)
        # self.polynomialFeatures.set(0)
        # self.standardScaler.set(0)
        # self.modelExperiment()
        # self.polynomialFeatures.set(1)
        # self.standardScaler.set(1)
        # self.modelExperiment()
        # self.polynomialFeatures.set(1)
        # self.standardScaler.set(0)
        # self.modelExperiment()
        # self.polynomialFeatures.set(0)
        # self.standardScaler.set(1)
        # self.modelExperiment()
        print("Termino Experimento 791k")
        #15k + 768k Bert
        # self.opcionBert.set(1)
        # self.cantidad_feature.set(783)
        # self.polynomialFeatures.set(0)
        # self.standardScaler.set(0)
        # self.modelExperiment()
        # self.polynomialFeatures.set(1)
        # self.standardScaler.set(1)
        # self.modelExperiment()
        # self.polynomialFeatures.set(1)
        # self.standardScaler.set(0)
        # self.modelExperiment()
        # self.polynomialFeatures.set(0)
        # self.standardScaler.set(1)
        # self.modelExperiment()
        # print("Termino Experimento 783k")
        

    def verificadorExperiment(self):
        if len(self.entryPath.get()) > 0 and len(self.entryTrees.get()) > 0:
            if int(self.entryTrees.get()) > 0:
                self.readFileExperiment()
                print('Termino... Proceso...')
            else:
                self.mensaje('No. trees must be greater than zero', 2)
                self.modeSytem()
        else:
            self.mensaje('Los campos de archivos del entrenamiento y de test no deben estar vacios', 3)
            self.modeSytem()

    def previewAnalyzeExperiment(self):
        thread = threading.Thread(target=self.verificadorExperiment)
        thread.start()

    


           
