from Arquivo import Arquivo

class Database():
    def __init__(self, arquivo = 'database_ipSearch.bin'):
        self.nomeArquivo = arquivo
        self.file = Arquivo(self.nomeArquivo)
        pass

    def search(self,ip):
        try: 
            database = self.file.getData()
            if [ip in database.keys()]:
                return database[ip]
            else:
                return -1
        except:
            return -1
    
    def insert(self, ip, data):
        try: 
            database = self.file.getData()
            database[ip] = data
            self.file.setData(database)
            return 1
        except:
            return 0

