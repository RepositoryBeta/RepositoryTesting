import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

CURSORCLASS = pymysql.cursors.DictCursor

def initiate_local_connection():
    try:
        connection = pymysql.connect(host=os.getenv("ENDPOINT"),
                                     port=int(os.getenv("PORT")),
                                     user=os.getenv("USER"),
                                     passwd=os.getenv("PASSWORD"),
                                     db=os.getenv("DBNAME"),
                                     cursorclass=CURSORCLASS)
        print('[+] Local Connection Successful')
    except Exception as e:
        print(f'[+] Local Connection Failed: {e}')
        connection = None

    return connection