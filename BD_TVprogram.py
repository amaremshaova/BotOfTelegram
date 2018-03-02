import requests
import tempfile
import zipfile
import os
import os.path


url = 'http://programtv.ru/jtv.zip'

response = requests.get(url)

file = tempfile.TemporaryFile()
file.write(response.content)

fzip = zipfile.ZipFile(file)
fzip.extractall('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\tmp') 



#for f in os.listdir('C:\\Users\\Anastasia\\Desktop\\TVprogram_bot\\tmp'):
	#path, f_name = os.path.split(f) 
    #print(str(f_name))
    #filename, extension = os.path.splitext(f_name)
    #os.rename(f, filename.encode('cp437').decode('cp866') + extension )	


fzip.close()
file.close