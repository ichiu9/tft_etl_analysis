import json
import psycopg2
import datetime
from modules.psycop_modules.createConnection import *

# ## Create Printing Functions

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
    
def print_response(response):
    print(response.status_code)
    jprint(response.json())

# Execute SQL Function

def execute_sql(sql, variables, cursor, connection):
    try:
        cursor.execute(sql, variables)
    except psycopg2.Error as e:
        print(e)

# UNIX to Readable Time

def epoch_to_date(epoch_time):
    time_stamp = epoch_time / 1000
    date_time = datetime.datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
    return date_time
