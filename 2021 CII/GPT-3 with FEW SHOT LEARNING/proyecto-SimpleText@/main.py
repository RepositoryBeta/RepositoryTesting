from colorama import init, Fore, Style
from src import *
import openai
import pandas as pd
import sys
import os
import re

init()

CORPUS = "adminlex"
TABLE_DATA = get_table_data(CORPUS)

# PROMPTS_BASE = {
#     # "PROMPT": 'select a number from 1 to 5 terms within the sentence named text, rank them from1 to 3 is the most difficult and finally give the meaning of each selected word or an example or use-case. Use next form (term, difficulty, "definition, example, use-case"). you have a maximum of 250 tokens you can t go over that\n',
#     # "PROMPT_EX": 'select a number from 1 to 5 terms within the sentence named text, rank them from1 to 3 is the most difficult and finally give the meaning of each selected word or an example or use-case. Use next form (term\ndifficulty\n"definition, example, use-case"). you have a maximum of 250 tokens you can t go over that.(here is an example)\ncontext: quantum computing\nText: This paper describes a tool that converts Unreal levels to web-ready environments in VRML and X3D.\n##\nTerm 1: X3D\nDifficulty:2\nDefinition: X3D is an ISO-ratified, file format and run-time architecture to represent and communicate 3D scenes and objects. · X3D fully represents 3-dimensional data.\n\nTerm 2: vrml\nDifficulty:2\nDefinition: Virtual Reality Modeling Language (VRML) is a standard file format for representing 3-dimensional interactive vector graphics, designed particularly with the World Wide Web in mind. It has been superseded by X3D.\nNow it s your turn\n',
#     "PRM_ZS_TASK2_1_V1": "To retrieve up to 5 difficult terms in a given passage from differents sources . Rank the list of difficult terms with corresponding scores on the scale 1-3 where 3 is the most difficult term.  you have a maximum of 250 tokens you can t go over that.\n##\n",
#     # "PRM_ZS_TASK2_1_V2": "To decide which difficult terms (up to 5) are in the complex scientific text. Rank the list of difficult terms with corresponding scores on the scale 1-3 where 3 is the most difficult term.  you have a maximum of 250 tokens you can t go over that.\n##\n",
#     # "PRM_FS_TASK2_1_V1": "To retrieve up to 5 difficult terms in a given passage from a scientific abstract. Rank the list of difficult terms with corresponding scores on the scale 1-3 where 3 is the most difficult term.  you have a maximum of 250 tokens you can t go over that. \n##\n\nTerm 1: X3D\nDifficulty:2\n\nTerm 2: vrml\nDifficulty:2\n\nNow it s your turn\n\n",
#     # "PRM_FS_TASK2_1_V2": "To decide which terms (up to 5) require explanation and contextualization to help a reader to understand a complex scientific text. Rank the list of difficult terms with corresponding scores on the scale 1-3 where 3 is the most difficult term.  you have a maximum of 250 tokens you can t go over that.\n##\n\nTerm 1: X3D\nDifficulty:2\n\nTerm 2: vrml\nDifficulty:2\n\nNow it s your turn\n\n",
#     # "PRM_ZS_TASK2_2_V1": "select a number from 1 to 5 terms within the sentence named text, rank them from1 to 3 is the most difficult and finally give the meaning of each difficult term and add an example and an use-case. Use next form (term, difficulty, 'definition, example, use-case'). you have a maximum of 250 tokens you can t go over that.\n\n",
#     # "PRM_FS_TASK2_2_V1": "select a number from 1 to 5 terms within the sentence named text, rank them from 1 to 3 is the most difficult and finally give the meaning of each difficult term and add an example and an use-case. Use next form (term\ndifficulty\n'definition, example, use-case'). you have a maximum of 250 tokens you can t go over that.(here is an example)\ncontext: quantum computing\nText: This paper describes a tool that converts Unreal levels to web-ready environments in VRML and X3D.\n##\nTerm 1: X3D\nDifficulty:2\nDefinition: X3D is an ISO-ratified, file format and run-time architecture to represent and communicate 3D scenes and objects. · X3D fully represents 3-dimensional data.\n\nTerm 2: vrml\nDifficulty:2\nDefinition: Virtual Reality Modeling Language (VRML) is a standard file format for representing 3-dimensional interactive vector graphics, designed particularly with the World Wide Web in mind. It has been superseded by X3D.\nNow it s your turn\n\n",
# }

