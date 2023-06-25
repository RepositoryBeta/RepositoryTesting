from colorama import init, Fore, Style
from operation import get_records, insert_record_result
import pandas as pd
from gpt import chatGPT
# init()

# # by Colorama’s constant shorthand for ANSI escape sequences:
# # -----------------------------------------------------------
# # from colorama import Fore, Back, Style
# # print('\033[31m' + 'some red text')
# # print('\033[39m') # and reset to default color

# # by manually printing ANSI sequences from your own code:
# # -------------------------------------------------------
# print(Fore.RED + 'some red text')
# # print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
# print('back to normal now')

# # by using your code sample
# # -------------------------
# green = Fore.GREEN
# print(f'{green}This is a test')

# params = {"table": "result_process"}
# data = get_records(params)
# data.to_excel("resultados_100_registros.xlsx")

# chatGPT()

folder = "results"
PRM_ZS_TASK2_1_V1 = get_records({"table": "result_task2_1_temp", "where": {"promptID": "PRM_ZS_TASK2_1_V1"}}).drop(['promptID'], axis=1) 
PRM_ZS_TASK2_1_V2 = get_records({"table": "result_task2_1_temp", "where": {"promptID": "PRM_ZS_TASK2_1_V2"}}).drop(['promptID'], axis=1) 
PRM_FS_TASK2_1_V1 = get_records({"table": "result_task2_1_temp", "where": {"promptID": "PRM_FS_TASK2_1_V1"}}).drop(['promptID'], axis=1)
PRM_FS_TASK2_1_V2 = get_records({"table": "result_task2_1_temp", "where": {"promptID": "PRM_FS_TASK2_1_V2"}}).drop(['promptID'], axis=1)
PRM_ZS_TASK2_2_V1 = get_records({"table": "result_task2_2_temp", "where": {"promptID": "PRM_ZS_TASK2_2_V1"}}).drop(['promptID'], axis=1)
PRM_FS_TASK2_2_V1 = get_records({"table": "result_task2_2_temp", "where": {"promptID": "PRM_FS_TASK2_2_V1"}}).drop(['promptID'], axis=1)

# PRM_ZS_TASK2_1_V1.to_excel(folder+"/"+"PRM_ZS_TASK2_1_V1"+".xlsx", index=False)
# PRM_ZS_TASK2_1_V2.to_excel(folder+"/"+"PRM_ZS_TASK2_1_V2"+".xlsx", index=False)
# PRM_FS_TASK2_1_V1.to_excel(folder+"/"+"PRM_FS_TASK2_1_V1"+".xlsx", index=False)
# PRM_FS_TASK2_1_V2.to_excel(folder+"/"+"PRM_FS_TASK2_1_V2"+".xlsx", index=False)
# PRM_ZS_TASK2_2_V1.to_excel(folder+"/"+"PRM_ZS_TASK2_2_V1"+".xlsx", index=False)
# PRM_FS_TASK2_2_V1.to_excel(folder+"/"+"PRM_FS_TASK2_2_V1"+".xlsx", index=False)

PRM_ZS_TASK2_1_V1.to_json(folder+"/"+"PRM_ZS_TASK2_1_V1"+".json")
PRM_ZS_TASK2_1_V2.to_json(folder+"/"+"PRM_ZS_TASK2_1_V2"+".json")
PRM_FS_TASK2_1_V1.to_json(folder+"/"+"PRM_FS_TASK2_1_V1"+".json")
PRM_FS_TASK2_1_V2.to_json(folder+"/"+"PRM_FS_TASK2_1_V2"+".json")
PRM_ZS_TASK2_2_V1.to_json(folder+"/"+"PRM_ZS_TASK2_2_V1"+".json")
PRM_FS_TASK2_2_V1.to_json(folder+"/"+"PRM_FS_TASK2_2_V1"+".json")

PRM_ZS_TASK2_1_V1.to_csv(folder+"/"+"PRM_ZS_TASK2_1_V1"+".tsv", sep="\t", index=False)
PRM_ZS_TASK2_1_V2.to_csv(folder+"/"+"PRM_ZS_TASK2_1_V2"+".tsv", sep="\t", index=False)
PRM_FS_TASK2_1_V1.to_csv(folder+"/"+"PRM_FS_TASK2_1_V1"+".tsv", sep="\t", index=False)
PRM_FS_TASK2_1_V2.to_csv(folder+"/"+"PRM_FS_TASK2_1_V2"+".tsv", sep="\t", index=False)
PRM_ZS_TASK2_2_V1.to_csv(folder+"/"+"PRM_ZS_TASK2_2_V1"+".tsv", sep="\t", index=False)
PRM_FS_TASK2_2_V1.to_csv(folder+"/"+"PRM_FS_TASK2_2_V1"+".tsv", sep="\t", index=False)