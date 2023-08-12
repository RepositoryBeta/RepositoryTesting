# Instalación de las bibliotecas necesarias
!pip install --upgrade accelerate
!pip install transformers accelerate

"""SE EJECUTA EN GOOGLE COLAB PARA INSTALAR LA LIBRERIA DE TRANSFORMERS"""
#!pip install transformers

"""PARA CLONAR EL MODELO A USAR EN GOOGLE COLAB - para no estar descargando el modelo"""
!git clone https://huggingface.co/dccuchile/bert-base-spanish-wwm-uncased #768
#!git clone https://huggingface.co/xlm-roberta-base                       #768
#!git clone https://huggingface.co/PlanTL-GOB-ES/roberta-large-bne        #1024
#!git clone https://huggingface.co/xlm-roberta-large                      #1024

#SE EJECUTA EN GOOGLE COLAB para conectar con google drive
#from google.colab import drive
#drive.mount('/content/drive')

import pandas as pd   #es una biblioteca para la manipulación y el análisis de datos.
import numpy as np    #es una biblioteca para operaciones numéricas y procesamiento de matrices.
import unicodedata    #proporciona acceso a la base de datos de caracteres Unicode.
import re             #es un módulo para expresiones regulares, que se utilizan para la coincidencia de patrones y el procesamiento de texto.
import os             #proporciona una forma de utilizar la funcionalidad dependiente del sistema operativo.
import csv            #es un módulo para leer y escribir archivos CSV.

"""es una biblioteca para aprendizaje automático y modelado estadístico en Python"""
import sklearn.metrics as metrics
from sklearn import metrics, feature_selection

"""math proporciona funciones matemáticas como sqr"""
from math import sqrt

"""transformers es un paquete de Python de Hugging Face que proporciona"""
from transformers import RobertaTokenizer, RobertaForMaskedLM
from transformers import BertTokenizer, BertModel, BertForSequenceClassification, AutoTokenizer, AutoModel
from transformers import RobertaForSequenceClassification, RobertaConfig
from transformers import Trainer, TrainingArguments
from transformers import EvalPrediction
from transformers import AutoModelForMaskedLM
from transformers import AutoTokenizer

"""torch es una biblioteca de PyTorch para el cálculo de tensores con un enfoque en el aprendizaje profundo."""
from torch.utils.data import Dataset, DataLoader
import torch
import torch.nn as nn

"""SequenceClassifierOutputes un módulo de Hugging Face que define la salida de un modelo de clasificación de secuencias."""
from transformers.modeling_outputs import SequenceClassifierOutput

print("Initializing")
    #SE ESCRIBE EL DIRECTORIO DEL CORPUS A CARGAR
DATA_FILE_PATH = "/content/drive/MyDrive/Tesis/corpus/LegalEc.xlsx"

   #SE ESCRIBE EL DIRECTORIO DEL MODELO QUE SE EJECUTARÁ
#MODEL_PATH = "/content/xlm-roberta-base"       #SE USA MODELO ROBERTA-BASE PARA MULTILENGUAJE
#MODEL_PATH = "/content/roberta-large-bne"      #SE USA MODELO ROBERTA-LARGE PARA IDIOMA ESPAÑOL
#MODEL_PATH =  "/content/xlm-roberta-large"     #SE USA MODELO XLM-ROBERTA-LARGE PARA MULTILENGUAJE
MODEL_PATH =  "/content/bert-base-spanish-wwm-uncased" #SE USA MODELO bert-base-spanish-wwm-uncased PARA IDIOMA ESPAÑOL

    #SE SELECCIONA QUE TIPO DE MODELO SE EJECUTARÁ"""
MODEL_TYPE = 'bert'
#MODEL_TYPE = 'roberta'

USE_FEATURES = True    #True para ejecutar con características, False para ejecutar sin características
EPOCHS = 30           #Se escribe la cantidad de épocas que se ejecutarán

    #SE ESCRIBE EL DIRECTORIO DONDE SE GUARDARÁ EL NUEVO MODELO EJECUTADO
OUTPUT_PATH = "/content/drive/MyDrive/Tesis/" + MODEL_PATH.split('/')[-1] + str(USE_FEATURES).split('/')[-1] + str(EPOCHS).split('/')[-1] + "-finetuned"

print('Tipo de modelo:',MODEL_TYPE)
print('Modelo:',MODEL_PATH.split('/')[-1])
print('Corpus:',DATA_FILE_PATH.split('/')[-1])
print('Usa Características:',USE_FEATURES)