PROMPTS_BASE = {
    # "PRM_ZS_TASK2_1_V1": "To retrieve up to 5 difficult terms in a given passage from differents sources . Rank the list of difficult terms with corresponding scores on the scale 1-3 where 3 is the most difficult term.  you have a maximum of 250 tokens you can t go over that.\n##\n"
    # "PRM_ZS_TASK2_1_V1": "To retrieve up to 5 difficult terms in a given passage from Law Studies. Rank the list of difficult terms with corresponding scores on the scale 1-3 where 3 is the most difficult term.  you have a maximum of 250 tokens you can t go over that.\n##\n"
    # "PRM_ZS_TASK2_1_V1": "To retrieve up to 5 difficult terms in a given passage from Computing studies. Rank the list of difficult terms with corresponding scores on the scale 1-3 where 3 is the most difficult term.  you have a maximum of 250 tokens you can t go over that.\n##\n"
    "PRM_ZS_TASK2_1_V1": "To retrieve up to 5 difficult terms in a given passage from public documents. Rank the list of difficult terms with corresponding scores on the scale 1-3 where 3 is the most difficult term.  you have a maximum of 250 tokens you can t go over that.\n##\n"
}

def pause(resultado):
    control = True
    while control:
        # print(resultado)
        response = input("system paused. you want to continue with the execution: (y / n): ")
        if response.upper() == "Y":
            control = False

        if response.upper() == "N":
            sys.exit()

def foreach(function, iterable):
    for element in iterable:
        function(element)

def validate_route(route):
    if not (os.path.isdir(route)):
        os.mkdir(route)
    return route

def search(use_list, sentence):
    for i in range(len(use_list)):
        if use_list[i] in sentence:
            return use_list[i]

def gerate_data_fine(data, prompt = ""):
    route = validate_route("fine_tune_data")
    file_name = "fine_train_2.json"
    data_final = prepare_data(data, prompt)
    data_final.to_json(route + "/" + file_name, orient="records")
    return data_final

def generate_prompts(row, prompt_selected = ""):
    header = PROMPTS_BASE.get(prompt_selected)
    source = row[TABLE_DATA.get("field").get("source")]
    sentence = row[TABLE_DATA.get("field").get("sentence")]
    prompt = "{}Context: {}\nText: {}\n\n###\n\n".format(header, source, sentence)
    return prompt

