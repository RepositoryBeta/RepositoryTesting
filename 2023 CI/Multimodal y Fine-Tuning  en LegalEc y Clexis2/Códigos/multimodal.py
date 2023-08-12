# Instalar la biblioteca multimodal-transformers
!pip install multimodal-transformers
# Actualizar o instalar la biblioteca accelerate
!pip install --upgrade accelerate
# Instalar la biblioteca transformers y accelerate
!pip install transformers accelerate
# Opcionalmente, se puede actualizar numpy
# !pip install --upgrade numpy

# Clonar el modelo XLM-RoBERTa-Large desde Hugging Face
!git clone https://huggingface.co/xlm-roberta-large

# Importar la biblioteca para montar Google Drive
from google.colab import drive
# Montar Google Drive para acceder a los archivos
drive.mount('/content/drive')

# Importar módulos y paquetes necesarios
from dataclasses import dataclass, field
import logging
import os
from typing import Optional

import numpy as np
import pandas as pd
from transformers import (
    AutoTokenizer,
    AutoConfig,
    Trainer,
    EvalPrediction,
    set_seed
)

import sklearn.metrics as metrics
from sklearn import metrics
from math import sqrt

from transformers.training_args import TrainingArguments

# Importar funciones y clases específicas de multimodal-transformers
from multimodal_transformers.data import load_data_from_folder
from multimodal_transformers.model import TabularConfig
from multimodal_transformers.model import RobertaWithTabular
from sklearn.preprocessing import LabelEncoder
import sklearn.metrics as metrics
from sklearn import metrics
from math import sqrt

# Configurar el nivel de registro de mensajes
logging.basicConfig(level=logging.INFO)
# Deshabilitar el modo COMET para evitar conflictos (se puede ignorar si no se utiliza COMET para el seguimiento del entrenamiento)

# Ruta del archivo de datos
DATA_PATH = '/content/drive/MyDrive/Tesis/corpus/LegalEc.tsv'
# Leer el archivo tsv en un DataFrame
df = pd.read_csv(DATA_PATH, sep='\t')

# Realizar transformaciones en la columna "sentence" para eliminar comillas dobles y comillas simples
df['sentence'] = df['sentence'].str.replace('"', '').str.replace("'", '')

# Crear una nueva columna "sentence_token" combinando las columnas "sentence" y "token"
df['sentence_token'] = df.apply(
      lambda x: str(x['sentence']).lower()+ ' </s> ' + str(x['token']).lower(),
      axis=1)

# Dividir el DataFrame en conjuntos de entrenamiento, validación y prueba
train_df, val_df, test_df = np.split(df.sample(frac=1), [int(.8*len(df)), int(.9 * len(df))])
print('Num ejemplos train-val-test')
print(len(train_df), len(val_df), len(test_df))
# Guardar los DataFrames de entrenamiento, validación y prueba en archivos CSV
train_df.to_csv('train.csv')
val_df.to_csv('val.csv')
test_df.to_csv('test.csv')

# Definir una clase con argumentos para el procesamiento de datos multimodales
@dataclass
class MultimodalDataTrainingArguments:
  # Ruta al archivo CSV que contiene el conjunto de datos
  data_path: str = field(metadata={
                            'help': 'the path to the csv file containing the dataset'
                        })
  # Ruta al archivo JSON que describe las columnas de texto, categóricas, numéricas y etiquetas
  column_info_path: str = field(
      default=None,
      metadata={
          'help': 'the path to the json file detailing which columns are text, categorical, numerical, and the label'
  })

  # Diccionario que referencia las columnas de texto, categóricas, numéricas y etiquetas
  column_info: dict = field(
      default=None,
      metadata={
          'help': 'a dict referencing the text, categorical, numerical, and label columns'
                  'its keys are text_cols, num_cols, cat_cols, and label_col'
  })

  # Tipo de codificación para variables categóricas
  categorical_encode_type: str = field(default='none',
                                        metadata={
                                            'help': 'sklearn encoder to use for categorical data',
                                            'choices': ['ohe', 'binary', 'label', 'none']
                                        })
  # Método para transformar variables numéricas
  numerical_transformer_method: str = field(default='none',
                                            metadata={
                                                'help': 'sklearn numerical transformer to preprocess numerical data',
                                                'choices': ['yeo_johnson', 'box_cox', 'quantile_normal', 'none']
                                            })
  # Tarea de entrenamiento (clasificación o regresión)
  task: str = field(default="regression",
                    metadata={
                        "help": "The downstream training task",
                        "choices": ["classification", "regression"]
                    })

  # Relación entre el número de dimensiones ocultas en una capa actual y la siguiente capa MLP
  mlp_division: int = field(default=4,
                            metadata={
                                'help': 'the ratio of the number of '
                                        'hidden dims in a current layer to the next MLP layer'
                            })

  # Método para combinar características categóricas y numéricas
  combine_feat_method: str = field(default='individual_mlps_on_cat_and_numerical_feats_then_concat',
                                    metadata={
                                        'help': 'method to combine categorical and numerical features, '
                                                'see README for all the method'
                                    })
  # Ratio de dropout utilizado para las capas MLP
  mlp_dropout: float = field(default=0.5,
                              metadata={
                                'help': 'dropout ratio used for MLP layers'
                              })
  # Aplicar batch normalization a las características numéricas
  numerical_bn: bool = field(default=True,
                              metadata={
                                  'help': 'whether to use batchnorm on numerical features'
                              })
  # Usar clasificador simple o MLP como clasificador final
  use_simple_classifier: str = field(default=False,
                                      metadata={
                                          'help': 'whether to use single layer or MLP as final classifier'
                                      })
  # Función de activación para las capas de ajuste fino
  mlp_act: str = field(default='linear',
                        metadata={
                            'help': 'the activation function to use for finetuning layers',
                            'choices': ['relu', 'prelu', 'sigmoid', 'tanh', 'linear']
                        })
  # Hiperparámetro beta utilizado para el gating de datos tabulares
  gating_beta: float = field(default=0.2,
                              metadata={
                                  'help': "the beta hyperparameters used for gating tabular data "
                                          "see https://www.aclweb.org/anthology/2020.acl-main.214.pdf"
                              })

