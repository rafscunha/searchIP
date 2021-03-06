from os import name
import requests
from bs4 import BeautifulSoup
import time

from Database import Database

class SearchIP:
    def __init__(self):
        self.database = Database()
        pass

    def getDatabase(self):
        return self.database.getDatabase()

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

    def excluirImg(self, text):
        if text.count('img') > 0:
            remove = text[text.find("<img"):text.rfind("/>")+2]
            return text.replace(remove, "")
            
        else:
            return text

    def conversor(self, html):
        text = str(html).replace('\n', '').replace("</table>", "").replace('\xa0', '').replace('\t', "")
        pos = text.find('>')
        text = text[pos+1:]

        linhas = text.split("</tr>")
        table = []
        for linha in linhas:
            linha = linha.replace("<tr>","")
            line = []
            if linha.count('td')>0:
                colunas = linha.split("</td>")
                for coluna in colunas:
                    coluna = coluna.replace("<td>", "")
                    if coluna != '' or coluna == ' N/A (N/A)':
                        line.append(self.excluirImg(coluna))
            else:
                line.append(linha) 
            if line != '':
                table.append(line)
        return table
    
    def getDicionarioByCampos(self, vetor, matrix):
        dicionario = {}
        for linha in matrix:
            if len(linha) > 1:
                if linha[0] in vetor:
                    dicionario[linha[0]] = linha[1]
        
        return dicionario
        pass


    def __getInfoIP(self, ip):
        
        content = self.request(ip)
        dicionario = {}
        if content != -1:
            soup = BeautifulSoup(content, 'html.parser')

            html_table = soup.find('table', {'class':'center results wide home'})
            matrix_table = self.conversor(html_table)       
            dicionario.update(self.getDicionarioByCampos(['ISP', 'ASN'],matrix_table))

            html_table = soup.find('table', {'class':'results wide home'})
            #print(html_table)
            matrix_table = self.conversor(html_table) 
            #print(matrix_table)
            dicionario.update(self.getDicionarioByCampos(['Continent', 'Country', 'State/region', 'City'],matrix_table))   

            return dicionario
            pass
        else:
            return -1

    def get(self, ip, campo=None):
        #Verificar base de dados
        if ip.count(':') > 0:
            ip = ip.split(':')[0]
        if ip == '127.0.0.1' or ip == "0.0.0.0":
            return 'localHost'

        database = self.database.search(ip)
        if database == -1:
            database = self.__getInfoIP(ip)
            if self.database.insert(ip, database):
                #print("Novo IP cadastrado com sucesso")
                time.sleep(0.1)
            else:
                print("Falha ao guardar aquivo")
            
        if campo != None:
            try:
                return {campo:database[campo]}
            except:
                return database
        else:
            return database

    def validateIP(self, ip):

        if ip.count('*') > 0 or ip.count(']') > 0:
            return 0
        else:
            return 1
    


#teste = SearchIP()
#var = teste.get('34.98.64.218:2020')
#print(var)