import pickle

class Arquivo:

    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo
        pass
    
    def setData(self, objeto):
        arquivo = open(self.nome_arquivo, "wb")
        pickle.dump(objeto,arquivo)
        arquivo.close()
        pass
    
    def getData(self):
        try:
            arquivo = open(self.nome_arquivo, "rb")
            objeto = pickle.load(arquivo)
            arquivo.close()
            return objeto
        except:
            return {}