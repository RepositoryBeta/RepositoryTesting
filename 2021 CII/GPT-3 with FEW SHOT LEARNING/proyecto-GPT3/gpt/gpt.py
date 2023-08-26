import traceback

import openai
import sys
import pandas as pd
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from .operation import temporal_storage

class Gpt3:

    def __init__(self, datos, prompt, key, chatgpt=False, load=False):
        self.__plantilla_resultados = "{:^5} {:^20} {:^20} {:^20} {:^20} {:^20} {:^20} {:^20}"
        self.__plantilla_porcentaje = "{:^5} {:^20} {:^20} {:^30} {:^30} {:^30} {:^30} {:^30}"
        self.__datos = datos
        self.__prompt = prompt
        self.__key = key
        self.load = load
        self.chatgpt = chatgpt
        self.__rango_escalas = {
            'very easy': (0, 0),
            'easy': (0, 0.25),
            'neutral': (0.25, 0.50),
            'difficult': (0.50, 0.75),
            'very difficult': (0.75, 1)
        }

    def __prompt_format(self, source, sentence, token):
        prompt = self.__prompt
        prompt = prompt.replace("@recurso", f"\"{source}\"")
        prompt = prompt.replace("@oracion", f"\"{sentence}\"")
        prompt = prompt.replace("@aEvaluar", f"\"{token}\"")
        # prompt = prompt.replace("@aEvaluar", "\"" + self.__datos["token"][indice] + "\"")
        return prompt

    def __imprimir_fila(self, indice, respuesta_gpt3, rango, complejidad_gpt3,
                        complejidad, complejidad_escala, comparacion):
        token = self.__datos["token"][indice]

        print(self.__plantilla_resultados.format(indice, token, respuesta_gpt3, rango,
                                                 complejidad_gpt3, complejidad, complejidad_escala,
                                                 comparacion))

    def __imprimir_fila_porcent(self, indice, respuesta_gpt3, respuesta_complex, opciones):
        token = self.__datos["token"][indice]

        print(self.__plantilla_porcentaje.format(indice, token, respuesta_gpt3, respuesta_complex, opciones[0],
                                                 opciones[1], opciones[2], opciones[3]))

    def __asig_etiqueta(self, valor):
        escala = ""

        if valor == 0:
            escala = "very easy"
        elif 0 < valor <= 0.25:
            escala = "easy"
        elif 0.25 < valor <= 0.50:
            escala = "neutral"
        elif 0.50 < valor <= 0.75:
            escala = "difficult"
        elif 0.75 < valor <= 1:
            escala = "very difficult"

        return escala

    def __filtro(self, respuesta_gpt3):
        resultado = ""

        for valor_escala in list(self.__rango_escalas.keys()):
            n_palabras = len(valor_escala.split())
            if n_palabras == 2 and respuesta_gpt3.count(valor_escala) >= 1:
                return valor_escala
            elif respuesta_gpt3.count(valor_escala) >= 1:
                resultado = valor_escala

        return resultado

    def __evaluar(self, orden):
        openai.api_key = self.__key

        if(self.chatgpt):
            model = "gpt-3.5-turbo"
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {
                    "role": "user",
                    "content": orden
                    }
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            respuesta = response.choices[0].message.content

        else:
            model = "text-davinci-003"
            response = openai.Completion.create(
                model=model,
                prompt=orden,
                temperature=0,
                max_tokens=5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                logprobs=5,
                stop=["\n"]
            )
            respuesta = response.choices[0].text

        # prob_tokens = response.choices[0].logprobs.top_logprobs
        return respuesta

    def search_response_GPT3(self, respuesta_gpt3, probs):
        dicc = []
        for index, val in enumerate(probs):
            key = list(val.keys())
            if key[0] in respuesta_gpt3:
                dicc.append(probs[index])
        return dicc

    
    def data_to_process(self):
        # load_da, minimo, maximo = load_data_temp() if self.load else (None, None, None)

        load_da, minimo, maximo = (None, None, None)

        if load_da is None:
            to_process = self.__datos
            to_process[f"Respuesta {'ChatGPT' if self.chatgpt else 'GPT3'}"] = None
            to_process[f"Rango {'ChatGPT' if self.chatgpt else 'GPT3'}"] = None
            to_process[f"Complejidad {'ChatGPT' if self.chatgpt else 'GPT3'}"] = 0.0
            to_process["comparacion"] = None
            for i in range(5):
                to_process[f"Porcentaje {i + 1}"] = ""
            minimo = 0
            maximo = self.__datos.shape[0] - 1

        elif load_da is not None:
            to_process = load_da
            to_process = pd.concat([to_process, self.__datos[minimo:]], ignore_index=True)
        else:
            sys.exit("Error de ingreso de parametros")

        return to_process, minimo, maximo


    def process_data(self, indice, row, resultado):
        temp = self.__prompt_format(
            row["source"],
            row["sentence"],
            row["token"]
        )

        # print(temp)

        try:
            respuesta_gpt3 = self.__evaluar(temp)
        except KeyError:
            sys.exit("No se encontro el resultado esperado"
                     " por GPT3")
        except openai.error.OpenAIError as error_openai:
            if indice - 1 != -1:
                temporal_storage(indice, self.__datos.tail(1).index[0], resultado.loc[0:indice - 1])
            sys.exit("Error: " + str(error_openai))
        except Exception:
            if indice - 1 != -1:
                temporal_storage(indice, self.__datos.tail(1).index[0], resultado.loc[0:indice - 1])
            sys.exit("Error: " + str(error_openai))
        return respuesta_gpt3

    def process_all(self, file_path="", version=False, save_result=False, percent=False, result_name = ""):

        resultado, minimo, maximo = self.data_to_process()
        # tokenizer = tiktoken.encoding_for_model("gpt-3")
        # last = time.time()
        # tokens_prompt = 0
        peticiones = 0

        if percent:
            print(self.__plantilla_porcentaje.format("N", "Token", f"Respuesta {'ChatGPT' if self.chatgpt else 'GPT3'}", "Respuesta CompLex", "Opcion 1",
                                                     "Opcion 2", "Opcion 3", "Opcion 4", "Opcion 5"))
        else:
            print(self.__plantilla_resultados.format("N", "Token", f"Respuesta {'ChatGPT' if self.chatgpt else 'GPT3'}", f"Rango {'ChatGPT' if self.chatgpt else 'GPT3'}", f"Complejidad {'ChatGPT' if self.chatgpt else 'GPT3'}",
                                                     "Complejidad compLex", "Rango compLex", "Comparacion") + "\n")

        # range_index = pd.RangeIndex(minimo, maximo + 1, 1)
        for index, row in self.__datos.iterrows():

            complejidad_gpt3 = self.process_data(index, row, resultado)

            # tokens_prompt += len(tokenizer(temp)['input_ids'])
            peticiones += 1

            # complejidad_gpt3 = self.__means.get(respuesta_gpt3)
            respuesta_gpt3 = self.__asig_etiqueta(float(complejidad_gpt3))
            rango = str(self.__rango_escalas.get(respuesta_gpt3))
            complejidad = row["complexity"]
            escala_complex = row["escala"]

            resultado.at[index, f"Respuesta {'ChatGPT' if self.chatgpt else 'GPT3'}"] = respuesta_gpt3
            resultado.at[index, f"Rango {'ChatGPT' if self.chatgpt else 'GPT3'}"] = rango
            resultado.at[index, f"Complejidad {'ChatGPT' if self.chatgpt else 'GPT3'}"] = float(complejidad_gpt3)

            if respuesta_gpt3 == escala_complex:
                comparacion = "Si"
            else:
                comparacion = "No"

            resultado.at[index, "comparacion"] = comparacion


            self.__imprimir_fila(index, respuesta_gpt3, rango, complejidad_gpt3,
                                     complejidad, escala_complex, comparacion)

            # ****************************** Control de Peticiones ***********************************
            # actual = time.time() - last

            # if actual >= 60:
            #     tokens_prompt = 0
            #     peticiones = 0
            #     last = time.time()

            # if tokens_prompt >= 200000 or peticiones >= 45:
            #     # if peticiones >= 55:
            #     seconds_to_wait = 60 - actual
            #     tokens_prompt = 0
            #     peticiones = 0
            #     time.sleep(seconds_to_wait)
            #     last = time.time()
            # ************************* Cierre de control de Peticiones ******************************

        true = resultado.loc[:, "complexity"]
        predicted = resultado.loc[:, f"Complejidad {'ChatGPT' if self.chatgpt else 'GPT3'}"]

        metrics = {
            "MAE": round(mean_absolute_error(true, predicted), 4),
            "MSE": round(mean_squared_error(true, predicted), 4),
            "RMSE": round(mean_squared_error(true, predicted, squared=False), 4),
            "R2": round(r2_score(true, predicted), 4),
            "Pearson": round(true.corr(predicted, method='pearson'), 4),
            "Spearman": round(true.corr(predicted, method='spearman'), 4)
        }

        for m in metrics:
            resultado[m] = metrics[m]
            print(f"{m}: {metrics[m]}")
        print("\n")

        getSd = resultado['comparacion'].value_counts()

        count_si = getSd.get("Si", 0)
        count_no = getSd.get("No", 0)

        resultado["Si %"] = (count_si / (count_no + count_si)) * 100
        resultado["No %"] = (count_no / (count_no + count_si)) * 100

        print(f"Porcentaje coincidencia: {(count_si / (count_no + count_si)) * 100}")

        resultado = resultado[["id", "sentence", "token", f"Respuesta {'ChatGPT' if self.chatgpt else 'GPT3'}", f"Rango {'ChatGPT' if self.chatgpt else 'GPT3'}", f"Complejidad {'ChatGPT' if self.chatgpt else 'GPT3'}",
                               "complexity", "escala", "comparacion", "Si %", "No %" ,"MAE", "MSE", "RMSE", "R2", "Pearson", "Spearman",
                               "Porcentaje 1", "Porcentaje 2", "Porcentaje 3", "Porcentaje 4", "Porcentaje 5"]]

        if version:
            resultado_metricas = {"Version": [version]}
            resultado_metricas.update(metrics)
            resultado_metricas = pd.DataFrame(resultado_metricas)
            # guardar_metricas(resultado_metricas)

        if save_result:
            if version:
                resultado.to_excel(f'resultados/resultado_{version}.xlsx')
            else:
                resultado.to_excel(f'docs/results/{result_name}.xlsx')