print("Loading data")
df = pd.read_excel(DATA_FILE_PATH)               #Lee el corpus ubicado en DATA_FILE_PATH
NUM_FEATURES = 23                                #SE ESCRIBE EL NÚMERO DE CARACTERÍSTICAS QUE TIENE EL CORPUS CARGADO
df['features'] = df.iloc[:,5:].values.tolist()   #SE ESCRIBE EL NÚMERO DE LA COLUMNA QUE EMPIEZAN LAS CARACTERÍSTICAS
#df['features'] = df.iloc[:,5:8].values.tolist()
df = df.dropna()                                 #elimina cualquier fila en el marco de datos que contenga valores faltantes

df['sentence_token'] = df.apply(                #crea una nueva columna llamada 'sentence_token'
      lambda x: str(x['sentence']).lower()      #La nueva columna se crea usando las columnas existentes 'sentence' y 'token'
      + ' </s> ' + str(x['token']).lower(),    # método 'lower() convierte ambos valores a minúsculas
      axis=1)                                   # axis=1 indica que la función debe aplicarse por filas
#print(df)
#df

#print(df)

print("Vectorizing texts")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH) #inicializa un tokenizador mediante la clase AUTOTOKENIZER -> carga un tokenizador previamente entrenado

def vectorize_text(s, max_length):

    # Unicode normalization
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')  # elimina cualquier diacrítico o acento de la cadena s
    s = re.sub(r"[^a-zA-Záéíóú.,!?;:()$€]+", r" ", s)   # reemplaza todas las coincidencias del patrón con un espacio

    '''convierte la entrada de texto sin formato en un formato numérico que se puede introducir en un modelo de aprendizaje automático'''
    input_ids = tokenizer.encode(   # utiliza el tokenizador previamente entrenado
      s,                            # para codificar una cadena "s" en sus identificadores de token correspondientes
      add_special_tokens=True,      # especifica si se agregan tokens especiales al principio y al final de la secuencia de tokens
      max_length=max_length,        # especifica la longitud máxima de la secuencia de tokens resultante
      padding='longest',            # especifica cómo rellenar secuencias más cortas a la misma longitud que la secuencia más larga.
      truncation=True,              # especifica si se truncan las secuencias que son más largas que "max_length"
      return_tensors='np'           # especifica que la salida debe devolverse como una matriz numpy.
    )
    return input_ids[0]             # devuelve solo el primer elemento de la matriz como una matriz numpy

    '''Crea una nueva columna en el DataFrame llamado 'text_vec'
    Los valores de 'text_vec' se calculan aplicando la función "vectorize_text" a la columna de la fila 'sentence_token'
    '''
df['text_vec'] = df.apply(lambda r: vectorize_text(r['sentence_token'], 512), axis=1)

#print(df)
#df

print("Creating datasets")

df = df.sample(frac=1)                    # seleccionar aleatoriamente todas las filas en el DataFrame
train_portion = 0.8                       # especifica la proporción de los datos que se usarán para el entrenamiento
split_point = int(train_portion*len(df))  # calcula el índice de la fila en la que dividir los datos en subconjuntos de entrenamiento y prueba
train_data, test_data =  df[:split_point], df[split_point:] # asigna las filas anteriores al punto de división train_data y las filas posteriores al punto de división a test_data
print(len(train_data), 'train, ', len(test_data), 'test')   # imprimen luego en la consola para indicar el número de filas en cada uno

class MyDataset(Dataset):             # define una nueva clase MyDataset que hereda de Dataset
    def __init__(self, dataframe):    # define el constructor  "__init__"  que toma un solo argumento dataframe
        #print(dataframe)
        self.len = len(dataframe)   # calcula la longitud de la entrada dataframe usando la funcion "len" y la almacena como una variable de instancia "self.len"
        self.data = dataframe       # se asigna la entrada dataframe a una variable de instancia "self.data"

    def __getitem__(self, index):   # define el método "__getitem__" que toma un solo argumento index
        ''' el metodo __getitem__ devuelve un diccionario que contiene cuatro claves: 'input_ids', 'attention_mask', 'labels'y 'added_features' '''
        input_ids = torch.tensor(self.data.text_vec.iloc[index]).cpu() # almacena las características de los datos de "text_vec" ​​que se han convertido en un vector de longitud fija.
        attention_mask = torch.ones([input_ids.size(0)]).cpu()  # attention_mask almacena los elementos de entrada que se debe prestar atención y cuáles se deben ignorar
        targets = self.data.complexity.iloc[index]              # almacena un valor escalar que representa la etiqueta de salida para la puntuación de complejidad
        added_features = self.data.features.iloc[index] if USE_FEATURES else None  #almacena las características adicionales que pueden usarse, esto solo se incluye si USE_FEATURES es True.
        return {
            'input_ids': input_ids,               # devuelve las características de entrada para el punto de datos
            'attention_mask': attention_mask,     # devuelve la máscara de atención para el punto de datos
            'labels': targets,                    # devuelve un valor escalar que representa la puntuación de complejidad
            'added_features': added_features,     # devuelve cualquier función adicional solo se incluye si USE_FEATURES es True
         }

    def __len__(self):
        return self.len   # devuelve la longitud del conjunto de datos personalizado

