from database import initiate_local_connection
import pandas as pd

connection = initiate_local_connection()

def get_records(params):
    try:
        if not ("table" in params):
            raise Exception("Table not found")
        
        table = params["table"]
        where = ""
        if "where" in params:
            where = " WHERE"
            num_items = len(params["where"])
            for index, value in enumerate(params["where"].items()):
                where += " {} = '{}'".format(value[0], value[1])
                if num_items != 1 and index < num_items - 1:
                    where += " AND "


        sql_query = "SELECT * FROM " + table + where
        with connection.cursor() as cursor:
            cursor.execute(sql_query)

        connection.commit()
        
        results = cursor.fetchall()
        
        df = pd.DataFrame(results)
                
        return df
        
    except Exception as e:
        return e

def insert_record_result(params):
    try:
        if not ("table" in params):
            raise Exception("Table not found")
        
        keys = params.keys()
        values = params.values()

        keys = list(map(lambda x: str(x).replace("'", ""), keys ))
        del keys[0]
        values = list(map(lambda x: str(x).replace("'", ""), values ))
        del values[0]
            
        sql_query = "INSERT INTO {} {} values {};".format(params["table"], str(tuple(keys)).replace("'",""), tuple(values))
        # print(sql_query)
        with connection.cursor() as cursor:
            cursor.execute(sql_query)

        connection.commit()
                        
    except Exception as e:
        print(f'Error encountered: {e}')
