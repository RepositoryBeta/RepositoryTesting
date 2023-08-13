from tkinter import *
import tkinter as tk
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
import seaborn as sn
from sklearn import metrics
from tkinter import filedialog
from tkinter import filedialog as fd
import os
from tkinter import ttk
from tkinter.messagebox import showinfo
from sklearn.linear_model import PassiveAggressiveRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
import seaborn as sn
from sklearn.ensemble import BaggingRegressor
from sklearn.datasets import make_regression
from sklearn.ensemble import VotingRegressor
from sklearn.ensemble import RandomForestRegressor


fields = ('N° Características', 'Valor Base Matriz de confusión', 'Nodos', 'Máximo de Iteraciones')


class Regresiones():
    def __init__(self):
        self.x_train = []
        self.x_test = []
        self.y_train = []
        self.y_test = []
        self.y_pred = []
        self.dataset = []
        self.datasetwo = []
        self.filename = None
        self.filenamet = None
        self.valuek = int
        self.nodos = float
        self.maxiteracc = int
        self.valconf = float
        self.maxiterc = int
        self.seleccion = str
        self.confmat = []
        self.absolutoMedio = float
        self.cuadradoMedio = float
        self.raizMedioCuadrado = float
        self.variable_Seteo = []
        self.datas = []
        self.independent_variables = []
        self.dependent_variable = str
        self.independent_variablestwo = []
        self.dependent_variabletwo = str
        self.contador = int

    def LeerArchivo(self):
        # definimos los columnas que tomaremos del archivo que se analizar
        print('por dataset')
        self.dataset = pd.read_csv(self.filename)
        print(len(self.dataset))
        # se imprime el número de elementos
        print(self.dataset.head())
        # oki = self.data_test
        print(self.dataset.describe())
        return self.dataset

    def LeerArchivotwo(self):
        print('por datasetwo')
        self.datasetwo = pd.read_csv(self.filenamet)
        print(len(self.datasetwo))
        # se imprime el número de elementos
        print(self.datasetwo.head())
        # oki = self.data_test
        print(self.datasetwo.describe())
        return self.datasetwo

    def CargarArchivo(self):
        self.filename = filedialog.askopenfilename(filetypes=(("Archivo csv", "*.csv"),))
        print(self.filename)
        self.LeerArchivo()

    def CargarArchivotwo(self):
        self.filenamet = fd.askopenfilename(filetypes=(("Archivo csv", "*.csv"),))
        print(self.filenamet)
        self.LeerArchivotwo()

    def columnasArchivo(self):
        if self.filename:
            self.dependent_variable = 'complexity'
            self.independent_variables = self.dataset.columns.tolist()
            self.independent_variables.remove('Order')
            self.independent_variables.remove('id')
            self.independent_variables.remove('token')
            self.independent_variables.remove(self.dependent_variable)
            variable_Seteo = self.independent_variables
            print(variable_Seteo)
            self.contadorTrain()
            self.valuektrain = self.contador
            print("Número de elementos en x_train: ", self.valuektrain)
        if self.filenamet:
            self.dependent_variabletwo = 'complexity'
            self.independent_variablestwo = self.datasetwo.columns.tolist()
            self.independent_variablestwo.remove('Order')
            self.independent_variablestwo.remove('id')
            self.independent_variablestwo.remove('token')
            self.independent_variablestwo.remove(self.dependent_variabletwo)
            variable_Seteo = self.independent_variablestwo
            print(variable_Seteo)
            self.contadorTest()
            self.valuektest = self.contador
            print("Número de elementos en x_test: ", self.valuektest)

    def SelectKBest(self):
        if not self.filename:
            showinfo(
                title='Error',
                message="Por favor cargue el archivo train"
            )
            return
        if not self.filenamet:
            showinfo(
                title='Error',
                message="Por favor cargue el archivo test"
            )
            return
        self.columnasArchivo()
        if self.valuektest > self.valuektrain:
            showinfo(
                title='Error',
                message='Archivo test no concuerda con el Archivo train'
            )
            return
        if self.valuektrain > self.valuektest:
            showinfo(
                title='Error',
                message='Archivo train no concuerda con el Archivo test'
            )
            return
        if self.valuek > self.valuektrain:
            showinfo(
                title='Error',
                message='El valor de ingreso de número de características sobrepasa a las columnas de los archivos'
            )
            return
        self.x_train = self.dataset[self.independent_variables].values
        self.x_test = self.datasetwo[self.independent_variablestwo].values
        self.y_test = self.datasetwo[self.dependent_variabletwo].values
        self.y_train = self.dataset[self.dependent_variable].values
        # # ignorar mensajes de division de np
        np.seterr(divide='ignore', invalid='ignore')
        fs = SelectKBest(score_func=f_regression, k=self.valuek)
        print('selec', fs)
        fs.fit(self.x_train, self.y_train)
        print(fs.get_support())
        # transform train input data
        self.x_train = fs.transform(self.x_train)
        # transform test input datzzza
        self.x_test = fs.transform(self.x_test)
        self.Algoritmos()

    def Algoritmos(self):
        if self.seleccion == 'Ada':
            print('ejecuto AdaBoostRegressor')
            regressor = AdaBoostRegressor(DecisionTreeRegressor(), n_estimators=self.nodos, random_state=0)
        if self.seleccion == 'Dt':
            print('ejecuto DecisionTreeRegressor')
            regressor = DecisionTreeRegressor(random_state=0)
        if self.seleccion == 'Rf':
            print('ejecuto RandomForestRegressor')
            regressor = RandomForestRegressor(n_estimators=self.nodos, random_state=0)
        if self.seleccion == 'Lr':
            print('ejecuto LinearRegression')
            regressor = LinearRegression()
        if self.seleccion == 'Pa':
            print('ejecuto PassiveAggressiveRegressor')
            regressor = make_pipeline(StandardScaler(),
                                      PassiveAggressiveRegressor(max_iter=self.maxiteracc, random_state=0, tol=1e-3))
        if self.seleccion == 'Sg':
            print('ejecuto SGDRegressor')
            regressor = make_pipeline(StandardScaler(),
                                      SGDRegressor(max_iter=self.maxiteracc, random_state=0))
        if self.seleccion == 'Svr':
            print('ejecuto SVR')
            regressor = SVR()
        if self.seleccion == 'Gr':
            print('ejecuto GradientBoostingRegressor')
            regressor = GradientBoostingRegressor(n_estimators=self.nodos,
                                                  random_state=0)
        if self.seleccion == 'Kn':
            print('ejecuto KNeighborsRegressor')
            regressor = KNeighborsRegressor(algorithm='auto', n_neighbors=5)

        if self.seleccion == 'vo':
            print('ejecuto vo')
            regressorada = AdaBoostRegressor(DecisionTreeRegressor(), n_estimators=self.nodos, random_state=0)
            regressordt = DecisionTreeRegressor(random_state=0)
            regressorrf = RandomForestRegressor(n_estimators=self.nodos, random_state=0)
            regressorada.fit(self.x_train, self.y_train)
            regressordt.fit(self.x_train, self.y_train)
            regressorrf.fit(self.x_train, self.y_train)
            pred1 = regressorada.predict(self.x_train)
            pred2 = regressordt.predict(self.x_train)
            pred3 = regressorrf.predict(self.x_train)
            regressor = VotingRegressor(estimators=[('ada', regressorada), ('dt', regressordt), ('rf', regressorrf)])
        # corro el entrenamiento
        regressor.fit(self.x_train, self.y_train)
        # realizo la prediccion con mi data
        self.y_pred = regressor.predict(self.x_test)
        if self.seleccion == 'Svr' or self.seleccion == 'Lr' or self.seleccion == 'Pa' or self.seleccion == 'Sg':
            # evaluo los valores de la prediccion desde el max al min 0.2 Linerar
            self.y_pred = np.maximum(self.y_pred, 0.2)
        y_pred_conf = np.zeros_like(self.y_pred)
        # añado un 1 si se pasa del valor base de confusion
        y_pred_conf[self.y_pred > self.valconf] = 1
        # inicializo una matriz llena de ceros segun y_test
        y_test_conf = np.zeros_like(self.y_test)
        # añado un 1 si se pasa del valor base de confusion
        y_test_conf[self.y_test > self.valconf] = 1
        data = {'Actual': y_test_conf,
                'Predicho': y_pred_conf
                }
        df = pd.DataFrame(data, columns=['Actual', 'Predicho'])
        self.confmat = confusion_matrix(df['Actual'], df['Predicho'])
        # imprimo la matriz de confusion
        print(self.confmat)
        print('Mean Absolute Error:', metrics.mean_absolute_error(self.y_test, self.y_pred))
        print('Mean Squared Error:', metrics.mean_squared_error(self.y_test, self.y_pred))
        print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(self.y_test, self.y_pred)))
        # guardo en variables los errores
        self.absolutoMedio = metrics.mean_absolute_error(self.y_test, self.y_pred)
        self.cuadradoMedio = metrics.mean_squared_error(self.y_test, self.y_pred)
        self.raizMedioCuadrado = np.sqrt(metrics.mean_squared_error(self.y_test, self.y_pred))
        if self.seleccion != 'vo':
            self.graficos()
            self.generaexcel()
        if self.seleccion == 'vo':
            print('ejecuto vo grafico')
            plt.figure()
            plt.plot(pred1, 'gd', label='AdaBoostRegressor')
            plt.plot(pred2, 'b^', label='DecisionTreeRegressor')
            plt.plot(pred3, 'ys', label='RandomForestRegressor')
            plt.plot(self.y_pred, 'r*', ms=10, label='VotingRegressor')

            plt.tick_params(axis='x', which='both', bottom=False, top=False,
                            labelbottom=False)
            plt.ylabel('predicho')
            plt.xlabel('entrenamiento')
            plt.legend(loc="best")
            plt.title('Predicciones de regresores y su promedio')
            plt.show()
            self.graficos()
            self.generaexcel()

    def graficos(self):
        sn.heatmap(self.confmat, annot=True)
        plt.show()
        # verdaderos positivos TP | falsos positivos FP
        # falsos negativos 	  FN | verdaderos negativos TN

        # imprimpro los valores en un dataset sobre lo entrenado
        df = pd.DataFrame({'Actual': self.y_test, 'Predicho': self.y_pred})
        print(df)
        x = range(len(self.x_test))
        y = self.y_test
        z = self.y_pred

        plt.scatter(x, y, c='b', alpha=1, marker='.', label='complexity')
        plt.scatter(x, z, c='r', alpha=1, marker='.', label='Predicted')

        plt.xlabel('x')
        plt.ylabel('y')
        if self.seleccion == 'Ada':
            plt.title("AdaBoostRegressor")
        if self.seleccion == 'Dt':
            plt.title("DecisionTreeRegressor")
        if self.seleccion == 'Rf':
            plt.title("RandomForestRegressor")
        if self.seleccion == 'Lr':
            plt.title("Linear Regressor")
        if self.seleccion == 'Pa':
            plt.title("PassiveAggressiveRegressor")
        if self.seleccion == 'Sg':
            plt.title("SGDRegressor")
        if self.seleccion == 'Svr':
            plt.title("SVR")
        if self.seleccion == 'Gr':
            plt.title("GradientBoostingRegressor")
        if self.seleccion == 'Kn':
            plt.title("KNeighborsRegressor")
        if self.seleccion == 'vo':
            plt.title("Ensemble Method")
        plt.grid(color='#D3D3D3', linestyle='solid')
        plt.legend(loc='lower right')
        plt.show()
        prediccion_train = self.y_pred
        residuos_train = np.subtract(prediccion_train, self.y_test)
        fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9, 8))
        axes.scatter(self.y_test, prediccion_train, edgecolors=(0, 0, 0), alpha=0.4)
        axes.plot([self.y_test.min(), self.y_test.max()], [self.y_test.min(), self.y_test.max()],
                  color='black', lw=1)
        axes.set_title('Valor predicho vs valor real', fontsize=10, fontweight="bold")
        axes.set_xlabel('Real')
        axes.set_ylabel('Predicción')
        axes.tick_params(labelsize=7)
        plt.show()

    def generaexcel(self):
        self.datas = self.dataset
        filtro = self.datas['Order'] <= len(self.y_pred)
        self.datas = self.datas[filtro]
        self.datas = self.datas.drop(columns=self.variable_Seteo)
        self.datas.insert(loc=4,
                          column='Prediccion',
                          value=self.y_pred)
        # Crear archivo
        if self.seleccion == 'Ada':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_AdaBoostRegressor.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Dt':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_DecisionTreeRegressor.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Rf':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_RandomForestRegressor.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Lr':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_LinearRegressor.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Pa':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_PassiveAggressiveRegressor.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Sg':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_SGDRegressor.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Svr':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_SVR.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Gr':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_GradientBoostingRegressor.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Kn':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_KNeighborsRegressor.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'vo':
           writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_VotingRegressor.xlsx',
                                  engine='xlsxwriter')
        # Convert de dataframe and insert in document
        self.datas.to_excel(writer, sheet_name='Result_test', index=False)
        # Close Document
        writer.save()
        valores = []
        poly = []
        scaler = []
        valores_ = []
        carateristicas = []
        errorMedio = []
        errorMedio = self.absolutoMedio
        valores = self.valuek
        carateristicas = 0
        scalar = 0
        valores_.append(valores)
        if carateristicas == 1:
            poly.append(1)
        else:
            poly.append(0)
        if scalar == 1:
            scaler.append(1)
        else:
            scaler.append(0)
        # Formar Excel
        df = pd.DataFrame({'ValueK': valores_,
                           'polynomialFeatures': poly,
                           'standardScaler': scaler,
                           'M.A.E.': errorMedio,
                           'M.S.E.': self.cuadradoMedio,
                           'R.M.S.E.': self.raizMedioCuadrado})
        print(df)
        # Crear archivo
        if self.seleccion == 'Ada':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_AdaBoostRegressor_errores.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Dt':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_DecisionTreeRegressor_errores.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Rf':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_RandomForestRegressor_errores.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Lr':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_LinearRegressor_errores.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Pa':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_PassiveAggressiveRegressor_errores.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Sg':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_SGDRegressor_errores.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Svr':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_SVR_errores.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Gr':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_GradientBoostingRegressor_errores.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'Kn':
            writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_KNeighborsRegressor_errores.xlsx',
                                    engine='xlsxwriter')
        if self.seleccion == 'vo':
           writer = pd.ExcelWriter('C:/Users/lisse/Desktop/TESIS/result_test_VotingRegressor_errores.xlsx',
                                  engine='xlsxwriter')
        # Convert de dataframe and insert in document
        df.to_excel(writer, sheet_name='Data', index=False)
        # Close Document
        writer.save()

    def validaentradas(self, entradas):
        try:
            self.valuek = int(entradas['N° Características'].get())
            self.valconf = float(entradas['Valor Base Matriz de confusión'].get())
            self.nodos = int(entradas['Nodos'].get())
            self.maxiteracc = int(entradas['Máximo de Iteraciones'].get())
            self.seleccion = selected_size.get()
            if not self.seleccion:
                showinfo(
                    title='Error',
                    message="Por favor seleccione un algoritmo a ejecutar"
                )
                return
            else:
                if self.seleccion == 'Ada' or self.seleccion == 'Gr' or self.seleccion=='Rf':
                    if 0 < self.valuek:
                        pass
                    else:
                        showinfo(
                            title='Error',
                            message="Por favor ingrese un valor mayor a 0 para N° Características"
                        )
                        return
                    if 0.01 <= self.valconf <= 1:
                        pass
                    else:
                        showinfo(
                            title='Error',
                            message="Por favor ingrese valores desde 0.01 a 1 para Valor Base Matriz de confusión"
                        )
                        return
                    if 0 < self.nodos:
                        pass
                    else:
                        showinfo(
                            title='Error',
                            message="Por favor ingrese valores positivos para los Nodos"
                        )
                        return
                    if not self.maxiteracc:
                        pass
                    else:
                        showinfo(
                            title='Error',
                            message="Este algoritmo no necesita Máximo de Iteraciones, por favor coloque 0"
                        )
                        return
                if self.seleccion == 'Dt' or self.seleccion =='Lr' or self.seleccion =='Svr' or self.seleccion =='Kn':
                    if 0 < self.valuek:
                        pass
                    else:
                        showinfo(
                            title='Error',
                            message="Por favor ingrese un valor mayor a 0 para N° Características"
                        )
                        return
                    if 0.01 <= self.valconf <= 1:
                        pass
                    else:
                        showinfo(
                            title='Error',
                            message="Por favor ingrese valores desde 0.01 a 1 para Valor Base Matriz de confusión"
                        )
                        return
                    if 0 < self.nodos:
                        showinfo(
                            title='Error',
                            message="Este algoritmo no necesita Nodos, por favor coloque 0"
                        )
                        return
                    if 0 < self.maxiteracc:
                        showinfo(
                            title='Error',
                            message="Este algoritmo no necesita Máximo de Iteraciones, por favor coloque 0"
                        )
                        return
                if self.seleccion == 'Pa' or self.seleccion == 'Sg':
                    if 0 < self.valuek:
                        pass
                    else:
                        showinfo(
                            title='Error',
                            message="Por favor ingrese un valor mayor a 0 para N° Características"
                        )
                        return
                    if 0.01 <= self.valconf <= 1:
                        pass
                    else:
                        showinfo(
                            title='Error',
                            message="Por favor ingrese valores desde 0.01 a 1 para Valor Base Matriz de confusión"
                        )
                        return
                    if 0 < self.maxiteracc:
                        pass
                    else:
                        showinfo(
                            title='Error',
                            message="Por favor ingrese valores positivos para el Máximo de Iteraciones"
                        )
                        return
                    if 0 < self.nodos:
                        showinfo(
                            title='Error',
                            message="Este algoritmo no necesita Nodos, por favor coloque 0"
                        )
                        return
                self.SelectKBest()
        except ValueError:
            showinfo(
                title='Error',
                message="Por favor no deben haber: valores no enteros con excepción de Valor Base Matriz de confusión, vacios o no numéricos")

    def contadorTrain(self):
        self.contador = 0
        for c in self.independent_variables:
            self.contador += 1
        return self.contador

    def contadorTest(self):
        self.contador = 0
        for c in self.independent_variablestwo:
            self.contador += 1
        return self.contador