train_set, test_set = MyDataset(train_data), MyDataset(test_data) # train_set contiene los datos para entrenar el modelo
                                                                  # test_set  contiene los datos para evaluar el rendimiento del modelo.

print("Creating model")

def collate_batch(batch):   # recopila muestras de datos en lotes antes de enviarlos a la red neuronal
    """ Optimize memory by setting all vectors in batch to a length equal to max
        length found
    """

    def pad_sequence(in_tensor, max_size):    # toma el tensor de entrada in_tensor y lo rellena con ceros para que su longitud sea igual a max_size
        """ Fill tensor with zeros up to max_size
        """
        out_tensor = np.zeros(max_size)                     # crea un tensor de salida out_tensor de ceros con longitud max_size
        out_tensor[:in_tensor.size(0)] = in_tensor.numpy()  #copia los valores del tensor de entrada in_tensor al tensor de salida comenzando en el primer índice.
                                                            # Si el tensor de entrada es más corto que max_size, entonces las entradas restantes en el tensor de salida ya están llenas de ceros
        return out_tensor                                   # devuelve el tensor de salida

    print("BATCH SIZE:", len(batch))      # imprime el tamaño de batch, que es el número de muestras en el lote.

    batch_inputs = []                     # crea listas vacías para batch_inputs, batch_attention_masks,
    batch_attention_masks = []            # batch_targetsy batch_added_featurespara que se llenen con datos de batch
    batch_targets = []
    batch_added_features = []

    ''' llena las listas vacías creadas previamente con datos de cada muestra en el lote '''
    max_size = max([ex['input_ids'].size(0) for ex in batch])  #  calcula el tamaño máximo del tensor de entrada input_ids para la muestra con la secuencia de entrada más larga
    for item in batch:                                         # el for itera sobre cada muestra del lote y extrae sus input_ids, attention_mask y labels
        batch_inputs.append(pad_sequence(item['input_ids'], max_size))    # rellena la secuencia de entrada hasta la longitud máxima del lote
        batch_attention_masks.append(pad_sequence(item['attention_mask'], max_size))  # rellena la máscara de atención hasta la longitud máxima del lote
        batch_targets.append([float(item['labels'])])         # labels se convierte en un flotante y se envuelve en una lista con un solo elemento
        if USE_FEATURES:                                       ## Si USE_FEATURES es True
            batch_added_features.append(item['added_features']) # las funciones adicionales de cada muestra del lote se agregan a la lista batch_added_features

    input_ids = torch.tensor(np.array(batch_inputs), dtype=torch.long)    # convierte las listas batch_inputs en tensores
    attention_mask = torch.tensor(np.array(batch_attention_masks), dtype=torch.long) # convierte las listas batch_attention_masks en tensores

    labels = torch.tensor(batch_targets, dtype=torch.float)    # convierte las listas batch_targets en tensores
    if USE_FEATURES:                                           # si USE_FEATURES es True
        added_features = torch.tensor(batch_added_features, dtype=torch.float) # convierte las listas batch_added_features en tensores
    else:                                                      # de lo contrario
        added_features = None                                  # se establece added_features en None

    return {                                # devuelve como salida los datos de la función collate_batch
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels,
        "added_features": added_features
    }

