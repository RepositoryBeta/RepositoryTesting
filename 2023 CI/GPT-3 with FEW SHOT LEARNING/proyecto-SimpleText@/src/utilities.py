from .operation import get_records
import json

def get_table_data(corpus):
    params = {"table": "corpus_table_info", "where": {"name": corpus}}
    result = get_records(params)
    return json.loads(result["data"][0])