import json
from sqlalchemy import create_engine




with open('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\data_connection.json', 'r', encoding = 'utf-8') as file_json: 
    data = json.load(file_json)

engine = create_engine('postgresql://{} : {} @ {} : {} / {}'.format(data['user'], data['password'], data['host'], data['port'], data['database']))
#engine = create_engine('postgresql://postgresql['user'] : postgresql['password']@postgresql['host'] : postgresql['port']/postgresql['database'])