from os import name
import requests
from bs4 import BeautifulSoup
import time

from Database import Database

class SearchIP:
    def __init__(self):
        self.database = Database()
        pass

    def request(self, ip):
        url = 'https://infobyip.com/ip-'+ip+'.html'
        user_agent = {'User-agent': 'Mozilla/5.0'}
        #print(url)
        req = requests.get(url, headers=user_agent)

        if req.status_code == 200:
            #print(req.content)
            return req.content
        else:
            return -1
    
    def getData(self, text, campo, next='Country'):
        array = text.split('\n')
        dicionario = {}
        for line in array:
            if line.count(campo) > 0:
                pos = line.rfind(campo)
                tam = len(campo)
                flag = 1 if line[(pos+tam)] == ' ' else 0
                data = line[(pos+tam+flag):]
                if data.count(next) > 0:
                    pos_end = line.rfind(next)
                    return line[(pos+tam+flag):pos_end]
                else:
                    return line[(pos+tam+flag):]
        
        return ''

    def __getInfoIP(self, ip):
        
        content = self.request(ip)
        dicionario = {}
        if content != -1:
            soup = BeautifulSoup(content, 'html.parser')
            table_1 = soup.find('table', {'class':'center results wide home'}).text.strip()
            for param in ['ISP', 'ASN']:
                dicionario[param] = self.getData(table_1, param)
            
            table_2 = soup.find('table', {'class':'results wide home'}).text.strip()
            for param in ['Continent', 'Country', 'State/region', 'City']:

                dicionario[param] = self.getData(table_2, param)

            return dicionario
            pass
        else:
            return -1

    def get(self, ip):
        #Verificar base de dados
        if ip.count(':') > 0:
            ip = ip.split(':')[0]
        if ip == '127.0.0.1' or ip == "0.0.0.0":
            return 'localHost'

        database = self.database.search(ip)
        if database != -1:
            return database
        else:
            newData = self.__getInfoIP(ip)
            self.database.insert(ip, newData)
            if self.database.insert(ip, newData):
                #print("Novo IP cadastrado com sucesso")
                time.sleep(1)
            else:
                print("Falha ao guardar aquivo")
            return newData

    def validateIP(self, ip):

        if ip.count('*') > 0 or ip.count(']') > 0:
            return 0
        else:
            return 1


#teste = SearchIP()
#var = teste.get('192.135.185.15:2020')
#print(var)