# Nombre del modelo preentrenado
model_name = 'xlm-roberta-large'

# Definir un diccionario con la información de las columnas del conjunto de datos
column_info_dict = {
    'text_cols': ['corpus','sentence_token'],
    'num_cols': ['abs_frecuency','rel_frecuency','length','number_syllables','token_possition','number_token_sentences','number_synonyms',
    'number_hyponyms','number_hypernyms','Part_of_speech','freq_relative_word_before','freq_relative_word_after','len_word_before',
    'len_word_after','mtld_diversity','propn','aux','verb','adp','noun','nn','sym','num'],
    'label_col': ['complexity']
}

# Crear una instancia de la clase MultimodalDataTrainingArguments con los argumentos específicos
data_args = MultimodalDataTrainingArguments(
    data_path='.',
    #combine_feat_method='text_only',
    combine_feat_method='concat',
    #combine_feat_method='individual_mlps_on_cat_and_numerical_feats_then_concat',
    #combine_feat_method='attention_on_cat_and_numerical_feats',
    #combine_feat_method='gating_on_cat_and_num_feats_then_sum',
    #combine_feat_method='weighted_feature_sum_on_transformer_cat_and_numerical_feats',
    column_info=column_info_dict,
    task='regression',
)

# Crear una instancia de la clase TrainingArguments con los argumentos específicos para el entrenamiento
training_args = TrainingArguments(
    output_dir="./logs/model_name",
    logging_dir="./logs/runs",
    overwrite_output_dir=True,
    do_train=True,
    do_eval=True,
    per_device_train_batch_size=32,
    num_train_epochs=10,
    evaluation_strategy='epoch',
    logging_strategy='epoch',
    logging_steps=16,
    eval_steps=5
)

# Establecer una semilla para la reproducibilidad del entrenamiento
set_seed(training_args.seed)

# Cargar el tokenizador preentrenado asociado con el modelo seleccionado
tokenizer = AutoTokenizer.from_pretrained(model_name)
print('Specified tokenizer: ', model_name)

# Cargar los conjuntos de datos de entrenamiento, validación y prueba utilizando multimodal-transformers
train_dataset, val_dataset, test_dataset = load_data_from_folder(
    data_args.data_path,
    data_args.column_info['text_cols'],
    tokenizer,
    label_col=data_args.column_info['label_col'],
    label_list = None,
    categorical_cols = None,
    numerical_cols=data_args.column_info['num_cols'],
    sep_text_token_str=' </s> ',
    categorical_encode_type = None
)

# Crear una configuración para el componente tabular del modelo
config = AutoConfig.from_pretrained(model_name)
tabular_config = TabularConfig(num_labels=1,
                               numerical_feat_dim=train_dataset.numerical_feats.shape[1],
                               **vars(data_args))
config.tabular_config = tabular_config

# Crear una instancia del modelo multimodal combinando XLM-RoBERTa-Large con características tabulares
model = RobertaWithTabular.from_pretrained(
        model_name,
        config=config
    )

# Definir una función para calcular métricas de regresión a partir de las predicciones y etiquetas
def calc_regression_metrics(p: EvalPrediction):
    predictions = p.predictions[0]
    preds = np.squeeze(predictions)
    labels = np.squeeze(p.label_ids)
    mse = metrics.mean_squared_error(labels, preds)
    rmse = sqrt(mse)
    mae = metrics.mean_absolute_error(labels, preds)
    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        'R2': metrics.r2_score(labels, preds)
    }

# Crear una instancia del objeto Trainer para entrenar el modelo
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=calc_regression_metrics
)

# Guardar el modelo entrenado en la ruta de salida especificada
OUTPUT_PATH = '/content/drive/MyDrive/Tesis/' + model_name.split('/')[-1] + '-Multimodal-' + data_args.combine_feat_method.split('/')[-1]
trainer.save_model(OUTPUT_PATH)