class SequenceClassifierWithFeatures(nn.Module):   # se utiliza para tareas de clasificación de secuencias en las que se incluyen características adicionales
                                                   # el módulo hereda de la clase nn.Module y es la clase base para todos los módulos de redes neuronales

    def __init__(self, num_labels=1, model_path=MODEL_PATH, model_type=MODEL_TYPE): # define el método constructor del módulo SequenceClassifierWithFeatures
        """
        model_type: "bert" or "roberta"
        """
        super(SequenceClassifierWithFeatures, self).__init__() # llama al constructor de la clase principal nn.Module para inicializar el módulo SequenceClassifierWithFeatures
                                # método __init__ nos aseguramos de que el módulo de red neuronal herede las propiedades y métodos de la clase nn.Module

        ''' input_dim corresponde a la dimensionalidad de las incrustaciones de entrada para el modelo pre entrenado'''
        input_dim = 768  #El input_dim se elije dependiendo del archivo config.json del modelo a usar
        #input_dim = 1024  # 1024 USA CONFIG.JSON DE LOS MODELOS LARGE
        if USE_FEATURES:                                            #si USE_FEATURES es True
            input_dim += NUM_FEATURES                               # agrega el número de caracteristicas adicionales a la input_dim
        print("input_dim:", input_dim, USE_FEATURES, NUM_FEATURES)  # imprime el valor de input_dim, USE_FEATURES y NUM_FEATURES

        output_dim = num_labels       # output_dim sea igual al número de etiquetas en el conjunto de datos

        ''' define la arquitectura del SequenceClassifierWithFeatures'''
        self.num_labels= num_labels         # almacena el número de etiquetas para el problema
        self.problem_type='regression'      # establece el tipo de problema en "regresión"
        self.model_path = model_path        # almacene la ruta al modelo pre-entrenado el tipo de modelo
        self.model_type = model_type        # almacene la ruta al tipo de modelo
        self.base_model = AutoModel.from_pretrained(model_path, num_labels=self.num_labels) # carga el modelo previamente entrenado desde la ruta dada
                                                        #establece el número de etiquetas que se usarán en la capa final y lo almacena en self.base_model
        self.dropout = nn.Dropout(0.5)      # crea una capa de abandono con una probabilidad de abandono de 0,5
        self.dense = nn.Linear(input_dim, input_dim)    # crea una capa completamente conectada con dimensiones de entrada y salida de input_dim
        self.linear = nn.Linear(input_dim, output_dim)  # crea una capa completamente conectada con la dimensión de entrada input_dim y la dimensión de salida de output_dim
        self.loss_func = nn.MSELoss()       # establece la función de pérdida que se utilizará durante el entrenamiento en la pérdida del error cuadrático medio (MSE).


    def forward(self, input_ids=None, attention_mask=None, labels=None, added_features=None): # FOWARD calcula la pérdida y devuelve el resultado final

        outputs = self.base_model(input_ids, attention_mask=attention_mask) # pasa input_ids y attention_mask como entradas al base_model
                                                                            # y asigna las salidas resultantes a la variable outputs
        if self.model_type == "bert":   # si model_tyoe es igual a bert
            outputs = outputs[1]        # toma solo el segundo elemento de la tupla outputs
                                        #Para los modelos BERT, el primer elemento de la tupla representa la salida a nivel de secuencia
                                        #y el segundo elemento representa la salida agrupada.'''
            if USE_FEATURES:
                outputs = torch.cat((outputs, added_features), dim = -1) # concatena el tensor outputs con tensor added_features a lo largo de la última dimensión
        elif self.model_type == "roberta":
            outputs = outputs[0][:,0,:]  # toma solo el primer elemento de la tupla outputs
                                        # [:,0,:] selecciona solo el primer token  de cada secuencia de entrada
            if USE_FEATURES:
                outputs = torch.cat((outputs, added_features), dim = -1) # concatena el tensor outputs con tensor added_features a lo largo de la última dimensión
            outputs = self.dropout(outputs) # aplica regularización de abandono al tensor outputs.
            outputs = self.dense(outputs)   # pasa el tensor outputs a través de una capa completamente conectada
            outputs = torch.tanh(outputs)   # aplica la función de activación de la tangente hiperbólica (tanh) al tensor outputs.
        else:
            raise Exception('Invalid model_type: only "bert" or "roberta" models are supported')

        outputs = self.dropout(outputs) # aplica regularización de abandono al tensor outputs.
        logits = self.linear(outputs) # pasa el tensor outputs a través de una capa completamente conectada que produce los logits de salida para cada etiqueta de clase posible.

        loss = None # Inicializa la variable loss a None
        if labels is not None:  # Si el argumento labels no es None, se calcula la pérdida
          loss = self.loss_func(logits.view(-1), labels.view(-1))   # calcula la pérdida usando la función loss_func de pérdida
          print("loss:", loss)  # imprime la pérdida calculada

        return SequenceClassifierOutput(loss=loss, logits=logits)

print("Defining custom training")   # Definimos el entrenamiento personalizado

