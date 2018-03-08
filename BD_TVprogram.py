import requests
import zipfile
import json
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, DateTime
import binascii
import os.path
from datetime import datetime, timedelta

class struct_TV(object):
    def __init__(self, nameChannel, nameTV, DataTime):
        self.nameChannel = nameChannel
        self.nameTV = nameTV
        self.DataTime = DataTime
    def __repr__(self):
        return "<User('%s','%s','%s')>" % (self.nameChannel, self.nameTV, self.DataTime)

def read_JTV(fzip, session):
    
    hex_array_countTV = []
    hex_array_low_data_time = []
    hex_array_high_data_time = []
    seek_array_file_pdt = []
    hex_array_length_nameTV = []
    	
    for file in fzip.namelist(): 
        if file.endswith('.ndx'):
            file_ndx = fzip.open(file, 'r') 
            		
            hex_array_countTV.append(binascii.hexlify(file_ndx.read(1)))  
            hex_array_countTV.append(binascii.hexlify(file_ndx.read(1)))
			
            countTV = int(hex_array_countTV[1] + hex_array_countTV[0], 16)
            
            hex_array_countTV.pop(1)
            hex_array_countTV.pop(0)
			
            for j in range(countTV):
                file_ndx.read(2)
				
                for i in range(4):
                    hex_array_low_data_time.append(binascii.hexlify(file_ndx.read(1)))
                
                hex_low_data_time = hex_array_low_data_time[3] + hex_array_low_data_time[2] + hex_array_low_data_time[1] + hex_array_low_data_time[0]

                for i in range(4):
                    hex_array_low_data_time.pop(3 - i)
            
                for i in range(4):
                    hex_array_high_data_time.append(binascii.hexlify(file_ndx.read(1)))
				
                hex_high_data_time = hex_array_high_data_time[3] + hex_array_high_data_time[2] + hex_array_high_data_time[1] + hex_array_high_data_time[0]
               
                for i in range(4):
                    hex_array_high_data_time.pop(3 - i)
                
                filetime = int(hex_high_data_time +  hex_low_data_time, 16)
            
                datatime_1601 = datetime(1601, 1, 1, 0, 0, 0)
                delta = timedelta(seconds = filetime/1e7)
                data_time = datatime_1601 + delta 

                #print(data_time)
			
                seek_array_file_pdt.append(binascii.hexlify(file_ndx.read(1)))
                seek_array_file_pdt.append(binascii.hexlify(file_ndx.read(1)))
				
                seek_file_pdt = int(seek_array_file_pdt[1] + seek_array_file_pdt[0] , 16)

                seek_array_file_pdt.pop(1)
                seek_array_file_pdt.pop(0)

                #print(seek_file_pdt)

                filename_pdt = ''
                num = file.find('.ndx')

                for el_name_file in range(num):
                    filename_pdt = filename_pdt + file[el_name_file]

                file_pdt = fzip.open(filename_pdt + '.pdt', 'r')
                file_pdt.read(seek_file_pdt)

                hex_array_length_nameTV.append(binascii.hexlify(file_pdt.read(1)))
                hex_array_length_nameTV.append(binascii.hexlify(file_pdt.read(1)))
			
                length_nameTV = int( hex_array_length_nameTV[1] + hex_array_length_nameTV[0], 16)
                
                hex_array_length_nameTV.pop(1)
                hex_array_length_nameTV.pop(0)
			
                byte_nameTV = file_pdt.read(length_nameTV)
                file_pdt.close()
                
                nameTV = byte_nameTV.decode('cp1251')

                #TV = {filename_pdt : nameTV }
                #TV = {filename_pdt : { nameTV : data_time } }

                TV_base = struct_TV(filename_pdt, nameTV, data_time)
                session.add(TV_base)
	
            file_ndx.close()     

	
if __name__ =='__main__':
	
    with open('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\data_connection.json', 'r', encoding = 'utf-8') as file_json:
        data = json.load(file_json)
    
    engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(data['user'],data['password'],data['host'],data['port'],data['database']))
    
    metadata = MetaData()
    
    TV_table = Table('TVprogram_base', metadata,
        Column('Name_channel', String),
        Column('Name_TVprogram', String),
        Column('DateTime', DateTime)
    )
    
    metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    
    #url = 'http://programtv.ru/jtv.zip'
    #response = requests.get(url)

    #fzip = open('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\jtv.zip', 'wb')
    #fzip.write(response.content)
    #fzip.close()

    fzip = zipfile.ZipFile('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\jtv.zip', 'r')
    
    
    #TV = {}
    read_JTV(fzip, session)
    #os.remove('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\jtv.zip')
    fzip.close()