def format_response(response, info, total_tokens, prompt_selected = "", task2_1_cond = False, task2_2_cond = False):
    task2_1 = []
    task2_2 = []
    term = ""
    difficulty = ""
    explicacion = ""
    regID = TABLE_DATA.get("field").get("regID")

    # if prompt_selected == "PROMPT":
    #     resultados = response.split("\n")
    #     resultados = list(filter( lambda value: value != "", resultados))
    #     i = 1
    #     for resultado in resultados:
    #         full = resultado.split(",", 2)
    #         term = full[0]
    #         difficulty = full[1]
    #         explicacion = full[2]

    #         if task2_1_cond:
    #             task2_1.append({
    #                 "table": "result_task2_1", 
    #                 "snt_id": info.get("snt_id"),  
    #                 "term": term, 
    #                 "difficulty": int(difficulty) - 1, 
    #                 "term_rank_snt": i,
    #                 "run_id": "{}_task_2.1_{}".format("SENADI",prompt_selected),
    #                 "promptID": prompt_selected,
    #                 "manual": 0
    #             })

    #         if task2_2_cond:
    #             task2_2.append({
    #                 "table": "result_task2_2",
    #                 "snt_id": info.get("snt_id"),  
    #                 "term": term, 
    #                 "difficulty": int(difficulty) - 1, 
    #                 "term_rank_snt": i,
    #                 "definition": explicacion,
    #                 "run_id": "{}_task_2.2_{}".format("SENADI", prompt_selected),
    #                 "promptID": prompt_selected,
    #                 "manual": 0
    #             })
    #         i += 1

    if prompt_selected in ["PROMPT_EX", "PRM_FS_TASK2_2_V1"]:
        resultados = response.split("\n\n")
        resultados = list(filter( lambda value: value != "", resultados))
        i = 1
        for resultado in resultados:
            full = resultado.split('\n')
            term = full[0].split(":")[1].strip()
            difficulty = re.findall(r"\d+", full[1])[0]
            explicacion = full[2].split(":", 1)[1].strip()
            # print("Arreglo total >>>>> ", len(full))
            if len(full) > 3:
                explicacion += ". " + full[3]
                # print("Here >>>>> ", full[3])
            
            if task2_1_cond:
                task2_1.append({
                "table": "result_task2_1", 
                TABLE_DATA.get("regID"): info.get("snt_id"),  
                "term": term, 
                "difficulty": int(difficulty) - 1, 
                "term_rank_snt": i,
                "run_id": "{}_task_2.1_{}".format("SENADI",prompt_selected),
                "promptID": prompt_selected,
                "manual": 0
                })

            if task2_2_cond:
                task2_2.append({
                    "table": "result_task2_2",
                    "snt_id": info.get("snt_id"),  
                    "term": term, 
                    "difficulty": int(difficulty) - 1, 
                    "term_rank_snt": i,
                    "definition": explicacion,
                    "run_id": "{}_task_2.2_{}".format("SENADI", prompt_selected),
                    "promptID": prompt_selected,
                    "manual": 0
                })
            i += 1

    if prompt_selected in ["PRM_ZS_TASK2_1_V1", "PRM_ZS_TASK2_1_V2"]:
        if response.find(":\n") != -1: resultados = resultados.split(":\n")[1] 
        resultados = response.split("\n")
        resultados = list(filter( lambda value: value != "", resultados))
        patron = r"\((Score:|score:)?( )?\(\d+\)"
        patron_acronym = r"(.*?) ?(\((.*?)\))?: ?\d+"
        patron2_acronym = r"\d+\. ?(.*?) ?\(( ?Score|| ?score)?:? ?\d+\)"
        patron_sin_score = re.compile(r"\d+\. ?(.*?) ?(\((.*?)\))?: ?\d+")
        i = 1
        for resultado in resultados:

            # if re.match(patron_acronym, resultado) != None:
            #     word = resultado.split(":")[0].split(".")[1].strip()
            #     difficulty = re.findall(r"\d+", resultado)[1]
            #     print("entro")
            if resultado.upper().strip() != "Difficult Terms:".upper() :
                if patron_sin_score.match(resultado):
                    # print("patron_sin_score")
                    resultado_h = patron_sin_score.search(resultado).group(0)
                    word = resultado_h.split(".", 1)[1].split(":")[0].strip()
                    difficulty = re.findall(r"\d+", resultado_h)[1]
                elif re.match(patron2_acronym, resultado) != None:
                    # print("patron2_acronym")
                    resultado_h = re.search(patron2_acronym, resultado).group(0)
                    word = resultado_h.split(".", 1)[1].split(" (")[0].strip()
                    difficulty = re.findall(r"\d+", resultado_h)[1]
                else:
                    # print("default")
                    word = resultado.split("(")[0]
                    word = word.split(".")[1].strip()
                    difficulty = re.findall(patron, resultado)[-1][1]


                if task2_1_cond:
                    task2_1.append({
                        "table": TABLE_DATA.get("results"), 
                        "regID": info.get("snt_id"),  
                        "term": word, 
                        "difficulty": int(difficulty) - 1, 
                        "term_rank_snt": i,
                        "run_id": "{}_task_2.1_{}".format("SENADI",prompt_selected),
                        "promptID": prompt_selected,
                        "manual": 0
                    })
                i += 1

    if prompt_selected == "PRM_FS_TASK2_1_V1":
        form = response.find("\n\n") == -1
        resultados = response.split("\n") if form else response.split("\n\n")
        resultados = list(filter( lambda value: value != "", resultados))
        i = 1
        for resultado in resultados:
            patron = r"Term \d+: ?(.*?) Difficulty: ?\d+"
            # print("3 prompts")
            if re.match(patron, resultado) != None :
                term = resultado.split(":",1)[1].split("Difficulty:")[0].strip().replace(":", "")
                difficulty = re.findall(r"\d+", resultado)[1]
            else :
                full = resultado.split('\n')
                term = full[0].split(":")[1].strip()
                difficulty = full[1].split(":")[1].strip()

            if task2_1_cond:
                task2_1.append({
                    "table": "result_task2_1", 
                    "snt_id": info.get("snt_id"),  
                    "term": term, 
                    "difficulty": int(difficulty) - 1, 
                    "term_rank_snt": i,
                    "run_id": "{}_task_2.1_{}".format("SENADI",prompt_selected),
                    "promptID": prompt_selected,
                    "manual": 0
                })
            i += 1

    if prompt_selected == "PRM_FS_TASK2_1_V2":
        form = response.find("\n\n") == -1
        resultados = response.split("\n") if form else response.split("\n\n")
        resultados = list(filter( lambda value: value != "", resultados))
        i = 1
        for resultado in resultados:

            term = ""
            difficulty = ""

            if form or resultado.find("\n") == -1: 
                full = resultado.split(':')
                term = full[1].replace("Difficulty", "").replace("-", " ").strip()
                difficulty = full[-1].strip()
            else :
                full = resultado.split('\n')
                term = full[0].split(":")[1].strip()
                difficulty = full[1].split(":")[1].strip()

            if task2_1_cond:
                task2_1.append({
                    "table": "result_task2_1", 
                    "snt_id": info.get("snt_id"),  
                    "term": term, 
                    "difficulty": int(difficulty) - 1, 
                    "term_rank_snt": i,
                    "run_id": "{}_task_2.1_{}".format("SENADI",prompt_selected),
                    "promptID": prompt_selected,
                    "manual": 0
                })
            i += 1

    if prompt_selected == "PRM_ZS_TASK2_2_V1":
        form = response.find("\n\n") == -1
        resultados = response.split("\n") if form else response.split("\n\n")
        resultados = list(filter( lambda value: value != "", resultados))
        patron = r"^(Term\s\d:|\d\.)\s?(.*?)$"
        i = 1
        for resultado in resultados:
        
            if re.match(patron, resultado) != None :
                full = resultado.split(",", 2)
                term = full[0].split(" ", 1)[1].strip() if full[0].find(":") == -1 else full[0].split(":", 1)[1].strip()
                difficulty = re.findall(r"\d+", full[1])[0].strip()
                definition = full[2].strip()
            else:
                full = resultado.split(",", 2)
                term = full[0].strip()
                difficulty = re.findall(r"\d+", full[1])[0].strip()
                definition = full[2].strip()

            # if definition.find(":") != -1:
            #     definition = definition.split(":")[1].strip()

            if task2_2_cond:
                task2_2.append({
                    "table": "result_task2_2", 
                    "snt_id": info.get("snt_id"),  
                    "term": term, 
                    "difficulty": int(difficulty) - 1,
                    "definition": definition,
                    "term_rank_snt": i,
                    "run_id": "{}_task_2.1_{}".format("SENADI",prompt_selected),
                    "promptID": prompt_selected,
                    "manual": 0
                })
            i += 1

    return task2_1, task2_2

