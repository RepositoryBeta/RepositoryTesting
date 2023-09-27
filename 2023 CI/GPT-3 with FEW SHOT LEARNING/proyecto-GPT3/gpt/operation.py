import pickle
import os
from datetime import datetime
import pandas as pd

def temporal_storage(minimo, maximo, data):
    if not os.path.exists("temp"):
        os.mkdir('temp')

    now = datetime.now()
    nombre_archivo = f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.second}.csv"
    data.to_csv(f"temp/{nombre_archivo}")
    dicc = {"minimo": minimo, "maximo": maximo, "archivo": nombre_archivo}
    with open("temp/datos_temp.pkl", "wb") as tf:
        pickle.dump(dicc, tf)