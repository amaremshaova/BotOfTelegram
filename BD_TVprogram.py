import requests
import tempfile
import zipfile
import os
import os.path
import json
from JTV import read_JTV
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Date, Time

with open('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\data_connection.json', 'r', encoding = 'utf-8') as file_json: 
    data = json.load(file_json)

engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(data['user'],data['password'],data['host'],data['port'],data['database']))

metadata = MetaData()
users_table = Table('TVprogram', metadata,
    Column('Name_TVprogram', String),
    Column('Date', Date),
    Column('Start Time', Time)
)

metadata.create_all(engine)


url = 'http://programtv.ru/jtv.zip'
response = requests.get(url)

file = tempfile.TemporaryFile()
file.write(response.content)

fzip = zipfile.ZipFile(file)

#for file_jtv in fzip.namelist(): #проходим по всем файлам с расширением .ndx в папке jtv
    #if file_jtv.endswith('.ndx'):
        #file_ndx = fzip.open(file_jtv)

read_JTV(fzip)



#for f in os.listdir('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\tmp'):
	#path, f_name = os.path.split(f) 
    #print(str(f_name))
    #filename, extension = os.path.splitext(f_name)
    #os.rename(f, filename.encode('cp437').decode('cp866') + extension )	


fzip.close()
file.close