def process_data(data):
    # data = data[0:2]
    count = 1
    # print(data)
    for index, row in data.iterrows():
        try:    
            prompt_selected = "PRM_ZS_TASK2_1_V1"
            regID = TABLE_DATA.get("field").get("regID")
            table = TABLE_DATA.get("results")
            params = {"table": table, "where": {"regID": row[regID], "promptID": prompt_selected}}
            result = get_records(params)

            if type(result) == Exception: raise Exception(str(result))
            not_result = result.empty
            if not_result:
                # print(generate_prompts(row, prompt_selected))
                resultados, total_tokens = evaluar(generate_prompts(row, prompt_selected))
                # if row["snt_id"] == "G01.1_1516508996_1": print("here")
                # Save tokens total
                new_exec = {
                    "table": "task_exec",
                    "snt_id": row[regID],
                    "prompt_num": total_tokens,
                    "promptID": prompt_selected,
                    "state": "success",
                    "corpus": CORPUS
                }

                to_save_task2_1, to_save_task2_2 = format_response(resultados, {"snt_id": row[regID]}, total_tokens, prompt_selected, task2_1_cond = True)

                insert_record_result(new_exec)
                foreach(insert_record_result, to_save_task2_1)
                # foreach(insert_record_result, to_save_task2_2)

                print(Fore.GREEN+"Record {} processed and saved successfully".format(row[regID])+Fore.RESET)
                # time.sleep(5)

                # sys.exit()
            else:
                print("{}: has already been processed".format(row[regID]))

        except openai.error.RateLimitError as limit_rate_error:
            print(Fore.RED+"Error during processing of {}: {}".format(row[regID],"Error openai -> " + str(limit_rate_error))+Fore.RESET)
            sys.exit()
        except openai.error.OpenAIError as error_openai:
            print(Fore.RED+"Error during processing of {}: {}".format(row[regID],"Error openai -> " + str(error_openai))+Fore.RESET)
            print(index)
            # sys.exit()
        except Exception as e:
            new_exec.update({"state": "error"})
            insert_record_result(new_exec)
            print(Fore.RED+"Error during processing of {}: {}".format(row[regID], e)+Fore.RESET)
            print(index)
            # if count != 1: sys.exit()
        count += 1
        # print(count)
        # if count == 4: sys.exit()
    
    print(Fore.YELLOW+"Proccess_data successfully executed")

# params = {"table": TABLE_DATA.get("main")}
# data = get_records(params)

# path = 'docs/corpus/compLex/test1.xlsx'
# path = 'docs/corpus/legalEC/final.xlsx'
# path = 'docs/corpus/clexis/final.xlsx'
path = 'docs/corpus/AdminLex/final.xlsx'
data = pd.read_excel(path)
# print(complex_data.shape)
# print(complex_data)
if type(data) != Exception:
    process_data(data)
else:
    print(Fore.RED + str(data))
