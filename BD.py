import os
import pyodbc
import binascii
import array 
import os.path
import win32
import time
from datetime import datetime, timedelta

if __name__ == '__main__':

    hex_array_countTV = []
    hex_array_low_data_time = []
    hex_array_high_data_time = []
    seek_array_file_pdt = []
    hex_array_length_nameTV = []
    	
    for file in os.listdir('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\jtv'): #проходим по всем файлам с расширением .ndx в папке jtv
        if file.endswith('.ndx'):
            file_ndx = open('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\jtv\\' +file, 'rb')
            #print(file) 
            		
            hex_array_countTV.append(binascii.hexlify(file_ndx.read(1)))  
            hex_array_countTV.append(binascii.hexlify(file_ndx.read(1)))
			
            countTV = int(hex_array_countTV[1] + hex_array_countTV[0], 16)
			
            print('countTV ' + file + ' ' + str(countTV))  
            
            hex_array_countTV.pop(1)
            hex_array_countTV.pop(0)
			
            for j in range(countTV):
                file_ndx.read(2)
				
                for i in range(4):
                    hex_array_low_data_time.append(binascii.hexlify(file_ndx.read(1)))
                
                hex_low_data_time = hex_array_low_data_time[3] + hex_array_low_data_time[2] + hex_array_low_data_time[1] + hex_array_low_data_time[0]
                LowDataTime = int(hex_low_data_time, 16)
                print('LowDataTime ' + file + ' ' + str(LowDataTime))  
                for i in range(4):
                    hex_array_low_data_time.pop(3 - i)
            
                for i in range(4):
                    hex_array_high_data_time.append(binascii.hexlify(file_ndx.read(1)))
				
                hex_high_data_time = hex_array_high_data_time[3] + hex_array_high_data_time[2] + hex_array_high_data_time[1] + hex_array_high_data_time[0]
                HighDataTime = int(hex_high_data_time, 16)	
                print('HighDataTime ' + file + ' ' + str(HighDataTime))
                for i in range(4):
                    hex_array_high_data_time.pop(3 - i)
			
            #filetime = int(str(LowDataTime)+ str(HighDataTime))
            #print(filetime)
            
            #a = datetime(1601, 1, 1, 0, 0, 0)
            #b = timedelta(seconds = filetime/1e7)
            #c = a + b
            #print(c)
			
                
            
                seek_array_file_pdt.append(binascii.hexlify(file_ndx.read(1)))
                seek_array_file_pdt.append(binascii.hexlify(file_ndx.read(1)))
				
                seek_file_pdt = int(seek_array_file_pdt[1] + seek_array_file_pdt[0] , 16)
			
                seek_array_file_pdt.pop(1)
                seek_array_file_pdt.pop(0)
			
                path, filename_ndx= os.path.split('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\jtv\\'+ file) 
                filename_pdt, extension = os.path.splitext(filename_ndx)
                file_pdt = open('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\jtv\\' +filename_pdt + '.pdt', 'rb')
            
                file_pdt.seek(seek_file_pdt)
            
                hex_array_length_nameTV.append(binascii.hexlify(file_pdt.read(1)))
                hex_array_length_nameTV.append(binascii.hexlify(file_pdt.read(1)))
			
                length_nameTV = int( hex_array_length_nameTV[1] + hex_array_length_nameTV[0], 16)
                print('length_nameTV' + file +' ' + str(length_nameTV))
                hex_array_length_nameTV.pop(1)
                hex_array_length_nameTV.pop(0)
			
                byte_nameTV = file_pdt.read(length_nameTV)
                file_pdt.close()
                
                nameTV = byte_nameTV.decode('utf-8')
			
                print(byte_nameTV)   			
            file_ndx.close()
			