def crearcajas(root, fields):
    entradas = {}
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=40, text=field + ": ", anchor='w')
        ent = Entry(row)
        ent.insert(0, "0")
        row.pack(side=TOP, fill=X, padx=15, pady=15)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entradas[field] = ent
    return entradas


root = tk.Tk()
root.wm_title("Corpus")
v = tk.IntVar()
# llamo a la clase
calcular = Regresiones()
ents = crearcajas(root, fields)
root.bind('<Return>', (lambda event, e=ents: fetch(e)))
label = ttk.Label(text="Seleccione el algoritmo")
label.pack(fill='x', padx=160, pady=10)
selected_size = tk.StringVar()
sizes = (('AdaBoostRegressor', 'Ada'),
         ('DecisionTree', 'Dt'),
         ('RandomForest', 'Rf'),
         ('LinearRegressor', 'Lr'),
         ('SGDRegressor', 'Sg'),
         ('Svr', 'Svr'),
         ('PassiveAggresiveRegressor', 'Pa'),
         ('GradientBoostingRegressor', 'Gr'),
         ('KNeighborsRegressor', 'Kn'),
         ('Method Voting', 'vo'))
# radio buttons
for size in sizes:
    r = ttk.Radiobutton(
        root,
        text=size[0],
        value=size[1],
        variable=selected_size
    )
    r.pack(fill='x', padx=70, pady=5)
b1 = tk.Button(root, text='Cargar Train', command=calcular.CargarArchivo)
b1.pack(fill='x', padx=15, pady=5)
b2 = tk.Button(root, text='Cargar Test', command=calcular.CargarArchivotwo)
b2.pack(fill='x', padx=15, pady=5)
b3 = Button(root, text='Ejecutar',
            command=(lambda e=ents: calcular.validaentradas(e)))
b3.pack(fill='x', padx=15, pady=5)
b4 = Button(root, text='Terminar', command=root.quit)
b4.pack(fill='x', padx=15, pady=5)
root.mainloop()