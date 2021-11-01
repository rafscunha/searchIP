from Arquivo import Arquivo

class Database():
    def __init__(self, arquivo = 'database_ipSearch.bin'):
        self.nomeArquivo = arquivo
        self.file = Arquivo(self.nomeArquivo)
        self.database = self.file.getData()
        pass

    def getDatabase(self):
        if self.database == {}:
            self.database = self.file.getData()
        return self.database

    def search(self,ip):
        try: 
            if self.database == {}:
                self.database = self.file.getData()
            self.database = self.file.getData()
            if [ip in self.database.keys()]:
                return self.database[ip]
            else:
                return -1
        except:
            return -1
    
    def insert(self, ip, data):
        try: 
            #database = self.file.getData()
            self.database[ip] = data
            self.file.setData(self.database)
            return 1
        except:
            return 0
                   

