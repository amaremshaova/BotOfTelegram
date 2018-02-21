import os
import pyodbc
import binascii
import array 
import os.path
import win32
import time
from datetime import datetime, timedelta

 #Структура файла PDT:
 #После константной текстовой метки "JTV 3.x TV Program Data"
 #($4A$54$56$20$33$2E$78$20$54$56$20$50$72$6F$67$72$61$6D$20$44$61$74$61)
 #и трёх байт с кодом 0Ah ($0A$0A$0A) идут записи переменной длины:
 #
 #два байта под количество символов в названии (длина строки),
 #затем само название телепередачи (строка)
 #и так до конца файла.

 #Структура файла NDX:
 #Два байта в начале файла - счётчик общего количества записей,
 #за ними расположились записи, каждая по 12 байт:
 
 #Первая пара всегда нулевая ($00$00), затем идут восемь (4+4)
 #байт структуры FILETIME (дата и время показа телепередачи),
 #считывается она инвертно: 4321.8765, последние 2 байта указывают на начало
 #(на первый из пары байт длины строки) названия этой передачи в файле PDT.

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
			