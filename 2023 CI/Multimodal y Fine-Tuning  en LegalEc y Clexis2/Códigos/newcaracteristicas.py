

**FRECUENCY NORMALIZADA**
"""

import pandas as pd

DATA_PATH = '/content/LegalEc.tsv'
data = pd.read_csv(DATA_PATH, sep='\t')

for index, row in data.iterrows():
    palabra = str(row['token'])
    oracion = str(row['sentence'])
    palabras_oracion = oracion.split()
    total_palabras = len(palabras_oracion)
    frecuencia_palabra = palabras_oracion.count(palabra) / total_palabras
    #print(f"Frecuencia normalizada de la palabra '{palabra}': {frecuencia_palabra}")

"""**NUM_SENSES NORMALIZADO**"""

!pip install nltk scikit-learn

import nltk
from nltk.corpus import wordnet
import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale

# Descargar los datos adicionales de WordNet
nltk.download('wordnet')

# Cargar los datos desde un archivo CSV (ejemplo: data.csv)
data = pd.read_csv(DATA_PATH, sep='\t')

# Crear una nueva columna llamada "num_senses" para almacenar el número de sentidos de cada palabra
data['num_senses'] = 0

# Iterar sobre cada fila y calcular el número de sentidos de la palabra en la columna "token"
for index, row in data.iterrows():
    token = row['token']
    if isinstance(token, str):  # Verificar si el valor es una cadena de texto
        word = token.lower()  # Convertir a minúsculas
        synsets = wordnet.synsets(word)
        num_senses = len(synsets)
        data.at[index, 'num_senses'] = num_senses
    else:  # Si no es una cadena de texto, asignar un valor predeterminado (por ejemplo, -1)
        data.at[index, 'num_senses'] = -1

# Normalizar la columna "num_senses" utilizando la normalización min-max
data['normalized_num_senses'] = minmax_scale(data[['num_senses']])
normalized_num_senses = data['normalized_num_senses']

# Imprimir el DataFrame actualizado
#print(data)

"""**NUMERO DE MORFEMAS NORMALIZADO**"""

!pip install -U spacy
!python -m spacy download en_core_web_sm
!python -m spacy download es_core_news_sm

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import spacy

# Cargar modelos de lenguaje para inglés y español
nlp_en = spacy.load('en_core_web_sm')
nlp_es = spacy.load('es_core_news_sm')

# Función para contar los morfemas en una palabra
def contar_morfemas(palabra):
    doc = nlp_en(palabra)
    num_morfemas_en = len(doc)

    doc = nlp_es(palabra)
    num_morfemas_es = len(doc)

    if num_morfemas_en <= num_morfemas_es:
        return num_morfemas_en, 'en'
    else:
        return num_morfemas_es, 'es'

# Cargar el archivo CSV
data = pd.read_csv(DATA_PATH, sep='\t')

# Crear una nueva columna para almacenar el número de morfemas
data['numero_morfemas'] = 0
data['idioma'] = ''

# Iterar sobre cada fila y contar los morfemas
for index, row in data.iterrows():
    palabra = row['token']

    if isinstance(palabra, str):  # Verificar si es una cadena de texto
        num_morfemas, idioma = contar_morfemas(palabra)
    else:
        num_morfemas, idioma = 0, ''

    data.at[index, 'numero_morfemas'] = num_morfemas
    data.at[index, 'idioma'] = idioma

# Normalizar el número de morfemas utilizando Min-Max Scaling
scaler = MinMaxScaler()
data['numero_morfemas_normalizado'] = scaler.fit_transform(data['numero_morfemas'].values.reshape(-1, 1))
numero_morfemas_normalizado = data['numero_morfemas_normalizado']
# Imprimir el DataFrame actualizado
#print(data)

"""**FRECUENCIA DE CONSONANTES EN LA PALABRA OBJETIVO**"""

import pandas as pd

def calcular_frecuencia_consonantes(palabra):
    consonantes = set("bcdfghjklmnñpqrstvwxyz")  # Conjunto de consonantes en el alfabeto
    num_consonantes = sum(1 for letra in str(palabra).lower() if letra in consonantes)
    return num_consonantes

def normalizar_frecuencia_consonantes(palabra):
    if isinstance(palabra, str):
        palabra = palabra.lower()
        if len(palabra) == 0:
            return 0.0
        num_consonantes = calcular_frecuencia_consonantes(palabra)
        return num_consonantes / len(palabra)
    return 0.0

data = pd.read_csv(DATA_PATH, sep='\t')

# Agregamos una nueva columna llamada "frec_consonantes" para almacenar los resultados
data["frec_consonantes"] = 0

# Iteramos sobre cada fila y calculamos la frecuencia de consonantes para la palabra en la columna "token"
for index, row in data.iterrows():
    palabra = row["token"]
    frecuencia_consonantes = calcular_frecuencia_consonantes(palabra)
    data.at[index, "frec_consonantes"] = frecuencia_consonantes

# Agregamos una nueva columna llamada "frec_consonantes_normalizada" para almacenar los resultados normalizados
data["frec_consonantes_normalizada"] = data["token"].apply(normalizar_frecuencia_consonantes)
frec_consonantes_normalizada = data['frec_consonantes_normalizada']

#print(data)

"""**CONTAR MAYUSCULAS EN LA ORACION**"""

import pandas as pd

def contar_letras_mayusculas(oracion):
    contador = 0
    for letra in oracion:
        if letra.isupper():
            contador += 1
    return contador

def normalizar(cantidad_mayusculas, total_letras):
    if total_letras == 0:
        return 0
    return cantidad_mayusculas / total_letras

# Leer el archivo .tsv usando pandas
data = pd.read_csv(DATA_PATH, sep='\t')

# Nombre del archivo .tsv y el nombre de la columna que contiene las oraciones
nombre_columna_oracion = 'sentence'

# Asegurarnos de que la columna 'oracion' sea de tipo str (cadena)
data[nombre_columna_oracion] = data[nombre_columna_oracion].astype(str)

# Calcular la cantidad de letras mayúsculas y total de letras en cada oración
data['cantidad_mayusculas'] = data[nombre_columna_oracion].apply(contar_letras_mayusculas)
data['total_letras'] = data[nombre_columna_oracion].apply(len)

# Normalizar el resultado y agregarlo como una nueva columna 'resultado_normalizado'
data['resultado_mayusculas_normalizado'] = data.apply(lambda row: normalizar(row['cantidad_mayusculas'], row['total_letras']), axis=1)

contar_mayusculas = data['resultado_mayusculas_normalizado']
# Mostrar el DataFrame con las nuevas columnas
#print(data)

"""**CONTAR MINUSCULAS EN LA ORACION**"""

def contar_letras_minusculas(oracion):
    contador = 0
    for letra in oracion:
        if letra.islower():
            contador += 1
    return contador

def normalizar(cantidad_minusculas, total_letras):
    if total_letras == 0:
        return 0
    return cantidad_minusculas / total_letras

# Leer el archivo .tsv usando pandas
data = pd.read_csv(DATA_PATH, sep='\t')

# Nombre del archivo .tsv y el nombre de la columna que contiene las oraciones
nombre_columna_oracion = 'sentence'

# Asegurarnos de que la columna 'oracion' sea de tipo str (cadena)
data[nombre_columna_oracion] = data[nombre_columna_oracion].astype(str)

# Calcular la cantidad de letras minúsculas y total de letras en cada oración
data['cantidad_minusculas'] = data[nombre_columna_oracion].apply(contar_letras_minusculas)
data['total_letras'] = data[nombre_columna_oracion].apply(len)

# Normalizar el resultado y agregarlo como una nueva columna 'resultado_normalizado'
data['resultado_minuscula_normalizado'] = data.apply(lambda row: normalizar(row['cantidad_minusculas'], row['total_letras']), axis=1)

contar_minusculas = data['resultado_minuscula_normalizado']
# Mostrar el DataFrame con las nuevas columnas
print(data)

"""**DIVERSIDAD LEXICA**"""

import nltk
nltk.download('punkt')

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize

def calcular_diversidad_lexica_normalizada(oracion):
    palabras = word_tokenize(str(oracion).lower())  # Convertir a minúsculas y dividir en palabras
    total_palabras = len(palabras)
    cantidad_palabras_unicas = len(set(palabras))
    diversidad_lexica_normalizada = cantidad_palabras_unicas / total_palabras
    return diversidad_lexica_normalizada

# Leer el archivo .tsv usando pandas
data = pd.read_csv(DATA_PATH, sep='\t')

nombre_columna_sentence = 'sentence'

# Calcular la diversidad léxica normalizada de cada oración
data['diversidad_lexica'] = data[nombre_columna_sentence].apply(calcular_diversidad_lexica_normalizada)
diversidad_lexica = data['diversidad_lexica']
# Imprimir el DataFrame con la nueva columna "diversidad_normalizada"
#print(data)

"""**ADJETIVOS**"""

!pip install nltk
!python -m nltk.downloader universal_tagset

import pandas as pd
import nltk
from nltk import word_tokenize, pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def count_adjectives(sentence):
    # Convertir el valor a una cadena de texto para evitar errores
    sentence_str = str(sentence)
    # Tokenizar la oración en palabras
    words = word_tokenize(sentence_str)
    # Obtener las etiquetas de partes del discurso para cada palabra
    pos_tags = pos_tag(words)
    # Filtrar las palabras que son adjetivos (etiqueta que comienza con 'JJ')
    adjectives = [word for word, pos in pos_tags if pos.startswith('JJ')]
    return len(adjectives)

# Crear una nueva columna en el DataFrame para almacenar el número de adjetivos en cada oración
data['num_adjectives'] = data['sentence'].apply(count_adjectives)

# Función para normalizar el número de adjetivos por el número total de palabras en la oración
def normalize_adjectives(row):
    num_words = len(word_tokenize(str(row['sentence'])))  # Convertir a cadena de texto antes de tokenizar
    num_adj = row['num_adjectives']
    if num_words > 0:
        return num_adj / num_words
    else:
        return 0

# Crear una nueva columna para almacenar el número normalizado de adjetivos
data['normalized_adjectives'] = data.apply(normalize_adjectives, axis=1)
adjetivos = data['normalized_adjectives']

# Imprimir el DataFrame con las columnas originales y la columna normalizada
#print(data[['sentence', 'num_adjectives', 'normalized_adjectives']])

print(data)

"""**Agregar columnas con las nuevas caracteristicas**"""

datos = pd.read_csv(DATA_PATH, sep='\t')
# Agregar las Nuevas columnas de las nuevas caracteristicas
datos['frecuency'] = frecuencia_palabra
datos['num_senses'] = normalized_num_senses
datos['morpheme_len'] = numero_morfemas_normalizado
datos['consonant_freq'] = frec_consonantes_normalizada
datos['mayusculas_sentence'] = contar_mayusculas
datos['minusculas_sentence'] = contar_minusculas
datos['diversidad_lexica_sentence'] = diversidad_lexica
datos['adjectives'] = adjetivos
# Resultados
print(datos.head())

"""**GUARDAR Y DESCARGAR LAS NUEVAS CARACTERISTICAS EN EXCEL**"""

# Guardar el DataFrame con la nueva característica en un nuevo archivo CSV
datos.to_excel('/content/LegalEc.xlsx', index=False)

# Descargar el archivo CSV con la nueva característica
from google.colab import files
files.download('/content/LegalEc.xlsx')