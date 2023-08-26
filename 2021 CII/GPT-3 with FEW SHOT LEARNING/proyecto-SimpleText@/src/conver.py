import pandas as pd

def conv_files():
    files = {
        "small_test": "test/simpletext-task2-test-small.json",
        "medium_test": "test/simpletext-task2-test-medium.json",
        "large_test": "test/simpletext-task2-test-large.json",
        "input_train": "train/simpletext-task2-train-input.json",
        "qrels_train": "train/simpletext-task2-train-qrels.json",
    }

    for key in files:
        path = key.split("_")[1] + "_conv/"
        df_json = pd.read_json(files[key])
        df_json.to_excel(path + key + ".xlsx")

def prepare_data(data, header = ""):
    data_filter = data["snt_id"].drop_duplicates().values
    new_df = []

    for dat in data_filter:
        rows = data[data["snt_id"] == dat ]
        prompt_ex = ""
        completion_ex = ""
        n_example = 1
        ex_total = len(rows)
        for index, row in rows.iterrows():
            if n_example == 1 : prompt_ex += "Context: {}\nText: {}".format(row["query_text"], row["source_snt"])
            completion_ex += "Term {}: {}\nDifficulty: {}\nDefinition: {}".format(n_example, row["term"], row["difficulty"], row["definition"])
            if ex_total != 1 and n_example < ex_total: completion_ex += "\n---\n"
            n_example += 1

        prompt = "{}{}\n\n###\n\n".format(header + "\n" if header else header, prompt_ex)
        completion = completion_ex + "###"
        new_df.append({'prompt': prompt, 'completion': completion})
    
    return pd.DataFrame(new_df)
    
    