class MyTrainer(Trainer):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def get_train_dataloader(self):   # carga el conjunto de datos de entrenamiento
    return DataLoader(
        self.train_dataset,
        collate_fn=collate_batch, # procesa varias muestras de datos de entrenamiento y convertirlas en un solo lote
        batch_size=self.args.per_device_train_batch_size  # el tamaño de lote que se utilizará
                                                          # durante el entrenamiento del modelo será igual al tamaño de lote
                                                          # que se entrena en cada dispositivo de procesamiento
    )

  def get_eval_dataloader(self, eval_dataset): # carga el conjunto de datos de evaluacion
    return DataLoader(
        self.eval_dataset,
        collate_fn=collate_batch, # procesar varias muestras de datos de evaluación y convertirlas en un solo lote
        batch_size=self.args.per_device_eval_batch_size # el tamaño de lote que se utilizará
                                                        # durante la evaluacion del modelo será igual al tamaño de lote
                                                        # que se entrena en cada dispositivo de procesamiento
    )

def compute_metrics(p: EvalPrediction): # calcula diversas métricas de evaluación
    preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
                    # si es una tupla, entonces preds se establece como el primer elemento de la tupla
                    # si no es una tupla, entonces se asume que es un tensor de predicciones, y preds se establece en este tensor.
    preds = np.squeeze(preds) # elimina dimensiones de tamaño 1 del tensor de predicciones preds
    labels = np.squeeze(p.label_ids) # elimina dimensiones de tamaño 1 del y del tensor de etiqueta p.label_ids
    print("SIZES::::",labels.shape, preds.shape)
    mse = metrics.mean_squared_error(labels, preds)
    return {"MAE": metrics.mean_absolute_error(labels, preds), # error absoluto medio EVALUAR LA PRECISIÓN
            'MSE': mse,       # el error cuadrático medio PREDICCIONES MÁS PRECISAS
            'RMSE': sqrt(mse),  # la raíz del error cuadrático medio DIFERENCIA ENTRE LOS VALORES PREDICHOS POR UN MODELO Y LOS VALORES REALES
            'R2': metrics.r2_score(labels, preds)#,# coeficiente de determinación INDICA QUÉ TAN BIEN EL MODELO DE REGRESIÓN SE AJUSTA A LOS DATOS OBSERVADOS
            # 'Poisson': metrics.mean_poisson_deviance(labels, preds), # devianza de Poisson media EVALUAR LA CALIDAD
            # 'Pearson': np.corrcoef(labels, preds)[0,1]
            } # correlación de Pearson
                              # EVALUAR LA RELACIÓN ENTRE LAS PREDICCIONES DEL MODELO Y LOS VALORES REALES DE LA VARIABLE OBJETIVO


training_args = TrainingArguments(    # configuracion o argumentos de la forma en que se realizará el entrenamiento y evaluacion del modelo
    output_dir= 'output',  # Directorio de salida donde se guardarán los archivos generados durante el entrenamiento
    evaluation_strategy='epoch',  # la evaluación se realiza después de cada época
    logging_strategy='epoch', # se realizará logging después de cada época
    num_train_epochs=EPOCHS,  # número de épocas de entrenamiento que se realizarán
    remove_unused_columns=False,  # se eliminarán las columnas no utilizadas en los datos de entrenamiento y evaluación
    per_device_train_batch_size=32, # Tamaño del lote de entrenamiento por dispositivo
    per_device_eval_batch_size=32,  # Tamaño del lote de evaluación por dispositivo
)

model = SequenceClassifierWithFeatures(model_path=MODEL_PATH, model_type=MODEL_TYPE)


trainer = MyTrainer(
    model=model,  # modelo que se entrenará.
    args=training_args, # argumentos de entrenamiento y evaluación que se utilizarán durante el proceso de entrenamiento y evaluación
    train_dataset=train_set,  # conjunto de datos de entrenamiento
    eval_dataset=test_set,  # conjunto de datos de evaluación
    compute_metrics=compute_metrics  # calcula las métricas de evaluación.
)

print("Training")
trainer.train()

print("Saving model")
if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)
trainer.save_model(OUTPUT_PATH)


# SE USA PARA QUE SE GUARDE UN ARCHIVO LLAMADO trainer_state.json DONDE SE GUARDAN LOS VALORES DE LAS METRICAS
"""
def save_state(self):

    if not self.is_world_process_zero():
        return

    path = os.path.join(self.args.output_dir, "trainer_state.json")
    self.state.save_to_json(path)

trainer.save_state()
"""